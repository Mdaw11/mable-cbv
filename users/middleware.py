from django.shortcuts import redirect
from django.urls import reverse

class RequireLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Exclude the login and registration pages from redirection
        if not request.user.is_authenticated and request.path not in [reverse('landing-page'), reverse('account-type'), reverse('login'), reverse('register'), reverse('logout')]:
            # Redirect to the login page
            return redirect(reverse('login'))
        return self.get_response(request)