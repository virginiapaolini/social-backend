
# -ˏˋ⋆ social network REST API ⋆ˊˎ-

Progetto finale di Back-end per il corso di PPM (2026).
Benvenut* nella **Social Network REST API**, un ecosistema back-end performante e sicuro strutturato secondo i più moderni standard del web. L'applicazione non si limita a archiviare informazioni, ma dà vita a una vera e propria rete di interazioni sociali digitali:
- *autenticazione blindata:* acesso sicuro garantito dallo standard **JSON Web Token (JWT)** con rotazione automatica delle chiavi di sessione.
- *relazioni dinamiche:* un sistema di connessioni fluido che permette agli utenti di seguirsi a vicenda, creando una rete sociale personalizzata.
- *feed intelligente:* un algoritmo ottimizzato che aggrega in tempo reale i contenuti pubblicati dagli utenti seguiti, ordinandoli cronologicamente per offrire un'esperienza d'uso naturale e immediata.
- *interazioni ad alto coinvolgimento*: possibilità di esprimere apprezzamento tramite like dinamici e di partecipare alle discussioni con un sistema di commenti nidificato.
- *controllo e moderazione (role-based access control):* una solida gerarchia di permessi protegge la community, separando i poteri degli utenti standard, dei moderatori (incaricati della sicurezza dei contenuti e del blocco utenti) e dell'amministratore.


## ⋆ tipo di progetto

**REST API**:  A back-end application with REST endpoints, token/JWT authentication, serializers or request validation, role-based permissions, JSON responses, and a documented testing workflow or minimal client.


## ⋆ link di deployment online
Il deployment è stato fatto su Render:
<https://social-backend-xwsc.onrender.com>
---

## ⋆ descrizione del progetto

Questa applicazione è una REST API per un piccolo e semplice social network.

La piattaforma permette agli utenti registrati di:
- autenticarsi tramite JWT
- visualizzare altri utenti
- seguire o smettere di seguire utenti
- visualizzare un feed personalizzato
- creare, modificare ed eliminare post
- mettere o rimuovere like dai post
- commentare i post
- applicare permessi diversi in base al ruolo dell'utente

Sono presenti ruoli diversi, in particolare:
- utente standard
- moderatore
- amministratore/superuser
---

## ⋆ framework utilizzati

- Python 3.11
- Django
- Django REST Framework
- Simple JWT per autenticazione JWT
- SQLite come database locale

---

## ⋆ funzionalità implementate

### Utente pubblico/non autenticato

Un utente non autenticato può:

- visualizzare la home API
- registrare un nuovo account
- effettuare il login e ottenere i token JWT

### Utente standard

Un utente standard autenticato può:

- visualizzare la lista degli utenti
- seguire o smettere di seguire altri utenti
- visualizzare tutti i post
- visualizzare un singolo post
- creare nuovi post
- modificare solo i propri post
- eliminare solo i propri post
- mettere o rimuovere like dai post
- commentare i post
- visualizzare il feed personalizzato con i post degli utenti seguiti

### Moderatore

Un moderatore autenticato può:

- usare le funzionalità dell'utente standard
- eliminare post inappropriati anche se creati da altri utenti
- bloccare o riattivare utenti tramite endpoint dedicato

### Amministratore/Superuser

L'amministratore può:

- accedere al pannello Django Admin
- gestire utenti e contenuti dal backend Django
- usare anche i permessi da moderatore

---

## ⋆ database locale SQLite

Il progetto include un database SQLite locale:
```text
db.sqlite3
```
Il database può contenere dati demo per testare immediatamente l'applicazione, tra cui:
- utenti
- post
- commenti
- like
- relazioni follow tra utenti

È inoltre presente uno script di popolamento:
```text
popola_db.py
```
che permette di ricreare dati demo coerenti nel database locale.

---

## ⋆ installazione locale

### 1. clonare il repository
```bash
git clone https://github.com/virginiapaolini/social-backend.git
cd <insert-repository-folder>
```
### 2. creare e attivare l'ambiente virtuale

Esempio con Conda:
```bash
conda create -n socialapi python=3.11
conda activate socialapi
```
### 3. installare le dipendenze di python
```bash
pip install -r requirements.txt
```
### 4. applicare le migrazioni
```bash
python manage.py migrate
```
### 5. popolare il database con i dati demo
```bash
python popola_db.py
```
Questo comando crea utenti demo, post, commenti, like e relazioni follow.

### 6. Avviare il server locale
```bash
python manage.py runserver
```
L'API sarà disponibile all'indirizzo:
```text
http://127.0.0.1:8000/
```
---
## ⋆ account demo

