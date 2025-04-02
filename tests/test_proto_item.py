import pytest

import proto_parsers.proto_item as pi
import proto_parsers.integer as ppi
import proto_parsers.field_and_wire_type as pfw

def test_convert_integer_to_uint32():
    read, t = ppi.decode(b'\xff\x01')
    fw = pfw.FieldAndWireType(1,0)
    item = pi.Item(fw, t)