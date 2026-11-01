import flet as ft
from UI.view import View
from model.model import DepositoStrumenti

'''
    CONTROLLER:
    - Funziona da intermediario tra MODELLO e VIEW
    - Gestisce la logica del flusso dell'applicazione
'''

class Controller:
    def __init__(self, view: View, model: DepositoStrumenti):
        self._model = model
        self._view = view

    def get_nome(self):
        return self._model.nome

    def get_responsabile(self):
        return self._model.responsabile

    def set_responsabile(self, responsabile):
        self._model.responsabile = responsabile

    def conferma_responsabile(self, e):
        self._model.responsabile = self._view.input_responsabile.value
        self._view.txt_responsabile.value = f"Responsabile: {self._model.responsabile}"
        self._view.update()

    # Altre Funzioni Event Handler

    def mostra_strumenti(self, e):
        # Gestisce il click sul bottone 'Mostra'

        # 1. Pulisce i risultati precedenti dalla ListView
        self._view.lista_strumenti.controls.clear()

        # 2. Richiama il modello
        strumenti = self._model.get_strumenti()

        # 3. Gestisce le varie casistiche
        if strumenti is None:
            self._view.show_alert("Errore di connessione: impossibile recuperare gli strumenti")
        elif len(strumenti) == 0:
            self._view.lista_strumenti.controls.append(ft.Text("Nessuno strumento presente nel deposito."))
        else:
            # Popola la lista chiamando il __str__ dell'oggetto Strumento
            for strumento in strumenti:
                self._view.lista_strumenti.controls.append(ft.Text(str(strumento)))

        # 4. Aggiorna l'interfaccia
        self._view.update()

    def cerca_strumenti(self, e):
        # Gestisce il click sul bottone 'Cerca'

        # 1. Recupera il testo inserito dall'utente e pulisce la lista
        tipo_cercato = self._view.input_tipo_strumento.value
        self._view.lista_strumenti_ricerca.controls.clear()

        # 2. Validazione dell'input
        if not tipo_cercato:
            self._view.show_alert("Attenzione: Inserire un tipo di strumento per avviare la ricerca.")
            self._view.update()
            return

        # 3. Richiama il modello passando il tipo
        strumenti = self._model.cerca_strumenti_per_tipo(tipo_cercato)

        # 4. Gestisce le casistiche
        if strumenti is None:
            self._view.show_alert("Errore di connessione durante la ricerca.")
        elif len(strumenti) == 0:
            self._view.lista_strumenti_ricerca.controls.append(ft.Text(f"Nessun risultato per: '{tipo_cercato}'."))
        else:
            for strumento in strumenti:
                self._view.lista_strumenti_ricerca.controls.append(ft.Text(str(strumento)))

        # 5. Aggiorna l'interfaccia
        self._view.update()

