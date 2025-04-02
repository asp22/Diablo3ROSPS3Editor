import proto_parsers.proto_message as pm
import proto_parsers.proto_item as pi
import py_proto.attribute_serializer as asz

class ParagonXpAttributesView:
    def __init__(self, attributes):
        self._saved_attributes = attributes;

    def has_default_xp(self):
        keys = [8187]
        found = []
        for sa in self._saved_attributes.saved_attribute_list:
            k = sa.message[0].unsigned
            found.append(k)

        return set(keys) == set(found)

    def has_paragon_xp(self):
        keys = [8185, 8187, 8183]
        found = []
        for sa in self._saved_attributes.saved_attribute_list:
            k = sa.message[0].unsigned
            found.append(k)

        return set(keys) == set(found)

    def _clear_xp_attributes(self):
        self._saved_attributes.clear_child_repeated_message(2)

    def make_default_xp(self):
        self._clear_xp_attributes()

        raw = "08fb3f1080f4ee06"
        self._saved_attributes.create_child_repeated_message(2, raw, asz.SavedAttribute)

    def make_paragon_xp(self):
        self._clear_xp_attributes()

        raw = "08f93f1002" # paragon level : 1 --- underlying value is 2 
        self._saved_attributes.create_child_repeated_message(2, raw, asz.SavedAttribute)

        raw = "08fb3f1002" # remaining in xp chuck; don't fully understand encoding but I know 0x2 means you have to earn 1 xp to go to next level
        self._saved_attributes.create_child_repeated_message(2, raw, asz.SavedAttribute)

        raw = "08f73f1000" # remaining chucks; set to zero so that we don't have to earn max int + 1
        self._saved_attributes.create_child_repeated_message(2, raw, asz.SavedAttribute)

    def set_paragon_level(self, v):
        if v == 0:
            self.make_default_xp()
        else:
            self.make_paragon_xp()
            self._saved_attributes.message[1][1].unsigned = v * 2

class HeroParagonAttributesView:
    def __init__(self, attributes):
        self._saved_attributes = attributes;

    def _has(self, key):
        for sa in self._saved_attributes.saved_attribute_list:
            k = sa.message[0].unsigned
            if key == k:
                return sa
        return None

    def has(self, key):
        res = self._has(key)
        if res is None:
            return False
        return True

    def get(self, key):
        sa = self._has(key)
        if sa is None:
            return 0
        return sa.message[1].unsigned // 2

    def set(self, key, v):
        sa = self._has(key)
        if sa is None:
            return
        v = v * 2
        sa.message[1].unsigned = v

    def reset(self):
        keys = [
            678133119,
            3114246784,
            1161962112,
            2544697984,
            129688192,
            2335793792,
            1322311039,
            4043956864,
            2162885248,
            1790295423,
            3665404544,
            2510111360,
            1553900160,
            1754546816,
            3622722943,
            2152538752,
            1790295423,
            323222911,
            599302784,
            3947478399,
            3347660159,
            804446848,
            1474986624,
            1759092095,
            1860600448,
            1663091328,
                ]

        for k in keys:
            self.set(k, 0)

    def get_wizard_intellligence_points(self):
        key = 678133119
        return self.get(key)

    def get_witchdoc_intellligence_points(self):
        key = 3114246784
        return self.get(key)

    def get_barbarian_strength_points(self):
        key = 1161962112
        return self.get(key)

    def get_cursader_strength_points(self):
        key = 2544697984
        return self.get(key)

    def get_monk_dexterity_points(self):
        key = 129688192
        return self.get(key)

    def get_demon_dexterity_points(self):
        key = 2335793792
        return self.get(key)


    def get_max_arcane_power_points(self):
        key = 1322311039
        return self.get(key)

    def get_max_mana_points(self):
        key = 4043956864
        return self.get(key)

    def get_max_fury_points(self):
        key = 2162885248
        return self.get(key)

    def get_max_wrath_points(self):
        key = 1790295423
        return self.get(key)

    def get_max_spirit_points(self):
        key = 3665404544
        return self.get(key)

    def get_max_hatred_points(self):
        key = 2510111360
        return self.get(key)


    def get_movement_points(self):
        key = 1553900160
        return self.get(key)

    def get_life_on_hit_points(self):
        key = 1754546816
        return self.get(key)

    def get_cooldown_reduction_points(self):
        key = 3622722943
        return self.get(key)

    def get_resist_all_points(self):
        key = 2152538752
        return self.get(key)

    def get_life_points(self):
        key = 1790295423
        return self.get(key)

    def get_critical_hit_damage_points(self):
        key = 323222911
        return self.get(key)

    def get_area_damaga_points(self):
        key = 599302784
        return self.get(key)

    def get_attack_speed_points(self):
        key = 3947478399
        return self.get(key)

    def get_vitality_points(self):
        key = 3347660159
        return self.get(key)

    def get_armour_points(self):
        key = 804446848
        return self.get(key)

    def get_critical_hit_chance_points(self):
        key = 1474986624
        return self.get(key)

    def get_life_regeneration_points(self):
        key = 1759092095
        return self.get(key)

    def get_resource_cost_points(self):
        key = 1860600448
        return self.get(key)

    def get_gold_find_points(self):
        key = 1663091328
        return self.get(key)
