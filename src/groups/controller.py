from typing import Optional

from .unit import GroupUnit, Credential, Data, Owner, Nonce
from .pool import Pool


class Controller:
    """The Manage class holds the Group Manage data
    """

    def __init__(self, pool: Optional[Pool] = None):
        self._pool = pool