import curses
from ui.ui_state import UiState
from ui.integer_menu import IntegerMenuUi

class ConsumableMenuUi:
    def __init__(self, stdscr, consumable_items):
        self.stdscr = stdscr
        self.consumable_items = consumable_items
        self.menu_current_idx = 0
        self.max_menu_current_idx = len(self.consumable_items) - 1

        self.order_consumable_items()

    def order_consumable_items(self):
        def by_category(a):
            return f'{a.get_category()}{a.get_name()}'
        self.consumable_items.sort(key=by_category)


        self.pad_height = self.max_menu_current_idx + 1
        self.pad_width = 200
        self.pad = curses.newpad(self.pad_height, self.pad_width)
        self.last_page = None

    def ui(self):
        self.stdscr.clear()

        def update_ui_state():
            item = self.consumable_items[self.menu_current_idx]
            UiState.ui_stack.append(IntegerMenuUi(self.stdscr, item.get_name(), item.get_stack_size, item.set_stack_size, [1, 1000]))

        def draw_menu(select_idx):
            for i, item in enumerate(self.consumable_items):
                self.pad.addstr(i, 0, f'{item.get_category():<25} : {item.get_name():<40} : {item.get_stack_size()}', curses.A_REVERSE if select_idx == i else curses.A_NORMAL)

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
            elif c in [curses.KEY_RIGHT, curses.KEY_ENTER, 10, 13, 0x1cb]:
                update_ui_state()
                return False;

        return True
