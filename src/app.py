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
    
    if not files or files[0].filename == '':
        return render_template('index.html', error="לא נבחרו קבצים")

    folder_path = app.config['UPLOAD_FOLDER']
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    for file in files:
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(folder_path, filename))

    from extractor import extract_all
    images_data = extract_all(folder_path)
    if type(images_data) != list:
        return render_template('index.html', error=images_data)
    
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