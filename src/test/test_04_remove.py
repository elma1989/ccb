from database import RecepeBook, Recepe, Ingrediant, Country, indb

def test_remove_active_ingrediant():
    sugar = Ingrediant('Zucker')

    assert sugar.remove() == 2

def test_remove_recepe():
    book = RecepeBook()
    fail = Recepe('Bratkartoffeln',Country('d'))
    pierogies = book.get_recepe(1)
    sausage = book.get_recepe(2)

    assert fail.remove() == 1
    assert pierogies.remove() == 0
    assert book.recepies(Country('pl')) == [sausage]

def test_remove_country():
    book = RecepeBook()
    d = Country('d')
    pl = Country('pl')
    ua = Country('ua')
    
    assert d.remove() == 1
    assert pl.remove() == 0
    assert book.recepies('pl') == None
    assert book.countries() == [ua]

def test_remove_ingrediant():
    eggs = Ingrediant('Eier')
    sugar = Ingrediant('Zucker')

    assert eggs.remove() == 1
    assert sugar.remove() == 0

    indb()