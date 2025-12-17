from django.shortcuts import redirect
from functools import wraps

def role_required(allowed_roles=[]):
    """
    Decorador para restringir vistas según rol de usuario.
    allowed_roles: lista de roles permitidos, ejemplo ['admin', 'analista']
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if hasattr(request.user, 'rol'):
                if request.user.rol in allowed_roles:
                    return view_func(request, *args, **kwargs)
            # Si no tiene rol permitido, redirige al dashboard
            return redirect('dashboard')
        return wrapper
    return decorator
