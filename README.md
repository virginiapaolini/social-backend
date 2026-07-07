# -ˏˋ⋆ social network rest api  ⋆ˊˎ-

**URL di deployment:** <https://social-backend-xwsc.onrender.com>

Progetto finale di Back-end per il corso di PPM (2025/2026) focalizzato sull'API design per apprendere al meglio la separazione tra client e back-end.

Tra le caratteristiche principali si ha:
- REST endpoints
- token/JWT authentication
- serializers/request validation
- role-based permissions
- JSON responses
- documented testing workflow (grazie ad httpie)
Sviluppato con Django e Django REST Framework, che, grazie al supporto build-in per modelli, autenticazione, permessi,form, serializers, class-based views.

---

## account demo (dati di test)
Il database SQLite incluso è già popolato tramite comando di seed. Di seguito le credenziali disponibili per la valutazione dei diversi ruoli e permessi:

| Username | Password | Ruolo | Descrizione |
| :--- | :--- | :--- | :--- |
| `user_demo` | `user12345` | Standard User | Può creare post, commenti, mettere like e seguire utenti. |
| `mod_demo` | `moderator12345` | Moderator | Può visualizzare i contenuti e cancellare post inappropriati. |
| `admin_demo` | `admin12345` | Superuser / Mod | Accesso completo al pannello di amministrazione. |

---

## documentazione degli Endpoint API

| Metodo | URL | Autenticazione | Ruolo Consentito | Richiesta (Body JSON) | Descrizione |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **POST** | `/api/auth/login/` | No | Pubblico | `{"username": "...", "password": "..."}` | Effettua il login e restituisce i Token JWT (access/refresh). |
| **GET** | `/api/users/` | Sì (JWT) | Qualsiasi ruolo autenticato | Nessuno | Restituisce la lista di tutti gli utenti registrati. |
| **POST** | `/api/users/<id>/follow/` | Sì (JWT) | STANDARD, MODERATOR | Nessuno | Permette di seguire o smettere di seguire l'utente specificato. |
| **GET** | `/api/posts/` | Sì (JWT) | Qualsiasi ruolo autenticato | Nessuno | Mostra la lista globale di tutti i post. |
| **POST** | `/api/posts/` | Sì (JWT) | STANDARD, MODERATOR | `{"content": "Testo del post (min 5 caratteri)"}` | Crea un nuovo post associando l'utente come autore. |
| **PUT** | `/api/posts/<id>/` | Sì (JWT) | Solo l'Autore originario | `{"content": "Nuovo testo modificato"}` | Aggiorna un post esistente. Restituisce 403 se non si è l'autore. |
| **DELETE**| `/api/posts/<id>/` | Sì (JWT) | Autore o MODERATOR | Nessuno | Elimina un post. Consentito all'autore o a utenti Moderatori. |
| **POST** | `/api/posts/<id>/like/` | Sì (JWT) | STANDARD, MODERATOR | Nessuno | Aggiunge o rimuove il "Like" al post indicato. |
| **GET** | `/api/feed/` | Sì (JWT) | STANDARD, MODERATOR | Nessuno | Restituisce il feed personalizzato con i post degli utenti seguiti. |

## workflow di testing con HTTPie (Client-Based Scenario)

Viene utilizzato **HTTPie** (https://httpie.io/) come client di test minimale per superare i problemi di parsing delle virgolette sui terminali Windows.

### 1. Installazione del Client di Test
Assicurandosi di avere l'ambiente virtuale attivo, installare HTTPie tramite pip:
```bash
pip install httpie

```

### 2. Autenticazione (Ottenere il Token JWT)

Inviare le credenziali dell'utente standard per ricevere i token:

```bash
http POST [http://127.0.0.1:8000/api/auth/login/](http://127.0.0.1:8000/api/auth/login/) username=user_demo password=user12345

```

*Risposta attesa:* Stato `200 OK` con i token `access` e `refresh`. Copiare il valore di `access` (senza virgolette).

### 3. Chiamata a Endpoint Autenticato (Lettura Dati)

Visualizzare la lista degli utenti inserendo il token nell'header di autorizzazione (sostituire `<TOKEN>` con il valore copiato):

```bash
http GET [http://127.0.0.1:8000/api/users/](http://127.0.0.1:8000/api/users/) "Authorization: Bearer <TOKEN>"

```

*Risposta attesa:* Stato `200 OK` con l'elenco JSON degli utenti.

### 4. Creazione Dati con Validazione JSON

Provare a inserire un nuovo post sulla piattaforma:

```bash
http POST [http://127.0.0.1:8000/api/posts/](http://127.0.0.1:8000/api/posts/) content="Nuovo post strutturato secondo linee guida!" "Authorization: Bearer <TOKEN>"

```

*Risposta attesa:* Stato `201 Created`.
*Verifica Validazione:* Se si invia un testo inferiore a 5 caratteri (es. `content="Ciao"`), l'API risponde correttamente con `400 Bad Request` esponendo l'errore di validazione del Serializer.

### 5. Test di un'Azione Proibita (Verifica Sicurezza Permessi)

Per verificare che i permessi siano applicati nella logica di business e non solo descritti, proviamo a modificare il post con ID `1` (il cui autore è `admin_demo`) usando il token appena generato di `user_demo`:

```bash
http PUT [http://127.0.0.1:8000/api/posts/1/](http://127.0.0.1:8000/api/posts/1/) content="Tentativo di modifica abusiva" "Authorization: Bearer <TOKEN>"

```

*Risposta attesa:* **`403 Forbidden`**. L'applicazione blocca la richiesta poiché l'utente autenticato non ha i permessi di autore sull'oggetto, confermando la robustezza del sistema.

