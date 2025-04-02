import curses
from ui.ui_state import UiState
from ui.consumable_menu import ConsumableMenuUi
from ui.non_consumable_menu import NonConsumableMenuUi

class StashUi:
    def __init__ (self, stdscr, game_items_view):
        self.stdscr = stdscr
        self.game_items_view = game_items_view
        self.menu_current_idx = 0
        self.consumable_items = self.game_items_view.get_stash_consumables()
        self.non_consumable_items = self.game_items_view.get_stash_non_consumables()
        self.menu_current_idx = 0
        self.max_menu_current_idx = 1

        self.pad_height = self.max_menu_current_idx + 1
        self.pad_width = 200
        self.pad = curses.newpad(self.pad_height, self.pad_width)

    def ui(self):
        self.stdscr.clear()

        def update_ui_state():
            if self.menu_current_idx == 0 and len(self.consumable_items):
                UiState.ui_stack.append(ConsumableMenuUi(self.stdscr, self.consumable_items))
            elif self.menu_current_idx == 1 and len(self.non_consumable_items):
                UiState.ui_stack.append(NonConsumableMenuUi(self.stdscr, self.non_consumable_items))

        def draw_menu(select_idx):
            self.pad.addstr(0, 0, f'Consumables    : {len(self.consumable_items)}', curses.A_REVERSE if select_idx == 0 else curses.A_NORMAL)
            self.pad.addstr(1, 0, f'Non Consumables: {len(self.non_consumable_items)}', curses.A_REVERSE if select_idx == 1 else curses.A_NORMAL)

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
            draw_menu(self.menu_current_idx)
            self.stdscr.refresh()

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
