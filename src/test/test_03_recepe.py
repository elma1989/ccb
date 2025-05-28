from database import Recepe, Ingrediant, Country

def test_recepe_add():
    fail1 = Recepe('piroggen', Country('pl'))
    fail2 = Recepe('Piroggen', Country('d'))

    pierogies = Recepe('Piroggen', Country('pl'))
    sausage = Recepe('Krakauer Würstchen', Country('pl'))

    assert fail1.add() == 1
    assert fail2.add() == 2

    assert not pierogies.exists()
    assert pierogies.add() == 0
    assert pierogies.add() == 3
    assert pierogies.exists()

    assert not sausage.exists()
    assert sausage.add() == 0
    assert sausage.add() == 3
    assert sausage.exists()

def test_recepe_to_dict():
    pierogies = Recepe('Piroggen', Country('pl'))
    sausage = Recepe('Krakauer Würstchen', Country('pl'))
    pierogies_dict = {
        'id':1,
        'name':'Piroggen'
    }
    sausage_dict = {
        'id':2,
        'name':'Krakauer Würstchen'
    }

    assert pierogies.to_dict() == pierogies_dict
    assert sausage.to_dict() == sausage_dict