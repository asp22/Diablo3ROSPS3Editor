
class Buffer:
    def __init__(self, payload):
        self.payload = payload

    @property
    def size(self):
        return len(self._payload)

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, val):
        if isinstance(val, bytes) == False:
            raise TypeError('buffer type expects byters')
        self._payload = val

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, i):
        self._item = i

    @property
    def string(self):
        out = self.payload.decode('ascii')
        return out

    @string.setter
    def string(self, value):
        self.payload = value.encode()

    def encode(self):
        return self.payload

    def __repr__(self):
        return f'Buffer: size: {self.size}, [{self.payload.hex()}]'

def encode(payload):
    return payload

def encode_type(t):
    return encode(t._payload)

def decode(payload):
    return len(payload), Buffer(payload)

