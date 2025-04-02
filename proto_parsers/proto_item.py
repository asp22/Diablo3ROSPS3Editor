
import proto_parsers.gobble as g

class Item:
    def __init__(self, fw, obj):
        self._field_wire = fw
        self._obj = obj
        obj.item = self

    @property
    def fn(self):
        return self._field_wire.field_number

    @property
    def wt(self):
        return self._field_wire.wire_type

    @property
    def obj(self):
        return self._obj

    @obj.setter
    def obj(self, val):
        self._obj = val
        self._obj.item = self

    def encode(self):
        a = self._field_wire.encode()
        b = self._obj.encode()
        if self.wt == 2:
            l = g.ungobble_int(len(b))
        else:
            l = b''

        out = a + l + b
        return out

    def to_derived(self, derived_type):
        self.obj = derived_type.make(self.obj)

    def __repr__(self):
        return f'{self._field_wire} => {self._obj}'
