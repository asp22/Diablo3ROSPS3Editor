import curses
from ui.ui_state import UiState
from ui.consumable_menu import ConsumableMenuUi
from ui.non_consumable_menu import NonConsumableMenuUi

class HeroInventoryUi:
    def __init__ (self, stdscr, hero_view, game_items_view):
        self.stdscr = stdscr
        self.hero_view = hero_view
        self.game_items_view = game_items_view
        self.menu_current_idx = 0
        self.consumable_items = self.game_items_view.get_hero_inventory_consumables()
        self.non_consumable_items = self.game_items_view.get_hero_inventory_non_consumables()
        self.equiped = self.game_items_view.get_hero_equiped()
        self.followers = self.game_items_view.get_followers_items()
        self.available_slots = self.game_items_view.get_available_inventory_slots()
        self.menu_current_idx = 0
        self.max_menu_current_idx = 4

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
            elif self.menu_current_idx == 2 and len(self.equiped):
                UiState.ui_stack.append(NonConsumableMenuUi(self.stdscr, self.equiped))
            elif self.menu_current_idx == 3 and len(self.followers):
                UiState.ui_stack.append(NonConsumableMenuUi(self.stdscr, self.followers))
            elif self.menu_current_idx == 4 and len(self.followers) and len(self.available_slots) > 0:
                self.game_items_view.fill_empty_inventory_with_horadaric_cache(self.hero_view.get_level())
                self.available_slots = self.game_items_view.get_available_inventory_slots()
                self.non_consumable_items = self.game_items_view.get_hero_inventory_non_consumables()
                UiState.saveable = True

        def draw_menu(select_idx):
            self.pad.addstr(0, 0, f'Inventory Consumables               : {len(self.consumable_items)}', curses.A_REVERSE if select_idx == 0 else curses.A_NORMAL)
            self.pad.addstr(1, 0, f'Inventory Non Consumables           : {len(self.non_consumable_items)}', curses.A_REVERSE if select_idx == 1 else curses.A_NORMAL)
            self.pad.addstr(2, 0, f'Equiped                             : {len(self.equiped)}', curses.A_REVERSE if select_idx == 2 else curses.A_NORMAL)
            self.pad.addstr(3, 0, f'Followers                           : {len(self.followers)}', curses.A_REVERSE if select_idx == 3 else curses.A_NORMAL)
            self.pad.addstr(4, 0, f'Fill Empty Slots With Horadric Cache: {len(self.available_slots)}', curses.A_REVERSE if select_idx == 4 else curses.A_NORMAL)
            self.pad.clrtoeol()

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
