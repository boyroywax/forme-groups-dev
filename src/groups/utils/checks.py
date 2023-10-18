from ..base.types import LinearContainer, NamedContainer, BaseContainerTypes


def is_linear_container(item: BaseContainerTypes) -> bool:
    """
    Checks if item is a linear container
    """
    return isinstance(item, LinearContainer)


def is_named_container(item: BaseContainerTypes) -> bool:
    """
    Checks if item is a named container
    """
    return isinstance(item, NamedContainer)


def is_any_container(item: BaseContainerTypes) -> bool:
    """
    Checks if item is any container
    """
    if item is None:
        return False
    return is_linear_container(item) or is_named_container(item)


def _contains_sub_container(item: BaseContainerTypes) -> bool:
    """
    Checks if container contains a sub container
    """
    assert is_any_container(item), f"Expected a container, but received a non-container {item}"

    if is_linear_container(item):
        for value in item:
            return is_any_container(value)

    elif is_named_container(item):
        for value in item.values():
            return is_any_container(value)

    return False