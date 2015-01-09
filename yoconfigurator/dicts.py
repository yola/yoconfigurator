"""Module for DotDict data structure and DotDict helpers."""


class DotDict(dict):

    """
    A dictionary with attribute access.

    On creation/assignment, child dicts and list-of-dicts will be converted to
    DotDict.

    This is a cleaner way to read a dict in the templates
    instead of using dict['field'], can now use dict.field
    """

    def __init__(self, *args, **kwargs):
        super(DotDict, self).__init__(*args, **kwargs)
        for key, value in self.iteritems():
            self[key] = self._convert_item(value)

    def __setitem__(self, dottedkey, value):
        value = self._convert_item(value)
        if '.' not in dottedkey:
            return super(DotDict, self).__setitem__(dottedkey, value)
        key, dottedkey = dottedkey.split('.', 1)
        target = self[key] = self.get(key, DotDict())
        target[dottedkey] = value

    def __getattr__(self, attr):
        if attr in self:
            return self[attr]
        raise AttributeError

    def __getitem__(self, dottedkey):
        if '.' not in dottedkey:
            return super(DotDict, self).__getitem__(dottedkey)
        key, dottedkey = dottedkey.split('.', 1)
        target = super(DotDict, self).__getitem__(key)
        return target[dottedkey]

    def setdefault(self, key, default=None):
        default = self._convert_item(default)
        super(DotDict, self).setdefault(key, default)

    def update(self, *args, **kwargs):
        converted = DotDict(*args, **kwargs)
        super(DotDict, self).update(converted)

    def _convert_item(self, obj):
        """
        Convert obj into a DotDict, or list of DotDict.

        Directly nested lists aren't supported.
        Returns the result
        """
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
    __delattr__ = dict.__delitem__


class DeletedValue(object):

    """
    A DotDict value that instructs merging to remove the config key.

    When used as a placeholder, any exisiting value and tree will be removed
    as well as the key DeletedValue() is assigned to.
    """


class MissingValue(object):

    """
    A placeholder value that must be replaced before serialising to JSON.

    Only subkey accesses can be caught by the methods below, but the JSON
    serialiazer will fail if it finds one of these objects.
    """

    def __init__(self, name=None):
        self.name = name

    def __getattr__(self, k):
        raise AttributeError("No value provided for %s" % self.name)

    def get(self, k, default=None):
        raise KeyError("No value provided for %s" % self.name)

    __getitem__ = get


def merge_dicts(d1, d2, _path=None):
    """
    Merge dictionary d2 into d1, overriding entries in d1 with values from d2.

    d1 is mutated.

    _path is for internal, recursive use.
    """
    if _path is None:
        _path = ()
    if isinstance(d1, dict) and isinstance(d2, dict):
        for k, v in d2.iteritems():
            if isinstance(v, MissingValue) and v.name is None:
                v.name = '.'.join(_path + (k,))

            if isinstance(v, DeletedValue):
                d1.pop(k, None)
            elif k not in d1:
                if isinstance(v, dict):
                    d1[k] = merge_dicts({}, v, _path + (k,))
                else:
                    d1[k] = v
            else:
                if isinstance(d1[k], dict) and isinstance(v, dict):
                    d1[k] = merge_dicts(d1[k], v, _path + (k,))
                elif isinstance(d1[k], list) and isinstance(v, list):
                    # Lists are only supported as leaves
                    d1[k] += v
                elif isinstance(d1[k], MissingValue):
                    d1[k] = v
                elif d1[k] is None:
                    d1[k] = v
                elif type(d1[k]) == type(v):
                    d1[k] = v
                else:
                    raise TypeError('Refusing to replace a %s with a %s'
                                    % (type(d1[k]), type(v)))
    else:
        raise TypeError('Cannot merge a %s with a %s' % (type(d1), type(d2)))

    return d1


def filter_dict(unfiltered, filter_keys):
    """Return a subset of a dictionary using the specified keys."""
    filtered = DotDict()
    for k in filter_keys:
        filtered[k] = unfiltered[k]
    return filtered
