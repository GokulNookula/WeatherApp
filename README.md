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

### Installation
1. **Clone the Repository**: 
   ```sh
   git clone https://github.com/your-username/weather-app.git