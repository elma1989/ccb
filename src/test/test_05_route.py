import requests as req

def test_index(url):
    index = req.get(url)
    assert index.status_code == 200