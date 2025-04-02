from re import I
import struct
import ps3_save.crypt as ps3c

def aligned_16(size):
    return (size + 16 - 1) & -16

def align_data(data):
    l = aligned_16(len(data))
    data += bytes(16)
    return data[0:l]

class Reader:
    def __init__(self, data):
        self._data = data
        self._pos = 0

    def read(self, count):
        s = self._pos
        e = s + count
        out = self._data[s:e]
        self._pos += count
        return out

    def rem(self):
        return len(self._data) - self._pos

class PFDEntry:
    def __init__(self, data):
        self._data = data
        self._parse()

    def _parse(self):
        r = Reader(self._data)
        self._additional_index = struct.unpack('>Q', r.read(8))[0]
        self._filename = r.read(65).decode('ascii').replace('\0','')
        self._padding_0 = r.read(7)
        self._key = r.read(64)
        self._hashes = []
        for i in range(0, 4):
            self._hashes.append(r.read(20))
        self._padding_1 = r.read(40)
        self._decrypted_file_size = struct.unpack('>Q', r.read(8))[0]

    def serialize(self):
        out = bytearray()
        out += struct.pack('>Q', self._additional_index)
        b = bytearray()
        b.extend(map(ord, self._filename))
        b += bytearray(65)
        out += b[0:65]
        out += self._padding_0
        out += self._key
        for h in self._hashes:
            out += h
        out += self._padding_1
        out += struct.pack('>Q', self._decrypted_file_size)
        return out


