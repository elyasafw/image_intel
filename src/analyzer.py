
fake_data = [
    {
        "filename": "vacation_pic1.png",
        "datetime": "2025-02-14 14:15:22",
        "latitude": 29.5577,
        "longitude": 34.9519,
        "camera_make": "Sony",
        "camera_model": "Alpha a7 III",
        "has_gps": True
    },
    {
        "filename": "DSC00123.JPG",
        "datetime": "2024-11-20 10:05:10",
        "latitude": 32.0853,
        "longitude": 34.7818,
        "camera_make": "Nikon",
        "camera_model": "Z6 II",
        "has_gps": True
    },
    {
        "filename": "test1.jpg",
        "datetime": "2025-01-12 08:30:00",
        "latitude": 32.0700,
        "longitude": 34.7700,
        "camera_make": "Samsung",
        "camera_model": "Galaxy S24",
        "has_gps": True
    },
    {
        "filename": "downloaded_meme.jpg",
        "datetime": None,
        "latitude": None,
        "longitude": None,
        "camera_make": None,
        "camera_model": None,
        "has_gps": False
    },
    {
        "filename": "IMG_9921.jpg",
        "datetime": "2025-03-01 18:45:00",
        "latitude": 32.7940,
        "longitude": 34.9896,
        "camera_make": "Apple",
        "camera_model": "iPhone 14",
        "has_gps": True
    },
    {
        "filename": "whatsapp_image_2025.jpeg",
        "datetime": "2025-01-08 22:10:05",
        "latitude": None,
        "longitude": None,
        "camera_make": "Samsung",
        "camera_model": "Galaxy A54",
        "has_gps": False
    },
    {
        "filename": "test2.jpg",
        "datetime": "2025-04-13 09:00:00",
        "latitude": 31.7683,
        "longitude": 35.2137,
        "camera_make": "Apple",
        "camera_model": "iPhone 15 Pro",
        "has_gps": True
    },
    {
        "filename": "edited_photo_final.png",
        "datetime": "2023-09-09 11:30:00",
        "latitude": None,
        "longitude": None,
        "camera_make": "Adobe",
        "camera_model": "Photoshop",
        "has_gps": False
    },
    {
        "filename": "panorama_view.jpg",
        "datetime": "2025-01-05 16:20:00",
        "latitude": 32.8000,
        "longitude": 34.9900,
        "camera_make": "Google",
        "camera_model": "Pixel 8 Pro",
        "has_gps": True
    },
    {
        "filename": "test3.jpg",
        "datetime": None,
        "latitude": None,
        "longitude": None,
        "camera_make": None,
        "camera_model": None,
        "has_gps": False
    }
]
import json
from collections import Counter
from geopy.geocoders import Nominatim
def analyze(images_data: list[dict]) -> dict:
    amount_img = len(images_data)
    img_with_gps = 0
    img_with_datetime = 0
    unique_camera = []
    dates = []
    date_camera = {}
    city_list = []
    insights = []
    for img in images_data:
        if img["has_gps"] == True:
            img_with_gps += 1
            geolocator = Nominatim(user_agent="image_intel")
            location = geolocator.reverse(f"{img['latitude']}, {img['longitude']}", language='en')
            address_dict = location.raw.get("address", {})
            city_name = address_dict.get("city", address_dict.get("town", "Unknown area"))
            city_list.append(city_name)
        if img["camera_model"] not in unique_camera and img["camera_model"] != None:
            unique_camera.append(img["camera_model"])
        if img["datetime"] != None:
            dates.append(img["datetime"])
            date_camera[img["datetime"]] = img["camera_model"]
            img_with_datetime += 1
    if unique_camera:
        insights.append(f"{len(unique_camera)} different devices found")
    sorted_data_camera = {k:v for k,v in sorted(date_camera.items(), key=lambda x: x[0])}
    change_camera_date = {}
    date_counter = ''
    for k,v in sorted_data_camera.items():
        if date_counter != v:
            if date_counter != '':
                change_camera_date[k] = v
            date_counter = v
    for key in change_camera_date:
        the_string = f"In {key[5:10]} the agent change camera to {change_camera_date[key]}"
        insights.append(the_string)
    city_counts = Counter(city_list)
    for city in city_counts:
        the_string = f"{city_counts[city]} photos were taken in {city}"
        insights.append(the_string)
    final_analyze = {
        "total_images":amount_img,
        "images_with_gps": img_with_gps,
        "images_with_datetime": img_with_datetime,
        "unique_cameras": unique_camera,
        "date_range": {"start": min(dates), "end": max(dates)},
        "insights": insights
        
    }
    return final_analyze

# print(analyze(fake_data))
# print(json.dumps(analyze(fake_data), indent=4))        
