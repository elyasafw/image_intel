import folium



def create_map(images_data):
    if not images_data:
        return "<h2>! לא נמצאו תמונות בנתיב שצוין !</h2>"
    all_latitude = 0
    all_longitude = 0
    data_counter = 0
    for item in images_data:
        if item["has_gps"] == True:
            all_latitude += item["latitude"]
            all_longitude += item["longitude"]
            data_counter += 1
    if data_counter == 0:
        return "<h2>! לא נמצאו תמונות עם GPS !</h2>"
    
    if data_counter > 0:
        avg_latitude = all_latitude / data_counter
        avg_longitude = all_longitude / data_counter
    m = folium.Map(location=[avg_latitude, avg_longitude], zoom_start=8, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',attr='Google Maps')

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
    
    valid_points = [item for item in images_data if item.get("has_gps") == True and item.get("datetime") != None]
    valid_points.sort(key=lambda x: x["datetime"])
    
    path_coords = [[item["latitude"], item["longitude"]] for item in valid_points]
    
    if len(path_coords) > 1:
        folium.PolyLine(
            path_coords,
            color="blue",
            weight=3,
            opacity=0.6,
            tooltip="מסלול כרונולוגי"
        ).add_to(m)

    return m._repr_html_()