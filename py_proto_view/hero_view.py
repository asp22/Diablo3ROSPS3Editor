
import py_proto_view.attribute_serializer_view
import py_proto_view.items_view

class SavedDefinitionView:
    def __init__(self, sd):
        self._sd = sd;

    def get_name(self):
        return self._sd.digest.hero_name.obj.string

    def get_level(self):
        return self._sd.digest.level.obj.unsigned // 2

    def set_level(self, v):
        v *= 2
        self._sd.digest.level.obj.unsigned = v

    def get_paragon_level(self):
        return self._sd.digest.dep_alt_level.obj.unsigned // 2

    def set_paragon_level(self, v):
        v = v * 2
        self._sd.digest.dep_alt_level.obj.unsigned = v
        self.get_paragon_attributes().reset()

    def get_paragon_attributes(self):
        return py_proto_view.attribute_serializer_view.HeroParagonAttributesView(self._sd.saved_attributes)
    
    def has_game_items(self):
        return self._sd.game_items != None

    def get_game_items(self):
        assert self.has_game_items()
        return py_proto_view.items_view.ItemListView(self._sd.game_items)

    def get_game_items_count(self):
        if self.has_game_items():
            return self.get_game_items().count()
        return 0
