from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

from properties.models import Property
from rentals.models import RentalRequest


@login_required
def dashboard_redirect(request):
    if request.user.is_owner:
        return redirect("dashboard:owner")
    return redirect("dashboard:tenant")


@login_required
def owner_dashboard(request):
    if not request.user.is_owner:
        return HttpResponseForbidden("Only property owners can view this dashboard.")

    properties = Property.objects.filter(owner=request.user)
    requests_qs = RentalRequest.objects.filter(property__owner=request.user)

    context = {
        "total_properties": properties.count(),
        "available_properties": properties.filter(is_available=True).count(),
        "total_requests": requests_qs.count(),
        "pending_requests": requests_qs.filter(status=RentalRequest.Status.PENDING).count(),
        "accepted_requests": requests_qs.filter(status=RentalRequest.Status.ACCEPTED).count(),
        "recent_properties": properties[:5],
        "recent_requests": requests_qs.select_related("property", "tenant")[:5],
    }
    return render(request, "dashboard/owner_dashboard.html", context)


@login_required
def tenant_dashboard(request):
    if not request.user.is_tenant:
        return HttpResponseForbidden("Only tenants can view this dashboard.")

    requests_qs = RentalRequest.objects.filter(tenant=request.user)

    context = {
        "total_requests": requests_qs.count(),
        "pending_requests": requests_qs.filter(status=RentalRequest.Status.PENDING).count(),
        "accepted_requests": requests_qs.filter(status=RentalRequest.Status.ACCEPTED).count(),
        "rejected_requests": requests_qs.filter(status=RentalRequest.Status.REJECTED).count(),
        "recent_requests": requests_qs.select_related("property", "property__owner")[:5],
    }
    return render(request, "dashboard/tenant_dashboard.html", context)
