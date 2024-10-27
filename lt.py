from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

class Calculation(BaseModel):
    num1: float
    num2: float
    operation: str

@app.post("/cal/")
async def calculate(calc: Calculation):
    if calc.operation == "add":
        result = calc.num1 + calc.num2
    elif calc.operation == "sub":
        result = calc.num1 - calc.num2
    elif calc.operation == "multi":
        result = calc.num1 * calc.num2
    elif calc.operation == "divide":
        result = calc.num1 / calc.num2 if calc.num2 != 0 else "Cannot divide by zero"
    else:
        return {"error": "Invalid operation"}
    return {"result": result}

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("calculator.html", {"request": request})
