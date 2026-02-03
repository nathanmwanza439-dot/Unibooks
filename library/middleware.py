from django.shortcuts import redirect


class ForcePasswordChangeMiddleware:
    """If user has force_password_change flag, redirect to change password page and block other pages.

    Allows admin paths and static files.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            if getattr(user, 'force_password_change', False):
                path = request.path
                # allow password change, logout and admin paths; be permissive to handle both
                # root and '/student/' prefixed routes to avoid redirect loops when URLs are included twice.
                if path.startswith('/admin/'):
                    return self.get_response(request)

                # allow any path that looks like the password change or logout endpoint
                if '/password-change/' in path or path.endswith('/logout/') or '/logout/' in path:
                    return self.get_response(request)

                # otherwise force redirect to the password change view
                return redirect('student:password_change')
        return self.get_response(request)


class SubscriptionMiddleware:
    """If a user's subscription has expired, log them out and redirect to a subscription info page.

    This middleware is conservative: it lets admin paths and static assets through, and only
    acts for authenticated non-staff users. It relies on `User.subscription_active()` helper.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        path = request.path
        # Allow admin to function uninterrupted
        if path.startswith('/admin/'):
            return self.get_response(request)
        # Allow static/media and the subscription_required page itself
        if path.startswith('/static/') or path.startswith('/media/') or path.startswith('/subscription_required') or path.startswith('/subscription-required'):
            return self.get_response(request)

        # If user is authenticated and payment date exists but subscription expired, log out and render page
        if user and user.is_authenticated and not user.is_staff:
            if getattr(user, 'date_paiement', None) and not getattr(user, 'subscription_is_active', False):
                # Render the subscription info page directly (pass the user for dates)
                from django.contrib.auth import logout
                from django.shortcuts import render
                # Log the user out so subsequent requests are anonymous
                logout(request)
                return render(request, 'student/subscription_required.html', {'profile_user': user})

        return self.get_response(request)
