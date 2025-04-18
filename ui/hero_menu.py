import curses
from ui.ui_state import UiState
from ui.hero_inventory import HeroInventoryUi
from ui.integer_menu import IntegerMenuUi

class HeroMenuUi:
    def __init__(self, stdscr, hero_sd_view):
        self.hero_sd_view = hero_sd_view
        self.stdscr = stdscr
        self.menu_current_idx = 0
        self.max_menu_current_idx = 1

        self.pad_height = self.max_menu_current_idx + 1 + 1
        self.pad_width = 200
        self.pad = curses.newpad(self.pad_height, self.pad_width)

    def ui(self):

        self.stdscr.clear()

        def update_ui_state():
            if self.menu_current_idx == 0:
                UiState.ui_stack.append(IntegerMenuUi(self.stdscr, 'Level', self.hero_sd_view.get_level, self.hero_sd_view.set_level, [1, 70]))
            else:
                if self.hero_sd_view.get_game_items_count() > 0:
                    UiState.ui_stack.append(HeroInventoryUi(self.stdscr, self.hero_sd_view, self.hero_sd_view.get_game_items()))

        def draw_menu(select_idx):
            self.pad.addstr(0, 0, f'{self.hero_sd_view.get_name()}')
            self.pad.addstr(1, 0, f'Level    :{self.hero_sd_view.get_level()}', curses.A_REVERSE if select_idx == 0 else curses.A_NORMAL)
            self.pad.addstr(2, 0, f'Inventory:{self.hero_sd_view.get_game_items_count()}', curses.A_REVERSE if select_idx == 1 else curses.A_NORMAL)

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
