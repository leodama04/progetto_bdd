from django.db import connection

# Esempio funzione per eseguire query con fetch
def run_select_query(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
    return results

# Esempio funzione per eseguire query di modifica (INSERT/UPDATE/DELETE)
def run_modify_query(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        # Se vuoi puoi fare connection.commit() ma Django lo gestisce
    return True


# --- OPERAZIONI CLIENTE ---

def iscrizione_utente(ruolo, password, data_di_nascita, nome, cognome, telefono):
    query = """
    INSERT INTO UTENTE (
      ruolo, password, data_di_nascita, nome, cognome, telefono
    ) VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = [ruolo, password, data_di_nascita, nome, cognome, telefono]
    return run_modify_query(query, params)

def login_utente(nome, password):
    query = """
    SELECT id_utente
    FROM UTENTE
    WHERE nome = %s AND password = %s
    """
    params = [nome, password]
    return run_select_query(query, params)

def riconoscimento_ruolo(id_utente):
    query = """
    SELECT ruolo
    FROM UTENTE
    WHERE id_utente = %s
    """
    params = [id_utente]
    return run_select_query(query, params)

def aggiunta_carta_di_credito(numero_carta, nome_titolare, data_di_scadenza, tipo, id_utente):
    query = """
    INSERT INTO CARTA_DI_CREDITO (
      numero_carta, nome_titolare, data_di_scadenza, tipo, id_utente
    ) VALUES (%s, %s, %s, %s, %s)
    """
    params = [numero_carta, nome_titolare, data_di_scadenza, tipo, id_utente]
    return run_modify_query(query, params)

def visualizza_serate_pubbliche():
    query = """
    SELECT
      codice_evento, nome, data, ora_inizio, ora_fine, prezzo
    FROM EVENTO
    WHERE tipo = 'pubblica'
    """
    return run_select_query(query)

def acquisto_biglietto(ID_ACQ, data, importo, codice_metodo_pagamento, id_utente, codice_biglietto):
    query_acquisto = """
    INSERT INTO ACQUISTO_BIGLIETTO (
      ID_ACQ, data, importo, codice_metodo_pagamento, id_utente
    ) VALUES (%s, %s, %s, %s, %s)
    """
    params_acquisto = [ID_ACQ, data, importo, codice_metodo_pagamento, id_utente]
    run_modify_query(query_acquisto, params_acquisto)

    query_biglietto = """
    INSERT INTO BIGLIETTO_ACQUISTATO (
      codice_biglietto, ID_ACQ
    ) VALUES (%s, %s)
    """
    params_biglietto = [codice_biglietto, ID_ACQ]
    return run_modify_query(query_biglietto, params_biglietto)

def visualizza_tavoli_per_evento(codice_evento):
    query = """
    SELECT
      codice_tavolo, posti_massimi, nome, area
    FROM TAVOLO
    WHERE codice_evento = %s
    """
    params = [codice_evento]
    return run_select_query(query, params)

def seleziona_tavolo(codice_tavolo, codice_biglietto):
    query = """
    UPDATE BIGLIETTO
    SET codice_tavolo = %s
    WHERE codice_biglietto = %s
    """
    params = [codice_tavolo, codice_biglietto]
    return run_modify_query(query, params)

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

def iscrizione_a_lista_pr(codice_lista, id_utente):
    query = """
    INSERT INTO ISCRIZIONE (
      codice_lista, id_utente
    ) VALUES (%s, %s)
    """
    params = [codice_lista, id_utente]
    return run_modify_query(query, params)

def richiesta_serata_privata(codice_richiesta, numero_invitati, descrizione, stato,
                            ora_inizio, ora_fine, data_serata, id_utente):
    query = """
    INSERT INTO RICHIESTA_PRENOTAZIONE_SERATA (
      codice_richiesta, numero_invitati, descrizione, stato,
      ora_inizio, ora_fine, data_serata, id_utente
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = [codice_richiesta, numero_invitati, descrizione, stato,
              ora_inizio, ora_fine, data_serata, id_utente]
    return run_modify_query(query, params)

def acquisto_serata_privata(codice_evento, codice_acquisto_serata, data, importo, codice_metodo_pagamento, id_utente):
    query = """
    INSERT INTO ACQUISTO_SERATA_PRIVATA (
      codice_evento, codice_acquisto_serata, data,
      importo, codice_metodo_pagamento, id_utente
    ) VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = [codice_evento, codice_acquisto_serata, data, importo, codice_metodo_pagamento, id_utente]
    return run_modify_query(query, params)

def visualizza_area_personale_biglietti(id_utente):
    query = """
    SELECT
      AB.ID_ACQ, B.codice_biglietto, B.tipo, B.prezzo AS prezzo_biglietto,
      E.nome AS nome_evento, E.data AS data_evento,
      E.ora_inizio, E.ora_fine,
      CASE WHEN B.codice_tavolo IS NULL THEN 'STANDARD' ELSE 'TAVOLO' END AS tipo_biglietto,
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
      codice_richiesta, numero_invitati, descrizione, stato,
      ora_inizio, ora_fine, data_serata
    FROM RICHIESTA_PRENOTAZIONE_SERATA
    WHERE id_utente = %s
    """
    params = [id_utente]
    return run_select_query(query, params)

def visualizza_area_personale_serate_acquistate(id_utente):
    query = """
    SELECT
      ASP.codice_acquisto_serata, ASP.codice_evento,
      E.nome AS nome_evento, ASP.data AS data_acquisto_serata,
      ASP.importo
    FROM ACQUISTO_SERATA_PRIVATA ASP
    JOIN EVENTO E ON ASP.codice_evento = E.codice_evento
    WHERE ASP.id_utente = %s
    """
    params = [id_utente]
    return run_select_query(query, params)


# --- OPERAZIONI AMMINISTRATORE ---

def aggiungere_evento(numero_partecipanti, tipo, descrizione, prezzo,
                      nome, data, genere, ora_inizio, ora_fine):
    query = """
    INSERT INTO EVENTO (
      numero_partecipanti, tipo, descrizione, prezzo,
      nome, data, genere, ora_inizio, ora_fine
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = [numero_partecipanti, tipo, descrizione, prezzo,
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

def aggiunta_lista_pr(codice_lista, nome_lista, codice_evento, codice_pr):
    query = """
    INSERT INTO LISTA_PR (
      codice_lista, nome_lista, codice_evento, codice_pr
    ) VALUES (%s, %s, %s, %s)
    """
    params = [codice_lista, nome_lista, codice_evento, codice_pr]
    return run_modify_query(query, params)

def rimozione_lista_pr(codice_evento, codice_pr):
    query = """
    DELETE FROM LISTA_PR
    WHERE codice_evento = %s AND codice_pr = %s
    """
    params = [codice_evento, codice_pr]
    return run_modify_query(query, params)

def aggiunta_tavolo(codice_tavolo, posti_massimi, nome, area, codice_evento):
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
