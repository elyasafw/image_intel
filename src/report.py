from datetime import datetime

def create_report(images_data, map_html, timeline_html, analysis):
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    insights_html = ""
    for insight in analysis.get("insights", []):
        insights_html += f"<li>{insight}</li>"
    
    cameras_html = ""
    for cam in analysis.get("unique_cameras", []):
        cameras_html += f"<span class='badge'>{cam}</span> "
    
    html = f"""
    <!DOCTYPE html>
<html lang="he" dir="rtl">

<head>
    <meta charset="UTF-8">
    <title>Image Intel Report</title>
    <style>
        body {{
            background-color: #f4f6f4;
            font-family: 'Courier New', monospace;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f4f6f4;
            background-image:
                linear-gradient(to right, #e0e7e0 1px, transparent 1px),
                linear-gradient(to bottom, #e0e7e0 1px, transparent 1px);
            background-size: 90px 90px;
        
        }}

        .header {{
            background: #353b16;
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
        }}

        .summary {{
            text-align: center;
            color: #353b16;
        }}

        .section {{
            background: #ffffffb7;
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            border: 1px solid #353b16;
        }}

        .stats {{
            display: flex;
            gap: 20px;
            justify-content: center;
            color: #ffffffb7;
            flex-wrap: wrap;
        }}

        .stat-card {{
            background: #353b16;
            padding: 15px 25px;
            border-radius: 8px;
            text-align: center;
            flex: 1;
            min-width: 200px;
            word-wrap: break-word;
        }}

        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #ffffff;
        }}

        .badge {{
            background: #2E86AB;
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            margin: 3px;
            display: inline-block;
        }}
    </style>
</head>

<body>
    <div class="header">
        <h1>Image Intel Report</h1>
        <p>נוצר ב-{now}</p>
    </div>

    <div class="section">
        <h2 class="summary">סיכום</h2>
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{analysis.get('total_images', 0)}</div>
                <div>תמונות</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{analysis.get('images_with_gps', 0)}</div>
                <div>עם GPS</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(analysis.get('unique_cameras', []))}</div>
                <div>מכשירים</div>
            </div>
        </div>
    </div>
    <div class="section">
        <h2 class="summary">מפה</h2>
        {map_html}
    </div>

    <div class="section">
        <h2 class="summary">תובנות מרכזיות</h2>
        <ul>{insights_html}</ul>
    </div>

    <div class="section">
        <h2 class="summary">ציר זמן</h2>
        {timeline_html}
    </div>

    <div class="section">
        <h2 class="summary">מכשירים</h2>
        {cameras_html}
    </div>

    <div style="text-align:center; color:#888; margin-top:30px;">
        Image Intel | האקתון 2025
    </div>
</body>

</html>
    """
    return html