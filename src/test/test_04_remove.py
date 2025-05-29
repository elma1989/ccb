from database import RecepeBook, Recepe, Ingrediant, Country

def test_remove_recepe():
    book = RecepeBook()
    fail = Recepe('Bratkartoffeln',Country('d'))
    pierogies = book.get_recepe(1)
    sausage = book.get_recepe(2)

    assert fail.remove() == 1
    assert pierogies.remove() == 0
    assert book.recepies(Country('pl')) == [sausage]