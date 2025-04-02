import curses
import py_proto.account
import py_proto.hero

class UiState:
    ui_state = 'MainMenu'
    in_dir = None
    param_pfd = None
    account_sd_view = None
    hero_sd_views = None

    ui_stack = []
    width = None
    height = None

    saveable = False

    @classmethod
    def save(cls):
        if cls.saveable == True:
            sd = cls.account_sd_view._sd
            account_filename = sd.filename

            # step 1 - update ACCOUNT.DAT 
            d3_encrypted_account = py_proto.account.saved_definition_to_encrypted_bytes(sd)
            cls.param_pfd.update_protected_file(account_filename, d3_encrypted_account)

            # step 2 - update *.HRO
            for h in cls.hero_sd_views:
                sd = h._sd
                filename = sd.filename
                d3_encrypted_hero = py_proto.hero.saved_definition_to_encrypted_bytes(sd)
                cls.param_pfd.update_protected_file(filename, d3_encrypted_hero)

            # save PARAM.PFD
            cls.param_pfd.verify(cls.in_dir)

            pfd_serialized = cls.param_pfd.serialize()
            with open(cls.in_dir / 'PARAM.PFD', 'wb') as f:
                f.write(pfd_serialized)

            cls.saveable = False
                

    @classmethod
    def update_width_hight(cls, stdscr):
        curses.curs_set(0)
        cls.height, cls.width = stdscr.getmaxyx()
