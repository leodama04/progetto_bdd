from django.db import models

class AcquistoBiglietto(models.Model):
    id_acq = models.AutoField(db_column='ID_ACQ', primary_key=True)
    codice_acquisto_biglietto = models.CharField(unique=True, max_length=10)
    data = models.DateField()
    importo = models.DecimalField(max_digits=10, decimal_places=2)
    codice_metodo_di_pagamento = models.ForeignKey('CartaDiCredito', models.DO_NOTHING, db_column='codice_metodo_di_pagamento', blank=True, null=True)
    id_utente = models.ForeignKey('Utente', models.DO_NOTHING, db_column='id_utente', blank=True, null=True)

    class Meta:
        db_table = 'acquisto_biglietto'


class AcquistoSerataPrivata(models.Model):
    codice_evento = models.OneToOneField('Evento', models.DO_NOTHING, db_column='codice_evento', primary_key=True)
    codice_acquisto_serata = models.CharField(unique=True, max_length=10)
    data = models.DateField()
    importo = models.DecimalField(max_digits=10, decimal_places=2)
    id_utente = models.ForeignKey('Utente', models.DO_NOTHING, db_column='id_utente', blank=True, null=True)
    codice_metodo_di_pagamento = models.ForeignKey('CartaDiCredito', models.DO_NOTHING, db_column='codice_metodo_di_pagamento', blank=True, null=True)

    class Meta:
        db_table = 'acquisto_serata_privata'


class Artista(models.Model):
    codice_artista = models.CharField(primary_key=True, max_length=10)
    nome = models.CharField(max_length=50)

    class Meta:
        db_table = 'artista'


class Biglietto(models.Model):
    codice_biglietto = models.CharField(primary_key=True, max_length=10)
    tipo = models.CharField(max_length=50, blank=True, null=True)
    prezzo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    codice_evento = models.ForeignKey('Evento', models.DO_NOTHING, db_column='codice_evento', blank=True, null=True)
    codice_tavolo = models.ForeignKey('Tavolo', models.DO_NOTHING, db_column='codice_tavolo', blank=True, null=True)

    class Meta:
        db_table = 'biglietto'


class BigliettoAcquistato(models.Model):
    codice_biglietto = models.OneToOneField(Biglietto, models.DO_NOTHING, db_column='codice_biglietto', primary_key=True)
    id_acq = models.ForeignKey(AcquistoBiglietto, models.DO_NOTHING, db_column='ID_ACQ')

    class Meta:
        db_table = 'biglietto_acquistato'


class CartaDiCredito(models.Model):
    codice_metodo_di_pagamento = models.CharField(primary_key=True, max_length=10)
    numero_di_carta = models.CharField(max_length=20)
    nome_titolare = models.CharField(max_length=50, blank=True, null=True)
    data_di_scadenza = models.DateField(blank=True, null=True)
    tipo = models.CharField(max_length=20, blank=True, null=True)
    id_utente = models.ForeignKey('Utente', models.DO_NOTHING, db_column='id_utente', blank=True, null=True)

    class Meta:
        db_table = 'carta_di_credito'


class Evento(models.Model):
    codice_evento = models.CharField(primary_key=True, max_length=10)
    nome = models.CharField(max_length=100)
    descrizione = models.TextField(blank=True, null=True)
    data = models.DateField()
    ora_inizio = models.TimeField(blank=True, null=True)
    ora_fine = models.TimeField(blank=True, null=True)
    tipo = models.CharField(max_length=20, blank=True, null=True)
    genere = models.CharField(max_length=50, blank=True, null=True)
    prezzo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    numero_partecipanti = models.IntegerField(blank=True, null=True)
    codice_richiesta = models.ForeignKey('RichiestaPrenotazioneSerata', models.DO_NOTHING, db_column='codice_richiesta', blank=True, null=True)

    class Meta:
        db_table = 'evento'


class Iscrizione(models.Model):
    codice_lista = models.ForeignKey('ListaPr', models.DO_NOTHING, db_column='codice_lista')
    id_utente = models.ForeignKey('Utente', models.DO_NOTHING, db_column='id_utente')

    class Meta:
        db_table = 'iscrizione'
        unique_together = (('codice_lista', 'id_utente'),)


class ListaPr(models.Model):
    codice_lista = models.CharField(primary_key=True, max_length=10)
    nome_lista = models.CharField(max_length=50, blank=True, null=True)
    codice_evento = models.ForeignKey(Evento, models.DO_NOTHING, db_column='codice_evento', blank=True, null=True)
    codice_pr = models.ForeignKey('Pr', models.DO_NOTHING, db_column='codice_pr', blank=True, null=True)

    class Meta:
        db_table = 'lista_pr'


class Partecipazione(models.Model):
    codice_evento = models.ForeignKey(Evento, models.DO_NOTHING, db_column='codice_evento')
    codice_artista = models.ForeignKey(Artista, models.DO_NOTHING, db_column='codice_artista')

    class Meta:
        db_table = 'partecipazione'
        unique_together = (('codice_evento', 'codice_artista'),)


class Pr(models.Model):
    codice_pr = models.CharField(primary_key=True, max_length=10)
    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=50)

    class Meta:
        db_table = 'pr'


class RichiestaPrenotazioneSerata(models.Model):
    codice_richiesta = models.CharField(primary_key=True, max_length=10)
    numero_invitati = models.IntegerField(blank=True, null=True)
    descrizione = models.TextField(blank=True, null=True)
    stato = models.CharField(max_length=9)
    ora_inizio = models.TimeField(blank=True, null=True)
    ora_fine = models.TimeField(blank=True, null=True)
    data_serata = models.DateField(blank=True, null=True)
    id_utente = models.ForeignKey('Utente', models.DO_NOTHING, db_column='id_utente', blank=True, null=True)

    class Meta:
        db_table = 'richiesta_prenotazione_serata'


class Tavolo(models.Model):
    codice_tavolo = models.CharField(primary_key=True, max_length=10)
    posti_massimi = models.IntegerField(blank=True, null=True)
    nome = models.CharField(max_length=50, blank=True, null=True)
    area = models.CharField(max_length=50, blank=True, null=True)
    codice_evento = models.ForeignKey(Evento, models.DO_NOTHING, db_column='codice_evento', blank=True, null=True)

    class Meta:
        db_table = 'tavolo'


class Utente(models.Model):
    id_utente = models.CharField(primary_key=True, max_length=10)
    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=50)
    data_di_nascita = models.DateField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    ruolo = models.CharField(max_length=7)
    password = models.CharField(max_length=100)

    class Meta:
        db_table = 'utente'
