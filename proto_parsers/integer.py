import proto_parsers.gobble as g

class Integer:
    def __init__(self, unsigned):
        self.unsigned = unsigned

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, i):
        self._item = i

    @property
    def unsigned(self):
        return self._unsigned

    @unsigned.setter
    def unsigned(self, val):
        if isinstance(val, int) == False:
            raise TypeError(f'argument type must be int')
        if val < 0:
            raise ValueError(f'argument must be >= 0')
        self._unsigned = val

    def _get_signed(self, n_bits):
        # check if high bit is set
        is_set = self.unsigned & (1 << (n_bits-1))
        if is_set == False:
            return self.unsigned
        return self.unsigned - (1 << n_bits)

    def _set_signed(self, val, n_bits):
        if val >= 0:
            self.unsigned = val
        else:
            self.unsigned = (1 << n_bits) + val
        self.unsigned = self.unsigned & ((1 << n_bits) - 1)

    def encode(self):
        return encode_type(self)

    def __repr__(self):
        return f'Integer: u:{self.unsigned} [{hex(self.unsigned)}]'


def encode(unsigned):        
	out = g.ungobble_int(unsigned)
	return out

def encode_type(t):
    return encode(t.unsigned)

def decode(payload):
	unsigned, read = g.gobble(payload)
	return read, Integer(unsigned)

