from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response= HTMLResponse)
async def readRoot(request:Request):
    return templates.TemplateResponse("index.html",{"request": request})