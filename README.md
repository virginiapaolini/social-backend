# Social Network REST API

Progetto finale per il corso di Back-end PPM 2026.
Sviluppato con Django e Django REST Framework.

**URL di Deployment:** [Inserisci qui il link di Render/Railway una volta caricato]

---

## 👥 Account Demo (Dati di Test)
Il database SQLite incluso è già popolato tramite comando di seed. Di seguito le credenziali disponibili:

| Username | Password | Ruolo | Descrizione |
| :--- | :--- | :--- | :--- |
| `user_demo` | `user12345` | Standard User | Può creare post, commenti, mettere like e seguire utenti. |
| `mod_demo` | `moderator12345` | Moderator | Può visualizzare i contenuti e cancellare post inappropriati. |
| `admin_demo` | `admin12345` | Superuser / Mod | Accesso completo al pannello di amministrazione. |

---

## 🚀 Scenario di Test delle API (Passo-Passo)

Seguire questi passaggi per verificare i requisiti minimi richiesti (Autenticazione, CRUD, Ruoli e Permessi).

### 1. Autenticazione (Ottenere il Token JWT)
Inviare una richiesta **POST** a `http://127.0.0.1:8000/api/auth/login/` con il corpo JSON:
```json
{
  "username": "user_demo",
  "password": "user12345"
}