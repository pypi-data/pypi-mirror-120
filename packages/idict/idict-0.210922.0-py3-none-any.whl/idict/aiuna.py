"""
lazy
ilazy
ldict
"""
from dataclasses import dataclass

from test.pickletester import H


@dataclass
class LazyVal:
    pass


class FrozenLazyDict:
    def __getitem__(self, item):
        pass


class IdFrozenLazyDict(FrozenLazyDict):
    def __init__(self, ids=None, hoshes=None, **kwargs):
        super().__init__(kwargs)
        if ids:
            if hoshes:
                raise Exception("Cannot provide arguments for both 'id' and 'hoshes'.")
            hoshes = {k: H.fromid(v) for k, v in ids}
        elif hoshes is None:
            hoshes = {}
        self.blobs, self.hashes, self.hoshes = {}
        for k, v in kwargs:
            if k in hoshes:
                self.hoshes[k] = hoshes[k]
            else:
                self.blobs[k] = v * 0
                self.hashes[k] = H(self.blob[k])
                self.hoshes[k] = self.hashes[k] ** 0


class LazyDict:  # ldict
    #  self.     FrozenLazyDict
    pass


class IdLazyDict:  # idict
    #  self.     IdFrozenLazyDict
    pass
