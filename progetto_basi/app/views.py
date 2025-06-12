from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import (
    UtenteForm, CartaDiCreditoForm, EventoForm, RichiestaPrenotazioneSerataForm,
    AcquistoBigliettoForm, AcquistoSerataPrivataForm
)
from .utils import (
    iscrizione_utente, login_utente, riconoscimento_ruolo,aggiunta_carta_di_credito,
    visualizza_serate_pubbliche, acquisto_biglietto, seleziona_tavolo,
    iscrizione_a_lista_pr, richiesta_serata_privata, acquisto_serata_privata,
    visualizza_area_personale_biglietti, visualizza_area_personale_richieste,
    visualizza_area_personale_serate_acquistate, aggiungere_evento, rimuovere_evento,
    accettare_rifiutare_richiesta, aggiunta_artista, rimozione_artista,
    aggiunta_lista_pr, rimozione_lista_pr, aggiunta_tavolo, rimozione_tavolo
)
from .decorators import admin_required

def home(request):
    if request.method == 'POST':
        # Gestione login, come già fai in login_view
        nome = request.POST.get('nome')
        password = request.POST.get('password')
        result = login_utente(nome, password)
        if result:
            request.session['id_utente'] = result[0]['id_utente']
            request.session['ruolo'] = result[0]['ruolo']  # se hai modificato login_utente come prima detto
            return redirect('dashboard')
        else:
            return render(request, 'home.html', {
                'login_error': "Login fallito",
                'utente_form': UtenteForm(),
            })
    else:
        # GET: mostra pagina con form login e link a registrazione
        return render(request, 'home.html', {
            'utente_form': UtenteForm(),  # se vuoi mostrare anche il form di registrazione
        })

def dashboard_view(request):
    id_utente = request.session.get('id_utente')
    if not id_utente:
        return redirect('login')

    ruolo = riconoscimento_ruolo(id_utente)
    # riconoscimento_ruolo ritorna lista di dizionari, prendi il primo risultato
    user_is_admin = False
    if ruolo and len(ruolo) > 0 and ruolo[0].get('ruolo') == 'admin':
        user_is_admin = True

    context = {
        'user_is_admin': user_is_admin,
    }
    return render(request, 'dashboard.html', context)


def logout_view(request):
    # Pulisci la sessione per fare logout
    request.session.flush()
    return redirect('login')

# --- UTENTE ---

