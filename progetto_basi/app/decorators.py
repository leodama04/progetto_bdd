from django.shortcuts import redirect
from .utils import riconoscimento_ruolo

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        id_utente = request.session.get('id_utente')
        
        if not id_utente:
            return redirect('login')
        
        ruolo = riconoscimento_ruolo(id_utente)

        ruolo_utente = ruolo[0]['ruolo'] if ruolo else None

        if ruolo_utente != 'A':
            return redirect('no_permission')
        
        return view_func(request, *args, **kwargs)
    return wrapper

