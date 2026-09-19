# Al-Khidmat Blood Response System — Patient Module Backend

FastAPI backend covering **Option 1: Patients / Patient Families** only
(FR-02, FR-06, FR-08, FR-09 from the PRD).

## Tech stack
- Python 3.11
- FastAPI + Uvicorn
- MongoDB via Motor + Beanie ODM
- Firebase Admin SDK (verifies the frontend's Firebase login token)
- Pydantic v2

## Setup (short version — see the beginner guide for full click-by-click steps)

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env       # then edit .env with your real Mongo URI
# put your real serviceAccountKey.json in this folder (see serviceAccountKey.json.example)
uvicorn app.main:app --reload --port 8000
```

Open **http://127.0.0.1:8000/docs** — every endpoint below is listed there and you can test it directly in the browser.

## Endpoints

| Method | Path | Auth | Purpose |
|---|---|---|---|
| POST | `/api/v1/auth/sync` | Firebase idToken (in body) | Verify login, create the user in MongoDB if new |
| POST | `/api/v1/patient/requests` | Patient | Create a blood request (FR-02) |
| GET | `/api/v1/patient/requests` | Patient | History of my requests (FR-08) |
| GET | `/api/v1/patient/requests/{id}/status` | Patient | Live progress + donor responses (FR-09) |
| GET | `/api/v1/patient/requests/{id}/donors` | Patient | Contact info of accepted/donated donors (FR-09) |

All routes except `/auth/sync` require an `Authorization: Bearer <Firebase idToken>` header.

## Folder structure

```
app/
├── main.py                  # FastAPI app, CORS, Mongo/Beanie startup
├── core/
│   ├── config.py            # reads .env into a Settings object
│   └── firebase.py          # initializes firebase_admin
├── models/                  # Beanie documents (MongoDB collections)
│   ├── user.py
│   ├── blood_request.py
│   └── donor_response.py
├── utils/
│   └── blood_compatibility.py
├── middlewares/
│   └── auth.py               # authenticate() + authorize(roles) dependencies
└── modules/
    ├── auth/                  # /api/v1/auth/sync
    └── patient/                # everything under /api/v1/patient
```

## Notes / assumptions
- The PRD PDF referenced in the brief wasn't available to read directly when this was generated — this build follows the FR-02/FR-06/FR-08/FR-09 spec exactly as written out in the request. If the actual PRD has extra fields or rules, send it over and this can be adjusted.
- `role`-based access control only enforces `PATIENT` here; donor/admin modules aren't part of this scope.
- Donor matching/notification logic (who gets notified when a request goes `OPEN`) isn't implemented here — that's Donor module territory. This module only reads `DonorResponse` records to show status/matched donors to the patient.
