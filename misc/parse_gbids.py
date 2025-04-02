# parse gbids.json and build maps
# pandas would be nice but I want to use standard python
import json
import argparse
from pathlib import Path

class GBIDS:
    items_ = []
    signed_int_to_item_ = {}
    items_by_category_ = {}

    class Item:
        def __init__(self, signed, name, cat):
            self.signed_int = signed
            self.name = name
            self.category = cat

        def __str__(self):
            return f'GBID: [{self.signed_int}] [{self.name}] [{self.category}]'

    @classmethod
    def add(cls, signed_int, name, category):
        i = cls.Item(signed_int, name, category)
        cls.items_.append(i)
        cls.signed_int_to_item_[signed_int] = i

        if category not in cls.items_by_category_:
            cls.items_by_category_[category] = []
        cls.items_by_category_[category].append(i)

    @classmethod
    def read_in_json(cls, filename):
        with open(filename, 'rt') as f:
            data = f.read()

        jdata = json.loads(data)
        for k, v in jdata.items():
            cls.add(int(k), v["name"], v["category"])

    @classmethod
    def size(cls):
        return len(cls.items_)

    @classmethod
    def find(cls, signed_int):
        if signed_int in cls.signed_int_to_item_:
            return cls.signed_int_to_item_[signed_int]
        return None

    @classmethod
    def check_loaded(cls):
        assert len(cls.items_) > 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script to encrypt/decrypt and modify Diablo III saves")
    parser.add_argument("-i", "--in-file", type=str, required=True, help="The account file you want to work with")
    args = parser.parse_args()
    filename = Path(args.in_file)
    assert filename.exists()

    GBIDS.read_in_json(filename)
    print(GBIDS.size())
    print(GBIDS.find(-1511400104))

    print('---sets')
    print(set(GBIDS.items_by_category_.keys()))
