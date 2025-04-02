
import struct
import proto_parsers.exceptions as exp

class Fixed32:
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
        return struct.unpack('<I', self._payload)[0]

    @unsigned.setter
    def unsigned(self, val):
        if isinstance(val, int) == False:
            raise TypeError(f'argument type must be int')
        if val < 0:
            raise ValueError(f'argument must be >= 0')
        self._payload = struct.pack('<I', val)

    @property
    def signed(self):
        # check if high bit is set
        is_set = self.unsigned & (1 << (32-1))
        if is_set == False:
            return self.unsigned
        return self.unsigned - (1 << 32)

    @signed.setter
    def signed(self, val):
        if val >= 0:
            self.unsigned = val
        else:
            self.unsigned = (1 << 32) + val

        self.unsigned = self.unsigned & ((1 << 32) - 1)

    def encode(self):
        return encode_type(self)

    def __repr__(self):
        return f'Fixed32: u:{self.unsigned} i:{self.signed} [{self._payload.hex()}]'


def encode(payload):
    if isinstance(payload, bytes) == False:
        raise TypeError('encode expects bytes')

    if len(payload) != 4:
        raise exp.InsufficientData('encode expects bytes of len 4')
    return payload

def encode_type(t):
    return encode(t._payload)

def decode(payload):
    if len(payload) < 4:
        raise exp.InsufficientData("Insufficient data to decode Fixed32")
    out = payload[:4]
    return 4, Fixed32(out)
