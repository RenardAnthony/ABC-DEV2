from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def staff_required(view_func):
    return user_passes_test(
        lambda u: u.is_staff,
        login_url='profile' # Rediriger vers la page de connexion si l'utilisateur n'est pas staff
    )(view_func)

def redirect_authenticated_user(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func