from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from core import ApplicationState
import uvicorn

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

state = ApplicationState()

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "equations": state.equations,
            "last_result": state.last_result,
        },
    )

@app.post("/", response_class=HTMLResponse)
async def post_equation(
    request: Request,
    title: str = Form(""),
    equation: str = Form(""),
    action: str = Form(""),
    index: int = Form(None),
):
    if action == "add" and title and equation:
        state.add_equation(title, equation)
    elif action == "delete" and index is not None:
        state.delete_equation(index)
    elif action == "solve" and index is not None:
        try:
            state.solve_equation(index)
        except IndexError:
            state.last_result = {"title": None, "equation": None, "result": None, "error": "Invalid equation index."}
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "equations": state.equations,
            "last_result": state.last_result,
        },
    )

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