Dopo aver eseguito:
```bash
python popola_db.py
```
sono disponibili i seguenti account demo:

| Username | Password | Ruolo | Descrizione |
| :--- | :--- | :--- | :--- |
| `admin_demo` | `admin12345` | Superuser / Moderator | Accesso al pannello admin e permessi completi. |
| `mod_demo` | `moderator12345` | Moderator | Può moderare contenuti e bloccare utenti. |
| `user_demo` | `user12345` | Standard | Utente standard per testare post, follow, like e commenti. |
| `maria_demo` | `maria12345` | Standard | Utente standard demo aggiuntivo. |
| `luca_demo` | `luca12345` | Standard | Utente standard demo aggiuntivo. |

---

## ⋆ base URL

### locale
```text
http://127.0.0.1:8000
```
### deployment
```
https://social-backend-xwsc.onrender.com
```
---

## ⋆ documentazione endpoints API

### API home view

| Metodo | URL | Autenticazione | Ruolo consentito | Body JSON | Descrizione |
| :--- | :--- | :--- | :--- | :--- | :--- |
| GET | `/` | No | Pubblico | Nessuno | Mostra informazioni generali e link agli endpoint principali. |

### esempio risposta
```
json
{
  "info": {
    "project_name": "Social Media REST API",
    "description": "Progetto finale per il corso di Back-end PPM 2026.",
    "status": "ONLINE",
    "version": "1.0.0"
  },
  "endpoints_disponibili": {
    "autenticazione_login": "http://127.0.0.1:8000/api/auth/login/",
    "lista_utenti": "http://127.0.0.1:8000/api/users/",
    "lista_post": "http://127.0.0.1:8000/api/posts/",
    "feed_personalizzato": "http://127.0.0.1:8000/api/feed/",
    "blocco_utenti_moderatore": "/api/users/<id>/block/"
  }
}
```
---

### autenticazione e utenti

| Metodo | URL | Autenticazione | Ruolo consentito | Body JSON | Esempio risposta | Descrizione |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| POST | `/api/auth/login/` | No | Pubblico | `{"username": "user_demo", "password": "user12345"}` | `{"refresh": "...", "access": "..."}` | Effettua il login e restituisce i token JWT. |
| POST | `/api/auth/refresh/` | No | Pubblico | `{"refresh": "<REFRESH_TOKEN>"}` | `{"access": "..."}` | Genera un nuovo access token. |
| POST | `/api/auth/register/` | No | Pubblico | `{"username": "new_user", "password": "newpass12345", "email": "new@example.com", "bio": "Ciao!"}` | Dati del nuovo utente | Registra un nuovo utente standard. |
| GET | `/api/users/` | Sì, JWT | Qualsiasi utente autenticato | Nessuno | Lista utenti | Restituisce la lista degli utenti. |
| POST | `/api/users/<user_id>/follow/` | Sì, JWT | Utente autenticato | Nessuno | Messaggio follow/unfollow | Segue o smette di seguire un utente. |
| POST | `/api/users/<user_id>/block/` | Sì, JWT | Solo Moderator | Nessuno | Messaggio blocco/sblocco | Blocca o riattiva un utente. |

---

### post, feed, like e commenti

| Metodo | URL | Autenticazione | Ruolo consentito | Body JSON | Esempio risposta | Descrizione |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| GET | `/api/posts/` | Sì, JWT | Utente autenticato | Nessuno | Lista post | Mostra tutti i post ordinati dal più recente. |
| POST | `/api/posts/` | Sì, JWT | Utente autenticato | `{"content": "Testo del nuovo post"}` | Post creato | Crea un nuovo post associato all'utente autenticato. |
| GET | `/api/posts/<id>/` | Sì, JWT | Utente autenticato | Nessuno | Dettaglio post | Mostra un singolo post con autore, like e commenti. |
| PUT | `/api/posts/<id>/` | Sì, JWT | Solo autore del post | `{"content": "Testo aggiornato"}` | Post aggiornato | Modifica un post esistente. |
| DELETE | `/api/posts/<id>/` | Sì, JWT | Autore o Moderator | Nessuno | Risposta 204 | Elimina un post. |
| POST | `/api/posts/<id>/like/` | Sì, JWT | Utente autenticato | Nessuno | Messaggio like/unlike | Aggiunge o rimuove like dal post indicato. |
| POST | `/api/posts/<id>/comments/` | Sì, JWT | Utente autenticato | `{"content": "Testo del commento"}` | Commento creato | Aggiunge un commento a un post. |
| GET | `/api/feed/` | Sì, JWT | Utente autenticato | Nessuno | Lista post | Mostra i post degli utenti seguiti. |

