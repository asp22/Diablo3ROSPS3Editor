# take an account.SavedDefinition object and allow displaying of properties
import py_proto.account
import py_proto.items
from pathlib import Path
import argparse
import proto_parsers.proto_message as pm
import proto_parsers.proto_item as pi
import proto_parsers.field_and_wire_type as fw
import py_proto_view.items_view
import py_proto_view.attribute_serializer_view

class AccountPartitionView:
    def __init__(self, partition):
        self._partition = partition;

    def has_currency_data(self):
        return self._partition.currency_data != None

    def create_currency_data(self):
        assert self.has_currency_data() == False

        raw = "0a070dffffffff10010a070dffffffff10010a070dffffffff10010a070dffffffff10010a070dffffffff10010a070dffffffff10010a070dffffffff10010a070dffffffff10010a070dffffffff10010a070dffffffff10010a070dffffffff10010a070dffffffff10010a070dffffffff10010a070dffffffff10010a070dffffffff10010a070dffffffff10010a070dffffffff10010a070dffffffff10010a070dffffffff10010a070dffffffff1001"
        self._partition.create_child_optional_message(9, raw, py_proto.items.CurrencySavedData)

    def get_currency_data(self):
        assert self.has_currency_data()
        return py_proto_view.items_view.CurrencySavedDataView(self._partition.currency_data)

    def lazy_get_currency_data(self):
        if self.has_currency_data() == False:
            self.create_currency_data()
        return py_proto_view.items_view.CurrencySavedDataView(self._partition.currency_data)

    def lazy_get_blood_shards(self):
        return self.lazy_get_currency_data().lazy_get_blood_shards()

    def lazy_set_blood_shards(self, v):
        self.lazy_get_currency_data().lazy_set_blood_shards(v)


    def has_paragon_level(self):
        return self._partition._alt_level != None

    def get_paragon_level(self):
        assert self.has_paragon_level()
        return self._partition.alt_level.obj.unsigned

    def set_paragon_level(self, v):
        assert self.has_paragon_level()
        self._partition.alt_level.obj.unsigned = v
        paragon_attributes = self.get_paragon_xp_attributes()
        paragon_attributes.set_paragon_level(v)

    def lazy_get_paragon_level(self):
        if self.has_paragon_level() == False:
            self.create_paragon_level()
        return self.get_paragon_level()

    def lazy_set_paragon_level(self, v):
        if self.has_paragon_level() == False:
            self.create_paragon_level()
        self.set_paragon_level(v)

    def create_paragon_level(self):
        assert self.has_paragon_level() == False
        raw = "4000"
        self._partition.create_child_optional_simple(8, raw)

    def has_game_items(self):
        return self._partition.game_items != None

    def get_game_items(self):
        assert self.has_game_items()
        return py_proto_view.items_view.ItemListView(self._partition._game_items)

    def create_game_items(self):
        assert self.has_game_items() == False

        raw = "0a2e0a080801108e80ccbe07200028c00830003800421908a7a6c4b10712070804152dd9605c30890238004001e801010a430a080801108f80d0be07200028c008300e3800422e08eb8ca1de051207080415fa1d87db1d0d36c75e1d1fc565ee1db7d6f9df30890238fb014000501260fb01e80101"
        self._partition.create_child_optional_message(3, raw, py_proto.items.ItemList)

    def lazy_get_game_items(self):
        if self.has_game_items() == False:
            self.create_game_items()
        return self.get_game_items()

    def lazy_get_gold(self):
        item_list_view = self.lazy_get_game_items()
        gold_item = item_list_view.lazy_get_gold_item()
        return gold_item.get_stack_size()

    def lazy_set_gold(self, v):
        item_list_view = self.lazy_get_game_items()
        gold_item = item_list_view.lazy_get_gold_item()
        gold_item.set_stack_size(v)

    def get_paragon_xp_attributes(self):
        return py_proto_view.attribute_serializer_view.ParagonXpAttributesView(self._partition.saved_attributes)


class SavedDefinitionView:
    def __init__(self, sd):
        self._sd = sd;

    def _get_paragon_level(self, partition):
        partition = self._sd.account_partition[partition]
        if partition._alt_level == None:
            return 0
        else:
            return partition._alt_level.obj.unsigned

    def get_normal_partition(self):
        return AccountPartitionView(self._sd.account_partition[0])

    def get_hardcore_partition(self):
        return AccountPartitionView(self._sd.account_partition[1])

if __name__ == "__main__":
    import argparse
    import parse_gbids
    import parse_affixes
    this_file = Path(__file__)

    parser = argparse.ArgumentParser(description="A script to encrypt/decrypt and modify Diablo III saves")
    parser.add_argument("-d", "--in-dir", type=str, required=True, help="The account file you want to work with")
    args = parser.parse_args()

    gbids_file = this_file.parent / 'assets/gbids.json'
    affix_file = this_file.parent / 'assets/affixes.json'

    parse_gbids.GBIDS.read_in_json(gbids_file)
    parse_affixes.AFFIXES.read_in_json(affix_file)


    # test by updating fresh account with paragon level 10
    # gold 2 million
    # blood shards 1 million
    sd = account.get_saved_definition_via_dir(Path(args.in_dir))
    view = SavedDefinitionView(sd)
    partition = view.get_normal_partition() 
    partition.set_paragon_level(1000)
    if partition.has_currency_data() == False:
        partition.create_currency_data()
    currency_data = partition.get_currency_data()

    if currency_data.has_blood_shards() == False:
        currency_data.create_blood_shards()
    currency_data.set_blood_shards(1000000)
    
    item_list_view = partition.get_game_items()
    if item_list_view.has_gold_item() == False:
        item_list_view.create_gold_item()
    gold_item = item_list_view.get_gold_item()
    gold_item.set_stack_size(2000000)

    stash_items = item_list_view.get_stash_items()
    item_name = stash_items[1].get_name()
    stash_items[1].add_effect()

    account.saved_definition_to_dir(sd, Path(args.in_dir))


    #view = AccountView(sd)
    #print(f'normal   paragon level: {view.get_normal_paragon_level()}')
    #print(f'normal   blood shard:   {view.get_normal_blood_shard_count()}')
    #print(f'normal   gold:          {view.get_normal_gold()}')
    #print(f'hardcore paragon level: {view.get_hardcore_paragon_level()}')
    #print(f'hardcore blood shard:   {view.get_hardcore_blood_shard_count()}')
    #print(f'hardcore gold:          {view.get_hardcore_gold()}')