def registra_utente(request):
    if request.method == 'POST':
        form = UtenteForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            iscrizione_utente(
                data['id_utente'],
                data['ruolo'],
                data['password'],
                data['data_di_nascita'],
                data['nome'],
                data['cognome'],
                data.get('telefono', '')
            
            )
            return redirect('home')  
    else:
        form = UtenteForm()
    return render(request, 'registrazione.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        password = request.POST.get('password')
        result = login_utente(nome, password)
        if result:
            # Esempio: salva id_utente in sessione
            request.session['id_utente'] = result[0]['id_utente']
            return redirect('dashboard')
        else:
            return HttpResponse("Login fallito")
    return render(request, 'login.html')


def aggiungi_carta(request):
    if request.method == 'POST':
        form = CartaDiCreditoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            id_utente = request.session.get('id_utente')
            aggiunta_carta_di_credito(
                data['numero_di_carta'], data.get('nome_titolare', ''),
                data.get('data_di_scadenza'), data.get('tipo', ''), id_utente
            )
            return redirect('success_page')
    else:
        form = CartaDiCreditoForm()
    return render(request, 'aggiungi_carta.html', {'form': form})


def mostra_serate_pubbliche(request):
    serate = visualizza_serate_pubbliche()
    return render(request, 'serate_pubbliche.html', {'serate': serate})


def acquista_biglietto_view(request):
    if request.method == 'POST':
        form = AcquistoBigliettoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            acquisto_biglietto(
                data['ID_ACQ'], data['data'], data['importo'],
                data['codice_metodo_di_pagamento'], data['id_utente'], data['codice_biglietto']
            )
            return redirect('success_page')
    else:
        form = AcquistoBigliettoForm()
    return render(request, 'acquista_biglietto.html', {'form': form})


def seleziona_tavolo_view(request):
    if request.method == 'POST':
        codice_tavolo = request.POST.get('codice_tavolo')
        codice_biglietto = request.POST.get('codice_biglietto')
        seleziona_tavolo(codice_tavolo, codice_biglietto)
        return redirect('success_page')
    # mostra form con tavoli e biglietti se vuoi
    return render(request, 'seleziona_tavolo.html')


def iscrizione_lista_pr_view(request):
    if request.method == 'POST':
        codice_lista = request.POST.get('codice_lista')
        id_utente = request.session.get('id_utente')
        iscrizione_a_lista_pr(codice_lista, id_utente)
        return redirect('success_page')
    return render(request, 'iscrizione_lista.html')


def richiesta_serata_privata_view(request):
    if request.method == 'POST':
        form = RichiestaSerataForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            richiesta_serata_privata(
                data['codice_richiesta'], data['numero_invitati'], data['descrizione'],
                data['stato'], data['ora_inizio'], data['ora_fine'], data['data_serata'],
                request.session.get('id_utente')
            )
            return redirect('success_page')
    else:
        form = RichiestaSerataForm()
    return render(request, 'richiesta_serata_privata.html', {'form': form})


def acquisto_serata_privata_view(request):
    if request.method == 'POST':
        form = AcquistoSerataPrivataForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            acquisto_serata_privata(
                data['codice_evento'], data['codice_acquisto_serata'], data['data'],
                data['importo'], data['codice_metodo_di_pagamento'], request.session.get('id_utente')
            )
            return redirect('success_page')
    else:
        form = AcquistoSerataPrivataForm()
    return render(request, 'acquisto_serata_privata.html', {'form': form})


# --- AREA PERSONALE ---

def area_personale_biglietti(request):
    id_utente = request.session.get('id_utente')
    biglietti = visualizza_area_personale_biglietti(id_utente)
    return render(request, 'area_personale_biglietti.html', {'biglietti': biglietti})


def area_personale_richieste(request):
    id_utente = request.session.get('id_utente')
    richieste = visualizza_area_personale_richieste(id_utente)
    return render(request, 'area_personale_richieste.html', {'richieste': richieste})


def area_personale_serate_acquistate(request):
    id_utente = request.session.get('id_utente')
    serate = visualizza_area_personale_serate_acquistate(id_utente)
    return render(request, 'area_personale_serate.html', {'serate': serate})


# --- AMMINISTRATORE ---

@admin_required
def aggiungi_evento_view(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            aggiungere_evento(
                data['numero_partecipanti'], data['tipo'], data['descrizione'],
                data['prezzo'], data['nome'], data['data'], data['genere'],
                data['ora_inizio'], data['ora_fine']
            )
            return redirect('success_page')
    else:
        form = EventoForm()
    return render(request, 'aggiungi_evento.html', {'form': form})


@admin_required
def rimuovi_evento_view(request, codice_evento):
    rimuovere_evento(codice_evento)
    return redirect('success_page')


@admin_required
def accetta_rifiuta_richiesta_view(request):
    if request.method == 'POST':
        codice_richiesta = request.POST.get('codice_richiesta')
        stato = request.POST.get('stato')
        accettare_rifiutare_richiesta(codice_richiesta, stato)
        return redirect('success_page')
    return render(request, 'gestione_richieste.html')


@admin_required
def aggiungi_artista_view(request):
    if request.method == 'POST':
        codice_evento = request.POST.get('codice_evento')
        codice_artista = request.POST.get('codice_artista')
        aggiunta_artista(codice_evento, codice_artista)
        return redirect('success_page')
    return render(request, 'aggiungi_artista.html')


@admin_required
def rimuovi_artista_view(request):
    if request.method == 'POST':
        codice_evento = request.POST.get('codice_evento')
        codice_artista = request.POST.get('codice_artista')
        rimozione_artista(codice_evento, codice_artista)
        return redirect('success_page')
    return render(request, 'rimuovi_artista.html')


@admin_required
def aggiungi_lista_pr_view(request):
    if request.method == 'POST':
        codice_lista = request.POST.get('codice_lista')
        nome_lista = request.POST.get('nome_lista')
        codice_evento = request.POST.get('codice_evento')
        codice_pr = request.POST.get('codice_pr')
        aggiunta_lista_pr(codice_lista, nome_lista, codice_evento, codice_pr)
        return redirect('success_page')
    return render(request, 'aggiungi_lista_pr.html')


@admin_required
def rimuovi_lista_pr_view(request):
    if request.method == 'POST':
        codice_evento = request.POST.get('codice_evento')
        codice_pr = request.POST.get('codice_pr')
        rimozione_lista_pr(codice_evento, codice_pr)
        return redirect('success_page')
    return render(request, 'rimuovi_lista_pr.html')


@admin_required
def aggiungi_tavolo_view(request):
    if request.method == 'POST':
        codice_evento = request.POST.get('codice_evento')
        numero_posti = request.POST.get('numero_posti')
        aggiunta_tavolo(codice_evento, numero_posti)
        return redirect('success_page')
    return render(request, 'aggiungi_tavolo.html')


@admin_required
def rimuovi_tavolo_view(request):
    if request.method == 'POST':
        codice_tavolo = request.POST.get('codice_tavolo')
        rimozione_tavolo(codice_tavolo)
        return redirect('success_page')
    return render(request, 'rimuovi_tavolo.html')
