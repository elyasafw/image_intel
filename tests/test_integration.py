def test_full_pipeline(tmp_path):
    from extractor import extract_all
    from map_view import create_map
    from timeline import create_timeline
    from analyzer import analyze
    from report import create_report
    

    
    img_dir = tmp_path / "test_images"
    img_dir.mkdir()
    (img_dir / "sample.jpg").write_text("dummy_data")
    
    images_data = extract_all(str(img_dir))
    assert isinstance(images_data, list), f"Expected list but got: {images_data}"
    assert len(images_data) > 0
    
    map_html = create_map(images_data)
    assert isinstance(map_html, str)
    
    timeline_html = create_timeline(images_data)
    assert isinstance(timeline_html, str)
    
    analysis = analyze(images_data)
    assert isinstance(analysis, dict)
    
    report_html = create_report(map_html, timeline_html, analysis, [])
    assert "<html" in report_html.lower()