from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import hmac
import hashlib
import struct

def calculate_hash_table_entry_index(name, capacity):
    length = len(name)
    num = 0
    for i in range(length):
        num = (num << 5) - num + ord(name[i])
    return num % capacity

class HMACSHA1:
    def __init__(self, key):
        self.key = key

    def compute_hash(self, data):
        return hmac.new(self.key, data, hashlib.sha1).digest()

def game_secure_file_id():
    return bytes.fromhex("CAEFAEB92722A7CB535D528722FA68DD")

def decrypt_with_portability(iv, data, data_size):
    # Ensure the IV is 16 bytes long
    if len(iv) < 16:
        iv = iv.ljust(16, b'\0')  # Pad with zeros if necessary
    elif len(iv) > 16:
        iv = iv[:16] 

    # syscon_manager_key
    static_key = bytes.fromhex("D413B89663E1FE9F75143D3BB4565274")
    
    # Create a Cipher object
    cipher = Cipher(algorithms.AES(static_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Decrypt the data
    decrypted_data = decryptor.update(data[:data_size]) + decryptor.finalize()
    
    return decrypted_data

def encrypt_with_portability(iv, data, data_size):
    # Ensure the IV is 16 bytes long
    if len(iv) < 16:
        iv = iv.ljust(16, b'\0')  # Pad with zeros if necessary
    elif len(iv) > 16:
        iv = iv[:16] 

    # syscon_manager_key
    static_key = bytes.fromhex("D413B89663E1FE9F75143D3BB4565274")
    
    # Create a Cipher object
    cipher = Cipher(algorithms.AES(static_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    data = encryptor.update(data[:data_size]) + encryptor.finalize()
    return data

def swap_byte_order(value: int) -> int:
    return struct.unpack("<Q", struct.pack(">Q", value))[0]

def decrypt(key: bytes, input_data: bytes, length: int) -> bytes:
    # Ensure the key is 16 bytes (AES-128)
    key = key[:16]
    
    # Create AES ECB ciphers
    aes_encrypt = Cipher(algorithms.AES(key), modes.ECB()).encryptor()
    aes_decrypt = Cipher(algorithms.AES(key), modes.ECB()).decryptor()
    
    num_blocks = length // 16
    output_data = bytearray(length)

    for i in range(num_blocks):
        block = input_data[i * 16:(i + 1) * 16]
        counter = struct.pack("Q", swap_byte_order(i)) + bytes(8)

        counter = aes_encrypt.update(counter)
        block = aes_decrypt.update(block)

        block = bytearray(block)
        for j in range(0, 16):
            block[j] ^= counter[j]

        output_data[i*16:(i+1)*16] = block
    
    return bytes(output_data)

def encrypt(key: bytes, input_data: bytes, length: int) -> bytes:
    # Ensure the key is 16 bytes (AES-128)
    key = key[:16]
    
    # Create AES ECB ciphers
    aes_encrypt = Cipher(algorithms.AES(key), modes.ECB()).encryptor()
    aes_decrypt = Cipher(algorithms.AES(key), modes.ECB()).decryptor()
    
    num_blocks = length // 16
    output_data = bytearray(length)

    for i in range(num_blocks):
        block = input_data[i * 16:(i + 1) * 16]
        counter = struct.pack("Q", swap_byte_order(i)) + bytes(8)

        counter = aes_encrypt.update(counter)
        

        block = bytearray(block)
        for j in range(0, 16):
            block[j] ^= counter[j]
        block = aes_encrypt.update(block)

        output_data[i*16:(i+1)*16] = block
    
    return bytes(output_data)

def generate_hash_key_for_secure_file_id(secureid):
    if len(secureid) != 16:
        raise Exception("SecureFileID must be 16 bytes in length")
    
    array = bytearray(20)
    array[0:16] = secureid[0:16]
    
    num = 0
    for i in range(len(array)):
        if i == 1:
            array[i] = 11
        elif i == 2:
            array[i] = 15
        elif i == 5:
            array[i] = 14
        elif i == 8:
            array[i] = 10
        else:
            array[i] = secureid[num]
            num += 1
    
    return bytes(array)

def get_hmac_sha1(key, data, start, length):
    # Create a new HMAC object using the provided key and SHA1 hash algorithm
    hmac_object = hmac.new(key, digestmod=hashlib.sha1)
    
    # Update the HMAC object with the specified slice of the data
    hmac_object.update(data[start:start + length])
    
    # Return the computed HMAC as a byte array
    return hmac_object.digest()
