from django import forms
from .models import (
    AcquistoBiglietto, AcquistoSerataPrivata, Artista, Biglietto,
    BigliettoAcquistato, CartaDiCredito, Evento, Iscrizione, ListaPr,
    Partecipazione, Pr, RichiestaPrenotazioneSerata, Tavolo, Utente
)

class AcquistoBigliettoForm(forms.ModelForm):
    class Meta:
        model = AcquistoBiglietto
        fields = '__all__'
        exclude = ['codice_acquisto_biglietto']  

class AcquistoSerataPrivataForm(forms.ModelForm):
    class Meta:
        model = AcquistoSerataPrivata
        fields = ['codice_metodo_di_pagamento']  


class ArtistaForm(forms.ModelForm):
    class Meta:
        model = Artista
        fields = '__all__'

class BigliettoForm(forms.ModelForm):
    class Meta:
        model = Biglietto
        fields = '__all__'

class BigliettoAcquistatoForm(forms.ModelForm):
    class Meta:
        model = BigliettoAcquistato
        fields = '__all__'

class CartaDiCreditoForm(forms.ModelForm):
    class Meta:
        model = CartaDiCredito
        fields = '__all__'

class EventoPubblicoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = '__all__'
        exclude = ['tipo', 'codice_richiesta', 'numero_partecipanti']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}), 
            'ora_inizio': forms.TimeInput(attrs={'type': 'time'}), 
            'ora_fine': forms.TimeInput(attrs={'type': 'time'}),  
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.tipo = 'pubblico'
        instance.numero_partecipanti = 0  
        if commit:
            instance.save()
        return instance

class IscrizioneForm(forms.ModelForm):
    class Meta:
        model = Iscrizione
        fields = '__all__'

class ListaPrForm(forms.ModelForm):
    class Meta:
        model = ListaPr
        fields = '__all__'

class PartecipazioneForm(forms.ModelForm):
    class Meta:
        model = Partecipazione
        fields = '__all__'

class PrForm(forms.ModelForm):
    class Meta:
        model = Pr
        fields = '__all__'

class RichiestaPrenotazioneSerataForm(forms.ModelForm):
    class Meta:
        model = RichiestaPrenotazioneSerata
        fields = '__all__'

class TavoloForm(forms.ModelForm):
    class Meta:
        model = Tavolo
        fields = '__all__'
        exclude = ['codice_tavolo']


class UtenteForm(forms.ModelForm):
    ruolo = forms.ChoiceField(choices=[('A', 'Amministratore'), ('C', 'Cliente')], label="Ruolo")

    class Meta:
        model = Utente
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(),  # Nascondi la password nel form
            'data_di_nascita': forms.DateInput(attrs={'type': 'date'}),  # per una data picker HTML5
        }