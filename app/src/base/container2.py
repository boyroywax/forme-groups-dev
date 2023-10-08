from attrs import define, field, validators
from typing import Optional, TypeAlias


from .interface import BaseInterface
from .types import UnitValueTypes, UnitTypes, NamedContainer, LinearContainer, Containers
from .value import BaseValue
from .exceptions import GroupBaseContainerException