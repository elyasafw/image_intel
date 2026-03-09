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
from pathlib import Path
import folium
from extractor import extract_all
#path = Path(__file__).parent.parent / "images" / "ready"
def sort_by_time(arr):
    pass

#data_list = extract_all(path)
def create_map(images_data):
    if not images_data:
        return "<h2>No images found in the specified path</h2>"
    all_latitude = 0
    all_longitude = 0
    data_counter = 0
    for item in images_data:
        if item["has_gps"] == True:
            all_latitude += item["latitude"]
            all_longitude += item["longitude"]
            data_counter += 1
    if data_counter == 0:
        return "<h2>No GPS data found in the images</h2>"
    
    if data_counter > 0:
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

    html = create_map(data_list)
    with open("test_map.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Map saved to test_map.html")
