from typing import Callable, Any
import functools
import pathlib
import toml
from pathlib import Path


def ensure_directory(dir: str):
    Path(dir).mkdir(parents=True, exist_ok=True)


def with_str(func: Callable) -> Callable:
    class FuncName:
        def __call__(self, *args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)

        def __str__(self) -> str:
            return func.__name__
    return functools.wraps(func)(FuncName())


def create_register(d: dict) -> Callable:
    def wrapper_register(func: Callable) -> Callable:
        d[func.__name__] = func

        @functools.wraps(func)
        def inner_register():
            return func()
        return inner_register
    return wrapper_register


def create_unregister(d: dict) -> Callable:
    def wrapper_unregister(func: Callable) -> Callable:

        @functools.wraps(func)
        def inner_unregister(name: str) -> None:
            d.pop(name)
            return None
        return inner_unregister
    return wrapper_unregister


def has_pyproject_toml():
    """Check whether there is a pyproject.toml file
    """
    return pathlib.Path("pyproject.toml").exists()


def detect_package_details():
    """Grab simple package details

    Returns
    -------
    {
        name: str,
        version: str
    }
    """
    retval = {
        'name': '',
        'version': ''
    }
    if has_pyproject_toml():
        x = toml.load("pyproject.toml")
        retval = {
            'name': x['tool']['poetry']['name'],
            'version': x['tool']['poetry']['version']
        }
    return retval
