# TruthLens Intelligence — Auth Commands

## Start the Server

```powershell
cd "A:\Cursor - Copy\TruthLens-AI"
.\venv\Scripts\activate
python backend\app.py
```

> Server runs at **http://127.0.0.1:5000** — keep this terminal open.

---

## Browser Pages

| URL | Page |
|-----|------|
| http://127.0.0.1:5000 | Fake News Detector (original) |
| http://127.0.0.1:5000/auth/register | Register page |
| http://127.0.0.1:5000/auth/login | Login page |

---

## Test via Terminal (open a new terminal)

### Register a new user
```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:5000/auth/register" -ContentType "application/json" -Body '{"username":"myuser", "password":"mypassword"}'
```

### Login (returns JWT token)
```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:5000/auth/login" -ContentType "application/json" -Body '{"username":"myuser", "password":"mypassword"}'
```

### Login with wrong password (expect 401)
```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:5000/auth/login" -ContentType "application/json" -Body '{"username":"myuser", "password":"wrongpass"}'
```

### Test prediction (unchanged from Review 1)
```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:5000/predict" -ContentType "application/json" -Body '{"text":"Scientists confirm the moon is made of cheese"}'
```

---

## Notes

- JWT token is stored in browser `localStorage` as `tl_token` after login — never displayed on screen.
- User database is stored at `backend/auth.db` (SQLite, auto-created on first run).
- Authentication logic is fully isolated in `backend/auth.py` — prediction API is untouched.
