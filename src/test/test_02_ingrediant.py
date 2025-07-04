from database import Ingrediant

def test_ingredieant_add():
    fail = Ingrediant('zucker')
    sugar = Ingrediant('Zucker')
    flower = Ingrediant('Mehl')

    assert fail.add() == 1

    assert not sugar.exists()
    assert sugar.add() == 0
    assert sugar.add() == 3
    assert sugar.exists()

    assert not flower.exists()
    assert flower.add() == 0
    assert flower.exists()

def test_ingredieant_to_dict():
    sugar = Ingrediant('Zucker')
    flower = Ingrediant('Mehl')
    sugar_dict = {
        'name':'Zucker',
        'id': 1
    }
    flower_dict = {
        'name':'Mehl',
        'id': 2
    }