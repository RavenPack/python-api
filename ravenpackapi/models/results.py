class Results(object):
    def __init__(self, data, name=None):
        self._data = data
        self.name = name

    @property
    def description(self):
        result = self.name + ". " if self.name else ""
        result += "%d records" % len(self._data)
        return result

    def __str__(self):
        return "Results %s" % self.description

    def __iter__(self):
        return self._data.__iter__()

    def __nonzero__(self):
        return bool(self._data)

    def __len__(self):
        return len(self._data)
