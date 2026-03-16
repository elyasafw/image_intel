from flask import Flask, render_template, request
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
    
    from extractor import extract_all

    if files and files[0].filename != '':
        upload_dir = app.config['UPLOAD_FOLDER']
        for f in os.listdir(upload_dir): os.remove(os.path.join(upload_dir, f))
        for file in files:
            if file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                from werkzeug.utils import secure_filename
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