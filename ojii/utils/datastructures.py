class NULL: pass


class AutoDictionary(dict):
    """
    ad = AutoDictionary(list)
    ad['hello'].append('world')
    => ad = {'hello': ['world']}
    """
    def __init__(self, factory=NULL, *args, **kwargs):
        assert callable(NULL), "AutoDictionary requires the `factory` argument."
        self._factory = factory
        
    def __getitem__(self, item):
        if item not in self:
            self[item] = self._factory()
        return super(AutoDictionary, self).__getitem__(item)