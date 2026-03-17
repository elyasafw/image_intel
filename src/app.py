from extractor import extract_all
from map_view import create_map
from timeline import create_timeline
from analyzer import analyze
from report import create_report
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/analyze', methods = ['POST'])
def analyze_images():
    files = request.files.getlist('images')
    folder_path = request.form.get('local_folder')
    scan_warnings = []
    images_data = []
    
    if files and files[0].filename != '':
        upload_dir = app.config['UPLOAD_FOLDER']
        os.makedirs(upload_dir, exist_ok=True)
        for f in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, f)
            if os.path.isfile(file_path): os.remove(file_path)
            
        for file in files:
            if file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                file.save(os.path.join(upload_dir, secure_filename(file.filename)))
        
        res = extract_all(upload_dir, warnings = scan_warnings)
        if type(res) == list: images_data.extend(res)

    if folder_path and folder_path.strip():
        res = extract_all(folder_path.strip(), warnings = scan_warnings)
        if type(res) == list:
            images_data.extend(res)
        elif not images_data:
            return render_template('index.html', error = res)

    if not images_data:
        return render_template('index.html', error = "⚠️ לא נמצאו תמונות לסריקה")
    
    map_html = create_map(images_data)
    timeline_html = create_timeline(images_data)
    analysis = analyze(images_data)
    report_html = create_report(map_html, timeline_html, analysis, scan_warnings)
    
    return report_html

if __name__ == '__main__':
    app.run(debug=True)