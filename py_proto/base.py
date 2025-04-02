
from _pytest import outcomes
import proto_parsers.proto_message as pm
import proto_parsers.proto_item as pi
import proto_parsers.field_and_wire_type as fw
from types import MethodType
import inspect

def _make_get(field_name):
    private_name = f'_{field_name}'
    def _get(self):
        return getattr(self, private_name)
    return _get


class Base:
    def __init_subclass__(cls):
        cls._properties_init_tasks = []

    def __init__(self, message):
        self.message = message

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, msg):
        self._message = msg
        self._init_properties()

    def _init_properties(self):
        for t in self._properties_init_tasks:
            t(self)


    @classmethod
    def _make_property_generic(cls, field_name, fn, _set):
        _get = _make_get(field_name)

        getter = f'get_{field_name}'
        setter = f'set_{field_name}'
        
        setattr(cls, getter, _get)
        setattr(cls, setter, _set)

        cls_getter = getattr(cls, getter)
        cls_setter = getattr(cls, setter)
        setattr(cls, field_name, property(fget=cls_getter, fset=cls_setter))

        def init(self):
            _set(self, self.message)

        cls._properties_init_tasks.append(init)


    @classmethod
    def _make_required_simple_value(cls, field_name, fn):
        private_name = f'_{field_name}'
        def _set(self, message):
            items = message.find_first_fn(fn)
            setattr(self, private_name, items[0])
        return cls._make_property_generic(field_name, fn, _set)

    @classmethod
    def _make_optional_simple_value(cls, field_name, fn):
        private_name = f'_{field_name}'
        def _set(self, message):
            items = message.find_first_fn(fn)
            if len(items) == 1:
                setattr(self, private_name, items[0])
            else:
                setattr(self, private_name, None)
        return cls._make_property_generic(field_name, fn, _set)

    @classmethod
    def _make_repeated_simple_value(cls, field_name, fn):
        private_name = f'_{field_name}'
        def _set(self, message):
            items = message.find_all_fn(fn)
            setattr(self, private_name, items)
        return cls._make_property_generic(field_name, fn, _set)


    @classmethod
    def _make_required_message(cls, field_name, fn, message_type):
        private_name = f'_{field_name}'
        def _set(self, message):
            item = message.find_first_fn(fn)[0]
            pm.expand_buffer_item(item)
            m = message_type(item.obj)
            setattr(self, private_name, m)
        return cls._make_property_generic(field_name, fn, _set)

    @classmethod
    def _make_optional_message(cls, field_name, fn, message_type):
        private_name = f'_{field_name}'
        def _set(self, message):
            items = message.find_first_fn(fn)
            if len(items) == 1:
                if pm.expand_buffer_item(items[0]):
                    m = message_type(items[0].obj)
                    setattr(self, private_name, m)
                    return
            setattr(self, private_name, None)
        return cls._make_property_generic(field_name, fn, _set)

    @classmethod
    def _make_repeated_message(cls, field_name, fn, message_type):
        private_name = f'_{field_name}'
        def _set(self, message):
            out = []
            items = self.message.find_all_fn(fn)
            for i in items:
                pm.expand_buffer_item(i)
                out.append(message_type(i.obj))
            setattr(self, private_name, out)
        return cls._make_property_generic(field_name, fn, _set)


    def create_child_optional_message(self, fn, byte_str, child_type):
        raw_bytes = bytes.fromhex(byte_str)
        read, t = pm.decode(raw_bytes)

        # give message to child_type and allow it to expand any buffers
        child_type(t)

        # make field and wire object
        f_w = fw.FieldAndWireType(fn, 2)
        item = pi.Item(f_w, t)

        # now try to add it to self.message
        # iterate items, and find the best index to insert at
        def update():
            target_field = item.fn
            for i, it in enumerate(self.message.items):
                if it.fn == target_field:
                    self.message.items[i].obj = item.obj
                    return
                if it.fn > target_field:
                    self.message.items.insert(i, item)
                    return
            self.message.items.append(item)
        update()

        # collapse message
        pm.shrink_message_to_buffer_recursive(self.message)
        self._init_properties()

    def create_child_repeated_message(self, fn, byte_str, child_type):
        raw_bytes = bytes.fromhex(byte_str)
        read, t = pm.decode(raw_bytes)

        # give message to child_type and allow it to expand any buffers
        child_type(t)

        # make field and wire object
        f_w = fw.FieldAndWireType(fn, 2)
        item = pi.Item(f_w, t)

        # now try to add it to self.message
        # iterate items, and find the best index to insert at
        def update():
            target_field = item.fn
            for i, it in enumerate(reversed(self.message.items)):
                pos = len(self.message.items) - 1 - i
                if it.fn <= target_field:
                    self.message.items.insert(pos+1, item)
                    return
            self.message.items.append(item)
        update()

        # collapse message
        pm.shrink_message_to_buffer_recursive(self.message)
        self._init_properties()

    def create_child_optional_simple(self, fn, byte_str):
        raw_bytes = bytes.fromhex(byte_str)
        read, t = pm.decode(raw_bytes)

        item = t.items[0]

        # now try to add it to self.message
        # iterate items, and find the best index to insert at
        def update():
            target_field = item.fn
            for i, it in enumerate(self.message.items):
                if it.fn == target_field:
                    self.message.items[i].obj = item.obj
                    return
                if it.fn > target_field:
                    self.message.items.insert(i, item)
                    return
            self.message.items.append(item)
        update()

        # collapse message
        pm.shrink_message_to_buffer_recursive(self.message)
        self._init_properties()

    def create_child_repeated_simple(self, fn, byte_str):
        raw_bytes = bytes.fromhex(byte_str)
        read, t = pm.decode(raw_bytes)

        item = t.items[0]

        # now try to add it to self.message
        # iterate items, and find the best index to insert at
        def update():
            target_field = item.fn
            for i, it in enumerate(reversed(self.message.items)):
                pos = len(self.message.items) - 1 - i
                if it.fn <= target_field:
                    self.message.items.insert(pos+1, item)
                    return
            self.message.items.append(item)
        update()

        # collapse message
        pm.shrink_message_to_buffer_recursive(self.message)
        self._init_properties()

    def clear_child_repeated_message(self, fn):
        def remove():
            reduced_items = [it for it in self.message.items if it.fn != fn]
            self.message.items = reduced_items
        remove()

        # collapse message
        pm.shrink_message_to_buffer_recursive(self.message)
        self._init_properties()
