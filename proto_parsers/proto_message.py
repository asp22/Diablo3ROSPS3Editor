
import proto_parsers.integer as Integer
import proto_parsers.fixed64 as Fixed64
import proto_parsers.fixed32 as Fixed32
import proto_parsers.buffer  as Buffer
import proto_parsers.proto_item as Item
import proto_parsers.field_and_wire_type as FieldAndWireType
import proto_parsers.exceptions as exp

def _parse_message(data):
    items = []

    offset = 0
    while offset < len(data):
        try:
            read, fw = FieldAndWireType.decode(data[offset:])
        except:
            return None

        offset += read

        if fw.wire_type == 0:
            read, t = Integer.decode(data[offset:])
            offset += read
            items.append(Item.Item(fw, t))
        elif fw.wire_type == 1:
            read, t = Fixed64.decode(data[offset:])
            offset += read
            items.append(Item.Item(fw, t))
        elif fw.wire_type == 5:
            read, t = Fixed32.decode(data[offset:])
            offset += read
            items.append(Item.Item(fw, t))
        elif fw.wire_type == 2:
            # use interger to read length
            read, t = Integer.decode(data[offset:])
            offset += read
            payload = data[offset:offset+t.unsigned]
            read, t = Buffer.decode(payload)
            items.append(Item.Item(fw, t))
            offset += read
        else:
            return None
            #raise exp.UnsupportedWireType(f'unhandled: wire_type {fw}')

    return items

def expand_buffer(obj):
    assert isinstance(obj, Buffer.Buffer)
    item = obj.item
    expand_buffer_item(item)
    return isinstance(item.obj, Message)

def expand_buffer_item(item):
    assert isinstance(item.obj, Buffer.Buffer)
    size = item.obj.size
    if size == 0:
        return False

    try:
        read, t = _decode(item.obj.payload)
        item.obj = t
        assert read == size
        return True
    except (exp.UnsupportedWireType, exp.InsufficientData) as e:
        return False

def expand_buffer_to_message_recursive(message):
    def _expand_buffers(items):
        for i in items:
            if isinstance(i.obj, Buffer.Buffer):
                res = expand_buffer_item(i)
                if res:
                    sub_items = i.obj.items
                    _expand_buffers(sub_items)
            elif isinstance(i.obj, Message):
                expand_buffer_to_message_recursive(i.obj)

    _expand_buffers(message.items)

def shrink_message(obj):
    assert isinstance(obj, Message)
    item = obj.item
    shrink_message_item(item)

def shrink_message_item(i):
    out = i.obj.encode()
    i.obj = Buffer.Buffer(out)

def shrink_message_to_buffer_recursive(message_type):

    def shrink_message_items(items):
        for i in items:
            if isinstance(i.obj, Message):
                shrink_message_item(i)


    shrink_message_items(message_type.items)


class Message:
    def __init__(self, items):
        self.items = items

    def __getitem__(self, i):
        return self.items[i].obj

    def find_first_fn(self, fn):
        for i in self.items:
            if i.fn == fn:
                return [i]
        return []

    def find_all_fn(self, fn):
        out = []
        for i in self.items:
            if i.fn == fn:
                out.append(i)
        return out

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, i):
        self._item = i

    @property
    def count(self):
        return len(self.items)

    def encode(self):
        out = b''
        for i, it in enumerate(self.items):
            a = it.encode()
            out += a
        return out

    def to_string(self, indent=0):
        padding = '  '*indent
        out = ""
        for i in self.items:
            if isinstance(i.obj, Message):
                out+=padding+str(i._field_wire)+'\n'+padding+'{\n'
                out+=i.obj.to_string(indent+1)
                out+=padding+'}\n'
            else:
                out+=f'{padding}'+str(i)
                out+='\n'
        return out

    def inject_item(self, item):
        # iterate items, and find the best index to insert at
        target_field = item.fn
        def update():
            for i, it in enumerate(self.items):
                if it.fn == target_field:
                    self.items[i].obj = item.obj
                    return
                if it.fn > target_field:
                    self.items.insert(i, item)
                    return

            self.items.append(items)

        update()


    def __str__(self):
        return self.to_string()

def _decode(data):
    items = _parse_message(data)
    if items == None:
        raise exp.InsufficientData("Insufficient Data to parse mesage")
    return len(data), Message(items)

def decode(data):
    return _decode(data)
