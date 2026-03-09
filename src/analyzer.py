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