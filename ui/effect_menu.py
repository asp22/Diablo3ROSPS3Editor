import copy
import curses
from misc.parse_affixes import AFFIXES
from ui.ui_state import UiState

class EffectMenuUi:
    @classmethod
    def init(cls):
        cls.pos_to_id = {}
        cls.id_to_pos = {}
        cls.effects = copy.deepcopy(AFFIXES.get_all())

        def sort(e):
            return f'{e.effect}{e.effectiveness}{e.signed_int}'
        cls.effects.sort(key=sort)

        for pos, e in enumerate(cls.effects):
            id_ = e.signed_int
            cls.pos_to_id[pos] = id_
            cls.id_to_pos[id_] = pos


        

    def __init__(self, stdscr, id, setter, deleter):
        self.stdscr = stdscr
        self.setter = setter
        self.deleter = deleter
        self.menu_current_idx = 0 if id == None else self.id_to_pos[id]+1
        self.max_menu_current_idx = len(self.effects)

        self.pad_height = self.max_menu_current_idx + 1
        self.pad_width = 200
        self.pad = curses.newpad(self.pad_height, self.pad_width)
        self.last_page = None

    def ui(self):
        self.stdscr.clear()

        def update_ui_state():
            if self.menu_current_idx == 0:
                self.deleter()
                UiState.saveable = True
            else:
                list_pos = self.menu_current_idx - 1
                id_ = self.pos_to_id[list_pos]
                self.setter(id_)
                UiState.saveable = True

        def draw_menu(select_idx):
            self.pad.addstr(0, 0, f'[Remove]', curses.A_REVERSE if select_idx == 0 else curses.A_NORMAL)
            for i, e in enumerate(self.effects):
                self.pad.addstr(i+1, 0, f'[{e.effect:<30}] : [{e.effectiveness}] [{e.signed_int}]', curses.A_REVERSE if select_idx == i+1 else curses.A_NORMAL)

            menu_page_format(select_idx)

        def menu_page_format(select_idx):
            h = min(self.pad_height, UiState.height) - 1
            w = min(self.pad_width,  UiState.width) - 1

            n_page = select_idx // UiState.height

            if n_page != self.last_page:
                self.stdscr.clear()
                self.stdscr.refresh()
                self.last_page = n_page
                
            self.pad.refresh(n_page * UiState.height,0, 0,0, h, w)

        while True:
            UiState.update_width_hight(self.stdscr)
            self.stdscr.refresh()
            draw_menu(self.menu_current_idx)

            c = self.stdscr.getch()
            if c == ord('q') or c == curses.KEY_LEFT:
                break
            elif c == curses.KEY_DOWN and self.menu_current_idx < self.max_menu_current_idx:
                self.menu_current_idx += 1
            elif c == curses.KEY_UP and self.menu_current_idx > 0:
                self.menu_current_idx -= 1
            elif c == curses.KEY_NPAGE:
                self.menu_current_idx += UiState.height
                self.menu_current_idx = min(self.menu_current_idx, self.max_menu_current_idx)
            elif c == curses.KEY_PPAGE:
                self.menu_current_idx -= UiState.height
                self.menu_current_idx = max(self.menu_current_idx, 0)
            elif c == curses.KEY_HOME:
                self.menu_current_idx = 0
            elif c == curses.KEY_END:
                self.menu_current_idx = self.max_menu_current_idx
            elif c in [curses.KEY_ENTER, 10, 13, 0x1cb]:
                update_ui_state()
                break

        return True

    
