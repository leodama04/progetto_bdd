from types import SimpleNamespace
from django.contrib import messages
from django.utils.dateparse import parse_time, parse_date
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from .forms import (
    UtenteForm, CartaDiCreditoForm, EventoPubblicoForm, RichiestaPrenotazioneSerataForm,
    AcquistoBigliettoForm, AcquistoSerataPrivataForm
)
from .utils import (
    iscrizione_utente, login_utente, riconoscimento_ruolo,aggiunta_carta_di_credito,
    visualizza_serate_pubbliche, acquisto_biglietto, 
    iscrizione_a_lista_pr, richiesta_serata_privata, acquisto_serata_privata,
    visualizza_area_personale_biglietti, visualizza_area_personale_richieste,
    visualizza_area_personale_serate_acquistate, aggiungere_evento, rimuovere_evento,
    accettare_rifiutare_richiesta, aggiunta_artista, rimozione_artista,
    aggiunta_lista_pr, rimozione_lista_pr, aggiunta_tavolo, rimozione_tavolo, get_artisti_disponibili, get_artisti_evento,
    visualizza_liste_pr, visualizza_tavoli_per_evento, visualizza_evento, get_pr_disponibili, get_richieste_in_attesa,
    visualizza_carte_di_credito, disiscrizione_da_lista_pr, get_liste_pr_utente, aggiungi_artista_db, rimuovi_artista_db,
    aggiungi_pr_db, rimuovi_pr_db, get_artisti, rimuovi_carta_di_credito, get_evento_da_richiesta
)
from .decorators import admin_required

def home(request):
    if request.method == 'POST':
        id_utente = request.POST.get('id_utente')
        password = request.POST.get('password')
        result = login_utente(id_utente, password)
        if result:
            request.session['id_utente'] = result[0]['id_utente']
            return redirect('dashboard')
        else:
            return render(request, 'home.html', {
                'login_error': "Login fallito",
            })
    else:
        return render(request, 'home.html')

def dashboard_view(request):
    id_utente = request.session.get('id_utente')
    if not id_utente:
        return redirect('home')  # o 'login' se hai una view separata

    ruolo_result = riconoscimento_ruolo(id_utente)
    user_is_admin = False
    if ruolo_result and ruolo_result[0].get('ruolo') == 'A':
        user_is_admin = True

    context = {
        'user_is_admin': user_is_admin,
        'id_utente': id_utente,
    }
    return render(request, 'dashboard.html', context)


def no_permission_view(request):
    return render(request, 'no_permission.html')

def logout_view(request):
    # Pulisci la sessione per fare logout
    request.session.flush()
    return redirect('home')

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
        id_utente = request.POST.get('id_utente')
        password = request.POST.get('password')
        result = login_utente(id_utente, password)
        if result:
            # Esempio: salva id_utente in sessione
            request.session['id_utente'] = result[0]['id_utente']
            return redirect('dashboard')
        else:
            return HttpResponse("Login fallito")
    return render(request, 'login.html')


def aggiungi_carta_view(request):
    id_utente = request.session.get('id_utente')

    if not id_utente:
        return redirect('login')  # o mostra messaggio di errore

    if request.method == 'POST':
        if 'aggiungi_carta' in request.POST:
            numero_carta = request.POST.get('numero_di_carta')
            nome_titolare = request.POST.get('nome_titolare')
            data_di_scadenza = request.POST.get('data_di_scadenza')
            tipo = request.POST.get('tipo')

            aggiunta_carta_di_credito(numero_carta, nome_titolare, data_di_scadenza, tipo, id_utente)
            return redirect('aggiungi_carta')  # reload per mostrare la nuova carta

        elif 'rimuovi_carta' in request.POST:
            codice_metodo = request.POST.get('codice_metodo')
            if codice_metodo:
                rimuovi_carta_di_credito(codice_metodo, id_utente)
            return redirect('aggiungi_carta')

    carte = visualizza_carte_di_credito(id_utente)

    return render(request, 'aggiungi_carta.html', {
        'carte': carte
    })



