from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx
from . import secret # Import the secret module for API Key
import requests

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class= HTMLResponse)
#Using async function to allow the server to process multiple requests and not wait for one at a time
# Thus making our website run faster
async def readRoot(request:Request):
    return templates.TemplateResponse("index.html",{"request": request})

@app.post("/", response_class= HTMLResponse)
async def getWeather(request: Request, city: str = Form(...)):
    city = city.strip().lower()
    
    if not city:  # If city is empty or only whitespace, don't make the API call
        return templates.TemplateResponse('index.html', {'request': request})
    
    apiKey = secret.api
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apiKey}&units=metric'

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    weather = response.json()
    
    # Handle errors from the API
    if weather.get("cod") != 200:
        errorMessage = "The City that you Entered is Incorrect. Please try again."  # Custom error message
        return templates.TemplateResponse('index.html', {'request': request, 'error': errorMessage})
    
    # Ensure the response is for a city
    if "name" in weather and weather.get("sys", {}).get("country"):
        return templates.TemplateResponse('index.html', {'request': request, 'weather': weather})
    else:
        errorMessage = "Please enter a valid city name, not a state or country."
        return templates.TemplateResponse('index.html', {'request': request, 'error': errorMessage})