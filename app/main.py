from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx
from . import secret  # Import the secret module for API Key
import requests
from datetime import datetime

app = FastAPI()

# Set the directory for HTML templates
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
# Define the root endpoint that serves the main HTML page
async def readRoot(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
# Define the endpoint to handle weather requests
async def getWeather(request: Request, city: str = Form(None), lat: str = Form(None), lon: str = Form(None)):
    apiKey = secret.api  # Retrieve the API key from the secret module

    if lat and lon:
        # If latitude and longitude are provided, use them to get weather data
        weatherUrl = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={apiKey}&units=metric'
        forecastUrl = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={apiKey}&units=metric'
    elif city:
        # If a city name is provided, use it to get weather data
        city = city.strip().lower()
        weatherUrl = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apiKey}&units=metric'
        forecastUrl = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={apiKey}&units=metric'
    else:
        # If neither city nor coordinates are provided, return the main page without data
        return templates.TemplateResponse('index.html', {'request': request})

    # Make asynchronous requests to the weather and forecast APIs
    async with httpx.AsyncClient() as client:
        weatherResponse = await client.get(weatherUrl)
        forecastResponse = await client.get(forecastUrl)

    # Parse the JSON responses
    weather = weatherResponse.json()
    forecast = forecastResponse.json()

    # Handle errors from the API
    if weather.get("cod") != 200 or forecast.get("cod") != "200":
        errorMessage = "The City or Location that you Entered is Incorrect. Please try again."  # Custom error message
        return templates.TemplateResponse('index.html', {'request': request, 'error': errorMessage})

    # Extract current weather data
    currentTemp = weather.get('main', {}).get('temp', 'N/A')
    weatherCondition = weather.get('weather', [{}])[0].get('description', 'N/A')
    cloudCoverage = weather.get('clouds', {}).get('all', 'N/A')
    rainfallAmount = weather.get('rain', {}).get('1h', 0)  # Rainfall in the last hour, if available

    # Prepare summary for 5-day forecast
    forecastSummary = {}
    for entry in forecast['list']:
        dateStr = entry['dt_txt']
        dateObj = datetime.strptime(dateStr, '%Y-%m-%d %H:%M:%S').date()  # Convert string to date

        if dateObj not in forecastSummary:
            # Initialize summary data for a new date
            forecastSummary[dateObj] = {
                "highTemp": entry['main']['temp_max'],
                "lowTemp": entry['main']['temp_min'],
                "rainChance": entry.get('pop', 0) * 100,  # Probability of precipitation as percentage
            }
        else:
            # Update summary data for an existing date
            forecastSummary[dateObj]['highTemp'] = max(forecastSummary[dateObj]['highTemp'], entry['main']['temp_max'])
            forecastSummary[dateObj]['lowTemp'] = min(forecastSummary[dateObj]['lowTemp'], entry['main']['temp_min'])
            forecastSummary[dateObj]['rainChance'] = max(forecastSummary[dateObj]['rainChance'], entry.get('pop', 0) * 100)

    # Convert the forecast summary to a list and limit to the first 5 days
    forecastData = [
        {
            "date": date.strftime('%A, %B %d, %Y'),
            "highTemp": day['highTemp'],
            "lowTemp": day['lowTemp'],
            "rainChance": day['rainChance']
        }
        for date, day in sorted(forecastSummary.items())[:5]
    ]

    # Render the template with the weather and forecast data
    return templates.TemplateResponse(
        'index.html',
        {
            'request': request,
            'weather': weather,
            'currentTemp': currentTemp,
            'highTemp': max(day['highTemp'] for day in forecastData),
            'lowTemp': min(day['lowTemp'] for day in forecastData),
            'rainfallAmount': f"{rainfallAmount}%",  # Change to percentage format
            'weatherCondition': weatherCondition,
            'cloudCoverage': cloudCoverage,
            'forecastSummary': forecastData,
        }
    )
