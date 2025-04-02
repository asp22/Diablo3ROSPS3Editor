import pytest
from pathlib import Path

import py_proto.account
import py_proto_view.account_view
import py_proto_view.items_view
import py_proto_view.attribute_serializer_view
import parse_gbids
import parse_affixes

@pytest.fixture
def account_sd_views():
    def load_account_sd_view(filename):
        sd = py_proto.account.get_saved_definition_via_filename(filename)
        view = py_proto_view.account_view.SavedDefinitionView(sd)
        return view

    this_file = Path(__file__)
    final_file = this_file.parent / 'data/account_view/final_ACCOUNT.DAT'
    new_file = this_file.parent / 'data/account_view/new_ACCOUNT.DAT'
    gbids_file = this_file.parent.parent / 'assets/gbids.json'
    affix_file = this_file.parent.parent / 'assets/affixes.json'

    parse_gbids.GBIDS.read_in_json(gbids_file)
    parse_affixes.AFFIXES.read_in_json(affix_file)

    return {
        'final': load_account_sd_view(final_file),
        'new': load_account_sd_view(new_file),
    }

    return [this_file]
    

def test_fixture(account_sd_views):
    pass

def test_normal_partition_final(account_sd_views):
    view = account_sd_views['final']
    assert isinstance(view, py_proto_view.account_view.SavedDefinitionView)

    partition = view.get_normal_partition() 
    assert isinstance(partition, py_proto_view.account_view.AccountPartitionView)

    assert partition.has_paragon_level() == True
    assert partition.get_paragon_level() == 10000

    assert partition.has_currency_data() == True
    currency_data = partition.get_currency_data()
    assert isinstance(currency_data, py_proto_view.items_view.CurrencySavedDataView)

    assert currency_data.has_blood_shards() == True
    assert currency_data.get_blood_shards() == 99971314
    
    assert partition.has_game_items() == True
    item_list_view = partition.get_game_items()
    assert isinstance(item_list_view, py_proto_view.items_view.ItemListView)

    assert item_list_view.has_gold_item() == True
    gold_item = item_list_view.get_gold_item()
    assert isinstance(gold_item, py_proto_view.items_view.SavedItemView)
    assert gold_item.get_stack_size() == 12789554

    saved_attributes = partition.get_paragon_xp_attributes()
    assert isinstance(saved_attributes, py_proto_view.attribute_serializer_view.ParagonXpAttributesView)
    assert saved_attributes.has_paragon_xp() == True
    assert saved_attributes.has_default_xp() == False

    stash_items = item_list_view.get_stash_items()
    assert len(stash_items) == 198
    item_name = stash_items[0].get_name()
    assert item_name == 'Key of Evil'
    assert stash_items[0].is_consumable()
    assert stash_items[0].get_stack_size() == 998
    stash_items[0].set_stack_size(999)
    assert stash_items[0].get_stack_size() == 999

    assert stash_items[1].get_name() == 'Legendary: Manald Heal'
    assert stash_items[1].is_consumable() == False
    assert stash_items[1].has_legendary_level()
    assert stash_items[1].get_legendary_level() == 70
    stash_items[1].set_legendary_level(7)
    assert stash_items[1].get_legendary_level() == 7


def test_hardcore_partition_final(account_sd_views):
    view = account_sd_views['final']

    partition = view.get_hardcore_partition() 
    assert isinstance(partition, py_proto_view.account_view.AccountPartitionView)

    assert partition.has_paragon_level() == True
    assert partition.get_paragon_level() == 10000

    assert partition.has_currency_data() == True
    currency_data = partition.get_currency_data()
    assert isinstance(currency_data, py_proto_view.items_view.CurrencySavedDataView)

    assert currency_data.has_blood_shards() == False
    currency_data.create_blood_shards()
    assert currency_data.has_blood_shards() == True
    assert currency_data.get_blood_shards() == 0
    
    assert partition.has_game_items() == True
    item_list_view = partition.get_game_items()
    assert isinstance(item_list_view, py_proto_view.items_view.ItemListView)

    assert item_list_view.has_gold_item() == True
    gold_item = item_list_view.get_gold_item()
    assert isinstance(gold_item, py_proto_view.items_view.SavedItemView)
    assert gold_item.get_stack_size() == 748802

    saved_attributes = partition.get_paragon_xp_attributes()
    assert saved_attributes.has_paragon_xp() == True
    assert saved_attributes.has_default_xp() == False

    ################### check if base data has been updated
    view = account_sd_views['final']
    partition = view.get_hardcore_partition() 
    assert currency_data.has_blood_shards() == True
    


