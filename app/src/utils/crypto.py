import hashlib
from typing import List
from attrs import define, field, validators


def hash_sha256(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


@define(slots=True)
class MerkleTree:
    """A Merkle Tree object.
    """

    leaves: tuple[str] = field(default=[], validator=validators.instance_of(tuple))
    levels: tuple[tuple[str]] = field(default=[], validator=validators.instance_of(tuple))

    def __init__(self, hashed_data: tuple[str] = ()):
        self.leaves: tuple[str] = hashed_data
        self.levels: tuple[tuple[str]] = (self.leaves, )
        self.build()

    def build(self):
        level = self.leaves

        while len(level) > 1:
            # print(level)
            hashed_level = self.hash_level(level)
            # print(hashed_level)
            self.levels = self.levels + (hashed_level, )
            level = self.levels[-1]
            # print(level)

    def hash_level(self, level: List[str]) -> tuple[str]:
        hashed_level: tuple[str] = tuple()
        for i in range(0, len(level), 2):
            if i + 1 == len(level):
                hashed_level = hashed_level + (self.hash_func(level[i] + level[i]), )
            else:
                hashed_level = hashed_level + (self.hash_func(level[i] + level[i + 1]), )
            # print(hashed_level)
        return hashed_level

    @staticmethod
    def hash_func(data):
        return hash_sha256(data)

    def root(self) -> str | None:
        # print(self.leaves)
        if self.levels is None or self.levels == tuple(tuple[str]) or self.leaves == tuple[str]:
            return None
        return self.levels[-1][0]

    def verify(self, leaf_hash: str) -> bool:
        if leaf_hash not in self.leaves:
            return False
        index = self.leaves.index(leaf_hash)
        current_hash = self.leaves[index]
        for i in range(len(self.levels) - 1):
            if index % 2 == 0:
                current_hash = self.hash_func(current_hash + self.levels[i][index + 1])
            else:
                current_hash = self.hash_func(self.levels[i][index - 1] + current_hash)
            index //= 2
        return current_hash == self.root()

    def __str__(self) -> str:
        return f"{self.root()}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(root={self.root()})"
