# parse gbids.json and build maps
# pandas would be nice but I want to use standard python
import json
import argparse
from pathlib import Path

class AFFIXES:
    signed_ints = []
    effects = []
    effectivenesses = []

    affixes_ = []
    signed_int_to_affix_ = {}

    affixes_by_effect_ = {}

    class Item:
        def __init__(self, signed, effect, ness):
            self.signed_int = signed
            self.effect = effect
            self.effectiveness = ness

        def __str__(self):
            return f'AFFIX: [{self.signed_int}] [{self.effect}] [{self.effectiveness}]'

    @classmethod
    def add(cls, signed_int, effect, effectiveness):
        i = cls.Item(signed_int, effect, effectiveness)
        cls.affixes_.append(i)
        cls.signed_int_to_affix_[signed_int] = i

        if effect not in cls.affixes_by_effect_:
            cls.affixes_by_effect_[effect] = []
        cls.affixes_by_effect_[effect] = i


    @classmethod
    def read_in_json(cls, filename):
        with open(filename, 'rt') as f:
            data = f.read()

        jdata = json.loads(data)
        for k, v in jdata.items():
            cls.add(int(k), v["effect"], v["effectiveness"])

    @classmethod
    def size(cls):
        return len(cls.signed_ints)

    @classmethod
    def find(cls, signed_int):
        if signed_int in cls.signed_int_to_affix_:
            return cls.signed_int_to_affix_[signed_int]
        return None

    @classmethod
    def get_all(cls):
        return cls.affixes_

    @classmethod
    def check_loaded(cls):
        assert len(cls.affixes_) > 0



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script to encrypt/decrypt and modify Diablo III saves")
    parser.add_argument("-i", "--in-file", type=str, required=True, help="The account file you want to work with")
    args = parser.parse_args()
    filename = Path(args.in_file)
    assert filename.exists()

    AFFIXES.read_in_json(filename)
    print(AFFIXES.size())
    print(AFFIXES.find(555585138))

    print('----- effects')
    l = list(AFFIXES.affixes_by_effect_.keys())
    l = sorted(l)
    for i, it in enumerate(l):
        if i == 51:
            print(AFFIXES.affixes_by_effect_[it])
        print(i, it)

    

