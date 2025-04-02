# take a parsed proto and use the classes within to view and modify data
from pathlib import Path
import copy
import proto_parsers.proto_message as pm
import proto_parsers.buffer as ppb
import misc.encryption as encrypt

import misc.parse_gbids as gbids
import misc.parse_affixes as affixs

import py_proto.attribute_serializer as attrib
import py_proto.items as Items
from py_proto.base import Base

class Digest(Base):
    @classmethod
    def MAKE_PROPS(self):
        self._make_optional_simple_value('hero_name', 3)
        self._make_required_simple_value('gbid_class', 4)
        self._make_required_simple_value('level', 5)
        self._make_required_simple_value('dep_alt_level', 20)

    def __init__(self, message):
        super().__init__(message)

class SavedData(Base):
    @classmethod
    def MAKE_PROPS(self):
        self._make_repeated_simple_value('boss_kill_flags', 13)
        self._make_repeated_simple_value('gbid_legendary_powers', 18)
    def __init__(self, message):
        super().__init__(message)


class SavedDefinition(Base):
    @classmethod
    def MAKE_PROPS(cls):
        cls._make_required_simple_value('version', 1)
        cls._make_optional_message('digest', 2, Digest)
        cls._make_required_message('saved_attributes', 3, attrib.SavedAttributes)
        cls._make_optional_message('saved_data', 4, SavedData)
        cls._make_optional_message('game_items', 6, Items.ItemList)

    def __init__(self, message, filename):
        super().__init__(message)
        self.filename = filename

SavedDefinition.MAKE_PROPS()
SavedData.MAKE_PROPS()
Digest.MAKE_PROPS()

def get_hero_saved_definition_via_filename(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    decrypted = encrypt.decrypt(data)
    read, msg = pm.decode(decrypted)
    sd = SavedDefinition(msg, filename)

    #out_file = filename.with_suffix('.TXT')
    #with open(out_file, 'wt') as f:
    #    pm.expand_buffer_to_message_recursive(msg)
    #    f.write(str(msg))

    return sd

def get_hero_saved_definitions(in_dir):
    def process_hro_file(filename):
        try:
            return get_hero_saved_definition_via_filename(filename)
        except:
            return None

    out = []
    for i in in_dir.iterdir():
        if i.is_file() and i.suffix == '.HRO':
            res = process_hro_file(i)
            if res is not None:
                out.append(res)
    return out

def saved_definition_to_encrypted_bytes(sd):
    b = sd.message.encode()
    encrypted = encrypt.encrypt(b)
    return encrypted

def saved_definition_to_filename(sd, filename):
    b = saved_definition_to_encrypted_bytes(sd)
    with open(filename, 'wb') as f:
        f.write(b)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="A script to encrypt/decrypt and modify Diablo III saves")
    parser.add_argument("-d", "--in-dir", type=str, required=True, help="The account file you want to work with")
    args = parser.parse_args()

    hero_saved_definitions = get_hero_saved_definitions(Path(args.in_dir))
    print(len(hero_saved_definitions))
