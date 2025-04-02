import pytest
from pathlib import Path

import py_proto.hero
import py_proto_view.hero_view
import py_proto_view.items_view
import py_proto_view.attribute_serializer_view
import parse_gbids
import parse_affixes

@pytest.fixture
def hero_views():
    def load_hero_views(filename):
        sd = py_proto.hero.get_hero_saved_definition_via_filename(filename)
        view = py_proto_view.hero_view.SavedDefinitionView(sd)
        return view

    this_file = Path(__file__)
    final_file = this_file.parent / 'data/hero_view/final_HERO.HRO'
    new_file = this_file.parent / 'data/hero_view/new_HERO.HRO'
    para_file = this_file.parent / 'data/hero_view/para_HERO.HRO'
    gbids_file = this_file.parent.parent / 'assets/gbids.json'
    affix_file = this_file.parent.parent / 'assets/affixes.json'

    parse_gbids.GBIDS.read_in_json(gbids_file)
    parse_affixes.AFFIXES.read_in_json(affix_file)

    return {
        'final': load_hero_views(final_file),
        'new': load_hero_views(new_file),
        'para': load_hero_views(para_file),
    }

    return [this_file]
    

def test_fixture(hero_views):
    pass

def test_final_hero(hero_views):
    view = hero_views['final']
    assert view.get_name() == "Storm"
    assert view.get_level() == 70
    assert view.get_paragon_level() == 10000

    attribs = view.get_paragon_attributes()

    assert attribs.get_barbarian_strength_points() == 7206
    assert attribs.get_vitality_points() == 2094
    assert attribs.get_movement_points() == 50
    assert attribs.get_max_fury_points() == 50

    assert attribs.get_attack_speed_points() == 50
    assert attribs.get_cooldown_reduction_points() == 50
    assert attribs.get_critical_hit_chance_points() == 50
    assert attribs.get_critical_hit_damage_points() == 50 

    assert attribs.get_life_points() == 50
    assert attribs.get_armour_points() == 50
    assert attribs.get_resist_all_points() == 50
    assert attribs.get_life_regeneration_points() == 50

    assert attribs.get_area_damaga_points() == 50
    assert attribs.get_resource_cost_points() == 50
    assert attribs.get_life_on_hit_points() == 50
    assert attribs.get_gold_find_points() == 50

    attribs.reset()
    assert attribs.get_barbarian_strength_points() == 0
    assert attribs.get_vitality_points() == 0
    assert attribs.get_movement_points() == 0
    assert attribs.get_max_fury_points() == 0

    assert view.has_game_items()
    item_list_view = view.get_game_items()
    hero_items = item_list_view.get_hero_items()
    assert len(hero_items) == 59

def test_new_hero(hero_views):
    view = hero_views['new']
    assert view.get_name() == "Lorenna"
    assert view.get_level() == 1
    assert view.get_paragon_level() == 0

    attribs = view.get_paragon_attributes()
    assert attribs.get_movement_points() == 0

    assert view.has_game_items()

def test_para_hero(hero_views):
    view = hero_views['para']
    assert view.get_name() == "Lorenna"
    assert view.get_level() == 1
    assert view.get_paragon_level() == 1000

    attribs = view.get_paragon_attributes()
    assert attribs.get_wizard_intellligence_points() == 1
    assert attribs.get_vitality_points() == 2
    assert attribs.get_movement_points() == 3
    assert attribs.get_max_arcane_power_points() == 4

    assert attribs.get_attack_speed_points() == 5
    assert attribs.get_cooldown_reduction_points() == 6
    assert attribs.get_critical_hit_chance_points() == 7
    assert attribs.get_critical_hit_damage_points() == 8

    assert attribs.get_life_points() == 9
    assert attribs.get_armour_points() == 10
    assert attribs.get_resist_all_points() == 11
    assert attribs.get_life_regeneration_points() == 12

    assert attribs.get_area_damaga_points() == 13
    assert attribs.get_resource_cost_points() == 14
    assert attribs.get_life_on_hit_points() == 15
    assert attribs.get_gold_find_points() == 16

    view.set_paragon_level(1001)
    assert view.get_paragon_level() == 1001
    assert attribs.get_area_damaga_points() == 0
    assert attribs.get_resource_cost_points() == 0
    assert attribs.get_life_on_hit_points() == 0
    assert attribs.get_gold_find_points() == 0
