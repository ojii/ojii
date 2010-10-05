from lxml import objectify


class Iterate(object):
    def __init__(self, *args, **kwargs):
        self.data = kwargs
        self.firstonly = len(args) == 1 and args[0]
        
    def parse(self, node):
        data = {}
        for key, value in self.data.items():
            subnode = getattr(node, key, None)
            if subnode is not None:
                values = [value.parse(childnode) for childnode in subnode]
                if self.firstonly:
                    data[key] = values[0]
                else:
                    data[key] = values
        return data
    
class FlatIterate(Iterate):
    default = []
    def __init__(self, key, child, firstonly=False):
        self.key = key
        self.child = child
        self.firstonly = firstonly
        
    def parse(self, root):
        subnode = getattr(root, self.key, None)
        if subnode is not None:
            data = [self.child.parse(node) for node in subnode]
            if self.firstonly:
                return data[0]
            return data
        return []


class Dictionary(object):
    default = {}
    def __init__(self, **kwargs):
        self.data = kwargs
        
    def parse(self, node):
        data = {}
        for key, value in self.data.items():
            if hasattr(node, key):
                try:
                    data[key] = value.parse(getattr(node, key))
                except TypeError:
                    print "could not get '%s' in '%s'" % (key, value)
                    raise
            else:
                data[key] = value.default
        return data


class Attribute(object):
    def __init__(self, name, typecast=unicode, default=None):
        self.name = name
        self.typecast = typecast
        self.default = default
        
    def parse(self, node):
        obj = getattr(node, self.name)
        if callable(obj):
            obj = obj()
        try:
            value = self.typecast(obj)
        except TypeError:
            print "could not cast '%s' to type using '%s' for '%s'" % (obj, self.typecast, self.name)
            raise
        return value
    
def xmlparse(fobj, definition):
    tree = objectify.parse(fobj)
    root = tree.getroot()
    return definition.parse(root)