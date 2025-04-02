import proto_parsers.gobble as g
import proto_parsers.exceptions as exp

class FieldAndWireType:
    def __init__(self, field_number, wire_type):
        self.field_number = field_number
        self.wire_type = wire_type

    @property
    def field_number(self):
        return self._field_number

    @field_number.setter
    def field_number(self, val):
        if isinstance(val, int) == False:
            raise TypeError(f'argument type must be int')
        if val <= 0:
            raise ValueError(f'argument must be > 0')
        self._field_number = val

    @property
    def wire_type(self):
        return self._wire_type

    @wire_type.setter
    def wire_type(self, val):
        if isinstance(val, int) == False:
            raise TypeError(f'argument type must be int')
        if val < 0:
            raise ValueError(f'argument must be >= 0')
        if val > 5:
            raise exp.UnsupportedWireType(f"wire type greater than 5 isn't supported")
        self._wire_type = val

    def __repr__(self):
        return f'fn:{self.field_number} wt:{self.wire_type}'

    def encode(self):
        return encode_type(self)

def encode(field_number, wire_type):
    out = b''
    value = field_number << 3 | wire_type
    out += g.ungobble_int(value)
    return out

def encode_type(t):
    return encode(t.field_number, t.wire_type)

def decode(payload):
    result, read = g.gobble(payload)

    wire_type = result & 0x07
    field_number = result >> 3

    if wire_type > 5:
        raise exp.UnsupportedWireType(f"wire type {wire_type} is not supported")

    if field_number == 0:
        raise exp.ZeroFieldNumber("Field number cannot be zero")

    return read, FieldAndWireType(field_number, wire_type)

