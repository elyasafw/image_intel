def create_timeline(images_data):
    # סינון רק תמונות עם זמן
    timeline_images = [img for img in images_data if img.get("datetime") is not None]
    
    # מיון מהישן לחדש
    timeline_images.sort(key=lambda img: img["datetime"])
    # טיפול ברשימה ריקה
    if not timeline_images:
        return "<div>לא נמצאו תמונות להצגה בציר הזמן.</div>"
        
    # פתיחת הקונטיינר הראשי
    html = '<div style="position:relative; padding:20px;">'
    
    # יצירת הקו האמצעי (הציר עצמו)
    html += '<div style="position:absolute; left:50%; width:2px; height:100%; background-color:#333;"></div>'
    
    # מעבר על התמונות ומיקומן (זיגזג - ימין ושמאל)
    for i, img in enumerate(timeline_images):
        side = "left" if i % 2 == 0 else "right"
        html += f'''
        <div style="margin:20px 0; text-align:{side}; width:45%; {side}:0; position:relative; {'margin-left:auto;' if side == 'right' else ''}">
            <strong>{img["datetime"]}</strong><br>
            {img.get("filename", "Unknown")}<br>
            <small>{img.get("camera_model", "Unknown")}</small>
        </div>'''
        
    html += '</div>'
    return html,
    