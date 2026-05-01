import os

from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from utils.spreadsheet import Sheet
from utils.gemini import suggest_priority
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

load_dotenv()


def _service_account_from_env():
    env_to_key = {
        "GOOGLE_SERVICE_ACCOUNT_TYPE": "type",
        "GOOGLE_SERVICE_ACCOUNT_PROJECT_ID": "project_id",
        "GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY_ID": "private_key_id",
        "GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY": "private_key",
        "GOOGLE_SERVICE_ACCOUNT_CLIENT_EMAIL": "client_email",
        "GOOGLE_SERVICE_ACCOUNT_CLIENT_ID": "client_id",
        "GOOGLE_SERVICE_ACCOUNT_AUTH_URI": "auth_uri",
        "GOOGLE_SERVICE_ACCOUNT_TOKEN_URI": "token_uri",
        "GOOGLE_SERVICE_ACCOUNT_AUTH_PROVIDER_X509_CERT_URL": "auth_provider_x509_cert_url",
        "GOOGLE_SERVICE_ACCOUNT_CLIENT_X509_CERT_URL": "client_x509_cert_url",
        "GOOGLE_SERVICE_ACCOUNT_UNIVERSE_DOMAIN": "universe_domain",
    }

    missing = []
    service_account = {}
    for env_name, json_key in env_to_key.items():
        value = os.getenv(env_name)
        if not value:
            missing.append(env_name)
            continue
        service_account[json_key] = value

    if missing:
        missing_vars = ", ".join(missing)
        raise RuntimeError(f"Missing required Google service account environment variables: {missing_vars}")

    service_account["private_key"] = service_account["private_key"].replace("\\n", "\n")
    return service_account

app = FastAPI()
sheet = Sheet(service_account_info=_service_account_from_env())

# Serve CSS/JS from templates/static at the /static URL path
app.mount("/static", StaticFiles(directory="templates/static"), name="static")

templates = Jinja2Templates(directory="templates")

class new_assgnment(BaseModel):
    assignment: str
    assign_to: str
    priority: str

class assignment_update(BaseModel):
    id: int
    update: str

class name(BaseModel):
    name: str

class priority_suggestion_request(BaseModel):
    assignment: str

class assignment_info(BaseModel): # to avoid confusion
    assignment: str

@app.get("/", response_class=HTMLResponse) # HTML response, not json
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.get("/create-assignment", response_class=HTMLResponse) # HTML response, not json
async def home(request: Request):
    return templates.TemplateResponse(request, "create_assignment.html")

@app.get("/update-status", response_class=HTMLResponse) # HTML response, not json
async def update_status_page(request: Request):
    return templates.TemplateResponse(request, "update_status.html")

@app.get("/view-assignments", response_class=HTMLResponse) # HTML response, not json
async def view_assignments(request: Request):
    return templates.TemplateResponse(request, "view_assignments.html")

@app.post("/new-assignment")
async def create_assignment(assignment: new_assgnment):
    status = sheet.new_assignment(assignment.assignment, assignment.assign_to, assignment.priority)
    return  {"status": f"Assignment created with ID {status[1]}"}

@app.post("/update-assignment-status")
async def update(update_status: assignment_update):
    status = True if update_status.update == "Yes" else False
    status = sheet.update_status(update_status.id, status)
    return  {"status": status}

@app.post("/view_assignments")
async def view(name: name):
    assignments = sheet.find_assignments(name.name)
    return {"assignments": assignments}

@app.post("/suggest-priority")
async def suggest_assignment_priority(payload: priority_suggestion_request):
    try:
        return suggest_priority(payload.assignment)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except RuntimeError as exc:
        status_code = 500 if "GEMINI_API_KEY" in str(exc) else 502
        raise HTTPException(status_code=status_code, detail=str(exc)) from exc

@app.post("/get-priority")
async def get_priority(assignment: assignment_info):
    assignment_text = assignment.assignment
    return sheet.get_priority(assignment_text)

@app.post("/view-assignments-full")
async def view_full(name: name):
    assignments = sheet.find_assignments_full(name.name)
    return {"assignments": assignments}
