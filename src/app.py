from flask import Flask, render_template, request
import os



def fake_create_timeline(images_data):
    return "<div style='background:#ddd; padding:20px;'>⏳ כאן יופיע ציר הזמן</div>"


def fake_create_report(images_data, map_html, timeline_html, analysis):
    insights_html = ""
    for insight in analysis.get('insights', []):
        insights_html += f"<li>{insight}</li>"
    return f"""
    <html>
        <body style='font-family:sans-serif; direction:rtl;'>
            <h1>דו"ח מודיעיני זמני</h1>
            <p>ניתוח עבור תיקייה: {len(images_data)} תמונות</p>
            <hr>
            {map_html}
            {timeline_html}
            <h3>תובנות:</h3>
            <ul><li>{insights_html}</li></ul>
        </body>
    </html>
    """


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_images():
    folder_path = request.form.get('folder_path')
    
    from extractor import extract_all
    images_data = extract_all(folder_path)
    if type(images_data) != list:
        return render_template('index.html', error = images_data)
    
    from map_view import create_map
    map_html = create_map(images_data)
    
    from timeline import create_timeline
    timeline_html = create_timeline(images_data)
    
    from analyzer import analyze
    analysis = analyze(images_data)
    
    # from report import create_report
    report_html = fake_create_report(images_data, map_html, timeline_html, analysis)
    
    return report_html

if __name__ == '__main__':
    app.run(debug=True)