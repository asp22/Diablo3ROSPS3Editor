
import struct
import proto_parsers.exceptions as exp

class Fixed64:
    def __init__(self, payload):
        self._payload = payload

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, i):
        self._item = i

    @property
    def unsigned(self):
        return struct.unpack('<Q', self._payload)[0]

    @unsigned.setter
    def unsigned(self, val):
        if isinstance(val, int) == False:
            raise TypeError(f'argument type must be int')
        if val < 0:
            raise ValueError(f'argument must be >= 0')
        self._payload = struct.pack('<Q', val)

    @property
    def signed(self):
        # check if high bit is set
        is_set = self.unsigned & (1 << (64-1))
        if is_set == False:
            return self.unsigned
        return self.unsigned - (1 << 64)

    @signed.setter
    def signed(self, val):
        if val >= 0:
            self.unsigned = val
        else:
            self.unsigned = (1 << 64) + val

        self.unsigned = self.unsigned & ((1 << 64) - 1)

    def encode(self):
        return encode_type(self)

    def __repr__(self):
        return f'Fixed64: u:{self.unsigned} i:{self.signed} [{self._payload.hex()}]'


def encode(payload):
    if isinstance(payload, bytes) == False:
        raise TypeError('encode expects bytes')

    if len(payload) != 8:
        raise exp.InsufficientData('encode expects bytes of len 8')
    return payload

def encode_type(t):
    return encode(t._payload)

def decode(payload):
    if len(payload) < 8:
        raise exp.InsufficientData("Insufficient data to decode Fixed64")
    out = payload[:8]
    return 8, Fixed64(out)