def mostra_serate_pubbliche(request):
    serate = visualizza_serate_pubbliche()
    return render(request, 'serate_pubbliche.html', {'serate': serate})


def acquista_biglietto_view(request, codice_evento):

    evento_raw = visualizza_evento(codice_evento)
    evento = evento_raw[0] if evento_raw else {}
    carte_di_credito = visualizza_carte_di_credito(request.session.get('id_utente'))

    if not evento:
        return HttpResponseNotFound("Evento non trovato")

    if request.method == 'POST':
        metodo = request.POST.get('carta_selezionata')
        if metodo:
            id_utente = request.session.get('id_utente')
            prezzo = evento['prezzo']

            codice_biglietto = acquisto_biglietto('S',prezzo, metodo, id_utente, codice_evento, codice_tavolo=None)

            return render(request, 'successo_acquisto_biglietto.html', {
                'codice_biglietto': codice_biglietto,
                'evento': evento,
            })
        else:
            return HttpResponseNotFound("Nessuna carta selezionata")

    else:
        form = AcquistoBigliettoForm()

    return render(request, 'acquista_biglietto.html', {
        'evento': evento,
        'carte': carte_di_credito
    })


def acquista_biglietto_tavolo_view(request, codice_evento):
    evento_raw = visualizza_evento(codice_evento)
    evento = evento_raw[0] if evento_raw else {}
    carte_di_credito = visualizza_carte_di_credito(request.session.get('id_utente'))
    tavoli = visualizza_tavoli_per_evento(codice_evento)

    if not evento:
        return HttpResponseNotFound("Evento non trovato")

    if request.method == 'POST':
        metodo = request.POST.get('carta_selezionata')
        id_utente = request.session.get('id_utente')
        tavolo_selezionato = request.POST.get('tavolo_selezionato')
        prezzo = evento['prezzo']

        if metodo and id_utente and tavolo_selezionato:
            codice_biglietto = acquisto_biglietto(
                tipo='T',
                importo=prezzo,
                codice_metodo_di_pagamento=metodo,
                id_utente=id_utente,
                codice_evento=codice_evento,
                codice_tavolo=tavolo_selezionato
            )

            return render(request, 'successo_acquisto_biglietto.html', {
                'codice_biglietto': codice_biglietto,
                'evento': evento,
            })

    return render(request, 'acquista_biglietto_tavolo.html', {
        'evento': evento,
        'carte': carte_di_credito,
        'tavoli': tavoli,
    })



def iscrizione_lista_pr_view(request, codice_evento):

    evento_raw = visualizza_evento(codice_evento)
    evento = SimpleNamespace(**evento_raw[0]) if evento_raw else None

    id_utente = request.session.get('id_utente')
    liste_pr = visualizza_liste_pr(codice_evento)
    iscrizioni = get_liste_pr_utente(id_utente)
    codici_iscritti = {i['codice_lista'] for i in iscrizioni}

    if request.method == 'POST':
        codice_lista = request.POST.get('codice_lista')
        azione = request.POST.get('azione')

        if azione == 'iscrivi':
            iscrizione_a_lista_pr(codice_lista, id_utente)
        elif azione == 'disiscrivi':
            disiscrizione_da_lista_pr(codice_lista, id_utente)

        return redirect('iscrizione_lista_pr', codice_evento=codice_evento)
    
    context = {
        'liste_pr': liste_pr,
        'codici_iscritti': codici_iscritti,
        'codice_evento': codice_evento,
        'evento': evento,
    }
    return render(request, 'iscrizione_lista.html', context)


