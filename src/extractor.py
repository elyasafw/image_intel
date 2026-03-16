from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
import os



def dms_to_decimal(dms_tuple, ref):
    degrees = float(dms_tuple[0])
    minutes = float(dms_tuple[1])
    seconds = float(dms_tuple[2])
    decimal = degrees + minutes / 60 + seconds / 3600
    if ref in [b'S', b'W', 'S', 'W']:
        decimal = -decimal
    return decimal


def has_gps(data: dict):
    gps_info = data.get('GPSInfo')
    if gps_info and 2 in gps_info and 4 in gps_info:
        return True
    return False
            

def latitude(data: dict):
    gps_info = data.get('GPSInfo')
    if gps_info and 2 in gps_info and 1 in gps_info:
        return dms_to_decimal(gps_info[2], gps_info[1])
    return None


def longitude(data: dict):
    gps_info = data.get('GPSInfo')
    if gps_info and 4 in gps_info and 3 in gps_info:
        return dms_to_decimal(gps_info[4], gps_info[3])
    return None


def datatime(data: dict):
    if data.get('DateTimeOriginal'):
        return data['DateTimeOriginal'].replace(":", "-", 2)
    return None


def camera_make(data: dict):
    if data.get("Make") == None:
        return data.get("Make")
    return data.get("Make").strip("\x00")


def camera_model(data: dict):
    if (data.get("Model")) == None:
        return data.get("Model")
    return data.get("Model").strip("\x00")


def extract_metadata(image_path):
    path = Path(image_path)

    try:
        img = Image.open(image_path)
        exif = img._getexif()
    except Exception:
        exif = None

    if exif is None:
        return {
            "filename": path.name,
            "datetime": None,
            "latitude": None,
            "longitude": None,
            "camera_make": None,
            "camera_model": None,
            "has_gps": False
        }

    data = {}
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        data[tag] = value

    exif_dict = {
        "filename": path.name,
        "datetime": datatime(data),
        "latitude": latitude(data),
        "longitude": longitude(data),
        "camera_make": camera_make(data),
        "camera_model": camera_model(data),
        "has_gps": has_gps(data)
    }

    return exif_dict


def extract_all(folder_path, warnings = None):
    if not os.path.isdir(folder_path):
        return f"⚠️ לא נמצאה תיקייה בנתיב:<br>{folder_path}"

    all_results = []
    found_access_issue = False

    def on_walk_error(err):
        nonlocal found_access_issue
        found_access_issue = True
        if warnings is not None:
            warnings.append(f"אין גישה לתיקיית בת: {err.filename}")

    try:
        for root, dirs, files in os.walk(folder_path, onerror = on_walk_error):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    file_path = os.path.join(root, file)
                    metadata = extract_metadata(file_path)
                    if metadata:
                        all_results.append(metadata)
        
        if not all_results:
            if found_access_issue:
                return f"⚠️ אין הרשאות גישה לתוכן התיקייה:<br>{folder_path}"
            return f"⚠️ לא נמצאו תמונות בנתיב:<br>{folder_path}"
            
        return all_results
    
    except Exception as e:
        return f"⚠️ אירעה שגיאה: {e}"