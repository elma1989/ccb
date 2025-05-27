from database import indb, Country

def test_country_add():
    fail1 = Country('ua')
    fail2 = Country('','Ukraine')
    fail3 = Country('ukra','Ukraine')
    ua = Country('ua','Ukraine')
    pl = Country('pl','Polen')

    indb()

    assert fail1.add() == 1
    assert fail2.add() == 1
    assert fail3.add() == 1

    assert not ua.exists()
    assert ua.add() == 0
    assert ua.add() == 3
    assert ua.exists()

    assert not pl.exists()
    assert pl.add() == 0
    assert pl.add() == 3
    assert pl.exists()

def test_country_to_dict():
    ua = Country('ua')
    pl = Country('pl')
    ua_dict = {
        'cs':'UA',
        'name':'Ukraine'
    }
    pl_dict = {
        'cs':'PL',
        'name':'Polen'
    }

    assert  ua.to_dict() == ua_dict
    assert  pl.to_dict() == pl_dict