---

## ⋆ workflow di test con HTTPie

HTTPie è un client da terminale per testare API REST.

Link ufficiale:
```text
https://httpie.io/
```
Installazione:
```bash
pip install httpie
```
NB: assicurarsi che il server sia attivo:
```bash
python manage.py runserver
```
---

### 1. Login e ottenimento token JWT
```bash
http POST http://127.0.0.1:8000/api/auth/login/ username=user_demo password=user12345
```
Risposta attesa:
```
json
{
  "refresh": "<REFRESH_TOKEN>",
  "access": "<ACCESS_TOKEN>"
}
```
Copiare il valore di `access`.

Negli esempi successivi sostituire `<TOKEN>` con il valore copiato.

---

### 2. Visualizzare la lista utenti
```bash
http GET http://127.0.0.1:8000/api/users/ "Authorization: Bearer <TOKEN>"
```
Risposta attesa:
```
json
[
  {
    "id": 1,
    "username": "admin_demo",
    "bio": "",
    "role": "MODERATOR",
    "followers_count": 0,
    "following_count": 0
  }
]
```
---

### 3. Visualizzare tutti i post
```bash
http GET http://127.0.0.1:8000/api/posts/ "Authorization: Bearer <TOKEN>"
```
Risposta attesa:
```
json
[
  {
    "id": 1,
    "author": {
      "id": 3,
      "username": "user_demo",
      "bio": "Ciao! Sono un utente standard del social network.",
      "role": "STANDARD",
      "followers_count": 2,
      "following_count": 2
    },
    "content": "Sto preparando il progetto finale di Back-end per il corso PPM 2026. Django REST Framework è fantastico!",
    "created_at": "2026-07-07T12:00:00Z",
    "updated_at": "2026-07-07T12:00:00Z",
    "likes_count": 3,
    "comments": []
  }
]
```
---

### 4. Creare un nuovo post
```bash
http POST http://127.0.0.1:8000/api/posts/ content="Nuovo post creato tramite HTTPie!" "Authorization: Bearer <TOKEN>"
```
Risposta attesa:
```
json
{
  "id": 7,
  "author": {
    "id": 3,
    "username": "user_demo",
    "bio": "Ciao! Sono un utente standard del social network.",
    "role": "STANDARD",
    "followers_count": 2,
    "following_count": 2
  },
  "content": "Nuovo post creato tramite HTTPie!",
  "created_at": "2026-07-07T12:00:00Z",
  "updated_at": "2026-07-07T12:00:00Z",
  "likes_count": 0,
  "comments": []
}
```
---

### 5. Validazione contenuto post

Il contenuto del post deve avere almeno 5 caratteri.

Comando di test:
```bash
http POST http://127.0.0.1:8000/api/posts/ content="Ciao" "Authorization: Bearer <TOKEN>"
```
Risposta attesa:
```
json
{
  "content": [
    "Il contenuto del post deve essere lungo almeno 5 caratteri."
  ]
}
```
Stato atteso:
```text
400 Bad Request
```
---

### 6. Mettere o togliere like a un post
```bash
http POST http://127.0.0.1:8000/api/posts/1/like/ "Authorization: Bearer <TOKEN>"
```
Risposta attesa se il like viene aggiunto:
```
json
{
  "message": "Like aggiunto.",
  "liked": true
}
```
Oppure, se il like era già presente:
```
json
{
  "message": "Like rimosso.",
  "liked": false
}
```
---

### 7. Commentare un post
```bash
http POST http://127.0.0.1:8000/api/posts/1/comments/ content="Commento creato tramite HTTPie!" "Authorization: Bearer <TOKEN>"
```
Risposta attesa:
```
json
{
  "id": 8,
  "post": 1,
  "author": {
    "id": 3,
    "username": "user_demo",
    "bio": "Ciao! Sono un utente standard del social network.",
    "role": "STANDARD",
    "followers_count": 2,
    "following_count": 2
  },
  "content": "Commento creato tramite HTTPie!",
  "created_at": "2026-07-07T12:00:00Z"
}
```
---

### 8. Seguire o smettere di seguire un utente
```bash
http POST http://127.0.0.1:8000/api/users/2/follow/ "Authorization: Bearer <TOKEN>"
```
Risposta attesa se l'utente viene seguito:
```
json
{
  "message": "Ora segui mod_demo."
}
```
Risposta attesa se l'utente era già seguito:
```
json
{
  "message": "Hai smesso di seguire mod_demo."
}
```
---

