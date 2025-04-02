import pytest

import proto_parsers.field_and_wire_type as fwt
import proto_parsers.exceptions as exp

def test_field_wire_encode():
    byte = fwt.encode(19, 0)
    assert byte == b'\x98\x01'

def test_field_wire_decode_unsup_wire():
    with pytest.raises(exp.UnsupportedWireType):
        data = b'\x06'
        read, t = fwt.decode(data)

def test_field_wire_decode_zero_field():
    with pytest.raises(exp.ZeroFieldNumber):
        data = b'\x05'
        read, t = fwt.decode(data)

def test_field_wire_decode_zero_success():
    data = b'\x98\x01'
    read, t = fwt.decode(data)
    assert t.field_number == 19
    assert t.wire_type == 0

def test_set_invalid_field_number_type():
    with pytest.raises(TypeError):
        fwt.FieldAndWireType('hello', 0)

def test_set_invalid_field_number():
    with pytest.raises(ValueError):
        fwt.FieldAndWireType(0, 0)

def test_set_valid_field_number():
    t = fwt.FieldAndWireType(1, 0)
    assert t.field_number == 1

def test_set_invalid_wire_type():
    with pytest.raises(TypeError):
        fwt.FieldAndWireType(1, 'a')

def test_set_invalid_wire_type_value():
    with pytest.raises(exp.UnsupportedWireType):
        fwt.FieldAndWireType(1, 6)

def test_to_string():
    str(fwt.FieldAndWireType(1, 4))

def test_encode_method():
    t = fwt.FieldAndWireType(19, 0)
    byte = t.encode()
    assert byte == b'\x98\x01'
