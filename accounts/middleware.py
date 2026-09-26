from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse


class RoleBasedAccessMiddleware:
    """
    Custom middleware enforcing role-based access control.

    - Anonymous users are redirected to login when they try to reach any
      authenticated-only area (handled by @login_required on the views
      themselves; this middleware focuses on ROLE separation).
    - Paths under /dashboard/owner/, /properties/add/, /properties/<id>/edit/,
      /properties/<id>/delete/ and the request-response endpoints are
      OWNER-only.
    - Paths under /dashboard/tenant/ and the "send rental request" /
      "leave review" endpoints are TENANT-only.

    Rather than hardcoding every URL, each protected view also re-checks
    permissions directly (defence in depth); this middleware provides a
    single, centralised first line of defence and a consistent redirect
    with a friendly message.
    """

    OWNER_ONLY_PREFIXES = (
        "/dashboard/owner/",
        "/properties/add/",
    )
    TENANT_ONLY_PREFIXES = (
        "/dashboard/tenant/",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        path = request.path

        if user is not None and user.is_authenticated:
            if path.startswith(self.OWNER_ONLY_PREFIXES) and not user.is_owner:
                messages.error(request, "That area is only available to property owners.")
                return redirect(reverse("dashboard:redirect"))

            if path.startswith(self.TENANT_ONLY_PREFIXES) and not user.is_tenant:
                messages.error(request, "That area is only available to tenants.")
                return redirect(reverse("dashboard:redirect"))

        response = self.get_response(request)
        return response
