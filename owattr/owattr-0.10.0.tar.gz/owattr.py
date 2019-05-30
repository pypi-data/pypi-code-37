from typing import (
    Any,
    Callable,
    Dict,
    Type,
)

__all__ = ['from_dict']
__author__ = "Motoki Naruse"
__copyright__ = "Motoki Naruse"
__credits__ = ["Motoki Naruse"]
__email__ = "motoki@naru.se"
__license__ = "MIT"
__maintainer__ = "Motoki Naruse"
__version__ = "0.10.0"


def from_dict(target_object: object, new_attrs: Dict[str, str]) -> None:
    if hasattr(target_object, '__all__'):
        # mypy says object doesn't have __all__, but module is sub type of
        # object.
        keys = target_object.__all__  # type: ignore
    else:
        keys = (key for key in dir(target_object) if not key.startswith('_'))

    for key in keys:
        if key not in new_attrs:
            continue

        original_attr = getattr(target_object, key)
        if isinstance(original_attr, Callable):  # type: ignore
            continue

        new_attr = _cast_value(new_attrs[key], type(original_attr))
        setattr(target_object, key, new_attr)


def _cast_value(new_value: str, OriginalType: Type) -> Any:
    # bool is a special case because bool('false') is True!
    if OriginalType is bool:
        if new_value in {'true', 'True'}:
            return True
        if new_value in {'', 'false', 'False'}:
            return False
        raise ValueError(new_value)

    return OriginalType(new_value)
