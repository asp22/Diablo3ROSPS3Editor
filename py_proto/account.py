# take a parsed proto and use the classes within to view and modify data
from pathlib import Path
import copy
import proto_parsers.proto_message as pm
import proto_parsers.integer as ppi
import misc.encryption as encrypt

import misc.parse_gbids as gbids
import misc.parse_affixes as affixs

import py_proto.attribute_serializer as attrib
import py_proto.items as Items
from py_proto.base import Base

class AccountPartition(Base):
    @classmethod
    def MAKE_PROPS(cls):
        pass
        cls._make_required_message('saved_attributes', 2, attrib.SavedAttributes)
        cls._make_optional_message('game_items', 3, Items.ItemList)
        cls._make_optional_simple_value('accepted_license_bits', 7)
        cls._make_optional_simple_value('alt_level', 8)
        cls._make_optional_message('currency_data', 9, Items.CurrencySavedData)

    def __init__(self, message):
        super().__init__(message)

class SavedDefinition(Base):
    @classmethod
    def MAKE_PROPS(cls):
        cls._make_repeated_message('account_partition', 20, AccountPartition)

    def __init__(self, message, filename):
        super().__init__(message)
        self.filename = filename

SavedDefinition.MAKE_PROPS()
AccountPartition.MAKE_PROPS()


def get_saved_definition_via_filename(filename):
    with open(filename, 'rb') as f:
        data = f.read()

    decrypted = encrypt.decrypt(data)
    read, msg = pm.decode(decrypted)
    sd = SavedDefinition(msg, filename)

    return sd

def get_saved_definition_via_dir(in_dir):
    for i in in_dir.iterdir():
        if i.is_file() and i.name == "ACCOUNT.DAT":
            return get_saved_definition_via_filename(i)

    return None

def saved_definition_to_encrypted_bytes(sd):
    b = sd.message.encode()
    encrypted = encrypt.encrypt(b)
    return encrypted

def saved_definition_to_filename(sd, filename):
    b = saved_definition_to_encrypted_bytes(sd)
    with open(filename, 'wb') as f:
        f.write(b)
    return len(b)

def saved_definition_to_dir(sd, out_dir):
    filename = out_dir / 'ACCOUNT.DAT'
    saved_definition_to_filename(sd, filename)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="A script to encrypt/decrypt and modify Diablo III saves")
    parser.add_argument("-d", "--in-dir", type=str, required=True, help="The account file you want to work with")
    args = parser.parse_args()

    sd = get_saved_definition_via_dir(Path(args.in_dir))
    print(sd.message)

    # testing; update account data to have 
