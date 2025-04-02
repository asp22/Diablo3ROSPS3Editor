import pytest

import proto_parsers.gobble as g
import proto_parsers.exceptions as exp

def test_gobble_insufficient():
    with pytest.raises(exp.InsufficientData):
        data = b'\xff'
        g.gobble(data)
    
def test_gobble_one_byte():
    data = b'\x7f'
    result, read = g.gobble(data)
    assert result == 127
    assert read == 1

def test_gobble_two_bytes():
    data = b'\xff\x01'
    result, read = g.gobble(data)
    assert result == 255, f'is {result}'
    assert read == 2, f'is {read}'

def test_ungobble_one():
    res = g.ungobble_int(127)
    assert len(res) == 1
    assert res == b'\x7f', f'res: {res}'

def test_ungobble_two():
    res = g.ungobble_int(255)
    assert len(res) == 2
    assert res == b'\xff\x01', f'res: {res}'
