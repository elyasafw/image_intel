import pytest



def get_fake_data():
    return [
        {"filename": "test1.jpg", "camera_model": "iPhone", "datetime": "2025-01-12 10:30:00"},
        {"filename": "test2.jpg", "camera_model": "Samsung", "datetime": "2025-01-12 12:00:00"},
    ]

def test_create_timeline_html_structure():
    from timeline import create_timeline
    result = create_timeline(get_fake_data())
    
    assert "timeline-container" in result
    assert "graph-area" in result
    assert "dot" in result
    assert "tooltip" in result

def test_create_timeline_data_insertion():
    from timeline import create_timeline
    data = get_fake_data()
    result = create_timeline(data)
    
    assert "test1.jpg" in result
    assert "iPhone" in result
    assert "10:30:00" in result

def test_create_timeline_handles_missing_date():
    from timeline import create_timeline
    data = [{"filename": "no_date.jpg", "datetime": None}]
    result = create_timeline(data)
    
    assert '<div class="dot"' not in result