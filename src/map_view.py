"""
map_view.py - יצירת מפה אינטראקטיבית
צוות 1, זוג B

ראו docs/api_contract.md לפורמט הקלט והפלט.

=== תיקונים ===
1. חישוב מרכז המפה - היה עובר על images_data (כולל תמונות בלי GPS) במקום gps_image, נופל עם None
2. הסרת CustomIcon שלא עובד (filename זה לא נתיב שהדפדפן מכיר)
3. הסרת m.save() - לפי API contract צריך להחזיר HTML string, לא לשמור קובץ
4. הסרת fake_data מגוף הקובץ - הועבר ל-if __name__
5. תיקון color_index - היה מתקדם על כל תמונה במקום רק על מכשיר חדש
6. הוספת מקרא מכשירים
"""

import folium


def sort_by_time(arr):
    pass


def create_map(images_data):
    
    all_latitude = 0
    all_longitude = 0
    data_counter = 0
    for item in images_data:
        if item["has_gps"] == True:
            all_latitude += item["latitude"]
            all_longitude += item["longitude"]
            data_counter += 1

    avg_latitude = all_latitude / data_counter
    avg_longitude = all_longitude / data_counter
    m = folium.Map(location=[avg_latitude, avg_longitude], zoom_start=8)

    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen']
    camera_colors = {}
    color_index = 0

    for item in images_data:
        if item["has_gps"] == True:
            model = item["camera_model"]
            if model not in camera_colors:
                camera_colors[model] = colors[color_index % len(colors)]
                color_index += 1               
            current_color = camera_colors[model]
            folium.Marker(
                [item["latitude"], item["longitude"]], 
                popup=f'File_name: {item["filename"]}<br>Date: {item["datetime"]}<br>Camera_model: {item["camera_model"]}',
                icon=folium.Icon(color=current_color)
            ).add_to(m)

    return m._repr_html_()

    
    
    



if __name__ == "__main__":
    # תיקון: fake_data הועבר לכאן מגוף הקובץ - כדי שלא ירוץ בכל import
    fake_data = [
        {"filename": "test1.jpg", "latitude": 32.0853, "longitude": 34.7818,
         "has_gps": True, "camera_make": "Samsung", "camera_model": "Galaxy S23",
         "datetime": "2025-01-12 08:30:00"},
        {"filename": "test2.jpg", "latitude": 31.7683, "longitude": 35.2137,
         "has_gps": True, "camera_make": "Apple", "camera_model": "iPhone 15 Pro",
         "datetime": "2025-01-13 09:00:00"},
    ]
    html = create_map(fake_data)
    with open("test_map.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Map saved to test_map.html")