class PFDParam:

    def __init__(self, data):
        self._data = data
        self._parse()

    def _parse(self):
        r = Reader(self._data)
        self._magic = struct.unpack('>Q', r.read(8))[0]
        assert self._magic == 1346782274;

        self._version = struct.unpack('>Q', r.read(8))[0]
        assert self._version in [3,4]

        self._header_key = r.read(16)

        self._encrypted_header_hashes = r.read(64)

        self._decrypted_header_hashes = ps3c.decrypt_with_portability(self._header_key, self._encrypted_header_hashes, 64)
        self._decrypted_header_hashes = bytearray(self._decrypted_header_hashes)

        self._decrypted_signature_key = self._make_decrypted_signature_key()

        self._n_file_indicies = struct.unpack('>Q', r.read(8))[0]
        self._n_total_protected_files = struct.unpack('>Q', r.read(8))[0]
        self._n_used_protected_files = struct.unpack('>Q', r.read(8))[0]

        self._file_indicies = []
        for i in range(0, self._n_file_indicies):
            self._file_indicies.append(struct.unpack('>Q', r.read(8))[0])

        self._pfd_entries = []
        for i in range(0, self._n_used_protected_files):
            self._pfd_entries.append(PFDEntry(r.read(272)))

        # skip unused
        r.read(272 * (self._n_total_protected_files - self._n_used_protected_files))

        self._bottom_hashes = []
        for i in range(0, self._n_file_indicies):
            self._bottom_hashes.append(r.read(20))

        r.read(44)
        assert r.rem() == 0, f"r.rem() is {r.rem()}"

    def serialize(self):
        out = bytearray()

        out += struct.pack('>Q', self._magic)
        out += struct.pack('>Q', self._version)
        out += self._header_key
        
        self._encrypted_header_hashes = ps3c.encrypt_with_portability(self._header_key, self._decrypted_header_hashes, 64)
        out += self._encrypted_header_hashes
        
        out += struct.pack('>QQQ', self._n_file_indicies, self._n_total_protected_files, self._n_used_protected_files)
        for i in self._file_indicies:
            out += struct.pack('>Q', i)

        for e in self._pfd_entries:
            out += e.serialize()

        # skip unused
        out += bytearray(272 * (self._n_total_protected_files - self._n_used_protected_files))
        for bh in self._bottom_hashes:
            out += bh

        out += bytearray(44)
        return out

    @property
    def magic(self):
        return self._magic

    @property
    def version(self):
        return self._version

    @property
    def header_key(self):
        return self._header_key

    @property
    def bottom_hash(self):
        return self._decrypted_header_hashes[0:20]

    @bottom_hash.setter
    def bottom_hash(self, v):
        self._decrypted_header_hashes[0:20] = v

    @property
    def top_hash(self):
        return self._decrypted_header_hashes[20:40]

    @property
    def encrypted_signature_key(self):
        return self._decrypted_header_hashes[40:60]

    @property
    def decrypted_signature_key(self):
        return self._decrypted_signature_key

    @property
    def pfd_count(self):
        return len(self._pfd_entries)

    def _make_decrypted_signature_key(self):
        if self.version == 3:
            return self.encrypted_signature_key
        else:
            #"keygen_key"
            key = bytes.fromhex("6B1ACEA246B745FD8F93763B920594CD53483B82")
            return ps3c.get_hmac_sha1(key, self.encrypted_signature_key, 0, 20)

    def calc_decrypted_bottom_hash(self):
        d = bytearray()
        for i in self._bottom_hashes:
            d += i
        return ps3c.HMACSHA1(self.decrypted_signature_key).compute_hash(d)

    def calc_decrypted_top_hash(self):
        c = struct.pack('>QQQ', self._n_file_indicies, self._n_total_protected_files, self._n_used_protected_files)
        for i in self._file_indicies:
            c += struct.pack('>Q', i)

        assert len(c) == 0x1e0
        return ps3c.HMACSHA1(self.decrypted_signature_key).compute_hash(c)

    def get_hero_filenames(self):
        out = []
        for e in self._pfd_entries:
            if e._filename.endswith('.HRO'):
                out.append(e._filename)
        return out

    def _find_protected_entry(self, name):
        for e in self._pfd_entries:
            if e._filename == name:
                return e
        return None

    def get_current_protected_file_hash(self, filename):
        name = filename.name
        pfd_entry = self._find_protected_entry(name)
        assert pfd_entry != None
        return pfd_entry._hashes[0]

    def calc_protected_file_hash(self, filename):
        # input file should be encrypted
        with open(filename, 'rb') as f:
            file_data = f.read()

        return self.calc_protected_file_hash_via_bytes(file_data)

    def calc_protected_file_hash_via_bytes(self, file_data):
        secure_file_hash = ps3c.generate_hash_key_for_secure_file_id(ps3c.game_secure_file_id())
        hs = ps3c.HMACSHA1(secure_file_hash)
        return hs.compute_hash(file_data)

    def calc_protected_file_bottom_hash(self, filename):
        name = filename.name
        num = ps3c.calculate_hash_table_entry_index(name, 0x39)
        num2 = self._file_indicies[num]

        hmac_sha = ps3c.HMACSHA1(self._decrypted_signature_key)
        data = bytearray()

        pfd_entry = self._find_protected_entry(name)
        while num2 < self._n_total_protected_files:
            entry = self._pfd_entries[num2]
            o = bytearray(272 - 8 - 7)
            x = entry._filename.encode()
            x += bytes(65)
            o[0:65] = x[0:65]
            o[65:129] = entry._key
            o[129:149] = entry._hashes[0]
            o[149:169] = entry._hashes[1]
            o[169:189] = entry._hashes[2]
            o[189:209] = entry._hashes[3]
            o[209:249] = bytes(40)
            o[249:257] = struct.pack('>Q', entry._decrypted_file_size)
            data += o
            num2 = entry._additional_index
        
        hash_value = hmac_sha.compute_hash(data)
        return hash_value, num

    def decrypt_protected_file(self, filename):
        name = filename.name

        pfd_entry = self._find_protected_entry(name)
        assert pfd_entry != None

        with open(filename, 'rb') as f:
            file_data = f.read()

        file_data = align_data(file_data)
        secure_file_hash = ps3c.generate_hash_key_for_secure_file_id(ps3c.game_secure_file_id())
        decrypt_hash_key = ps3c.decrypt_with_portability(secure_file_hash, pfd_entry._key, len(pfd_entry._key))
        decrypted_data = ps3c.decrypt(decrypt_hash_key, file_data, len(file_data))

        return decrypted_data, pfd_entry._decrypted_file_size

    def encrypt_protected_file(self, filename, data):
        name = filename.name
        out = align_data(data)

        pfd_entry = self._find_protected_entry(name)
        assert pfd_entry != None

        secure_file_hash = ps3c.generate_hash_key_for_secure_file_id(ps3c.game_secure_file_id())
        encrypt_hash_key = ps3c.decrypt_with_portability(secure_file_hash, pfd_entry._key, len(pfd_entry._key))

        encrypted_data = ps3c.encrypt(encrypt_hash_key, out, len(out))
        return encrypted_data

    def update_protected_file(self, filename, ps3_decrypted):
        name = filename.name
        pfd_entry = self._find_protected_entry(name)
        pfd_entry._decrypted_file_size = len(ps3_decrypted)

        ps3_encrypted = self.encrypt_protected_file(filename, ps3_decrypted)
        hash_ = self.calc_protected_file_hash_via_bytes(ps3_encrypted)
        pfd_entry._hashes[0] = hash_

        bottom_hash, pos = self.calc_protected_file_bottom_hash(filename)
        self._bottom_hashes[pos] = bottom_hash

        # calculate new bottom hash, and update
        decrypted_bottom_hash = self.calc_decrypted_bottom_hash()
        self.bottom_hash = decrypted_bottom_hash

        # finally write encrypted file to disk
        with open(filename, 'wb') as f:
            f.write(ps3_encrypted)

    def verify(self, dir_to_files):
        # start with top hash
        # this shouldn't change as we aren't adding any new files
        decrypted_top_hash = self.calc_decrypted_top_hash()
        assert decrypted_top_hash == self.top_hash

        # file hashes
        for pfd_entry in self._pfd_entries:
            if pfd_entry._filename == 'PARAM.SFO':
                continue
            filename = dir_to_files / pfd_entry._filename
            hash_ = self.calc_protected_file_hash(filename)
            assert pfd_entry._hashes[0] == hash_, f'failed hash check on {pfd_entry._filename}'

        # now the bottom hash
        decrypted_bottom_hash = self.calc_decrypted_bottom_hash()
        assert decrypted_bottom_hash == self.bottom_hash

        