### 9. Visualizzare il feed personalizzato
```bash
http GET http://127.0.0.1:8000/api/feed/ "Authorization: Bearer <TOKEN>"
```
Risposta attesa:
```
json
[
  {
    "id": 3,
    "author": {
      "id": 2,
      "username": "mod_demo",
      "bio": "Moderatore ufficiale della piattaforma.",
      "role": "MODERATOR",
      "followers_count": 2,
      "following_count": 1
    },
    "content": "Avviso di servizio: mantenete toni rispettosi e costruttivi all'interno della piattaforma.",
    "likes_count": 3,
    "comments": []
  }
]
```
---

### 10. Test permesso negato: modifica post non proprio

Effettuare login come `user_demo`:
```bash
http POST http://127.0.0.1:8000/api/auth/login/ username=user_demo password=user12345
```
Poi provare a modificare un post creato da un altro utente, per esempio un post del moderatore o dell'admin:
```bash
http PUT http://127.0.0.1:8000/api/posts/12/ content="Tentativo di modifica abusiva" "Authorization: Bearer <TOKEN>"
```
Risposta attesa:
```
json
{
  "detail": "Non hai i permessi per eseguire questa azione."
}
```
Stato atteso:
```text
403 Forbidden
```
---

### 11. Test moderatore: bloccare o riattivare un utente

Prima fare login come moderatore:
```bash
http POST http://127.0.0.1:8000/api/auth/login/ username=mod_demo password=moderator12345
```
Copiare il token `access` del moderatore.

Poi bloccare un utente:
```bash
http POST http://127.0.0.1:8000/api/users/2/block/ "Authorization: Bearer <MOD_TOKEN>"
```
Risposta attesa:
```
json
{
  "message": "L'utente user_demo è stato bloccato con successo."
}
```
Se un utente è bloccato non può accedere alla piattaforma finché non viene sbloccato.\
Se si esegue di nuovo lo stesso comando, l'utente viene riattivato:
```
json
{
  "message": "L'utente user_demo è stato riattivato."
}
```
---

### 12. Test utente standard: blocco non consentito

Fare login come utente standard:
```bash
http POST http://127.0.0.1:8000/api/auth/login/ username=user_demo password=user12345
```
Provare a bloccare un altro utente:
```bash
http POST http://127.0.0.1:8000/api/users/2/block/ "Authorization: Bearer <TOKEN>"
```
Risposta attesa:
```
json
{
  "detail": "Azione consentita solo ai moderatori."
}
```
Stato atteso:
```text
403 Forbidden
```
---

## ⋆ test automatici Django

Per eseguire i test automatici:
```bash
python manage.py test
```
Al momento il progetto può essere testato principalmente tramite workflow manuale con HTTPie e database demo.

---

## ⋆ note tecniche

### autenticazione

L'API usa JWT. Dopo il login viene restituito un token `access`, da inviare negli endpoint protetti tramite header:
```text
Authorization: Bearer <TOKEN>
```
## ⋆ permessi

Le regole principali sono:

- gli endpoint pubblici sono accessibili senza autenticazione
- gli endpoint di lettura utenti/post richiedono login
- la creazione dei post richiede login
- la modifica di un post è consentita solo all'autore
- l'eliminazione di un post è consentita all'autore o al moderatore
- il blocco utenti è consentito solo ai moderatori
- i nuovi utenti registrati pubblicamente vengono creati come utenti standard

## ⋆ validazioni

Sono presenti validazioni sui contenuti:

- i post devono avere almeno 5 caratteri
- i commenti non possono essere vuoti o composti solo da spazi

---

## ⋆ struttura principale del progetto
```text
PythonProject/
├── posts/
│   ├── models.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── urls.py
│   └── views.py
├── users/
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── socialAPI/
│   ├── settings.py
│   └── urls.py
├── db.sqlite3
├── fixtures.json
├── manage.py
├── popola_db.py
├── README.md
└── requirements.txt
```
---

## ⋆ comandi rapidi

Preparazione completa del progetto in locale:
```bash
python manage.py migrate
python popola_db.py
python manage.py runserver
```
Login utente standard:
```bash
http POST http://127.0.0.1:8000/api/auth/login/ username=user_demo password=user12345
```
Lista post:
```bash
http GET http://127.0.0.1:8000/api/posts/ "Authorization: Bearer <TOKEN>"
```
Creazione post:
```bash
http POST http://127.0.0.1:8000/api/posts/ content="Post creato da terminale!" "Authorization: Bearer <TOKEN>"
```
Feed personalizzato:
```bash
http GET http://127.0.0.1:8000/api/feed/ "Authorization: Bearer <TOKEN>"
```
⋆

Corso Progettazione e Produzione multimediale (2025/2026)\
Virginia Paolini