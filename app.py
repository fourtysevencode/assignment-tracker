from fastapi import FastAPI, Request
from utils.spreadsheet import Sheet
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
sheet = Sheet()

templates = Jinja2Templates(directory="templates")

class new_assgnment(BaseModel):
    id: int
    assignment: str
    assign_to: str
    priority: str

@app.get("/", response_class=HTMLResponse) # HTML response, not json
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.post("/new-assignment")
async def create_assignment(assignment: new_assgnment):
    status = sheet.new_assignment(assignment.id, assignment.assignment, assignment.assign_to, assignment.priority)
    return  {"status": status}

@app.post("/update-assignment")
async def update(id, status:bool):
    status = sheet.update_status(id, status)
    return  {"status": status}