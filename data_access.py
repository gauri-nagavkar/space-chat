import os
import requests
from dotenv import load_dotenv

load_dotenv() 

# Now you can access the API key using os.environ
api_key = os.environ.get("NASA_API_KEY") 


def fetch_apod_data(date: str = None, count: int = None, thumbs: bool = False) -> dict:
  """Fetches Astronomy Picture of the Day data from NASA API.

  Args:
      date: Date for which to fetch data (YYYY-MM-DD format). Defaults to None.
      count: Number of days for which to fetch data. Defaults to None.
      thumbs: Whether to include thumbnail URLs in the response. Defaults to False.

  Returns:
      A dictionary containing the fetched data or an error message.
  """
  url = "https://api.nasa.gov/planetary/apod"
  params = {
      "api_key": os.environ["NASA_API_KEY"],
      "date": date,
      "count": count,
      "thumbs": thumbs,
  }
  response = requests.get(url, params=params)
  if response.status_code == 200:
    return response.json()
  else:
    return {"error": response.json().get("msg", "Unable to fetch data")}


def fetch_mars_rover_photos(rover_name: str = "curiosity", sol: int = 1000, camera: str = None, page: int = 1) -> dict:
  """Fetches Mars Rover Photos data from NASA API.

  Args:
      rover_name: Name of the Mars rover (curiosity, opportunity, or spirit). Defaults to "curiosity".
      sol: Martian sol (day) on which images were taken. Defaults to 1000.
      camera: Name of the camera (e.g., FHAZ, RHAZ, MAST, etc.). Defaults to None.
      page: Page number of the results (1-indexed). Defaults to 1.

  Returns:
      A dictionary containing the fetched data or an error message.
  """
  url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover_name}/photos"
  params = {
      "api_key": os.environ["NASA_API_KEY"],
      "sol": sol,
      "camera": camera,
      "page": page,
  }
  response = requests.get(url, params=params)
  if response.status_code == 200:
    return response.json().get("photos", [])
  else:
    return {"error": response.json().get("msg", "Unable to fetch data")}


def fetch_moon_phase_and_weather(location="Santa Clara,CA", date="today"):
    """
    Fetch moon phase and weather information using Visual Crossing Weather API.

    Args:
        location (str): Location in "City,State" or latitude,longitude format.
        date (str): Date for the weather and moon phase (e.g., "2023-01-22" or "today").

    Returns:
        str: Moon phase and weather information.
    """
    api_key = os.environ["weather_api_key"]
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{date}?key={api_key}&include=days"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        day_data = data["days"][0]  # Get the first day's data
        moon_phase = day_data.get("moonphase", "Unknown")
        description = day_data.get("description", "No weather description available")
        temp = day_data.get("temp", "N/A")
        feels_like = day_data.get("feelslike", "N/A")
        humidity = day_data.get("humidity", "N/A")
        
        # Format moon phase percentage
        moon_phase_percentage = moon_phase * 100 if isinstance(moon_phase, float) else "Unknown"

        return (
            f"Moon Phase: {moon_phase_percentage:.1f}%\n"
            f"Weather: {description}\n"
            f"Temperature: {temp}°C (Feels like {feels_like}°C)\n"
            f"Humidity: {humidity}%"
        )
    else:
        return f"Could not fetch data. Error: {response.status_code} - {response.text}"

    

    

# Fetch the current ISS location
def fetch_iss_location():
    url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        latitude = data["iss_position"]["latitude"]
        longitude = data["iss_position"]["longitude"]
        timestamp = data["timestamp"]
        return f"The ISS is currently at latitude {latitude} and longitude {longitude} (timestamp: {timestamp})."
    else:
        return f"Could not fetch ISS location. Error: {response.status_code}"

# Fetch the list of people currently in space
def fetch_people_in_space():
    url = "http://api.open-notify.org/astros.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        people = data["people"]
        number = data["number"]
        people_list = ", ".join([f"{person['name']} ({person['craft']})" for person in people])
        return f"There are currently {number} people in space: {people_list}."
    else:
        return f"Could not fetch data about people in space. Error: {response.status_code}"
    

# Fetch space weather events from DONKI API
def fetch_space_weather(event_type="FLR"):
    """
    Fetch space weather data from NASA's DONKI API.

    Args:
        event_type (str): Type of space weather event (e.g., "FLR" for solar flares, "GST" for geomagnetic storms).
                         Supported event types: FLR, GST, CME, SEP, MPC, RBE, IPS.
    Returns:
        str: A summary of recent events of the specified type.
    """
    base_url = "https://api.nasa.gov/DONKI"
    api_key = os.environ["NASA_API_KEY"] 
    url = f"{base_url}/{event_type}?api_key={api_key}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if len(data) == 0:
            return f"No recent {event_type} events found."

        # Format the first few events into a user-friendly summary
        events = []
        for event in data[:5]:  # Limit to the first 5 events
            start_time = event.get("beginTime", "Unknown start time")
            details = event.get("note", "No additional details available.")
            events.append(f"- Event started on {start_time}: {details}")

        return f"Here are the most recent {event_type} events:\n" + "\n".join(events)
    else:
        return f"Could not fetch space weather data. Error: {response.status_code} - {response.text}"
