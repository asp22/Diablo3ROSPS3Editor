import py_proto.account
import py_proto.items
from pathlib import Path
import random
import argparse
import proto_parsers.proto_message as pm
import proto_parsers.proto_item as pi
from misc.parse_gbids import GBIDS
from misc.parse_affixes import AFFIXES

class CurrencySavedDataView:
    def __init__(self, currencySavedData):
        self._currency_saved_data = currencySavedData;

    def has_blood_shards(self):
        currency_list = self._currency_saved_data.currency
        for c in currency_list:
            if c._deb_gbid.obj.signed == -1691237125:
                return True
        return False

    def create_blood_shards(self):
        assert self.has_blood_shards() == False;
        currency_list = self._currency_saved_data.currency
        for c in currency_list:
            if c._deb_gbid.obj.signed == -1:
                c._deb_gbid.obj.signed = -1691237125
                c._count.obj.unsigned = 0
                return

    def get_blood_shards(self):
        assert self.has_blood_shards()
        currency_list = self._currency_saved_data.currency
        for c in currency_list:
            if c._deb_gbid.obj.signed == -1691237125:
                return c._count.obj.unsigned

    def lazy_get_blood_shards(self):
        if self.has_blood_shards() == False:
            self.create_blood_shards()
        return self.get_blood_shards()

    def set_blood_shards(self, v):
        assert self.has_blood_shards()
        currency_list = self._currency_saved_data.currency
        for c in currency_list:
            if c._deb_gbid.obj.signed == -1691237125:
                c._count.obj.unsigned = v

    def lazy_set_blood_shards(self, v):
        if self.has_blood_shards() == False:
            self.create_blood_shards()
        self.set_blood_shards(v)

class SavedItemView:
    def __init__(self, saved_item):
        self._saved_item = saved_item;

    def get_stack_size(self):
        return self._saved_item.generator.stack_size.obj.unsigned

    def set_stack_size(self, v):
        self._saved_item.generator.stack_size.obj.unsigned = v

class ConsumableItemView:
    def __init__(self, game_item):
        self._game_item = game_item
        self._gbid_id = game_item.generator.gb_handle.gbid.obj.signed
        self._gbid = GBIDS.find(self._gbid_id)

    def is_consumable(self):
        return True

    def get_name(self):
        return self._gbid.name

    def get_category(self):
        return self._gbid.category

    def get_stack_size(self):
        s = self._game_item.generator.stack_size.obj.unsigned
        return s

    def set_stack_size(self, v):
        self._game_item.generator.stack_size.obj.unsigned = v

    def get_square_index(self):
        return self._game_item.square_index.obj.unsigned

class NonConsumableItemView:
    def __init__(self, game_item):
        self._game_item = game_item
        self._gbid_id = game_item.generator.gb_handle.gbid.obj.signed
        self._gbid = GBIDS.find(self._gbid_id)

    @property
    def gbid_id(self):
        return self._gbid_id

    def is_consumable(self):
        return False

    def has_legendary_level(self):
        return self._game_item.generator.legendary_item_level != None

    def get_legendary_level(self):
        assert self.has_legendary_level()
        return self._game_item.generator.legendary_item_level.obj.unsigned 

    def set_legendary_level(self, v):
        assert self.has_legendary_level()
        self._game_item.generator.legendary_item_level.obj.unsigned = v

    def get_name(self):
        return self._gbid.name

    def get_category(self):
        return self._gbid.category

    def get_square_index(self):
        return self._game_item.square_index.obj.unsigned

    def has_effects(self):
        return len(self._game_item.generator.base_affixes_list) > 0

    def get_effects(self):
        effects = []
        for id_ in self._game_item.generator.base_affixes_list:
            effects.append(AFFIXES.find(id_.obj.signed))
        return effects

    def update_effect(self, index, id_):
        # TODO optimize
        ids = []
        effects = self.get_effects()
        for e in effects:
            ids.append(e.signed_int)

        ids[index] = id_
        self._game_item.generator.clear_child_repeated_message(3)
        for i in ids:
            self.add_effect(i)

    def delete_effect(self, index):
        # TODO optimize
        ids = []
        effects = self.get_effects()
        for i, e in enumerate(effects):
            if i == index:
                continue
            ids.append(e.signed_int)

        self._game_item.generator.clear_child_repeated_message(3)
        for i in ids:
            self.add_effect(i)

        

    def add_effect(self, id_):
        raw = "1d7f7d6b28"
        raw_bytes = bytes.fromhex(raw)
        read, t = pm.decode(raw_bytes)
        t[0].signed = id_
        raw = t.encode().hex()

        self._game_item.generator.create_child_repeated_simple(3, raw)

def make_game_item_view(saved_item):
    consumable = ConsumableItemView(saved_item)
    if consumable.get_stack_size() > 0:
        return consumable

    non_consumable = NonConsumableItemView(saved_item)
    return non_consumable