def richiesta_serata_privata_view(request):
    id_utente = request.session.get('id_utente')
    if not id_utente:
        return redirect('login')  # o altra pagina di login

    if request.method == 'POST':
        numero_invitati = request.POST.get('numero_invitati')
        descrizione = request.POST.get('descrizione')
        ora_inizio_str = request.POST.get('ora_inizio')
        ora_fine_str = request.POST.get('ora_fine')
        data_serata_str = request.POST.get('data_serata')
        nome_evento = request.POST.get('nome_evento')
        genere = request.POST.get('genere')

        # Converti stringhe in tipi corretti
        ora_inizio = parse_time(ora_inizio_str) if ora_inizio_str else None
        ora_fine = parse_time(ora_fine_str) if ora_fine_str else None
        data_serata = parse_date(data_serata_str) if data_serata_str else None

        # Validazione base (esempio)
        if not numero_invitati or not data_serata or not nome_evento:
            messages.error(request, "Numero invitati, data serata e nome evento sono obbligatori.")
        else:
            richiesta_serata_privata(
                numero_invitati, descrizione, ora_inizio, ora_fine, data_serata, id_utente, nome_evento, genere
            )
            messages.success(request, "Richiesta inviata con successo.")


    return render(request, 'richiesta_serata_privata.html')

def acquisto_serata_privata_view(request,codice_richiesta):

    codice_evento = get_evento_da_richiesta(codice_richiesta)

    evento_raw = visualizza_evento(codice_evento)
    evento = SimpleNamespace(**evento_raw[0]) if evento_raw else None


    id_utente = request.session.get('id_utente')
    carte_raw = visualizza_carte_di_credito(id_utente)
    carte = [SimpleNamespace(**carta) for carta in carte_raw]

    if request.method == 'POST':
        codice_metodo = request.POST.get('carta_selezionata')
        if not codice_metodo:
            return render(request, 'acquisto_serata_privata.html', {
                'evento': evento,
                'carte': carte,
                'errore': 'Seleziona una carta',
            })

        acquisto_serata_privata(
            codice_evento=codice_evento,
            codice_metodo_di_pagamento=codice_metodo,
            id_utente=id_utente
        )
        return render(request, 'successo_acquisto_serata.html')

    return render(request, 'acquisto_serata_privata.html', {
        'evento': evento,
        'carte': carte,
    })




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
def gestione_eventi_view(request):
    if request.method == 'POST':
        # Controlla se è una richiesta di rimozione
        if 'rimuovi_evento' in request.POST:
            codice_evento = request.POST.get('codice_evento_da_rimuovere')
            if codice_evento:
                rimuovere_evento(codice_evento)
            return redirect('gestione_eventi')

        # Altrimenti è una richiesta di aggiunta evento
        form = EventoPubblicoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            aggiungere_evento(
                numero_partecipanti=0,
                tipo='pubblico',
                descrizione=data['descrizione'],
                prezzo=data['prezzo'],
                nome=data['nome'],
                data=data['data'],
                genere=data['genere'],
                ora_inizio=data['ora_inizio'],
                ora_fine=data['ora_fine'],
            )
            return redirect('gestione_eventi')
    else:
        form = EventoPubblicoForm()

    eventi = visualizza_serate_pubbliche()

    return render(request, 'gestione_eventi.html', {
        'form': form,
        'eventi': eventi,
    })

@admin_required
def gestione_richieste_view(request):
    richieste = get_richieste_in_attesa()

    if request.method == 'POST':
        codice_richiesta = request.POST.get('codice_richiesta')
        stato_input = request.POST.get('stato')

        # Mappatura pulsanti → stato DB
        if stato_input == 'accetta':
            stato = 'A'  # Accettata
        elif stato_input == 'rifiuta':
            stato = 'R'  # Rifiutata
        else:
            stato = 'P'  # Di default o errore

        accettare_rifiutare_richiesta(codice_richiesta, stato)
        return redirect('gestione_richieste')

    return render(request, 'gestione_richieste.html', {'richieste': richieste})



@admin_required
def gestione_artisti_view(request, codice_evento):
    # ottieni artista associati e disponibili
    artisti_associati = get_artisti_evento(codice_evento)
    artisti_disponibili = get_artisti_disponibili(codice_evento)

    if request.method == 'POST':
        if 'aggiungi_artista' in request.POST:
            codice_artista = request.POST.get('codice_artista')
            aggiunta_artista(codice_evento, codice_artista)
            return redirect('gestione_artisti', codice_evento=codice_evento)

        elif 'rimuovi_artista' in request.POST:
            codice_artista = request.POST.get('codice_artista')
            rimozione_artista(codice_evento, codice_artista)
            return redirect('gestione_artisti', codice_evento=codice_evento)

    context = {
        'codice_evento': codice_evento,
        'artisti_associati': artisti_associati,
        'artisti_disponibili': artisti_disponibili,
    }
    return render(request, 'gestione_artisti.html', context)

