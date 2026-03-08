from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
import os

"""
extractor.py - שליפת EXIF מתמונות
צוות 1, זוג A

ראו docs/api_contract.md לפורמט המדויק של הפלט.

"""

def dms_to_decimal(dms_tuple, ref):
    # בגרסאות חדשות של Pillow, האיברים בתוך dms_tuple הם אובייקטים
    # שניתן להמיר ישירות ל-float
    degrees = float(dms_tuple[0])
    minutes = float(dms_tuple[1])
    seconds = float(dms_tuple[2])
    
    decimal = degrees + minutes / 60 + seconds / 3600
    
    if ref in [b'S', b'W', 'S', 'W']:
        decimal = -decimal
    return decimal

{'GPSInfo': {1: 'N', 2: (31.0, 15.0, 10.8), 3: 'E', 4: (34.0, 47.0, 29.4)}, 'ExifOffset': 114, 'Make': 'Samsung', 'Model': 'Galaxy S23', 'Software': 'ImageIntel Prep Tool', 'DateTimeOriginal': '2025:01:15 09:30:00', 'DateTimeDigitized': '2025:01:15 09:30:00', 'UserComment': b'UNICODE\x00\xd7\x05\xd6\x05\xe8\x05\xd4\x05 \x00\xdc\x05\xde\x05\xdb\x05\xe9\x05\xd9\x05\xe8\x05 \x00\xd4\x05\xde\x05\xe7\x05\xd5\x05\xe8\x05\xd9\x05'}

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
    if data['DateTimeOriginal']:
        return data['DateTimeOriginal']
    return None


def camera_make(data: dict):
    pass


def camera_model(data: dict):
    pass


def extract_metadata(image_path):
    """
    שולף EXIF מתמונה בודדת.

    Args:
        image_path: נתיב לקובץ תמונה

    Returns:
        dict עם: filename, datetime, latitude, longitude,
              camera_make, camera_model, has_gps
    """
    path = Path(image_path)

    # תיקון: טיפול בתמונה בלי EXIF - בלי זה, exif.items() נופל עם AttributeError
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

    # תיקון: הוסר print(data) שהיה כאן - הדפיס את כל ה-EXIF הגולמי על כל תמונה

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


def extract_all(folder_path):
    """
    שולף EXIF מכל התמונות בתיקייה.

    Args:
        folder_path: נתיב לתיקייה

    Returns:
        list של dicts (כמו extract_metadata)
    """
    pass


print(extract_metadata(r'C:\Users\elyasaf\Desktop\my_projects\image_intel\images\uploads\IMG_009.jpg'))