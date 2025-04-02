
from numbers import Rational
import proto_parsers.proto_message as pm
import proto_parsers.fixed32 as ppf32
import proto_parsers.integer as ppi
import py_proto.game_balance
import py_proto.online_service
from py_proto.base import Base

class CurrencyData(Base):
    @classmethod
    def MAKE_PROPS(cls):
        cls._make_optional_simple_value('deb_gbid', 1)
        cls._make_required_simple_value('count', 2)
        cls._make_optional_simple_value('id', 3)
        cls._make_optional_simple_value('persistent_flags', 4)

    def __init__(self, message):
        super().__init__(message)

class CurrencySavedData(Base):
    @classmethod
    def MAKE_PROPS(cls):
        cls._make_repeated_message('currency', 1, CurrencyData)

    def __init__(self, message):
        super().__init__(message)


class RareItemName(Base):
    @classmethod
    def MAKE_PROPS(cls):
        cls._make_required_simple_value('item_name_is_prefix', 1)
        cls._make_required_simple_value('sno_affix_string_list',2)
        cls._make_required_simple_value('affix_string_list_index',3)
        cls._make_required_simple_value('item_string_list_index',4)

    def __init__(self, message):
        super().__init__(message)

class EmbeddedGenerator(Base):
    @classmethod
    def MAKE_PROPS(cls):
        cls._make_required_message('generator', 2, Generator)

    def __init__(self, message):
        super().__init__(message)


class Generator(Base):
    @classmethod
    def MAKE_PROPS(cls):
        cls._make_required_message('gb_handle', 2, py_proto.game_balance.Handle)
        cls._make_repeated_simple_value('base_affixes_list', 3)
        cls._make_optional_message('rare_item_name', 4, RareItemName)
        cls._make_optional_simple_value('dep_enchant_affix', 5)
        cls._make_required_simple_value('durability', 7)
        cls._make_required_simple_value('stack_size', 8)
        cls._make_optional_simple_value('item_quality_level', 10)
        cls._make_optional_simple_value('item_binding_level', 11)
        cls._make_optional_simple_value('max_durability', 12)
        cls._make_repeated_message('contents', 13, EmbeddedGenerator)
        cls._make_optional_simple_value('legendary_item_level', 16)
        cls._make_optional_simple_value('enchanted_affix_old', 20)
        cls._make_optional_simple_value('enchanted_affix_new', 21)
        cls._make_optional_simple_value('legendary_base_item_gbid', 22)
        cls._make_optional_simple_value('jewel_rank', 27)
        cls._make_optional_simple_value('console_max_level', 28)
        cls._make_optional_simple_value('hardcore', 30)
        cls._make_optional_simple_value('dep_crafted_item_level', 31)

    def __init__(self, message):
        super().__init__(message)

class SavedItem(Base):
    @classmethod
    def MAKE_PROPS(cls):
        cls._make_required_message('id', 1, py_proto.online_service.ItemId)
        cls._make_required_simple_value('hireling_class', 4)
        cls._make_required_simple_value('item_slot',5)
        cls._make_required_simple_value('square_index', 6)
        cls._make_required_simple_value('used_socket_count', 7)
        cls._make_optional_message('generator', 8, Generator)

    def __init__(self, message):
        super().__init__(message)

class ItemList(Base):
    @classmethod
    def MAKE_PROPS(cls):
        cls._make_repeated_message('saved_item_list', 1, SavedItem)

    def __init__(self, message):
        super().__init__(message)

ItemList.MAKE_PROPS()
SavedItem.MAKE_PROPS()
Generator.MAKE_PROPS()
EmbeddedGenerator.MAKE_PROPS()
RareItemName.MAKE_PROPS()
CurrencySavedData.MAKE_PROPS()
CurrencyData.MAKE_PROPS()
