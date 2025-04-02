from sys import getsizeof

BYTE_MAX_VALUE = 255
XOR_KEY = 0x305F92D82EC9A01B

def _truncate(num: int, boundary: int, signed: bool, endian: str = "little") -> int:
    return int.from_bytes(num.to_bytes(getsizeof(num), endian, signed=signed)[:boundary], endian, signed=signed)

def decrypt(data):
    global XOR_KEY

    if isinstance(data, bytes):
        data = bytearray(data)

    num = XOR_KEY
    for i in range(len(data)):
        data[i] ^= (num & BYTE_MAX_VALUE)
        num = _truncate((((num ^ data[i]) << 56) | num >> 8), 8, False)

    return bytes(data)

def encrypt(data):
    global XOR_KEY

    if isinstance(data, bytes):
        data = bytearray(data)

    num1 = XOR_KEY
    for i in range(len(data)):
        num2 = data[i]
        data[i] ^= (num1 & BYTE_MAX_VALUE)
        num1 = _truncate(((num1 ^ num2) << 56) | num1 >> 8, 8, False)

    return bytes(data)
