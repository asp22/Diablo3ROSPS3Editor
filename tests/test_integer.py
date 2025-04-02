import pytest

import proto_parsers.integer as ppi

def test_integer_encode():
    unsigned = 255
    res = ppi.encode(unsigned)
    assert res == b'\xff\x01', f"res: {res}"

def test_integer_decode():
    read, t = ppi.decode(b'\xff\x01')
    assert t.unsigned == 255
    assert read == 2

def test_integer_create_with_string():
    with pytest.raises(TypeError):
        ppi.Integer('a')

def test_integer_create_with_negative():
    with pytest.raises(ValueError):
        ppi.Integer(-1)

def test_integer_create_with_zero():
    ppi.Integer(0)

def test_block_setting_negative_number():
    with pytest.raises(ValueError):
        t = ppi.Integer(0)
        t.unsigned = -1

def test_allow_setting_valid_numbers():
    t = ppi.Integer(0)
    t.unsigned = 0
    t.unsigned = 1

def test_encode_method():
    t = ppi.Integer(255)
    res = t.encode()
    assert res == b'\xff\x01', f"res: {res}"
