from numb3rs import validate

def test_validate():
    assert validate("255.255.255.255") == True
    assert validate("10.10.10.10.10") == False
    assert validate("cat") == False
    assert validate("0") == False
    assert validate("192.999.999.999") == False
