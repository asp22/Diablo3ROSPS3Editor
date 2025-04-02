import curses
from ui.ui_state import UiState
from ui.integer_menu import IntegerMenuUi
from ui.stash import StashUi

class AccountParitionMenuUi:
    def __init__ (self, stdscr, account_partition):
        self.stdscr = stdscr
        self.partition = account_partition
        self.menu_current_idx = 0
        self.max_menu_current_idx = 3

        self.pad_height = self.max_menu_current_idx + 1
        self.pad_width = 200
        self.pad = curses.newpad(self.pad_height, self.pad_width)

    def ui(self):

        self.stdscr.clear()

        def update_ui_state():
            if self.menu_current_idx == 0:
                # setter function is special. We'll have to reset heros paragon levels and points
                def setter(value):
                    self.partition.lazy_set_paragon_level(value)
                    for h in UiState.hero_sd_views:
                        h.set_paragon_level(value)

                UiState.ui_stack.append(IntegerMenuUi(self.stdscr, 'Paragon Level', self.partition.lazy_get_paragon_level, setter, [0, 10000]))
            elif self.menu_current_idx == 1:
                UiState.ui_stack.append(IntegerMenuUi(self.stdscr, 'Blood Shards', self.partition.lazy_get_blood_shards, self.partition.lazy_set_blood_shards, [0, (1 << 32) -1 ]))
            elif self.menu_current_idx == 2:
                UiState.ui_stack.append(IntegerMenuUi(self.stdscr, 'Gold', self.partition.lazy_get_gold, self.partition.lazy_set_gold, [0, (1 << 32) -1 ]))
            elif self.menu_current_idx == 3:
                UiState.ui_stack.append(StashUi(self.stdscr, self.partition.lazy_get_game_items()))

        def draw_menu(select_idx):
            self.pad.addstr(0, 0, f'Paragon Level: {self.partition.lazy_get_paragon_level()}', curses.A_REVERSE if select_idx == 0 else curses.A_NORMAL)
            self.pad.clrtoeol()
            self.pad.addstr(1, 0, f'Blood Shards : {self.partition.lazy_get_blood_shards()}', curses.A_REVERSE if select_idx == 1 else curses.A_NORMAL)
            self.pad.clrtoeol()
            self.pad.addstr(2, 0, f'Gold         : {self.partition.lazy_get_gold()}', curses.A_REVERSE if select_idx == 2 else curses.A_NORMAL)
            self.pad.clrtoeol()
            self.pad.addstr(3, 0, f'Stash', curses.A_REVERSE if select_idx == 3 else curses.A_NORMAL)

            menu_page_format(select_idx)

        def menu_page_format(select_idx):
            h = min(self.pad_height, UiState.height) - 1
            w = min(self.pad_width,  UiState.width) - 1

            n_page = select_idx // UiState.height

            self.stdscr.clear()
            self.stdscr.refresh()
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
            elif c in [curses.KEY_RIGHT, curses.KEY_ENTER, 10, 13, 0x1cb]:
                update_ui_state()
                return False;

        return True
