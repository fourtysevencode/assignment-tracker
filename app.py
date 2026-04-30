from fastapi import FastAPI, Request
from utils.spreadsheet import Sheet
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

@app.get("/", response_class=HTMLResponse) # HTML response, not json
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.get("/create-assignment", response_class=HTMLResponse) # HTML response, not json
async def home(request: Request):
    return templates.TemplateResponse(request, "create_assignment.html")

@app.get("/update-status", response_class=HTMLResponse) # HTML response, not json
async def update_status_page(request: Request):
    return templates.TemplateResponse(request, "update_status.html")

@app.post("/new-assignment")
async def create_assignment(assignment: new_assgnment):
    status = sheet.new_assignment(assignment.assignment, assignment.assign_to, assignment.priority)
    return  {"status": f"Assignment created with ID {status[1]}"}

@app.post("/update-assignment-status")
async def update(update_status: assignment_update):
    status = True if update_status.update == "Yes" else False
    status = sheet.update_status(update_status.id, status)
    return  {"status": status}