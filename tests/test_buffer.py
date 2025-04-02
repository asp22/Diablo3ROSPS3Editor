import pytest

import proto_parsers.buffer as ppb

def test_encode():
    a = b'hello'
    assert len(a) == 5
    res = ppb.encode(a)
    assert a == res

def test_decode():
    a = b'hello'
    read, t = ppb.decode(a)
    assert read == 5
    assert t.payload == a
    assert t.size == 5

def test_block_try_to_init_with_int():
    with pytest.raises(TypeError):
        t = ppb.Buffer(1)

def test_as_string_not_string():
    t = ppb.Buffer(b'\x10')
    t.string == None

def test_as_string():
    t = ppb.Buffer(str.encode('hello'))
    t.string == 'hello'
    str(t)
