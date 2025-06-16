import datetime
import random
import string
from django.db import connection


def generate_codice():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


def run_select_query(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
    return results

def run_modify_query(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.lastrowid  # restituisci l'ID dell'ultimo record inserito



# --- OPERAZIONI CLIENTE ---

def iscrizione_utente(id_utente, ruolo, password, data_di_nascita, nome, cognome, telefono):
    query = """
    INSERT INTO UTENTE (
      id_utente, ruolo, password, data_di_nascita, nome, cognome, telefono
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    params = [id_utente, ruolo, password, data_di_nascita, nome, cognome, telefono]
    return run_modify_query(query, params)

def login_utente(id_utente, password):
    query = """
    SELECT id_utente
    FROM UTENTE
    WHERE id_utente = %s AND password = %s
    """
    params = [id_utente, password]
    return run_select_query(query, params)

def riconoscimento_ruolo(id_utente):
    query = """
    SELECT ruolo
    FROM UTENTE
    WHERE id_utente = %s
    """
    params = [id_utente]
    return run_select_query(query, params)

def aggiunta_carta_di_credito(numero_di_carta, nome_titolare, data_di_scadenza, tipo, id_utente):
    codice_metodo_di_pagamento = generate_codice() 
    query = """
    INSERT INTO CARTA_DI_CREDITO (
      codice_metodo_di_pagamento, numero_di_carta, nome_titolare, data_di_scadenza, tipo, id_utente
    ) VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = [codice_metodo_di_pagamento, numero_di_carta, nome_titolare, data_di_scadenza, tipo, id_utente]
    return run_modify_query(query, params)

def rimuovi_carta_di_credito(codice_metodo_di_pagamento, id_utente):
    query = """
    DELETE FROM CARTA_DI_CREDITO
    WHERE codice_metodo_di_pagamento = %s AND id_utente = %s
    """
    params = [codice_metodo_di_pagamento, id_utente]
    return run_modify_query(query, params)


def visualizza_evento(codice_evento):
    query = """
    SELECT
      codice_evento, nome, data, ora_inizio, ora_fine, prezzo, numero_partecipanti, genere
    FROM EVENTO
    WHERE codice_evento = %s
    """
    params = [codice_evento]
    return run_select_query(query, params)


def get_evento_da_richiesta(codice_richiesta):
    query = """
    SELECT codice_evento
    FROM EVENTO
    WHERE codice_richiesta = %s
    """
    result = run_select_query(query, [codice_richiesta])

    if not result:
        print(f"[DEBUG] Nessun evento trovato per richiesta: {codice_richiesta}")
        return None

    row = result[0]
    return row['codice_evento'] if 'codice_evento' in row else None


def visualizza_serate_pubbliche():
    query = """
    SELECT
      codice_evento, nome, data, ora_inizio, ora_fine, prezzo, numero_partecipanti, genere, descrizione
    FROM EVENTO
    WHERE tipo = 'pubblico'
    """
    return run_select_query(query)

def visualizza_carte_di_credito(id_utente):
    query = """
    SELECT
      codice_metodo_di_pagamento, numero_di_carta, nome_titolare, data_di_scadenza, tipo
    FROM CARTA_DI_CREDITO
    WHERE id_utente = %s
    """
    params = [id_utente]
    return run_select_query(query, params)

from app.models import AcquistoBiglietto, Biglietto
from datetime import date

def acquisto_biglietto(tipo, importo, codice_metodo_di_pagamento, id_utente, codice_evento, codice_tavolo):

    #Scritto in django, ma la logica è la stessa

    codice_biglietto = generate_codice()
    codice_acquisto_biglietto = generate_codice()

    acquisto = AcquistoBiglietto.objects.create(
        data=date.today(),
        importo=importo,
        codice_metodo_di_pagamento_id=codice_metodo_di_pagamento,
        id_utente_id=id_utente,
        codice_acquisto_biglietto=codice_acquisto_biglietto
    )

    Biglietto.objects.create(
        codice_biglietto=codice_biglietto,
        tipo=tipo,
        prezzo=importo,
        codice_evento_id=codice_evento,
        codice_tavolo_id=codice_tavolo if tipo == 'T' else None    
    )

    query_biglietto = """
    INSERT INTO biglietto_acquistato (
        codice_biglietto, ID_ACQ
    ) VALUES (%s, %s)
    """
    params_biglietto = [codice_biglietto, acquisto.id_acq]
    run_modify_query(query_biglietto, params_biglietto)

    return codice_biglietto


def visualizza_tavoli_per_evento(codice_evento):
    query = """
    SELECT
      codice_tavolo, posti_massimi, nome, area
    FROM TAVOLO
    WHERE codice_evento = %s
    """
    params = [codice_evento]
    return run_select_query(query, params)

def visualizza_liste_pr(codice_evento):
    query = """
    SELECT
      LP.codice_lista, LP.nome_lista, PR.codice_pr, PR.nome, PR.cognome
    FROM LISTA_PR LP
    JOIN PR ON LP.codice_pr = PR.codice_pr
    WHERE LP.codice_evento = %s
    """
    params = [codice_evento]
    return run_select_query(query, params)

def get_liste_pr_utente(id_utente):
    query = """
    SELECT
      LP.codice_lista, LP.nome_lista, PR.codice_pr, PR.nome, PR.cognome
    FROM ISCRIZIONE I
    JOIN LISTA_PR LP ON I.codice_lista = LP.codice_lista
    JOIN PR ON LP.codice_pr = PR.codice_pr
    WHERE I.id_utente = %s
    """
    params = [id_utente]
    return run_select_query(query, params)

def iscrizione_a_lista_pr(codice_lista, id_utente):
    query = """
    INSERT INTO ISCRIZIONE (
      codice_lista, id_utente
    ) VALUES (%s, %s)
    """
    params = [codice_lista, id_utente]
    return run_modify_query(query, params)

def disiscrizione_da_lista_pr(codice_lista, id_utente):
    query = """
    DELETE FROM ISCRIZIONE
    WHERE codice_lista = %s AND id_utente = %s
    """
    params = [codice_lista, id_utente]
    return run_modify_query(query, params)

def richiesta_serata_privata(numero_invitati, descrizione,
                              ora_inizio, ora_fine, data_serata,
                              id_utente, nome_evento, genere):
    codice_richiesta = generate_codice()
    codice_evento = generate_codice()
    stato = 'P'
    prezzo = 1000 # prezzo fisso per serata privata, può essere modificato in futuro

    query_richiesta = """
    INSERT INTO RICHIESTA_PRENOTAZIONE_SERATA (
        codice_richiesta, numero_invitati, descrizione, stato,
        ora_inizio, ora_fine, data_serata, id_utente, nome_evento
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    params_richiesta = [
        codice_richiesta, numero_invitati, descrizione, stato,
        ora_inizio, ora_fine, data_serata, id_utente, nome_evento
    ]
    run_modify_query(query_richiesta, params_richiesta)

    query_evento = """
    INSERT INTO EVENTO (
        codice_evento, nome, descrizione, data,
        ora_inizio, ora_fine, tipo, genere,
        prezzo, numero_partecipanti, codice_richiesta
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    params_evento = [
        codice_evento,
        nome_evento,
        descrizione,
        data_serata,
        ora_inizio,
        ora_fine,
        'privato',
        genere,
        prezzo,
        numero_invitati,
        codice_richiesta
    ]
    success_evento = run_modify_query(query_evento, params_evento)

    return success_evento


def acquisto_serata_privata(codice_evento, codice_metodo_di_pagamento, id_utente):
    codice_acquisto_serata = generate_codice()

    query_prezzo = "SELECT prezzo FROM evento WHERE codice_evento = %s"
    result = run_select_query(query_prezzo, [codice_evento])
    if not result or result[0]['prezzo'] is None:
        raise ValueError("Prezzo evento non trovato o nullo")

    importo = result[0]['prezzo']
    data = datetime.date.today()  

    query = """
    INSERT INTO ACQUISTO_SERATA_PRIVATA (
        codice_evento, codice_acquisto_serata, data,
        importo, codice_metodo_di_pagamento, id_utente
    ) VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = [codice_evento, codice_acquisto_serata, data, importo, codice_metodo_di_pagamento, id_utente]
    run_modify_query(query, params)

    return codice_acquisto_serata

def visualizza_area_personale_biglietti(id_utente):
    query = """
    SELECT
      AB.ID_ACQ, B.codice_biglietto, B.tipo AS tipo_biglietto, B.prezzo AS prezzo_biglietto,
      E.nome AS nome_evento, E.data AS data_evento,
      E.ora_inizio, E.ora_fine,
      T.codice_tavolo, T.nome AS nome_tavolo, T.posti_massimi, T.area
    FROM ACQUISTO_BIGLIETTO AB
    JOIN BIGLIETTO_ACQUISTATO BA ON AB.ID_ACQ = BA.ID_ACQ
    JOIN BIGLIETTO B ON BA.codice_biglietto = B.codice_biglietto
    JOIN EVENTO E ON B.codice_evento = E.codice_evento
    LEFT JOIN TAVOLO T ON B.codice_tavolo = T.codice_tavolo
    WHERE AB.id_utente = %s
    """
    params = [id_utente]
    return run_select_query(query, params)

def visualizza_area_personale_richieste(id_utente):
    query = """
    SELECT
      R.codice_richiesta, R.numero_invitati, R.descrizione, R.stato,
      R.ora_inizio, R.ora_fine, R.data_serata, R.nome_evento
    FROM RICHIESTA_PRENOTAZIONE_SERATA R
    LEFT JOIN EVENTO E ON E.codice_richiesta = R.codice_richiesta
    LEFT JOIN ACQUISTO_SERATA_PRIVATA A ON A.codice_evento = E.codice_evento
    WHERE R.id_utente = %s
      AND A.codice_acquisto_serata IS NULL
    """
    params = [id_utente]
    return run_select_query(query, params)


def visualizza_area_personale_serate_acquistate(id_utente):
    query = """
    SELECT
    ASP.codice_acquisto_serata, ASP.codice_evento,
    E.nome AS nome_evento, E.descrizione,
    ASP.data AS data_acquisto_serata,
    ASP.importo
    FROM ACQUISTO_SERATA_PRIVATA ASP
    JOIN EVENTO E ON ASP.codice_evento = E.codice_evento
    WHERE ASP.id_utente = %s
    """
    params = [id_utente]
    return run_select_query(query, params)

def get_artisti_evento(codice_evento):
    query = """
    SELECT A.codice_artista, A.nome
    FROM ARTISTA A
    JOIN PARTECIPAZIONE P ON A.codice_artista = P.codice_artista
    WHERE P.codice_evento = %s
    """
    return run_select_query(query, [codice_evento])


# --- OPERAZIONI AMMINISTRATORE ---

def aggiungi_artista_db(nome):
    codice_artista = generate_codice()  
    query = """
    INSERT INTO ARTISTA (
      codice_artista, nome
    ) VALUES (%s, %s)
    """
    params = [codice_artista, nome]
    return run_modify_query(query, params)

def rimuovi_artista_db(codice_artista):
    query = """
    DELETE FROM ARTISTA
    WHERE codice_artista = %s
    """
    params = [codice_artista]
    return run_modify_query(query, params)

def aggiungi_pr_db(nome, cognome):
    codice_pr = generate_codice()  
    query = """
    INSERT INTO PR (
      codice_pr, nome, cognome
    ) VALUES (%s, %s, %s)
    """
    params = [codice_pr, nome, cognome]
    return run_modify_query(query, params)

def rimuovi_pr_db(codice_pr):
    query = """
    DELETE FROM PR
    WHERE codice_pr = %s
    """
    params = [codice_pr]
    return run_modify_query(query, params)

def aggiungere_evento(numero_partecipanti, tipo, descrizione, prezzo,
                      nome, data, genere, ora_inizio, ora_fine):
    codice_evento = generate_codice()  
    query = """
    INSERT INTO EVENTO (
      codice_evento, numero_partecipanti, tipo, descrizione, prezzo,
      nome, data, genere, ora_inizio, ora_fine
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = [codice_evento, numero_partecipanti, tipo, descrizione, prezzo,
              nome, data, genere, ora_inizio, ora_fine]
    return run_modify_query(query, params)


def rimuovere_evento(codice_evento):
    query = """
    DELETE FROM EVENTO
    WHERE codice_evento = %s
    """
    params = [codice_evento]
    return run_modify_query(query, params)

def accettare_rifiutare_richiesta(codice_richiesta, stato):
    query = """
    UPDATE RICHIESTA_PRENOTAZIONE_SERATA
    SET stato = %s
    WHERE codice_richiesta = %s
    """
    params = [stato, codice_richiesta]
    return run_modify_query(query, params)

def aggiunta_artista(codice_evento, codice_artista):
    query = """
    INSERT INTO PARTECIPAZIONE (
      codice_evento, codice_artista
    ) VALUES (%s, %s)
    """
    params = [codice_evento, codice_artista]
    return run_modify_query(query, params)

def rimozione_artista(codice_evento, codice_artista):
    query = """
    DELETE FROM PARTECIPAZIONE
    WHERE codice_evento = %s AND codice_artista = %s
    """
    params = [codice_evento, codice_artista]
    return run_modify_query(query, params)

def aggiunta_lista_pr(nome_lista, codice_evento, codice_pr):
    codice_lista = generate_codice()  
    query = """
    INSERT INTO LISTA_PR (
      codice_lista, nome_lista, codice_evento, codice_pr
    ) VALUES (%s, %s, %s, %s)
    """
    params = [codice_lista, nome_lista, codice_evento, codice_pr]
    return run_modify_query(query, params)

def rimozione_lista_pr(codice_lista):
    query = """
    DELETE FROM LISTA_PR
    WHERE codice_lista = %s
    """
    params = [codice_lista]
    return run_modify_query(query, params)

def aggiunta_tavolo(posti_massimi, nome, area, codice_evento):
    codice_tavolo = generate_codice()  
    query = """
    INSERT INTO TAVOLO (
      codice_tavolo, posti_massimi, nome, area, codice_evento
    ) VALUES (%s, %s, %s, %s, %s)
    """
    params = [codice_tavolo, posti_massimi, nome, area, codice_evento]
    return run_modify_query(query, params)

def rimozione_tavolo(codice_tavolo, codice_evento):
    query = """
    DELETE FROM TAVOLO
    WHERE codice_tavolo = %s AND codice_evento = %s
    """
    params = [codice_tavolo, codice_evento]
    return run_modify_query(query, params)


def get_artisti_disponibili(codice_evento):
    query = """
    SELECT codice_artista, nome
    FROM ARTISTA
    WHERE codice_artista NOT IN (
        SELECT codice_artista FROM PARTECIPAZIONE WHERE codice_evento = %s
    )
    """
    return run_select_query(query, [codice_evento])

def get_artisti():
    query = "SELECT codice_artista, nome FROM ARTISTA"
    return run_select_query(query)

def get_richieste_in_attesa():
    query = """
    SELECT codice_richiesta, numero_invitati, descrizione, stato,
           ora_inizio, ora_fine, data_serata, id_utente, nome_evento
    FROM RICHIESTA_PRENOTAZIONE_SERATA
    WHERE stato = 'P'
    """
    return run_select_query(query)

def get_pr_disponibili():
    query = "SELECT codice_pr, nome, cognome FROM PR"
    return run_select_query(query)