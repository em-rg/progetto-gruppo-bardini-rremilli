class Studente:
    """
    Rappresenta uno studente con nome e cognome.

    Parameters
    ----------
    nome : str
        Il nome dello studente.
    cognome : str
        Il cognome dello studente.
    """

    def __init__(self, nome, cognome):
        self.nome = nome
        self.cognome = cognome

    def __str__(self):
        """
        Restituisce la rappresentazione in stringa dello studente.

        Returns
        -------
        str
            Nome e cognome dello studente.
        """
        return f"{self.nome} {self.cognome}"


def aggiungi_studente(studenti):
    """
    Aggiunge uno studente alla lista dopo aver richiesto nome e cognome.

    Parameters
    ----------
    studenti : list of Studente
        La lista degli studenti a cui aggiungere il nuovo studente.

    Returns
    -------
    None
    """
    try:
        nome = input("Inserisci il nome: ").strip()
        if not nome.isalpha():
            print("Errore: Il nome deve contenere solo lettere.")
            return
        cognome = input("Inserisci il cognome: ").strip()
        if not cognome.isalpha():
            print("Errore: Il cognome deve contenere solo lettere.")
            return
        studenti.append(Studente(nome.title(), cognome.title()))
        print("Studente aggiunto correttamente.")
    except Exception as e:
        print(f"Errore inatteso durante l'aggiunta dello studente: {e}")


def elenca_studenti(studenti):
    """
    Elenca tutti gli studenti ordinati per cognome e nome.

    Parameters
    ----------
    studenti : list of Studente
        La lista degli studenti da elencare.

    Returns
    -------
    None
    """
    try:
        if not studenti:
            print("Nessuno studente presente.")
            return
        studenti_ordinati = sorted(studenti, key=lambda s: (s.cognome.lower(), s.nome.lower()))
        print("Elenco studenti:")
        for studente in studenti_ordinati:
            print(f"- {studente}")
    except Exception as e:
        print(f"Errore inatteso durante l'elenco degli studenti: {e}")


def cerca_studente(studenti):
    """
    Cerca studenti per nome nella lista.

    Parameters
    ----------
    studenti : list of Studente
        La lista degli studenti in cui cercare.

    Returns
    -------
    None
    """
    try:
        query = input("Inserisci il nome da cercare: ").strip().lower()
        if not query:
            print("Errore: Inserire almeno una lettera.")
            return
        trovati = [s for s in studenti if query in s.nome.lower()]
        if trovati:
            print("Studenti trovati:")
            for studente in trovati:
                print(f"- {studente}")
        else:
            print("Nessuno studente trovato con questo nome.")
    except Exception as e:
        print(f"Errore inatteso durante la ricerca dello studente: {e}")
