import curses

import py_proto.account
import py_proto.hero
from py_proto_view.account_view import SavedDefinitionView as AccountSD
from py_proto_view.hero_view import SavedDefinitionView as HeroSD
from misc.parse_affixes import AFFIXES
from misc.parse_gbids import GBIDS
from ps3_save.param_pfd2 import PFDParam
import misc.encryption as d3c
import proto_parsers.proto_message as pm

import argparse
from pathlib import Path

from ui.ui_state import UiState
from ui.main_menu import MainMenuUi
from ui.effect_menu import EffectMenuUi

def make_parser():
    parser = argparse.ArgumentParser(description="A script to encrypt/decrypt and modify Diablo III saves")
    parser.add_argument("-d", "--in-dir", type=str, required=True, help="The account file you want to work with")
    parser.add_argument("-g", "--gbids-file", type=str, required=False, help="The account file you want to work with", default=Path("./assets/gbids.json"))
    parser.add_argument("-a", "--affixes-file", type=str, required=False, help="The account file you want to work with", default=Path("./assets/affixes.json"))
    return parser

def load_param_pfd(in_dir):
    param_pfd_file = in_dir / 'PARAM.PFD'
    with open(param_pfd_file, 'rb') as f:
        data = f.read()
    param_pfd = PFDParam(data)
    param_pfd.verify(in_dir)
    return param_pfd

def load_account(in_dir, param_pfd):
    account_file = in_dir / 'ACCOUNT.DAT'

    ps3_decrypted, pfd_entry_file_size = param_pfd.decrypt_protected_file(account_file)
    d3_decrypted = d3c.decrypt( ps3_decrypted[0:pfd_entry_file_size] )
    read, msg = pm.decode(d3_decrypted)
    return py_proto.account.SavedDefinition(msg, account_file)

def load_heros(in_dir, param_pfd):
    hero_files = param_pfd.get_hero_filenames()
    out = []
    for h in hero_files:
        filename = in_dir / h
        ps3_decrypted, pfd_entry_file_size = param_pfd.decrypt_protected_file(filename)
        d3_decrypted = d3c.decrypt( ps3_decrypted[0:pfd_entry_file_size] )
        try:
            read, msg = pm.decode(d3_decrypted)
            out.append(py_proto.hero.SavedDefinition(msg, filename))
        except:
            print(f'failed to load hero: {h}. continuing...')
            continue

    return out

def load_assets(gbids_filename, affixes_filename):
    GBIDS.read_in_json(gbids_filename)
    AFFIXES.read_in_json(affixes_filename)

def make_ui():

    def ui(stdscr):
        stdscr.clear()
        stdscr.refresh()
        UiState.ui_stack.append(MainMenuUi(stdscr))

        while len(UiState.ui_stack):
            res = UiState.ui_stack[-1].ui()
            if res:
                UiState.ui_stack.pop()

    return ui

class SaveReseter:
    def __init__(self, in_dir):
        self._in_dir = in_dir
        self._data = {}
        self._load_files_into_memory()

    def _load_files_into_memory(self):
        for child in self._in_dir.iterdir():
            if child.is_file():
                with open(child, 'rb') as f:
                    self._data[child.name] = f.read()

    def reset_files(self):
        print('restoring files....')
        for name, data in self._data.items():
            with open(self._in_dir / name, 'wb') as f:
                f.write(data)
            print(f'{name} restored')


def main():
    parser = make_parser()
    args = parser.parse_args()
    in_dir = Path(args.in_dir)
    gbids = Path(args.gbids_file)
    affixes = Path(args.affixes_file)

    load_assets(gbids, affixes)
    param_pfd = load_param_pfd(in_dir)
    account_sd = load_account(in_dir, param_pfd)
    hero_sds = load_heros(in_dir, param_pfd)
    save_reseter = SaveReseter(in_dir)

    EffectMenuUi.init()

    UiState.in_dir = in_dir
    UiState.param_pfd = param_pfd
    UiState.account_sd_view = AccountSD(account_sd)
    UiState.hero_sd_views = [HeroSD(s) for s in hero_sds]

    ui = make_ui()

    try:
        curses.wrapper(ui)
    except:
        print('exception caught')
        save_reseter.reset_files()

if __name__ == "__main__":
    main()
