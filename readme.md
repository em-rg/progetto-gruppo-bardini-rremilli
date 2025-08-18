# Progetto Gruppo Bardini–Rremilli  
**Esercizio 2 — Gestione studenti (liste e funzioni)**

---
# Obiettivo

Realizzare un programma a riga di comando per gestire una lista di studenti.  
Il progetto è sviluppato in modalità **collaborativa su GitHub**, rispettando i vincoli tecnici e metodologici richiesti a lezione.

---
# Funzioni Implementate
- **Aggiunta studente**: inserimento di nome e cognome con validazione input.  
- **Elenco studenti**: visualizzazione in ordine alfabetico.  
- **Ricerca studenti**: per nome o cognome (case-insensitive, match parziale).  
- **Gestione in memoria**: dati solo in memoria, senza file o database.  

---
# Vincoli tecnici rispettati
- Utilizzo esclusivo di **liste, cicli, condizioni, funzioni e/o oggetti**.  
- **Validazione input** con messaggi di errore chiari.  
- Strutturazione del codice in più funzioni:  
  - `aggiungi_studente`  
  - `elenca_studenti`  
  - `cerca_studenti`  
  - `main` (loop principale + menu testuale)  
- **Docstring stile NumPy** per garantire chiarezza e compatibilità con strumenti come Sphinx.  
- **No duplicazioni di codice**, funzioni brevi e coese.  
- Centralizzazione delle costanti in `config.py`.  

---
# Struttura del progetto
progetto-gruppo-bardini-rremilli/
│
├── student_manager/
│ ├── init.py
│ ├── config.py
│ ├── student_manager.py # funzioni core (aggiungi, elenca, cerca)
│ └── main.py # CLI e menu principale
│
├── requirements.txt
├── README.md
└── .github/workflows/python-ci.yml # GitHub Action (lint)
