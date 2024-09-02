from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx
import secret # Import the secret module for API Key
import requests

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class= HTMLResponse)
#Using async function to allow the server to process multiple requests and not wait for one at a time
# Thus making our website run faster
async def readRoot(request:Request):
    return templates.TemplateResponse("index.html",{"request": request})

@app.post("/", response_class= HTMLResponse)
async def getWeather(request= Request, city: str = Form(...)):
    apiKey = secret.api
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apiKey}&units=metric'

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    
    weather = response.json()
    return templates.TemplateResponse('index.html', {'request': request, 'weather': weather})