import requests
import os
import json
from PIL import Image
from io import BytesIO
import random

lat = random.uniform(-85, 85)
lon = random.uniform(-180, 180)
print(f"Random location: Latitude {lat:.4f}, Longitude {lon:.4f}")

MAX_IMAGES = 20

RADIUS = 2000

api_url = "https://api.openstreetcam.org/1.0/photo/nearby"

os.makedirs("kartaview_images", exist_ok=True)

def fetch_image_metadata(lat, lon, radius, limit=20):
    params = {
        'lat': lat,
        'lon': lon,
        'distance': radius,
        'limit': limit
    }
    response = requests.get(api_url, params=params)
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code} - {response.text}")
    data = response.json()
    return data.get("photos", [])

def download_images(photos):
    for i, photo in enumerate(photos):
        photo_id = photo["id"]
        lat, lon = photo["lat"], photo["lon"]
        url = photo["thumbUrl"] 
        print(f"Downloading {i+1}/{len(photos)}: {url}")

        img_data = requests.get(url).content
        image = Image.open(BytesIO(img_data))
        image.save(f"kartaview_images/{photo_id}.jpg")

        with open(f"kartaview_images/{photo_id}.json", "w") as f:
            json.dump({'id': photo_id, 'lat': lat, 'lon': lon}, f)

photos = fetch_image_metadata(lat, lon, RADIUS, limit=MAX_IMAGES)

if photos:
    download_images(photos)
    print("Download complete.")
else:
    print("No images found at this location. Try running the script again.")
