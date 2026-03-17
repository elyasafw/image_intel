import folium
from folium import plugins



def create_map(images_data):
    if not images_data:
        return "<h2>! לא נמצאו תמונות בנתיב שצוין !</h2>"
    
    valid_gps = [item for item in images_data if item.get("has_gps")]
    if not valid_gps:
        return "<h2>! לא נמצאו תמונות עם GPS !</h2>"
    
    avg_lat = sum(item["latitude"] for item in valid_gps) / len(valid_gps)
    avg_lon = sum(item["longitude"] for item in valid_gps) / len(valid_gps)

    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=8, tiles=None, control_scale=True)

    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}&hl=iw',
        attr='Google Hybrid', name='תצוגת לוויין', overlay=False, control=True
    ).add_to(m)

    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}&hl=iw',
        attr='Google Terrain', name='תצוגת שטח', overlay=False, control=True
    ).add_to(m)

    marker_cluster = plugins.MarkerCluster(name="נקודות ציון").add_to(m)
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'cadetblue', 'yellow', 'lightblue', 'pink', 'lightgreen', 'beige']
    camera_colors = {}
    color_index = 0

    for item in valid_gps:
        model = item.get("camera_model", "Unknown")
        if model not in camera_colors:
            camera_colors[model] = colors[color_index % len(colors)]
            color_index += 1
        
        popup_html = f'''
        <div dir="rtl" style="text-align: right; font-family: 'Courier New', monospace; font-size: 12px; min-width: fit contact;">
            <b style="color: #000000;">קובץ:</b> {item["filename"]}<br>
            <b style="color: #000000;">תאריך:</b> {item["datetime"]}<br>
            <b style="color: #000000;">מצלמה:</b> {model}
        </div>
        '''
        
        folium.Marker(
            [item["latitude"], item["longitude"]],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color=camera_colors[model], icon='camera', prefix='fa')
        ).add_to(marker_cluster)

    valid_points = sorted([p for p in valid_gps if p.get("datetime")], key=lambda x: x["datetime"])
    if len(valid_points) > 1:
        folium.PolyLine([[p["latitude"], p["longitude"]] for p in valid_points], color="#fff704", weight=4, opacity=0.7, name="נתיב תנועה").add_to(m)

    plugins.Fullscreen(position='topright').add_to(m)
    folium.LayerControl(position='bottomright', collapsed=False).add_to(m)

    return m._repr_html_()