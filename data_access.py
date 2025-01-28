import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API keys
nasa_api_key = os.getenv("NASA_API_KEY")
weather_api_key = os.getenv("WEATHER_API_KEY")

def fetch_apod_data(date: str = None, count: int = None, thumbs: bool = False) -> dict:
    """
    Fetch Astronomy Picture of the Day (APOD) data from NASA API.

    Args:
        date (str): Date in YYYY-MM-DD format for which to fetch data. Defaults to None.
        count (int): Number of images to fetch. Defaults to None.
        thumbs (bool): Include thumbnail URLs in the response. Defaults to False.

    Returns:
        dict: Fetched data or an error message.
    """
    url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": nasa_api_key,
        "date": date,
        "count": count,
        "thumbs": thumbs,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return {"error": response.json().get("msg", "Unable to fetch data")}

def fetch_mars_rover_photos(
    rover_name: str = "curiosity",
    sol: int = 1000,
    camera: str = None,
    page: int = 1
) -> dict:
    """
    Fetch Mars Rover Photos data from NASA API.

    Args:
        rover_name (str): Name of the Mars rover (curiosity, opportunity, spirit). Defaults to "curiosity".
        sol (int): Martian sol (day) on which images were taken. Defaults to 1000.
        camera (str): Camera name (e.g., FHAZ, RHAZ, MAST). Defaults to None.
        page (int): Page number of the results. Defaults to 1.

    Returns:
        dict: Fetched data or an error message.
    """
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover_name}/photos"
    params = {
        "api_key": nasa_api_key,
        "sol": sol,
        "camera": camera,
        "page": page,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("photos", [])
    return {"error": response.json().get("msg", "Unable to fetch data")}

def fetch_moon_phase_and_weather(location: str = "Santa Clara,CA", date: str = "today") -> str:
    """
    Fetch moon phase and weather information using the Visual Crossing Weather API.

    Args:
        location (str): Location in "City,State" or latitude,longitude format.
        date (str): Date for weather and moon phase data (e.g., "2023-01-22" or "today").

    Returns:
        str: Moon phase and weather information.
    """   
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{date}?key={weather_api_key}&include=days"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        day_data = data["days"][0]
        moon_phase = day_data.get("moonphase", "Unknown")
        description = day_data.get("description", "No weather description available")
        temp = day_data.get("temp", "N/A")
        feels_like = day_data.get("feelslike", "N/A")
        humidity = day_data.get("humidity", "N/A")
        moon_phase_percentage = moon_phase * 100 if isinstance(moon_phase, float) else "Unknown"

        return (
            f"Moon Phase: {moon_phase_percentage:.1f}%\n"
            f"Weather: {description}\n"
            f"Temperature: {temp}°C (Feels like {feels_like}°C)\n"
            f"Humidity: {humidity}%"
        )
    return f"Could not fetch data. Error: {response.status_code} - {response.text}"

def fetch_iss_location() -> str:
    """
    Fetch the current location of the International Space Station (ISS).

    Returns:
        str: ISS latitude, longitude, and timestamp.
    """
    url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        latitude = data["iss_position"]["latitude"]
        longitude = data["iss_position"]["longitude"]
        timestamp = data["timestamp"]
        return f"The ISS is currently at latitude {latitude} and longitude {longitude} (timestamp: {timestamp})."
    return f"Could not fetch ISS location. Error: {response.status_code}"

def fetch_people_in_space() -> str:
    """
    Fetch the list of people currently in space.

    Returns:
        str: Number of people and their names with respective spacecraft.
    """
    url = "http://api.open-notify.org/astros.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        people = data["people"]
        number = data["number"]
        people_list = ", ".join([f"{person['name']} ({person['craft']})" for person in people])
        return f"There are currently {number} people in space: {people_list}."
    return f"Could not fetch data about people in space. Error: {response.status_code}"

def fetch_space_weather(event_type: str = "FLR") -> str:
    """
    Fetch space weather data from NASA's DONKI API.

    Args:
        event_type (str): Type of space weather event (e.g., FLR, GST, CME).

    Returns:
        str: Summary of recent space weather events.
    """
    base_url = "https://api.nasa.gov/DONKI"
    url = f"{base_url}/{event_type}"
    params = {
        "api_key": nasa_api_key,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if not data:
            return f"No recent {event_type} events found."
        events = [
            f"- Event started on {event.get('beginTime', 'Unknown start time')}: {event.get('note', 'No additional details available.')}"
            for event in data[:5]
        ]
        return f"Here are the most recent {event_type} events:\n" + "\n".join(events)
    return f"Could not fetch space weather data. Error: {response.status_code} - {response.text}"
