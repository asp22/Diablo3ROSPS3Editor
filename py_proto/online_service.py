
import proto_parsers.proto_message as pm
import proto_parsers.integer as ppi
from py_proto.base import Base

class ItemId(Base):
    @classmethod
    def MAKE_PROPS(cls):
        cls._make_required_simple_value('id_high', 1)
        cls._make_required_simple_value('id_low', 2)

    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        return f'high:{self.id_high.obj.unsigned} low:{self.id_low.obj.unsigned}'

ItemId.MAKE_PROPS()
