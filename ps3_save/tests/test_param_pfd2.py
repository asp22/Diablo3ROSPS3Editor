import pytest
import ps3_save.param_pfd2 as pfd
from pathlib import Path
import tempfile
import shutil

import misc.encryption as d3c
import proto_parsers.proto_message as pm
import py_proto.account as account
import py_proto_view.account_view as account_view

def test_load_param_pfd():
    this_file = Path(__file__)
    param_pfd_file = this_file.parent / 'data' / 'save' / 'PARAM.PFD'
    account_file = param_pfd_file.parent / 'ACCOUNT.DAT'
    assert param_pfd_file.exists()
    assert account_file.exists()

    with open(param_pfd_file, 'rb') as f:
        data = f.read()

    pfd_param = pfd.PFDParam(data)

    assert pfd_param.header_key.hex() == "3dd3794a0a33f23ab6aebe40d4bb55db"
    assert pfd_param.decrypted_signature_key.hex() == "442b1a5b83b83442ccf9fdfed6ea50091e26f0dc"
    assert pfd_param.pfd_count == 14
    assert pfd_param.calc_decrypted_bottom_hash() == pfd_param.bottom_hash
    assert pfd_param.calc_decrypted_top_hash() == pfd_param.top_hash

    assert pfd_param.calc_protected_file_hash(account_file).hex() == "4daeca61ed251c1294566ad2e39dbafa4fbf5f86"
    assert pfd_param.calc_protected_file_hash(account_file) == pfd_param.get_current_protected_file_hash(account_file)
    assert pfd_param.calc_protected_file_bottom_hash(account_file)[0].hex() == "796cd9774ec865e931104f61640db27ae5f61e71"

    with open(account_file, 'rb') as f:
        account_file_bytes = f.read()

    decrypted_account, pfd_entry_file_size = pfd_param.decrypt_protected_file(account_file)
    encrypted_account = pfd_param.encrypt_protected_file(account_file, decrypted_account)
    assert encrypted_account == account_file_bytes

def test_load_param_pfd_prefs():
    this_file = Path(__file__)
    param_pfd_file = this_file.parent / 'data' / 'save' / 'PARAM.PFD'
    prefs_file = param_pfd_file.parent / 'PREFS.DAT'
    assert param_pfd_file.exists()
    assert prefs_file.exists()

    with open(param_pfd_file, 'rb') as f:
        data = f.read()

    pfd_param = pfd.PFDParam(data)

    with open(prefs_file, 'rb') as f:
        file_bytes = f.read()

    decrypted_prefs, pfd_entry_file_size = pfd_param.decrypt_protected_file(prefs_file)
    encrypted_prefs = pfd_param.encrypt_protected_file(prefs_file, decrypted_prefs)
    assert encrypted_prefs == file_bytes

def test_verify_param_pfd():
    this_file = Path(__file__)
    param_pfd_file = this_file.parent / 'data' / 'save' / 'PARAM.PFD'
    assert param_pfd_file.exists()

    with open(param_pfd_file, 'rb') as f:
        data = f.read()

    pfd_param = pfd.PFDParam(data)
    pfd_param.verify(param_pfd_file.parent)

def test_param_pfd_serialize():
    this_file = Path(__file__)
    param_pfd_file = this_file.parent / 'data' / 'save' / 'PARAM.PFD'
    assert param_pfd_file.exists()

    with open(param_pfd_file, 'rb') as f:
        data = f.read()

    pfd_param = pfd.PFDParam(data)
    out = pfd_param.serialize()
    assert out == data

def test_save_updated_account():
    this_file = Path(__file__)
    save_dir = this_file.parent / 'data' / 'save'

    with tempfile.TemporaryDirectory() as temp_dir:
        for i in save_dir.iterdir():
            dst = Path(temp_dir) / i.name
            shutil.copy(i, dst)

        param_pfd_file = Path(temp_dir) / 'PARAM.PFD'
        account_file = param_pfd_file.parent / 'ACCOUNT.DAT'

        with open(param_pfd_file, 'rb') as f:
            data = f.read()

        pfd_param = pfd.PFDParam(data)
        decrypted_account, pfd_entry_file_size = pfd_param.decrypt_protected_file(account_file)
        # use proto tools to read in account and update some values
        d3_encrypted_account = d3c.decrypt(decrypted_account[0:pfd_entry_file_size])
        read, msg = pm.decode(d3_encrypted_account)
        assert read == 32659

        sd = account.SavedDefinition(msg, account_file)
        view = account_view.SavedDefinitionView(sd)
        view.get_normal_partition().lazy_set_gold(123)

        d3_encrypted_account = account.saved_definition_to_encrypted_bytes(sd)
        pfd_param.update_protected_file(account_file, d3_encrypted_account)

        pfd_serialized = pfd_param.serialize()

        # save file and attempt a reload
        with open(param_pfd_file, 'wb') as f:
            f.write(pfd_serialized)

        # reopen and attempt to read
        with open(param_pfd_file, 'rb') as f:
            data = f.read()

        pfd_param = pfd.PFDParam(data)
        pfd_param.verify(param_pfd_file.parent)
