from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_images():
    files = request.files.getlist('images')
    local_folder = request.form.get('local_folder')
    
    from extractor import extract_all
    all_images_data = []

    # 1. עיבוד הקבצים שנגררו לאתר
    if files and files[0].filename != '':
        folder_path = app.config['UPLOAD_FOLDER']
        
        # ניקוי התיקייה הזמנית
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        
        # שמירת הקבצים החדשים
        for file in files:
            if file:
                from werkzeug.utils import secure_filename
                filename = secure_filename(file.filename)
                file.save(os.path.join(folder_path, filename))
        
        dragged_data = extract_all(folder_path)
        if isinstance(dragged_data, list):
            all_images_data.extend(dragged_data)

    # 2. עיבוד הנתיב המקומי (כולל תיקיות בת)
    if local_folder and local_folder.strip() != '':
        folder_data = extract_all(local_folder.strip())
        if isinstance(folder_data, list):
            all_images_data.extend(folder_data)
        elif not all_images_data: # שגיאה רק אם גם הגרירה ריקה
            return render_template('index.html', error=folder_data)

    # אם לא הוכנס כלום באף אחת מהאפשרויות
    if not all_images_data:
        return render_template('index.html', error="לא נמצאו תמונות לסריקה בשום מקור.")

    images_data = all_images_data
    
    from map_view import create_map
    map_html = create_map(images_data)
    
    from timeline import create_timeline
    timeline_html = create_timeline(images_data)
    
    from analyzer import analyze
    analysis = analyze(images_data)
    
    from report import create_report
    report_html = create_report(map_html, timeline_html, analysis)
    
    return report_html

if __name__ == '__main__':
    app.run(debug=True)