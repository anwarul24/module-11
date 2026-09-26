from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PropertyForm, PropertySearchForm
from .models import Property, FavoriteProperty


def home(request):
    featured = Property.objects.filter(is_available=True)[:6]
    return render(request, "home.html", {"featured": featured})


def property_list(request):
    """Public listing page with search + filter + pagination."""
    properties = Property.objects.filter(is_available=True).select_related("owner")
    form = PropertySearchForm(request.GET or None)

    if form.is_valid():
        location = form.cleaned_data.get("location")
        property_type = form.cleaned_data.get("property_type")
        min_rent = form.cleaned_data.get("min_rent")
        max_rent = form.cleaned_data.get("max_rent")

        if location:
            properties = properties.filter(location__icontains=location)
        if property_type:
            properties = properties.filter(property_type=property_type)
        if min_rent is not None:
            properties = properties.filter(monthly_rent__gte=min_rent)
        if max_rent is not None:
            properties = properties.filter(monthly_rent__lte=max_rent)

    paginator = Paginator(properties, 9)
    page_obj = paginator.get_page(request.GET.get("page"))

    favorite_ids = set()
    if request.user.is_authenticated and request.user.is_tenant:
        favorite_ids = set(
            FavoriteProperty.objects.filter(tenant=request.user).values_list("property_id", flat=True)
        )

    return render(
        request,
        "properties/property_list.html",
        {"form": form, "page_obj": page_obj, "favorite_ids": favorite_ids},
    )


def property_detail(request, pk):
    property_obj = get_object_or_404(Property.objects.select_related("owner"), pk=pk)
    reviews = property_obj.reviews.select_related("tenant").order_by("-created_at")

    can_review = False
    already_requested_pending = False
    is_favorited = False

    if request.user.is_authenticated and request.user.is_tenant:
        from rentals.models import RentalRequest

        has_accepted_request = RentalRequest.objects.filter(
            property=property_obj, tenant=request.user, status=RentalRequest.Status.ACCEPTED
        ).exists()
        already_reviewed = reviews.filter(tenant=request.user).exists()
        can_review = has_accepted_request and not already_reviewed
        already_requested_pending = RentalRequest.objects.filter(
            property=property_obj, tenant=request.user, status=RentalRequest.Status.PENDING
        ).exists()
        is_favorited = FavoriteProperty.objects.filter(tenant=request.user, property=property_obj).exists()

    return render(
        request,
        "properties/property_detail.html",
        {
            "property": property_obj,
            "reviews": reviews,
            "can_review": can_review,
            "already_requested_pending": already_requested_pending,
            "is_favorited": is_favorited,
        },
    )


@login_required
def property_create(request):
    if not request.user.is_owner:
        return HttpResponseForbidden("Only property owners can add listings.")

    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.owner = request.user
            property_obj.save()
            messages.success(request, "Property listed successfully.")
            return redirect("properties:detail", pk=property_obj.pk)
    else:
        form = PropertyForm()
    return render(request, "properties/property_form.html", {"form": form, "mode": "create"})


@login_required
def property_edit(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    if property_obj.owner_id != request.user.id:
        return HttpResponseForbidden("You can only edit your own properties.")

    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES, instance=property_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Property updated successfully.")
            return redirect("properties:detail", pk=property_obj.pk)
    else:
        form = PropertyForm(instance=property_obj)
    return render(request, "properties/property_form.html", {"form": form, "mode": "edit", "property": property_obj})


@login_required
def property_delete(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    if property_obj.owner_id != request.user.id:
        return HttpResponseForbidden("You can only delete your own properties.")

    if request.method == "POST":
        property_obj.delete()
        messages.success(request, "Property deleted.")
        return redirect("dashboard:owner")
    return render(request, "properties/property_confirm_delete.html", {"property": property_obj})


@login_required
def my_properties(request):
    if not request.user.is_owner:
        return HttpResponseForbidden("Only property owners have a property list.")
    properties = Property.objects.filter(owner=request.user)
    return render(request, "properties/my_properties.html", {"properties": properties})


@login_required
def toggle_favorite(request, pk):
    if not request.user.is_tenant:
        return HttpResponseForbidden("Only tenants can save favorites.")
    property_obj = get_object_or_404(Property, pk=pk)
    favorite, created = FavoriteProperty.objects.get_or_create(tenant=request.user, property=property_obj)
    if not created:
        favorite.delete()
        messages.info(request, "Removed from favorites.")
    else:
        messages.success(request, "Added to favorites.")
    return redirect("properties:detail", pk=pk)


@login_required
def my_favorites(request):
    if not request.user.is_tenant:
        return HttpResponseForbidden("Only tenants have favorites.")
    favorites = FavoriteProperty.objects.filter(tenant=request.user).select_related("property")
    return render(request, "properties/my_favorites.html", {"favorites": favorites})
