from django.contrib import admin
from .models import (
    Utente, Evento, Biglietto, Tavolo, AcquistoBiglietto,
    AcquistoSerataPrivata, BigliettoAcquistato, CartaDiCredito,
    ListaPr, Partecipazione, Pr, RichiestaPrenotazioneSerata,
    Artista, Iscrizione
)

admin.site.register(Utente)
admin.site.register(Evento)
admin.site.register(Biglietto)
admin.site.register(Tavolo)
admin.site.register(AcquistoBiglietto)
admin.site.register(AcquistoSerataPrivata)
admin.site.register(BigliettoAcquistato)
admin.site.register(CartaDiCredito)
admin.site.register(ListaPr)
admin.site.register(Partecipazione)
admin.site.register(Pr)
admin.site.register(RichiestaPrenotazioneSerata)
admin.site.register(Artista)
admin.site.register(Iscrizione)