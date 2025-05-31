import requests as req
from database import Country, Ingrediant, Recepe

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

def test_recepies(url):
    sugar = Ingrediant('Zucker', 500.0, 'g')
    flower = Ingrediant('Mehl', 200.0, 'g')
    assert sugar.add() == 0
    assert flower.add() == 0

    pierogies = Recepe('Piroggen', Country('pl'))
    assert pierogies.add() == 0
    assert pierogies.add_ingrediant(sugar) == 0
    assert pierogies.add_ingrediant(flower) == 0
    pierogies.preparation = 'Nudeln kochen'

    sausage = Recepe('Krakauer Würstchen', Country('pl'))
    assert sausage.add() == 0
    assert sausage.add_ingrediant(sugar) == 0
    assert sausage.add_ingrediant(flower) == 0
    sausage.preparation = 'Würstchen braten'

    pl_data = [
        {
            'id':2,
            'name':'Krakauer Würstchen'
        },{
            'id':1,
            'name':'Piroggen'
        }
    ]

    without_country = req.get(url + 'recepies')
    fail_country = req.get(url + 'recepies?country=d')
    pl_country = req.get(url + 'recepies?country=pl')

    assert without_country.status_code == 400
    assert fail_country.status_code == 404
    assert pl_country.status_code == 200
    assert pl_country.json() == pl_data

def test_recepe_details(url):
    pierogies_data = {
        'id':1,
        'name':'Piroggen',
        'country':'PL',
        'ingrediants': [{
            'id':2,
            'name':'Mehl',
            'amount':200.0,
            'unit':'g'
        },{
            'id':1,
            'name':'Zucker',
            'amount':500.0,
            'unit':'g'
        }],
        'preparation':'Nudeln kochen'
    }
    fail_recepe = req.get(url + 'recepies/3')
    pierogies = req.get(url + 'recepies/1')

    assert fail_recepe.status_code == 404
    assert pierogies.status_code == 200
    assert pierogies.json() == pierogies_data