from database import Recepe, Ingrediant, Country, RecepeBook

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

def test_recepe_book_get_recepe():
    book = RecepeBook()

    assert book.get_recepe(1) == Recepe('Piroggen', Country('pl'))
    assert book.get_recepe(2) == Recepe('Krakauer Würstchen', Country('pl'))
    assert not book.get_recepe(3)

def test_recepe_to_dict():
    book = RecepeBook()
    pierogies = book.get_recepe(1)
    sausage = book.get_recepe(2)
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

def test_recepe_book_find():
    book = RecepeBook()

    assert book.find('Piroggen',Country('pl')) == book.get_recepe(1)
    assert book.find('Krakauer Würstchen',Country('pl')) == book.get_recepe(2)
    assert not book.find('Bratkartoffeln', Country('d'))