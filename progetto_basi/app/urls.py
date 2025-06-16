from django.urls import path
from . import views

urlpatterns = [
    # UTENTE
    path('', views.home, name='home'),
    path('registrazione/', views.registra_utente, name='registra_utente'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('no-permission/', views.no_permission_view, name='no_permission'),
    path('aggiungi_carta/', views.aggiungi_carta_view, name='aggiungi_carta'),
    path('serate_pubbliche/', views.mostra_serate_pubbliche, name='mostra_serate_pubbliche'),
    path('serate_pubbliche/acquisto_biglietto_standard/<str:codice_evento>/', views.acquista_biglietto_view, name='acquista_biglietto'),
    path('serate_pubbliche/acquisto_biglietto_tavolo/<str:codice_evento>/', views.acquista_biglietto_tavolo_view, name='acquista_biglietto_tavolo'),
    path('serate_pubbliche/iscrizione_lista_pr/<str:codice_evento>/', views.iscrizione_lista_pr_view, name='iscrizione_lista_pr'),
    path('richiesta_serata_privata/', views.richiesta_serata_privata_view, name='richiesta_serata_privata'),

    # AREA PERSONALE
    path('area_personale/biglietti/', views.area_personale_biglietti, name='area_personale_biglietti'),
    path('area_personale/richieste/', views.area_personale_richieste, name='area_personale_richieste'),
    path('area_personale/serate_acquistate/', views.area_personale_serate_acquistate, name='area_personale_serate_acquistate'),
    path('acquisto_serata_privata/<str:codice_richiesta>/', views.acquisto_serata_privata_view, name='acquisto_serata_privata'),

    # AMMINISTRATORE
    path('admin/gestione_eventi/', views.gestione_eventi_view, name='gestione_eventi'),
    path('admin/gestione_eventi/gestione_artisti/<str:codice_evento>/', views.gestione_artisti_view, name='gestione_artisti'),
    path('admin/gestione_eventi/gestione_liste_pr/<str:codice_evento>/', views.gestione_liste_pr_view, name='gestione_liste_pr'),
    path('admin/gestione_eventi/gestione_tavoli/<str:codice_evento>/', views.gestione_tavoli_view, name='gestione_tavoli'),
    path('admin/gestione_richieste/', views.gestione_richieste_view, name='gestione_richieste'),
    path('admin/gestione_artisti_db', views.gestione_artisti_db_view, name='gestione_artisti_db'),
    path('admin/gestione_pr_db', views.gestione_pr_db_view, name='gestione_pr_db'),


]
