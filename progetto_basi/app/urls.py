from django.urls import path
from . import views

urlpatterns = [
    # UTENTE - pubblico o autenticato
    path('', views.home, name='home'),
    path('registrazione/', views.registra_utente, name='registra_utente'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    path('aggiungi_carta/', views.aggiungi_carta, name='aggiungi_carta'),
    path('serate_pubbliche/', views.mostra_serate_pubbliche, name='mostra_serate_pubbliche'),
    path('acquista_biglietto/', views.acquista_biglietto_view, name='acquista_biglietto_view'),
    path('seleziona_tavolo/', views.seleziona_tavolo_view, name='seleziona_tavolo_view'),
    path('iscrizione_lista_pr/', views.iscrizione_lista_pr_view, name='iscrizione_lista_pr_view'),
    path('richiesta_serata_privata/', views.richiesta_serata_privata_view, name='richiesta_serata_privata_view'),
    path('acquisto_serata_privata/', views.acquisto_serata_privata_view, name='acquisto_serata_privata_view'),

    # AREA PERSONALE
    path('area_personale/biglietti/', views.area_personale_biglietti, name='area_personale_biglietti'),
    path('area_personale/richieste/', views.area_personale_richieste, name='area_personale_richieste'),
    path('area_personale/serate_acquistate/', views.area_personale_serate_acquistate, name='area_personale_serate_acquistate'),

    # AMMINISTRATORE
    path('admin/aggiungi_evento/', views.aggiungi_evento_view, name='aggiungi_evento_view'),
    path('admin/rimuovi_evento/<int:codice_evento>/', views.rimuovi_evento_view, name='rimuovi_evento_view'),
    path('admin/gestione_richieste/', views.accetta_rifiuta_richiesta_view, name='accetta_rifiuta_richiesta_view'),
    path('admin/aggiungi_artista/', views.aggiungi_artista_view, name='aggiungi_artista_view'),
    path('admin/rimuovi_artista/', views.rimuovi_artista_view, name='rimuovi_artista_view'),
    path('admin/aggiungi_lista_pr/', views.aggiungi_lista_pr_view, name='aggiungi_lista_pr_view'),
    path('admin/rimuovi_lista_pr/', views.rimuovi_lista_pr_view, name='rimuovi_lista_pr_view'),
    path('admin/aggiungi_tavolo/', views.aggiungi_tavolo_view, name='aggiungi_tavolo_view'),
    path('admin/rimuovi_tavolo/', views.rimuovi_tavolo_view, name='rimuovi_tavolo_view'),
]
