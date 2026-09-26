from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from properties.models import Property
from rentals.models import RentalRequest
from .forms import ReviewForm
from .models import Review


@login_required
def add_review(request, property_pk):
    if not request.user.is_tenant:
        return HttpResponseForbidden("Only tenants can leave reviews.")

    property_obj = get_object_or_404(Property, pk=property_pk)

    has_accepted_request = RentalRequest.objects.filter(
        property=property_obj, tenant=request.user, status=RentalRequest.Status.ACCEPTED
    ).exists()
    if not has_accepted_request:
        messages.error(request, "You can only review properties after your rental request was accepted.")
        return redirect("properties:detail", pk=property_pk)

    if Review.objects.filter(property=property_obj, tenant=request.user).exists():
        messages.warning(request, "You have already reviewed this property.")
        return redirect("properties:detail", pk=property_pk)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.property = property_obj
            review.tenant = request.user
            review.save()
            messages.success(request, "Thanks for your review!")
            return redirect("properties:detail", pk=property_pk)
    else:
        form = ReviewForm()
    return render(request, "reviews/review_form.html", {"form": form, "property": property_obj})
