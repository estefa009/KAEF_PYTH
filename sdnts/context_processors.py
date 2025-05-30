from .models import Carrito

def carrito(request):
    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(usuario=request.user, completado=False)
    else:
        carrito = None
        if 'session_key' in request.session:
            session_key = request.session['session_key']
            carrito, created = Carrito.objects.get_or_create(session_key=session_key, completado=False)
    
    return {'carrito': carrito}