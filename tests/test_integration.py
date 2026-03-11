def test_full_pipeline():
    from extractor import extract_all
    from map_view import create_map
    from timeline import create_timeline
    from analyzer import analyze
    from report import create_report
    
    images_data = extract_all("images/sample_data")
    assert len(images_data) > 0
    
    map_html = create_map(images_data)
    assert isinstance(map_html, str)
    
    timeline_html = create_timeline(images_data)
    assert isinstance(timeline_html, str)
    
    analysis = analyze(images_data)
    assert isinstance(analysis, dict)
    
    report_html = create_report(map_html, timeline_html, analysis)
    assert "<html" in report_html.lower()