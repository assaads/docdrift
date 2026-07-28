from __future__ import annotations

from collections.abc import Callable


class UnknownExtractor(KeyError):
    """Raised when a manifest names an extractor that isn't registered."""


class ExtractorRegistry:
    _by_name: dict[str, type] = {}

    @classmethod
    def register(cls, name: str) -> Callable[[type], type]:
        def wrap(ext_cls: type) -> type:
            assert hasattr(ext_cls, "extract"), f"{ext_cls} must implement extract()"
            ext_cls.name = name  # type: ignore[attr-defined]
            cls._by_name[name] = ext_cls
            return ext_cls
        return wrap

    @classmethod
    def get(cls, name: str):
        try:
            return cls._by_name[name]()
        except KeyError as e:
            raise UnknownExtractor(
                f"unknown extractor {name!r}; available: {sorted(cls._by_name)}"
            ) from e

    @classmethod
    def names(cls) -> list[str]:
        return sorted(cls._by_name)


# Convenience module-level decorator.
def register(name: str) -> Callable[[type], type]:
    return ExtractorRegistry.register(name)
