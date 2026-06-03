import pytest
from working import convert

# Valid cases — require space between hour and AM/PM


def test_valid_inputs():
    assert convert("9 AM to 5 PM") == "09:00 to 17:00"
    assert convert("10:30 AM to 8:15 PM") == "10:30 to 20:15"
    assert convert("12 AM to 12 PM") == "00:00 to 12:00"
    assert convert("12 PM to 12 AM") == "12:00 to 00:00"
    assert convert("1:05 PM to 2:00 AM") == "13:05 to 02:00"

# Invalid format: missing space between time and AM/PM


def test_missing_space():
    with pytest.raises(ValueError):
        convert("9AM to 5PM")
    with pytest.raises(ValueError):
        convert("10:30AM to 8:15PM")
    with pytest.raises(ValueError):
        convert("12AM to 12PM")

# Invalid time values


def test_invalid_times():
    with pytest.raises(ValueError):
        convert("13 AM to 5 PM")   # hour > 12
    with pytest.raises(ValueError):
        convert("9:75 AM to 5 PM")  # invalid minute
    with pytest.raises(ValueError):
        convert("0 AM to 5 PM")     # hour < 1

# Invalid general formats


def test_invalid_formatting():
    with pytest.raises(ValueError):
        convert("9 AM 5 PM")            # missing "to"
    with pytest.raises(ValueError):
        convert("AM 9 to PM 5")         # flipped format
    with pytest.raises(ValueError):
        convert("9 to 5")               # missing AM/PM
    with pytest.raises(ValueError):
        convert("noon to midnight")     # invalid strings
    with pytest.raises(ValueError):
        convert("")                     # empty string
