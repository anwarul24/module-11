from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from properties.models import Property
from .forms import RentalRequestForm
from .models import RentalRequest


def _notify(subject, message, recipient_email):
    """Best-effort email notification (bonus feature). Never raises to the user."""
    if not recipient_email:
        return
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email], fail_silently=True)
    except Exception:
        pass


@login_required
def send_request(request, property_pk):
    if not request.user.is_tenant:
        return HttpResponseForbidden("Only tenants can send rental requests.")

    property_obj = get_object_or_404(Property, pk=property_pk)

    if property_obj.owner_id == request.user.id:
        messages.error(request, "You cannot request your own property.")
        return redirect("properties:detail", pk=property_pk)

    if RentalRequest.objects.filter(
        property=property_obj, tenant=request.user, status=RentalRequest.Status.PENDING
    ).exists():
        messages.warning(request, "You already have a pending request for this property.")
        return redirect("properties:detail", pk=property_pk)

    if request.method == "POST":
        form = RentalRequestForm(request.POST)
        if form.is_valid():
            rental_request = form.save(commit=False)
            rental_request.property = property_obj
            rental_request.tenant = request.user
            try:
                rental_request.full_clean()
            except ValidationError as exc:
                for err in exc.messages:
                    messages.error(request, err)
                return render(request, "rentals/request_form.html", {"form": form, "property": property_obj})
            rental_request.save()
            _notify(
                f"New rental request: {property_obj.title}",
                f"{request.user.username} sent a rental request for '{property_obj.title}'.",
                property_obj.owner.email,
            )
            messages.success(request, "Your rental request has been sent.")
            return redirect("dashboard:tenant")
    else:
        form = RentalRequestForm()
    return render(request, "rentals/request_form.html", {"form": form, "property": property_obj})


@login_required
def cancel_request(request, pk):
    rental_request = get_object_or_404(RentalRequest, pk=pk)
    if rental_request.tenant_id != request.user.id:
        return HttpResponseForbidden("You can only cancel your own requests.")
    if rental_request.status != RentalRequest.Status.PENDING:
        messages.error(request, "Only pending requests can be cancelled.")
        return redirect("dashboard:tenant")

    if request.method == "POST":
        rental_request.delete()
        messages.info(request, "Rental request cancelled.")
        return redirect("dashboard:tenant")
    return render(request, "rentals/request_confirm_cancel.html", {"rental_request": rental_request})


@login_required
def owner_requests(request):
    if not request.user.is_owner:
        return HttpResponseForbidden("Only property owners can view this page.")
    requests_qs = RentalRequest.objects.filter(property__owner=request.user).select_related("property", "tenant")
    return render(request, "rentals/owner_requests.html", {"requests": requests_qs})


@login_required
def tenant_requests(request):
    if not request.user.is_tenant:
        return HttpResponseForbidden("Only tenants can view this page.")
    requests_qs = RentalRequest.objects.filter(tenant=request.user).select_related("property", "property__owner")
    return render(request, "rentals/tenant_requests.html", {"requests": requests_qs})


@login_required
def respond_request(request, pk, action):
    rental_request = get_object_or_404(RentalRequest, pk=pk)
    if rental_request.property.owner_id != request.user.id:
        return HttpResponseForbidden("You can only respond to requests for your own properties.")
    if rental_request.status != RentalRequest.Status.PENDING:
        messages.error(request, "This request has already been resolved.")
        return redirect("rentals:owner_requests")

    if action == "accept":
        rental_request.status = RentalRequest.Status.ACCEPTED
        rental_request.property.is_available = False
        rental_request.property.save(update_fields=["is_available"])
        messages.success(request, f"Accepted request from {rental_request.tenant.username}.")
    elif action == "reject":
        rental_request.status = RentalRequest.Status.REJECTED
        messages.info(request, f"Rejected request from {rental_request.tenant.username}.")
    else:
        return HttpResponseForbidden("Invalid action.")

    rental_request.save(update_fields=["status", "updated_at"])
    _notify(
        f"Your rental request was {rental_request.status.lower()}",
        f"Your request for '{rental_request.property.title}' was {rental_request.status.lower()}.",
        rental_request.tenant.email,
    )
    return redirect("rentals:owner_requests")
