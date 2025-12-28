import inspect
from typing import TypeVar, Callable, Any

from turbolightdi.container import context

T = TypeVar("T", bound=type)
F = TypeVar("F", bound=Callable[..., Any])


def cy(cls: T) -> T:
    setattr(cls, "_is_cy", True)
    return cls


def borg(func: F) -> F:
    setattr(func, "_is_borg", True)
    hint = inspect.signature(func).return_annotation
    setattr(func, "_return_type", hint)
    return func


def component(cls=None, *, role="Component"):
    def decorator(cls):
        cls._is_component = True
        cls._turbodi_role = role
        if role == "Controller":
            cls._is_controller = True

        context.register_component(cls)
        return cls

    if cls is None:
        return decorator
    return decorator(cls)


Type = TypeVar("Type", bound=type)


def auto_configure(arg: Type | str | None = None, *, base_package: str | None = None):
    def decorator(cls: Type) -> Type:
        if not inspect.isclass(cls):
            raise TypeError("@configure must be used on a Class, not a function.")

        pkg = base_package or (
            arg if isinstance(arg, str) else cls.__module__.split(".")[0]
        )

        from .scanner import scan_packages

        scan_packages(pkg)

        cls._is_root = True
        return cls

    if inspect.isclass(arg):
        return decorator(arg)
    return decorator


def controller(cls):
    return component(cls, role="Controller")


def service(cls):
    return component(cls, role="Service")


def repository(cls):
    return component(cls, role="Repository")
