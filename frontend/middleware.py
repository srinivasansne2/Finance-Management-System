from django.shortcuts import redirect
from django.contrib import messages

class AuthRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        protected_paths = ['/dashboard', '/transactions', '/users']

        if any(request.path.startswith(p) for p in protected_paths):

            if not request.session.get('token'):
                messages.error(request, "⚠️ Please login first")
                return redirect('login')

        return self.get_response(request)