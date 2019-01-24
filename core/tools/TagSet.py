import pandas as pd

'''
    The tag smart manuf exclusive tag sets and their descriptions.
    These tags begin with \ABC[ and ends with \]
'''

class TagSet(dict):
    __slots__ = [
        "_tags",
        "_uniqids",
        "_tagtoids"
    ]

    def __init__(self, **kwargs):
        super(TagSet, self).__init__(**kwargs)
        self._uniqids = {}
        self._tagtoids = {}

    def getTagIds(self):
        if not self._uniqids:
            u, k = pd.factorize(list(self.keys()))
            self._uniqids = dict(zip(u, k))
            self._tagtoids = dict(zip(k, u))
        return self._uniqids

