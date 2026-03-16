from flask import Flask, render_template, request, redirect, url_for
import os
import shutil
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reset_session', methods=['POST'])
def reset_session():
    upload_dir = app.config['UPLOAD_FOLDER']
    for f in os.listdir(upload_dir):
        os.remove(os.path.join(upload_dir, f))
    return redirect(url_for('index'))

@app.route('/stage_files', methods=['POST'])
def stage_files():
    upload_dir = app.config['UPLOAD_FOLDER']
    existing_files = os.listdir(upload_dir)
    
    files = request.files.getlist('images')
    for file in files:
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            if filename not in existing_files:
                file.save(os.path.join(upload_dir, filename))
                existing_files.append(filename)
                
    folder_path = request.form.get('folder_path')
    if folder_path and folder_path.strip() and os.path.isdir(folder_path.strip()):
        for root, dirs, filenames in os.walk(folder_path.strip()):
            for f in filenames:
                if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                    safe_name = secure_filename(f)
                    if safe_name not in existing_files:
                        source_path = os.path.join(root, f)
                        dest_path = os.path.join(upload_dir, safe_name)
                        shutil.copy2(source_path, dest_path)
                        existing_files.append(safe_name)
                        
    current_files = os.listdir(upload_dir)
    return render_template('staging.html', files=current_files)

@app.route('/delete_file/<filename>', methods=['POST'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    if os.path.exists(file_path):
        os.remove(file_path)
    
    current_files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('staging.html', files=current_files)

@app.route('/loading', methods=['POST'])
def loading_screen():
    return render_template('loading.html')

@app.route('/do_analyze', methods=['GET'])
def do_analyze():
    upload_dir = app.config['UPLOAD_FOLDER']
    scan_warnings = []
    images_data = []
    
    from extractor import extract_all
    
    res = extract_all(upload_dir, warnings=scan_warnings)
    if type(res) == list: 
        images_data.extend(res)

    if not images_data:
        return render_template('index.html', error="⚠️ לא נמצאו תמונות תקינות לסריקה בזיכרון המערכת")
    
    from map_view import create_map
    map_html = create_map(images_data)
    
    from timeline import create_timeline
    timeline_html = create_timeline(images_data)
    
    from analyzer import analyze
    analysis = analyze(images_data)
    
    from report import create_report
    report_html = create_report(map_html, timeline_html, analysis, scan_warnings)
    
    return report_html

if __name__ == '__main__':
    app.run(debug=True)