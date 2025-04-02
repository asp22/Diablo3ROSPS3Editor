import curses
from ui.ui_state import UiState
from ui.account_normal_hardcore_menu import AccountNormalHardcoreMenuUi
from ui.hero_menu import HeroMenuUi

class MainMenuUi:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.menu_current_idx = 0
        self.max_menu_current_idx = len(UiState.hero_sd_views) + 1

        self.pad_height = self.max_menu_current_idx + 1
        self.pad_width = 200
        self.pad = curses.newpad(self.pad_height, self.pad_width)

    def ui(self):

        self.stdscr.clear()

        def draw_menu(select_idx):
            account_hi = curses.A_REVERSE if select_idx == 0 else curses.A_NORMAL 
            self.pad.addstr(0, 0, f'Account', account_hi)

            for i , hero_view in enumerate(UiState.hero_sd_views):
                if i+1 == select_idx:
                    self.pad.addstr(i+1, 0, f'{hero_view.get_name()}', curses.A_REVERSE)
                else:
                    self.pad.addstr(i+1, 0, f'{hero_view.get_name()}', curses.A_NORMAL)

            self.pad.addstr(i+2, 0, f'Saveable: {UiState.saveable}', curses.A_REVERSE if select_idx == i+2 else curses.A_NORMAL)
            self.pad.clrtoeol()

            menu_page_format(select_idx)

        def menu_page_format(select_idx):
            h = min(self.pad_height, UiState.height) - 1
            w = min(self.pad_width,  UiState.width) - 1

            n_page = select_idx // UiState.height

            self.stdscr.clear()
            self.stdscr.refresh()
            self.pad.refresh(n_page * UiState.height,0, 0,0, h, w)

        def update_ui_state():
            if self.menu_current_idx == 0:
                UiState.ui_stack.append(AccountNormalHardcoreMenuUi(self.stdscr))
            elif self.menu_current_idx == self.max_menu_current_idx:
                if UiState.saveable:
                    UiState.save()
            else:
                UiState.ui_stack.append(HeroMenuUi(self.stdscr, UiState.hero_sd_views[self.menu_current_idx - 1]))

        while True:
            UiState.update_width_hight(self.stdscr)
            self.stdscr.refresh()
            draw_menu(self.menu_current_idx)

            c = self.stdscr.getch()
            if c == ord('q'):
                break
            elif c == curses.KEY_DOWN and self.menu_current_idx < self.max_menu_current_idx:
                self.menu_current_idx += 1
            elif c == curses.KEY_UP and self.menu_current_idx > 0:
                self.menu_current_idx -= 1
            elif c in [curses.KEY_RIGHT, curses.KEY_ENTER, 10, 13, 0x1cb]:
                update_ui_state()
                return False
            #else:
            #    self.stdscr.addstr(21, 0, "Key pressed: {}            ".format(hex(c)))

        return True
