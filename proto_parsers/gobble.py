# methods to combine bytes: i.e. use high bit to determine if we should continue or stop

import proto_parsers.exceptions as exp

def gobble(data):
    result = 0
    shift = 0

    read = 0
    found_zero_high_bit = False
    for b in data:
        result |= (b & 0x7f) << shift
        read += 1
        if b & 0x80 == 0:
            found_zero_high_bit = True
            break
        shift += 7

    if not found_zero_high_bit:
        raise exp.InsufficientData("Insufficient data to gobble")
    
    return result, read

def ungobble_int(value):
    encoded = []
    if value == 0:
        return b'\x00'

    while value > 0:
        a = value & 0x7f
        encoded.append(value & 0x7f)
        value >>= 7

    if len(encoded) > 1:
        for i in range(0, len(encoded)-1):
            encoded[i] |= 0x80

    return bytes(encoded)
