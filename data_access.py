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