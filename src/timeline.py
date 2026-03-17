def create_timeline(images_data):
    timeline_tree = {}

    for img in images_data:
        dt_str = img.get("datetime")
        if not dt_str: continue
            
        date_part, time_part = dt_str.split(" ")
        h, m, s = [int(x) for x in time_part.split(":")]
        
        if date_part not in timeline_tree:
            timeline_tree[date_part] = {}
        if h not in timeline_tree[date_part]:
            timeline_tree[date_part][h] = []
            
        img_info = img.copy()
        img_info['minute'] = m
        timeline_tree[date_part][h].append(img_info)

    dates = sorted(timeline_tree.keys())
    graph_height = max(165, len(dates) * 25)

    html = f'''
    <style>
        .timeline-container {{
            position: relative;
            width: 85%;
            height: {graph_height}px;
            margin: 30px auto;
            text-align: right;
            background: white;
            padding: 20px 60px 30px 15px;
            font-family: 'Courier New', monospace;
        }}
        .graph-area {{
            position: relative;
            width: 100%;
            height: 100%;
            border-right: 2px solid #4b5320;
            border-bottom: 2px solid #4b5320;
        }}
        .y-label {{
            position: absolute;
            right: -75px;
            font-size: 0.65rem;
            color: #4b5320;
            font-weight: bold;
            white-space: nowrap;
        }}
        .x-label {{
            position: absolute;
            top: 102%;
            font-size: 0.65rem;
            color: #4b5320;
        }}
        .grid-line {{
            position: absolute;
            background: #e6ede6;
        }}
        .grid-line-major {{
            position: absolute;
            background: #d0d7d0;
        }}
        .dot {{
            width: 10px;
            height: 10px;
            background: #f72222;
            border-radius: 50%;
            position: absolute;
            cursor: help;
            transition: transform 0.2s;
            transform: translate(-50%, 50%);
            z-index: 10;
        }}
        .dot:hover {{
            transform: translate(-50%, 50%) scale(1.6);
            background: #4b5320;
            z-index: 100;
        }}
        
        .dot .tooltip {{
            visibility: hidden;
            width: 155px;
            background-color: rgba(253, 253, 253, 0.92);
            backdrop-filter: blur(3px);
            -webkit-backdrop-filter: blur(3px);
            color: #000000;
            text-align: right;
            padding: 8px;
            position: absolute;
            z-index: 200;
            bottom: 150%;
            left: 50%;
            margin-left: -85px;
            opacity: 1 !important;
            font-size: 0.60rem;
            line-height: 1.3;
            pointer-events: none;
            border: 1px solid #4b5320;
        }}
        .truncate {{
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            display: block;
            width: 100%;
        }}
        .dot:hover .tooltip {{
            visibility: visible;
        }}
    </style>
    <div class="timeline-container">
        <div class="graph-area">'''
    
    for hr in range(0, 25):
        x_pos = (hr / 24) * 100
        is_major = hr % 4 == 0
        line_class = "grid-line-major" if is_major else "grid-line"
        line_width = "1.5px" if is_major else "0.5px"
        
        html += f'''
        <div class="{line_class}" style="left: {x_pos}%; top: 0; bottom: 0; width: {line_width};"></div>'''
        
        if is_major:
            html += f'<div class="x-label" style="left: {x_pos}%; transform: translateX(-50%);">{hr:02d}:00</div>'

    for i, date in enumerate(dates):
        y_pos = (i / (len(dates) - 1 if len(dates) > 1 else 1)) * 100
        
        html += f'''
        <div class="grid-line-major" style="bottom: {y_pos}%; left: 0; right: 0; height: 1px;"></div>
        <div class="y-label" style="bottom: {y_pos}%; transform: translateY(50%);">{date}</div>'''
        
        for hour in timeline_tree[date]:
            for img in timeline_tree[date][hour]:
                x_pos = ((hour * 60 + img['minute']) / (24 * 60)) * 100
                info = f'''
                        <div class="truncate"><b>קובץ:</b> {img['filename']}</div>
                        <div class="truncate"><b>מצלמה:</b> {img['camera_model']}</div>
                        <div class="truncate"><b>זמן:</b> {img['datetime']}</div>
                        '''                
                html += f'''
                <div class="dot" style="left: {x_pos}%; bottom: {y_pos}%;">
                    <span class="tooltip">{info}</span>
                </div>'''
            
    html += '   </div>\n    </div>'
    
    return html