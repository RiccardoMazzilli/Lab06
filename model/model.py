from database.DB_connect import get_connection
from model import strumento
from model.strumento import Strumento
from model.prestito import Prestito



'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        self._nome = nome
        self._responsabile = responsabile

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def responsabile(self):
        return self._responsabile

    @responsabile.setter
    def responsabile(self, responsabile):
        self._responsabile = responsabile

    def get_strumenti(self) -> list[Strumento] | None:
        """
            Funzione che legge tutti gli strumenti nel database
            :return: una lista con tutti gli strumenti presenti oppure None
        """
        conn = get_connection()
        if conn is None:
            return None

        strumenti = []
        try:
            # utilizzo del dizionario per accedere ai risultati tramite i nomi delle colonne
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM strumento"
            cursor.execute(query)

            for row in cursor.fetchall():
                strumento = (
                    row['codice'],
                    row['tipo'],
                    row['marca'],
                    row['anno_acquisto'],
                    row['valore'],
                    row['disponibile']
                )
                strumenti.append(strumento)

            cursor.close()
            conn.close()
            return strumenti
        except Exception as e:
            print(f"Errore durante la lettura degli strumenti : {e}")
            if conn.is_connected():
                conn.close()
            return None


    def cerca_strumenti_per_tipo(self, tipo) -> list[Strumento] | None:
        """
            Funzione che recupera una lista con tutti gli strumenti presenti nel database di un certo tipo
            :param tipo: il tipo dello strumento (es. "Chitarra")
            :return: una lista con tutti gli strumenti del tipo indicato oppure None
        """
        conn = get_connection()
        if conn is None:
            return None

        strumenti = []
        try:
            cursor = conn.cursor(dictionary=True)
            # Utilizzo %s come segnaposto
            query = "SELECT * FROM strumento WHERE tipo = %s"
            cursor.execute(query, (tipo,))

            for row in cursor.fetchall():
                strumento = Strumento(
                    row['codice'],
                    row['tipo'],
                    row['marca'],
                    row['anno_acquisto'],
                    row['valore'],
                    row['disponibile']
                )
                strumenti.append(strumento)

            cursor.close()
            conn.close()
            return strumenti
        except Exception as e:
            print(f"Errore durante la ricerca per tipo: {e}")
            if conn.is_connected():
                conn.close()
            return None
