class Studente:
    """
    Rappresenta uno studente con nome, cognome e classe.

    Parameters
    ----------
    nome : str
        Il nome dello studente.
    cognome : str
        Il cognome dello studente.
    classe : str
        La classe dello studente (es. '1A', '5F').
    """

    def __init__(self, nome, cognome, classe):
        self.nome = nome
        self.cognome = cognome
        self.classe = classe

    def __str__(self):
        """
        Restituisce la rappresentazione in stringa dello studente.

        Returns
        -------
        str
            Nome, cognome e classe dello studente.
        """
        return f"{self.nome} {self.cognome} ({self.classe})"


def aggiungi_studente(studenti):
    """
    Aggiunge uno studente alla lista dopo aver richiesto nome, cognome e classe.

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
        classe = input("Inserisci la classe (es. 1A, 5F): ").strip().upper()
        # Validazione classe: deve essere tra 1-5 seguito da una lettera maiuscola
        if len(classe) != 2 or not classe[0].isdigit() or not (1 <= int(classe[0]) <= 5) or not classe[1].isalpha() or not classe[1].isupper():
            print("Errore: La classe deve essere nel formato corretto (es. 1A, 5F).")
            return
        studenti.append(Studente(nome.title(), cognome.title(), classe))
        print("Studente aggiunto correttamente.")
    except Exception as e:
        print(f"Errore inatteso durante l'aggiunta dello studente: {e}")


def elenca_studenti(studenti):
    """
    Elenca tutti gli studenti ordinati per cognome e nome, mostrando anche la classe.

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
            print(f"- {studente}")  # __str__ mostra anche la classe
    except Exception as e:
        print(f"Errore inatteso durante l'elenco degli studenti: {e}")


def cerca_studente(studenti):
    """
    Cerca studenti per nome nella lista, mostrando anche la classe.

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
                print(f"- {studente}")  # __str__ mostra anche la classe
        else:
            print("Nessuno studente trovato con questo nome.")
    except Exception as e:
        print(f"Errore inatteso durante la ricerca dello studente: {e}")

def cerca_classe(studenti):
    """
    Cerca tutti gli studenti appartenenti a una classe specifica.

    Parameters
    ----------
    studenti : list of Studente
        La lista degli studenti in cui cercare.

    Returns
    -------
    None
    """
    try:
        classe_query = input("Inserisci la classe da cercare (es. 1A, 5F): ").strip().upper()
        if len(classe_query) != 2 or not classe_query[0].isdigit() or not (1 <= int(classe_query[0]) <= 5) or not classe_query[1].isalpha() or not classe_query[1].isupper():
            print("Errore: La classe deve essere nel formato corretto (es. 1A, 5F).")
            return
        trovati = [s for s in studenti if s.classe == classe_query]
        if trovati:
            print(f"Studenti nella classe {classe_query}:")
            for studente in trovati:
                print(f"- {studente}")
        else:
            print(f"Nessuno studente trovato nella classe {classe_query}.")
    except Exception as e:
        print(f"Errore inatteso durante la ricerca della classe: {e}")