def test_normal_partition_new(account_sd_views):
    view = account_sd_views['new']

    partition = view.get_normal_partition() 
    assert isinstance(partition, py_proto_view.account_view.AccountPartitionView)

    assert partition.has_paragon_level() == True
    assert partition.get_paragon_level() == 0
    partition.set_paragon_level(10)
    assert partition.get_paragon_level() == 10


    assert partition.has_currency_data() == False
    partition.create_currency_data()
    assert partition.has_currency_data() == True

    currency_data = partition.get_currency_data()
    assert isinstance(currency_data, py_proto_view.items_view.CurrencySavedDataView)
    
    assert currency_data.has_blood_shards() == False
    currency_data.create_blood_shards()
    assert currency_data.has_blood_shards() == True
    assert currency_data.get_blood_shards() == 0
    currency_data.set_blood_shards(1000000)
    assert currency_data.get_blood_shards() == 1000000
    
    
    assert partition.has_game_items() == True
    item_list_view = partition.get_game_items()
    assert isinstance(item_list_view, py_proto_view.items_view.ItemListView)

    assert item_list_view.has_gold_item() == False
    item_list_view.create_gold_item()
    assert item_list_view.has_gold_item() == True
    gold_item = item_list_view.get_gold_item()
    assert gold_item.get_stack_size() == 0
    gold_item.set_stack_size(2000000)
    assert gold_item.get_stack_size() == 2000000

    assert item_list_view.get_stash_item_count() == 2
    stash_items = item_list_view.get_stash_items()
    assert len(stash_items) == 2
    item_name = stash_items[0].get_name()
    assert item_name == 'Guardian Facade'
    item_name = stash_items[1].get_name()
    assert item_name == 'Legendary: Signet Ring of the Blizzard'
    assert stash_items[1].has_legendary_level() == False
    assert len(stash_items[1].get_effects()) == 3
    stash_items[1].add_effect(-335431120)
    assert len(stash_items[1].get_effects()) == 4

    effects = stash_items[1].get_effects()
    assert effects[0] != effects[3]

    stash_items[1].update_effect(0, -335431120)
    effects = stash_items[1].get_effects()
    assert effects[0] == effects[3]

    stash_items[1].delete_effect(3)
    effects = stash_items[1].get_effects()
    assert len(effects) == 3
    assert effects[0] != effects[2]

    saved_attributes = partition.get_paragon_xp_attributes()
    assert saved_attributes.has_paragon_xp() == True
    assert saved_attributes.has_default_xp() == False

    ################## check if base data has been updated
    view = account_sd_views['new']
    partition = view.get_normal_partition() 
    assert partition.has_currency_data() == True

    currency_data = partition.get_currency_data()
    assert currency_data.has_blood_shards() == True
    assert currency_data.get_blood_shards() == 1000000

    item_list_view = partition.get_game_items()
    assert item_list_view.has_gold_item() == True
    gold_item = item_list_view.get_gold_item()
    assert gold_item.get_stack_size() == 2000000