class ItemListView:
    def __init__(self, item_list):
        self._item_list = item_list;

    def count(self):
        return len(self._item_list.saved_item_list)

    def _has_item_id(self, id):
        for i in self._item_list.saved_item_list:
            if i.generator != None and i.generator.gb_handle.gbid.obj.signed == id:
                return True

        return False

    def _get_item_id(self, id):
        for i, saved_item in enumerate(self._item_list.saved_item_list):
            if saved_item.generator != None and saved_item.generator.gb_handle.gbid.obj.signed == id:
                return SavedItemView(saved_item)

        assert False

    def get_stash_item_count(self):
        c = 0
        for i, saved_item in enumerate(self._item_list.saved_item_list):
            if saved_item.item_slot.obj.unsigned == 1088:
                c += 1
        return c

    def get_slot_items(self, keys):
        out = []
        for i, saved_item in enumerate(self._item_list.saved_item_list):
            if saved_item.item_slot.obj.unsigned in keys:
                out.append(make_game_item_view(saved_item))
        return out

    def get_stash_items(self):
        return self.get_slot_items([1088])

    def get_hero_items(self):
        keys = [272, 288, 304, 320, 336, 352, 368, 384, 400, 416, 432, 448, 464, 480, 1296, 1312, 1328, 1344, 1360, 1376]
        keys = [k*2 for k in keys]
        return self.get_slot_items(keys)

    def get_hero_inventory_consumables(self):
        out = []
        keys = [272]
        keys = [k*2 for k in keys]
        items = self.get_slot_items(keys)
        for s in items:
            if s.is_consumable():
                out.append(s)
        return out

    def get_hero_inventory_non_consumables(self):
        out = []
        keys = [272]
        keys = [k*2 for k in keys]
        items = self.get_slot_items(keys)
        for s in items:
            if s.is_consumable() == False:
                out.append(s)
        return out

    def get_available_inventory_slots(self):
        idx = set([i*2 for i in range(60)])
        keys = [272]
        keys = [k*2 for k in keys]
        items = self.get_slot_items(keys)
        for s in items:
            sq = s.get_square_index()
            idx.remove(sq)

        return list(idx)


    def get_hero_equiped(self):
        out = []
        keys = [288, 304, 320, 336, 352, 368, 384, 400, 416, 432, 448, 464, 480]
        keys = [k*2 for k in keys]
        items = self.get_slot_items(keys)
        for s in items:
            out.append(s)
        return out

    def get_followers_items(self):
        out = []
        keys = [1296, 1312, 1328, 1344, 1360, 1376]
        keys = [k*2 for k in keys]
        items = self.get_slot_items(keys)
        for s in items:
            out.append(s)
        return out

    def get_stash_consumables(self):
        out = []
        stash_items = self.get_stash_items()
        for s in stash_items:
            if s.is_consumable():
                out.append(s)
        return out

    def get_stash_non_consumables(self):
        out = []
        stash_items = self.get_stash_items()
        for s in stash_items:
            if s.is_consumable() == False:
                out.append(s)
        return out

    def debug_get_slots(self):
        out = {}
        for i, saved_item in enumerate(self._item_list.saved_item_list):
            s = saved_item.item_slot.obj.unsigned // 2
            if s not in out:
                out[s] = 0
            out[s] += 1
        return out

    def has_gold_item(self):
        gold_id = 126259831
        return self._has_item_id(gold_id)

    def get_gold_item(self):
        gold_id = 126259831
        return self._get_item_id(gold_id)

    def lazy_get_gold_item(self):
        if self.has_gold_item() == False:
            self.create_gold_item()
        return self.get_gold_item()

    def create_gold_item(self):
        assert self.has_gold_item() == False
        last_saved_item = self._item_list.saved_item_list[-1]
        low_id = last_saved_item.id.id_low.obj.unsigned
        gold_low_id = low_id + 65537

        #raw = "0a280a08080110af81ecc307200028e0083000380042130800120708041577928607300938004082da2d"
        #raw = "0a08080110af81ecc307200028e0083000380042130800120708041577928607300938004082da2d"
        raw = "0a0408011000200028e0083000380042110800120708041577928607300938004000"
        raw_bytes = bytes.fromhex(raw)
        read, t = pm.decode(raw_bytes)
        pm.expand_buffer_to_message_recursive(t)
        t[0][1].unsigned = gold_low_id
        raw = t.encode().hex()

        self._item_list.create_child_repeated_message(1, raw, py_proto.items.SavedItem)


    def fill_empty_inventory_with_horadaric_cache(self, level):
        last_saved_item = self._item_list.saved_item_list[-1]
        low_id = last_saved_item.id.id_low.obj.unsigned

        available = self.get_available_inventory_slots()
        for i, av in enumerate(available):

            new_low_id = low_id + 65537*(i+1)

            raw = "0a0d080110b88688f7fbffffffff01200028a00430243800421908eedaddda0f1207080415fdf7950430890238004000800146"
            raw_bytes = bytes.fromhex(raw)
            read, t = pm.decode(raw_bytes)
            pm.expand_buffer_to_message_recursive(t)

            t[0][1].unsigned = new_low_id
            t[3].unsigned = av
            t[5][0].unsigned = random.randint(1,0xFFFFFFFF)
            t[5][5].unsigned = level

            x = [-1369696815, 584615634, -1756039213, 198273236, -2142381611]
            random_idx = random.randint(0,4)
            t[5][1][1].signed = x[random_idx]
            raw = t.encode().hex()

            self._item_list.create_child_repeated_message(1, raw, py_proto.items.SavedItem)

        return len(available)
