from project import deposit, withdraw, check_balance
import pytest

def test_deposit():
    assert deposit(100, 50) == 150

def test_deposit_negative():
    with pytest.raises(ValueError):
        deposit(100, -10)

def test_withdraw():
    assert withdraw(100, 40) == 60

def test_withdraw_overdraft():
    assert withdraw(100, 200) == 100

def test_withdraw_negative():
    with pytest.raises(ValueError):
        withdraw(100, -5)

def test_check_balance():
    assert check_balance(250) == 250
