# -ˏˋ⋆ social network rest api  ⋆ˊˎ-

Progetto finale di Back-end per il corso di PPM 2026.
Sviluppato con Django e Django REST Framework.

**URL di Deployment:** [link render]

---

## account demo (dati di test)
Il database SQLite incluso è già popolato tramite comando di seed. Di seguito le credenziali disponibili per la valutazione dei diversi ruoli e permessi:

| Username | Password | Ruolo | Descrizione |
| :--- | :--- | :--- | :--- |
| `user_demo` | `user12345` | Standard User | Può creare post, commenti, mettere like e seguire utenti. |
| `mod_demo` | `moderator12345` | Moderator | Può visualizzare i contenuti e cancellare post inappropriati. |
| `admin_demo` | `admin12345` | Superuser / Mod | Accesso completo al pannello di amministrazione. |

---

## scenario di verifica delle Sspecifiche (comandi cURL / HTTP Client)

Di seguito viene descritto lo scenario passo-passo per verificare i requisiti minimi richiesti dal bando (Autenticazione, CRUD, validazione JSON e permessi sui ruoli).

*(Nota: Sostituire `http://127.0.0.1:8000` con l'URL di Render se il test viene eseguito sulla versione live online).*

### 1. autenticazione (ottenere il Token JWT)
Inviare una richiesta **POST** all'endpoint di login per autenticare l'utente e ricevere i relativi Token JWT:

```bash
curl -X POST [http://127.0.0.1:8000/api/auth/login/](http://127.0.0.1:8000/api/auth/login/) \
     -H "Content-Type: application/json" \
     -d '{"username": "user_demo", "password": "user12345"}'

```

*Risultato atteso:* Ricezione delle due stringhe JSON `access` e `refresh`. Copiare il token contenuto nel campo `access` per utilizzarlo nelle richieste successive.

### 2. chiamata a un endpoint autenticato (vedere la lista utenti)

Inviare una richiesta **GET** inserendo il token nell'Header di autorizzazione per visualizzare la lista degli iscritti:

```bash
curl -X GET [http://127.0.0.1:8000/api/users/](http://127.0.0.1:8000/api/users/) \
     -H "Authorization: Bearer <INSERISCI_IL_TOKEN_ACCESS_QUI>"

```

*Risultato atteso:* Elenco completo degli utenti in formato JSON. Se eseguito senza l'header di autorizzazione o con un token errato, il sistema blocca la richiesta restituendo `401 Unauthorized`.

### 3. creazione dati con validazione JSON (crea un post)

Inviare una richiesta **POST** per pubblicare un nuovo contenuto inserendo il testo nel corpo JSON:

```bash
curl -X POST [http://127.0.0.1:8000/api/posts/](http://127.0.0.1:8000/api/posts/) \
     -H "Authorization: Bearer <INSERISCI_IL_TOKEN_ACCESS_QUI>" \
     -H "Content-Type: application/json" \
     -d '{"content": "Nuovo post strutturato secondo linee guida!"}'

```

*Risultato atteso:* Risposta con stato `201 Created` e generazione del record del Post (es. con ID `1`).
*Nota sulla validazione:* Se si tenta di inviare un testo inferiore a 5 caratteri o vuoto, il sistema risponde con `400 Bad Request` mostrando l'errore di validazione JSON.

### 4. test azione proibita (sicurezza & permessi)

Per verificare il corretto isolamento e la sicurezza dei dati, provare a effettuare una modifica (**PUT** o **PATCH**) sul post appena creato (ID 1) utilizzando il token di un utente che non ne è l'autore (ad esempio effettuando il login con `mod_demo` o registrandone uno nuovo):

```bash
curl -X PUT [http://127.0.0.1:8000/api/posts/1/](http://127.0.0.1:8000/api/posts/1/) \
     -H "Authorization: Bearer <TOKEN_DI_UN_ALTRO_UTENTE>" \
     -H "Content-Type: application/json" \
     -d '{"content": "Tentativo di modifica non autorizzata"}'

```

*Risultato atteso:* Risposta con stato `403 Forbidden`. L'applicazione rifiuta la richiesta in quanto l'utente autenticato non coincide con l'autore originario del post, rispettando i vincoli di sicurezza impostati.


