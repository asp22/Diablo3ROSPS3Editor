
import proto_parsers.proto_message as pm
import proto_parsers.fixed32 as ppf32
from py_proto.base import Base

class Handle(Base):
    @classmethod
    def MAKE_PROPS(cls):
        cls._make_required_simple_value('game_balance_type', 1)
        cls._make_required_simple_value('gbid', 2)

    def __init__(self, message):
        super().__init__(message)

Handle.MAKE_PROPS()
