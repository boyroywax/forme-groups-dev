import hashlib
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

        if len(self.levels[0]) == 1:
            self.levels = self.levels + ((self._hash_items(level[0]), ), )

        while len(level) > 1:
            hashed_level = self.hash_level(level)
            self.levels = self.levels + (hashed_level, )

            level = self.levels[-1]

    @staticmethod
    def _hash_func(data) -> str:
        return hash_sha256(data)

    @staticmethod
    def _hash_items(item1: str = None, item2: str = None) -> str:
        if item1 is None:
            raise ValueError('item1 cannot be None')

        if item2 is None:
            return MerkleTree._hash_items(item1, item1)

        return MerkleTree._hash_func(item1 + item2)

    @staticmethod    
    def hash_level(level: tuple[str]) -> tuple[str]:
        hashed_level = ()
        for i in range(0, len(level), 2):
            if (i + 1) % 2 != 0 and i == len(level) - 1:
                hashed_level = hashed_level + (MerkleTree._hash_items(level[i]), )
            elif (i + 1 <= len(level) - 1):
                hashed_level = hashed_level + (MerkleTree._hash_items(level[i], level[i + 1]), )
            else:
                raise Exception("This should never happen")

        return hashed_level

    def _find_levels_count(self) -> int:
        return len(self.levels)

    def root(self) -> str | None:
        if self.levels[-1] is None or len(self.levels) == 0 or len(self.leaves) == 0:
            return None
        return self.levels[-1][0]

    def verify(self, leaf_hash: str) -> bool:
        if leaf_hash not in self.leaves:
            return False
        else:
            return True

    def __str__(self) -> str:
        return f"{self.root()}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(root={self.root()})"