def test_hardcore_partition_new(account_sd_views):
    view = account_sd_views['new']

    partition = view.get_hardcore_partition() 
    assert isinstance(partition, py_proto_view.account_view.AccountPartitionView)

    assert partition.has_paragon_level() == False
    partition.create_paragon_level()
    assert partition.has_paragon_level() == True
    assert partition.get_paragon_level() == 0

    assert partition.has_currency_data() == False
    partition.create_currency_data()
    assert partition.has_currency_data() == True
    currency_data = partition.get_currency_data()
    assert isinstance(currency_data, py_proto_view.items_view.CurrencySavedDataView)

    
    assert currency_data.has_blood_shards() == False
    currency_data.create_blood_shards()
    assert currency_data.has_blood_shards() == True
    assert currency_data.get_blood_shards() == 0
    
    assert partition.has_game_items() == False
    partition.create_game_items() 
    assert partition.has_game_items() == True
    item_list_view = partition.get_game_items()
    assert isinstance(item_list_view, py_proto_view.items_view.ItemListView)

    assert item_list_view.has_gold_item() == False
    item_list_view.create_gold_item()
    assert item_list_view.has_gold_item() == True
    gold_item = item_list_view.get_gold_item()
    assert gold_item.get_stack_size() == 0

    saved_attributes = partition.get_paragon_xp_attributes()
    assert saved_attributes.has_paragon_xp() == False
    assert saved_attributes.has_default_xp() == False
    saved_attributes.make_default_xp()
    assert saved_attributes.has_paragon_xp() == False
    assert saved_attributes.has_default_xp() == True
    saved_attributes.make_paragon_xp()
    assert saved_attributes.has_paragon_xp() == True
    assert saved_attributes.has_default_xp() == False

    ################## check if base data has been updated
    view = account_sd_views['new']
    partition = view.get_hardcore_partition() 
    assert partition.has_currency_data() == True

    currency_data = partition.get_currency_data()
    assert currency_data.has_blood_shards() == True
    assert currency_data.get_blood_shards() == 0

    item_list_view = partition.get_game_items()
    assert item_list_view.has_gold_item() == True
    gold_item = item_list_view.get_gold_item()
    assert gold_item.get_stack_size() == 0

    saved_attributes = partition.get_paragon_xp_attributes()
    assert saved_attributes.has_default_xp() == False
    assert saved_attributes.has_paragon_xp() == True

def test_hardcore_partition_new_lazy_get_paragon_level(account_sd_views):
    view = account_sd_views['new']
    partition = view.get_hardcore_partition() 
    assert partition.lazy_get_paragon_level() == 0

def test_hardcore_partition_new_lazy_set_paragon_level(account_sd_views):
    view = account_sd_views['new']
    partition = view.get_hardcore_partition() 
    partition.lazy_set_paragon_level(50)
    assert partition.get_paragon_level() == 50

def test_normal_partition_final_set_paragon_to_zero(account_sd_views):
    view = account_sd_views['final']
    assert isinstance(view, py_proto_view.account_view.SavedDefinitionView)

    partition = view.get_normal_partition() 
    assert partition.get_paragon_level() == 10000
    saved_attributes = partition.get_paragon_xp_attributes()
    assert saved_attributes.has_paragon_xp() == True
    assert saved_attributes.has_default_xp() == False
    partition.set_paragon_level(0)
    assert saved_attributes.has_paragon_xp() == False
    assert saved_attributes.has_default_xp() == True

def test_hardcore_partition_new_lazy_get_blood_shards(account_sd_views):
    view = account_sd_views['new']

    partition = view.get_hardcore_partition() 
    currency_data = partition.lazy_get_currency_data()
    assert currency_data.lazy_get_blood_shards() == 0

def test_hardcore_partition_new_lazy_set_blood_shards(account_sd_views):
    view = account_sd_views['new']

    partition = view.get_hardcore_partition() 
    currency_data = partition.lazy_get_currency_data()
    currency_data.lazy_set_blood_shards(40) 
    assert currency_data.get_blood_shards() == 40


def test_hardcore_partition_new_lazy_get_gold_item(account_sd_views):
    view = account_sd_views['new']

    partition = view.get_hardcore_partition() 
    item_list_view = partition.lazy_get_game_items()
    gold_item = item_list_view.lazy_get_gold_item()
    assert gold_item.get_stack_size() == 0

def test_hardcore_partition_new_lazy_get_gold(account_sd_views):
    view = account_sd_views['new']

    partition = view.get_hardcore_partition() 
    assert partition.lazy_get_gold() == 0

def test_hardcore_partition_new_lazy_get_gold(account_sd_views):
    view = account_sd_views['new']

    partition = view.get_hardcore_partition() 
    partition.lazy_set_gold(40)
    assert partition.lazy_get_gold() == 40