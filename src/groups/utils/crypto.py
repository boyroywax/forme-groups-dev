import hashlib
from attrs import define, field, validators


def hash_sha256(data: str | bytes) -> str:
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(data).hexdigest()


@define(slots=True)
class MerkleTree:
    """A Merkle Tree object.
    """

    leaves: tuple[str, ...] = field(
        default=[],
        validator=validators.deep_iterable(validators.instance_of(str),
        iterable_validator=validators.instance_of(tuple)))
    
    levels: tuple[tuple[str, ...]] = field(
        default=[],
        validator=validators.deep_iterable(validators.deep_iterable(validators.instance_of(str),
        iterable_validator=validators.instance_of(tuple)),
        iterable_validator=validators.instance_of(tuple)))

    def __init__(self, hashed_data: tuple[str, ...] = ()) -> None:
        self.leaves = hashed_data
        self.levels = (self.leaves, )
        self.build()

    def build(self) -> None:
        level = self.leaves

        if len(self.levels[0]) == 1:
            self.levels = self.levels + ((self._hash_items(level[0]), ), )

        while len(level) > 1:
            hashed_level = self.hash_level(level)
            self.levels = self.levels + (hashed_level, )

            level = self.levels[-1]

    @staticmethod
    def _hash_func(data: str | bytes) -> str:
        return hash_sha256(data)

    @staticmethod
    def _hash_items(item1: str | bytes | None = None, item2: str | bytes | None = None) -> str:
        # assert ((type(item1) is str) or (type(item2) is None)), f"{type(item2)} must be str or None"
        if item1 is None:
            raise ValueError(f'item1 cannot be None, but received {T}')

        if item2 is None:
            return MerkleTree._hash_items(item1, item1)

        return MerkleTree._hash_func(item1 + item2)

    @staticmethod
    def hash_level(level: tuple[str | bytes, ...]) -> tuple[str, ...]:
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
