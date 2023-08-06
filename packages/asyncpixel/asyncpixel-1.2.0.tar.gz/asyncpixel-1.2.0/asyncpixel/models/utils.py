"""Utils for pydantic models."""
from typing import Any
from typing import Dict
from typing import Optional

from pydantic import BaseModel
from pydantic import root_validator


def to_camel(string: str) -> str:
    """Convert str to camel case.

    Args:
        string (str): input.

    Returns:
        str: camelCase version of str.
    """
    char = string.split("_")[0]
    if len(string.split("_")) != 0:
        char += "".join(word.capitalize() for word in string.split("_")[1:])
    return char


class BaseNestingSupport(BaseModel):
    """Base nestring support loader."""

    @root_validator(pre=True)
    def traverse_sources(  # noqa: D102,
        cls, values: Dict[str, Any]  # noqa: B902, N805
    ) -> Optional[Any]:
        for (name, field) in cls.__fields__.items():
            source_selector = field.field_info.extra.get("source")
            if source_selector is not None:
                source_path = source_selector.split(".")

                if not len(source_path) > 0:
                    raise ValueError(
                        f"{cls.__name__}: Invalid "  # type: ignore
                        f"source path: '{source_selector}'"
                    )

                pointer = values
                for selector in source_path:
                    if selector not in pointer:
                        if not field.required:
                            _pointer = None
                            break

                        raise ValueError(
                            f"{cls.__name__}: Value for"  # type: ignore
                            f" '{selector}' missing, path: "
                            f"'{source_selector}'"
                        )

                    _pointer = pointer.get(selector)

                values[name] = _pointer

        return values

    class Config:
        """Config."""

        extra = "ignore"
