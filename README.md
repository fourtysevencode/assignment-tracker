# Assignment Tracker

A FastAPI + Google Sheets assignment management app with a web UI and Gemini-powered priority suggestions.

## Architecture

```mermaid
flowchart TD
    U["Browser UI - Jinja templates and JS"] -->|HTTP| A["FastAPI app - app.py"]
    A -->|Render pages| T["templates/*.html"]
    A -->|Static assets| S["templates/static/style.css"]
    A -->|CRUD assignment data| G["utils/spreadsheet.py - gspread"]
    G -->|Google API| GS["Google Sheet: assignments-sheet"]
    A -->|Priority suggestion| M["utils/gemini.py"]
    M -->|generateContent API| GM["Gemini API"]
    A --> E["Environment variables via .env"]
```

## Project structure

```text
assignment-tracker/
├─ app.py                      # FastAPI routes + template rendering
├─ requirements.txt            # Python dependencies
├─ templates/
│  ├─ index.html               # Home page
│  ├─ create_assignment.html   # Create flow + AI priority suggestion
│  ├─ update_status.html       # Status update flow
│  ├─ view_assignments.html    # Assignment listing + mark done
│  └─ static/
│     └─ style.css             # Shared UI styling
└─ utils/
   ├─ spreadsheet.py           # Google Sheets data access layer
   ├─ gemini.py                # Gemini priority suggestion client
   └─ assignment-tracker-...json (local fallback key file, optional)
```

## Features

- Create assignments with assignee and priority.
- Update assignment completion status by ID.
- View assignments for a given team member.
- Mark assignments as done from the UI.
- Get AI-suggested priority (`High`, `Medium`, `Low`) with a short reason.

## Running locally

### 1. Prerequisites

- Python 3.10+
- A Google service account with access to your target Google Sheet
- (Optional) Gemini API key for AI priority suggestions

### 2. Install dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Configure environment

Create a `.env` file in the project root:

```powershell
GOOGLE_SERVICE_ACCOUNT_TYPE=service_account
GOOGLE_SERVICE_ACCOUNT_PROJECT_ID=...
GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY_ID=...
GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
GOOGLE_SERVICE_ACCOUNT_CLIENT_EMAIL=...
GOOGLE_SERVICE_ACCOUNT_CLIENT_ID=...
GOOGLE_SERVICE_ACCOUNT_AUTH_URI=https://accounts.google.com/o/oauth2/auth
GOOGLE_SERVICE_ACCOUNT_TOKEN_URI=https://oauth2.googleapis.com/token
GOOGLE_SERVICE_ACCOUNT_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
GOOGLE_SERVICE_ACCOUNT_CLIENT_X509_CERT_URL=...
GOOGLE_SERVICE_ACCOUNT_UNIVERSE_DOMAIN=googleapis.com

# Optional (required only for /suggest-priority)
GEMINI_API_KEY=your-api-key
```

### 4. Start the app

```powershell
uvicorn app:app --reload
```

Open:

- App UI: `http://127.0.0.1:8000/`

## API endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/` | Home page |
| GET | `/create-assignment` | Create assignment page |
| GET | `/update-status` | Update status page |
| GET | `/view-assignments` | View assignments page |
| POST | `/new-assignment` | Create assignment in sheet |
| POST | `/update-assignment-status` | Update assignment completion |
| POST | `/view_assignments` | List assignment titles for assignee |
| POST | `/view-assignments-full` | List detailed assignments for assignee |
| POST | `/get-priority` | Get stored priority from sheet |
| POST | `/suggest-priority` | Gemini-based priority suggestion |

## Notes

- `app.py` currently initializes Google Sheets at startup and requires Google service account env variables to be set.
- If Gemini is not configured, all non-Gemini routes still work; only `/suggest-priority` fails.
- This project used generative AI to write the fronted logic.
