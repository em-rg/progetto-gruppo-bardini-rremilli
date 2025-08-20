from student_manager import aggiungi_studente, elenca_studenti, cerca_studente, cerca_classe

def main():
    """
    Avvia il menu principale per la gestione degli studenti.

    Permette di aggiungere, elencare e cercare studenti tramite input da console.

    Returns
    -------
    None
    """
    studenti = []
    while True:
        try:
            print("\n--- MENU STUDENTI ---")
            print("1. Aggiungi studente")
            print("2. Elenca studenti (ordine alfabetico)")
            print("3. Cerca studente per nome")
            print("4. Cerca studenti per classe")
            print("5. Esci")
            scelta = input("Scegli un'opzione (1-5): ").strip()
            if scelta == "1":
                aggiungi_studente(studenti)
            elif scelta == "2":
                elenca_studenti(studenti)
            elif scelta == "3":
                cerca_studente(studenti)
            elif scelta == "4":
                cerca_classe(studenti)
            elif scelta == "5":
                print("Uscita dal programma.")
                break
            else:
                print("Opzione non valida. Riprova.")
        except Exception as e:
            print(f"Errore inatteso: {e}")

if __name__ == "__main__":
    main()