@admin_required
def gestione_liste_pr_view(request, codice_evento):
    if request.method == 'POST':
        azione = request.POST.get('azione')
        nome_lista = request.POST.get('nome_lista')
        codice_pr = request.POST.get('codice_pr')
        codice_lista = request.POST.get('codice_lista')  # necessario solo per rimozione

        if azione == 'aggiungi':
            if nome_lista and codice_pr:
                aggiunta_lista_pr(nome_lista, codice_evento, codice_pr)

        elif azione == 'rimuovi':
            if codice_lista:
                rimozione_lista_pr(codice_lista)

        return redirect('gestione_liste_pr', codice_evento=codice_evento)

    # Caricamento dati per il template
    liste_pr = visualizza_liste_pr(codice_evento)  # Presumibilmente restituisce una lista di dizionari
    evento_raw = visualizza_evento(codice_evento)
    evento = evento_raw[0] if evento_raw else {}
    pr_disponibili = get_pr_disponibili()

    return render(request, 'gestione_liste_pr.html', {
        'codice_evento': codice_evento,
        'liste_pr': liste_pr,
        'evento': evento,
        'pr': pr_disponibili,
    })


@admin_required
def gestione_tavoli_view(request, codice_evento):
    if request.method == 'POST':
        if 'aggiungi_tavolo' in request.POST:
            posti_massimi = request.POST.get('posti_massimi')
            nome = request.POST.get('nome')
            area = request.POST.get('area')

            if posti_massimi and nome and area:
                try:
                    posti_massimi = int(posti_massimi)
                    aggiunta_tavolo(posti_massimi, nome, area, codice_evento)
                except ValueError:
                    # gestione errore, posti_massimi non è un numero valido
                    pass

        elif 'rimuovi_tavolo' in request.POST:
            codice_tavolo = request.POST.get('codice_tavolo_rimuovi')
            if codice_tavolo:
                rimozione_tavolo(codice_tavolo, codice_evento)

        return redirect('gestione_tavoli', codice_evento=codice_evento)

    # Funzione che recupera i tavoli dal DB, la devi implementare tu
    tavoli = visualizza_tavoli_per_evento(codice_evento)
    evento_raw = visualizza_evento(codice_evento)
    evento = evento_raw[0] if evento_raw else {}


    return render(request, 'gestione_tavoli.html', {
        'codice_evento': codice_evento,
        'tavoli': tavoli,
        'evento': evento,
    })

@admin_required
def gestione_artisti_db_view(request):
    if request.method == 'POST':
        if 'aggiungi_artista' in request.POST:
            nome = request.POST.get('nome')
            if nome:
                aggiungi_artista_db(nome)
        elif 'rimuovi_artista' in request.POST:
            codice_artista = request.POST.get('codice_artista')
            if codice_artista:
                rimuovi_artista_db(codice_artista)
        return redirect('gestione_artisti_db')

    # Presumo esista una funzione per ottenere gli artisti:
    artisti = get_artisti()

    return render(request, 'gestione_artisti_db.html', {'artisti': artisti})

def gestione_pr_db_view(request):
    if request.method == 'POST':
        if 'aggiungi_pr' in request.POST:
            nome = request.POST.get('nome')
            cognome = request.POST.get('cognome')
            if nome and cognome:
                aggiungi_pr_db(nome, cognome)
        elif 'rimuovi_pr' in request.POST:
            codice_pr = request.POST.get('codice_pr')
            if codice_pr:
                rimuovi_pr_db(codice_pr)
        return redirect('gestione_pr_db')

    # Presumo esista una funzione per ottenere i pr:
    prs = get_pr_disponibili()

    return render(request, 'gestione_pr_db.html', {'prs': prs})