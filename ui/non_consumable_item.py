import curses
from ui.ui_state import UiState
from ui.integer_menu import IntegerMenuUi
from ui.effect_menu import EffectMenuUi

class NonConsumableItemUi:
    def __init__(self, stdscr, non_consumable_item):
        self.stdscr = stdscr
        self.non_consumable_item = non_consumable_item
        self.menu_current_idx = 0
        self.max_menu_current_idx = 6

        if non_consumable_item.has_legendary_level():
            self.max_menu_current_idx += 1

        self.pad_height = self.max_menu_current_idx + 1 + 1
        self.pad_width = 200
        self.pad = curses.newpad(self.pad_height, self.pad_width)
        self.last_page = None

    def ui(self):
        self.stdscr.clear()

        def update_ui_state():
            n_effects = len(self.non_consumable_item.get_effects())
            n_add = 1 if n_effects < 6 else 0

            legendary_idx = None
            if self.non_consumable_item.has_legendary_level():
                legendary_idx = n_effects + n_add

            if self.menu_current_idx == legendary_idx:
                UiState.ui_stack.append(IntegerMenuUi(self.stdscr, "Legendary Level", self.non_consumable_item.get_legendary_level, self.non_consumable_item.set_legendary_level, [1, 70]))

            elif n_add == 1 and self.menu_current_idx == n_effects:
                # handle adding
                def setter(v):
                    self.non_consumable_item.add_effect(v)
                def deleter():
                    pass
                
                UiState.ui_stack.append(EffectMenuUi(self.stdscr, None, setter, deleter))
            else:
                effect = self.non_consumable_item.get_effects()[self.menu_current_idx]
                def setter(v):
                    self.non_consumable_item.update_effect(self.menu_current_idx, v)

                def deleter():
                    self.non_consumable_item.delete_effect(self.menu_current_idx)
                    self.pad.clear()

                UiState.ui_stack.append(EffectMenuUi(self.stdscr, effect.signed_int, setter, deleter))
            self.stdscr.clear()


        def draw_menu(select_idx):
            self.pad.addstr(0, 0, f'{self.non_consumable_item.get_category():<28} : {self.non_consumable_item.get_name()}')

            effects = self.non_consumable_item.get_effects()
            i = 0
            for i, e in enumerate(effects):
                self.pad.addstr(i+1, 0, f'[{e.signed_int:<11}] [{e.effect}] [{e.effectiveness}]', curses.A_REVERSE if select_idx == i else curses.A_NORMAL)
                self.pad.clrtoeol()

            if len(effects):
                i += 1

            if len(effects) != 6:
                self.pad.addstr(i+1, 0, f'[--- ADD ---]', curses.A_REVERSE if select_idx == i else curses.A_NORMAL)
                self.pad.clrtoeol()
                i += 1

            if self.non_consumable_item.has_legendary_level():
                self.pad.addstr(i+1, 0, f'Legendary Level: {self.non_consumable_item.get_legendary_level()}', curses.A_REVERSE if select_idx == i else curses.A_NORMAL)
                self.pad.clrtoeol()

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

            def calc_max_row_index():
                n_effects = len(self.non_consumable_item.get_effects())
                n_add = 1 if n_effects < 6 else 0
                if self.non_consumable_item.has_legendary_level():
                    return n_effects + n_add
                else:
                    return n_effects + n_add - 1

            max_row_idx = calc_max_row_index()

            c = self.stdscr.getch()
            if c == ord('q') or c == curses.KEY_LEFT:
                break
            elif c == curses.KEY_DOWN and self.menu_current_idx < max_row_idx:
                self.menu_current_idx += 1
            elif c == curses.KEY_UP and self.menu_current_idx > 0:
                self.menu_current_idx -= 1
            elif c in [curses.KEY_RIGHT, curses.KEY_ENTER, 10, 13, 0x1cb]:
                update_ui_state()
                return False;

        return True
