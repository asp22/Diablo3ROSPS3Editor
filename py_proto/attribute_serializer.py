
import proto_parsers.proto_message as pm
import proto_parsers.integer as ppi
from py_proto.base import Base

class SavedAttribute(Base):
    @classmethod
    def MAKE_PROPS(cls):
        cls._make_required_simple_value('key', 1)
        cls._make_required_simple_value('value', 2)

    def __init__(self, message):
        super().__init__(message)


class SavedAttributes(Base):
    @classmethod
    def MAKE_PROPS(cls):
        cls._make_repeated_message('saved_attribute_list',2, SavedAttribute)

    def __init__(self, message):
        super().__init__(message)

SavedAttributes.MAKE_PROPS()
SavedAttribute.MAKE_PROPS()
