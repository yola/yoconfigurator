class DotDict(dict):
    '''
    A dictionary with attribute access

    On creation/assignment, child dicts and list-of-dicts will be converted to
    DotDict.

    This is a cleaner way to read a dict in the templates
    instead of using dict['field'], can now use dict.field
    '''

    def __init__(self, *args, **kwargs):
        super(DotDict, self).__init__(*args, **kwargs)
        for key, value in self.iteritems():
            self[key] = self._convert_item(value)

    def __setitem__(self, key, value):
        value = self._convert_item(value)
        super(DotDict, self).__setitem__(key, value)

    def setdefault(self, key, default=None):
        default = self._convert_item(default)
        super(DotDict, self).setdefault(key, default)

    def update(self, *args, **kwargs):
        converted = DotDict(*args, **kwargs)
        super(DotDict, self).update(converted)

    def _convert_item(self, obj):
        '''Convert obj into a DotDict, or list of DotDict.
        Directly nested lists aren't supported.
        Returns the result
        '''
        if isinstance(obj, dict) and not isinstance(obj, DotDict):
            obj = DotDict(obj)
        elif isinstance(obj, list):
            # must mutate and not just reassign, otherwise it will
            # just use original object mutable/immutable
            for i, item in enumerate(obj):
                if isinstance(item, dict) and not isinstance(item, DotDict):
                    obj[i] = DotDict(item)
        return obj

    __setattr__ = __setitem__
    __getattr__ = dict.__getitem__
    __delattr__ = dict.__delitem__


class MissingValue(object):
    '''
    A placeholder value that must be replaced before serialising to JSON.
    Only subkey accesses can be caught by the methods below, but the JSON
    serialiazer will fail if it finds one of these objects.
    '''
    def __init__(self, name):
        self.name = name

    def __getattr__(self, k):
        raise AttributeError("No value provided for %s" % self.name)

    def get(self, k, default=None):
        raise KeyError("No value provided for %s" % self.name)

    __getitem__ = get


def merge_dicts(d1, d2):
    '''
    Merge dictionary d2 into d1, overriding entries in d1 with values from d2.

    d1 is mutated.
    '''
    if isinstance(d1, dict) and isinstance(d2, dict):
        for k, v in d2.iteritems():
            if k not in d1:
                d1[k] = v
            else:
                if isinstance(d1[k], dict) and isinstance(v, dict):
                    d1[k] = merge_dicts(d1[k], v)
                else:
                    d1[k] = v
    return d1
