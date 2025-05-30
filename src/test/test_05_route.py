import requests as req
from database import Country

def test_index(url):
    index = req.get(url)
    assert index.status_code == 200

def test_countries(url):
    data = [
        {
            'cs':'PL',
            'name':'Polen'
        }, {
            'cs':'UA',
            'name':'Ukraine'
        }
    ]
    ua = Country('ua','Ukraine')
    pl = Country('pl','Polen')

    assert ua.add() == 0
    assert pl.add() == 0

    countries = req.get(url + 'countries')
    assert countries.status_code == 200
    assert countries.json() == data