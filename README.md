# Weather App

## Overview
This Weather App allows users to retrieve current weather information and a 5-day weather forecast for a specific city or based on their current location (latitude and longitude). The application is built using FastAPI, a modern web framework for Python, and serves the data in a user-friendly web interface.

## Features
- Get current weather details including temperature, condition, cloud coverage, and chance of rainfall.
- View a 5-day weather forecast with high/low temperatures and chances of rainfall for each day.
- Option to search by city name or use your current geographical location (latitude and longitude).

## Libraries Used
The following libraries are used in this project:
1. **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints.
2. **Uvicorn**: An ASGI web server implementation for Python. Used to run FastAPI applications.
3. **Requests**: A simple, yet elegant HTTP library for Python, used to make requests to external APIs.
4. **jinja2**: A template engine for Python that is used to render HTML pages dynamically.
5. **httpx**: An asynchronous HTTP client for Python, used to make non-blocking HTTP requests.
6. **python-multipart**: A library to handle form data in web applications, particularly useful when dealing with file uploads and form submissions.

## Setup and Installation

### Prerequisites
Ensure you have Python 3.6 or higher installed on your machine.

1. ### Installation
**Clone the Repository**:
```sh
git clone https://github.com/your-username/weather-app.git

2. ## Navigate to the Project Directory

```sh
cd weather-app

3. ## Create and Activate a Virtual Environment
```sh
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

4. ## Install the Required Libraries
pip install -r requirements.txt

5. ## Running the Application
    ## Start the Uvicorn Server
```sh
uvicorn app.main:app --reload

# The application will start on http://127.0.0.1:8000. You can visit this URL in your web browser to use the app.

## Using the Application

- Enter the name of the city you wish to check the weather for in the input box.
- Alternatively, provide your latitude and longitude to get the weather for your current location.

## API Key Configuration

The application uses the OpenWeatherMap API to fetch weather data. Ensure you have an API key from OpenWeatherMap. Store the API key in a `secret.py` file within the `app` directory:

```python
api = "your_openweathermap_api_key"