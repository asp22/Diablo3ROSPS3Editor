import pytest

import proto_parsers.fixed64 as f64
import proto_parsers.exceptions as exp

def test_encode():
    payload = b'\xff\xff\xff\xff\xff\xff\xff\xff'
    res = f64.encode(payload)
    assert res == payload

def test_encode_insufficient():
    with pytest.raises(exp.InsufficientData):
        payload = b'\xff\xff\xff\xff\xff\xff\xff'
        res = f64.encode(payload)

def test_decode():
    payload = b'\xff\xff\xff\xff\xff\xff\xff\xff'
    read, t = f64.decode(payload)
    assert read == 8
    assert t.unsigned == pow(2,64)-1
    assert t.signed   == -1

def test_decode_insufficient():
    with pytest.raises(exp.InsufficientData):
        payload = b'\xff\xff\xff\xff\xff\xff\xff'
        read, t = f64.decode(payload)

def test_update_unsigned():
    payload = b'\xff\xff\xff\xff\xff\xff\xff\xff'
    read, t = f64.decode(payload)
    assert t.unsigned == pow(2,64)-1
    t.unsigned = 4
    assert t.unsigned == 4
    assert t.signed == 4

def test_block_setting_unsigned_with_string():
    payload = b'\xff\xff\xff\xff\xff\xff\xff\xff'
    read, t = f64.decode(payload)
    assert t.unsigned == pow(2,64)-1
    with pytest.raises(TypeError):
        t.unsigned = 'a'

def test_block_setting_unsigned_with_negative():
    payload = b'\xff\xff\xff\xff\xff\xff\xff\xff'
    read, t = f64.decode(payload)
    assert t.unsigned == pow(2,64)-1
    with pytest.raises(ValueError):
        t.unsigned = -1

def test_set_signed():
    payload = b'\x00\x00\x00\x00\x00\x00\x00\x00'
    read, t = f64.decode(payload)
    t.signed = -1
    assert t.unsigned == pow(2,64)-1
    assert t.signed == -1

def test_set_positive_signed():
    payload = b'\x00\x00\x00\x00\x00\x00\x00\x00'
    read, t = f64.decode(payload)
    t.signed = 2
    assert t.unsigned == 2
    assert t.signed == 2

def test_encode_method():
    payload = b'\xff\xff\xff\xff\xff\xff\xff\xff'
    read, t = f64.decode(payload)
    assert payload == t.encode()

