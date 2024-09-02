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

    weatherUrl = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apiKey}&units=metric'
    forecastUrl = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={apiKey}&units=metric'

    async with httpx.AsyncClient() as client:
        weatherResponse = await client.get(weatherUrl)
        forecastResponse = await client.get(forecastUrl)

    weather = weatherResponse.json()
    forecast = forecastResponse.json()  # This line is now correctly using forecastResponse

    print("Weather Response:", weather)  # Log weather data
    print("Forecast Response:", forecast)  # Log forecast data
    
    # Handle errors from the API
    if weather.get("cod") != 200 or forecast.get("cod") != "200":
        errorMessage = "The City that you Entered is Incorrect. Please try again."  # Custom error message
        return templates.TemplateResponse('index.html', {'request': request, 'error': errorMessage})
    
    # Extract required data from weather and forecast responses
    currentTemp = weather['main']['temp']
    weatherCondition = weather['weather'][0]['description']
    cloudCoverage = weather['clouds']['all']
    rainfallAmount = weather.get('rain', {}).get('1h', 0)  # Rainfall in the last hour, if available

    # Find the highest and lowest temperatures in the 5-day forecast
    highTemp, highTempTime = None, None
    lowTemp, lowTempTime = None, None
    for entry in forecast['list']:
        temp = entry['main']['temp']
        if highTemp is None or temp > highTemp:
            highTemp = temp
            highTempTime = entry['dt_txt']
        if lowTemp is None or temp < lowTemp:
            lowTemp = temp
            lowTempTime = entry['dt_txt']

    # Prepare data for 5-day forecast
    forecastData = []
    for day in forecast['list']:
        dayForecast = {
            "date": day['dt_txt'],
            "temp": day['main']['temp'],
            "condition": day['weather'][0]['description'],
            "rainfall": day.get('rain', {}).get('3h', 0),
        }
        forecastData.append(dayForecast)

    return templates.TemplateResponse(
        'index.html',
        {
            'request': request,
            'weather': weather,
            'currentTemp': currentTemp,
            'highTemp': highTemp,
            'highTempTime': highTempTime,
            'lowTemp': lowTemp,
            'lowTempTime': lowTempTime,
            'rainfallAmount': rainfallAmount,
            'weatherCondition': weatherCondition,
            'cloudCoverage': cloudCoverage,
            'forecast': forecastData
        }
    )