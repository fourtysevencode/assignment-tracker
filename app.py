from fastapi import FastAPI, Request, HTTPException
from utils.spreadsheet import Sheet
from utils.gemini import suggest_priority
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
sheet = Sheet()

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
