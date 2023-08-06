"""General package utility functions."""

from typing import Callable, Any, Dict
import functools
import pathlib
import toml
from warnings import warn


def _find_root() -> pathlib.Path:
    """Find root of project.

    Assumes that this is a project that has been created using
    poetry and therefore has at least a pyproject.toml or poetry.lock file
    at its root

    @returns: pathlib.Path - estimate of root of project
    """
    cwd = pathlib.Path.cwd()
    while not (
        pathlib.Path(cwd, "pyproject.toml").exists() or
        pathlib.Path(cwd, "poetry.lock").exists() or
        pathlib.Path("/") == cwd
    ):
        cwd = cwd.parent
    return cwd


def ensure_directory(dir: str) -> None:
    """Ensure directory exists.

    @param dir: str, path to directory.
    @returns: None
    """
    pathlib.Path(dir).mkdir(parents=True, exist_ok=True)


def _with_str(func: Callable) -> Callable:
    class FuncName:
        def __call__(self, *args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)

        def __str__(self) -> str:
            return func.__name__
    return functools.wraps(func)(FuncName())


def has_pyproject_toml() -> bool:
    """Check whether there is a pyproject.toml file.

    @returns: bool - True if file exists
    """
    return pathlib.Path(_find_root(), "pyproject.toml").exists()


def detect_package_details() -> Dict:
    """Grab simple package details.

    @returns: dict{
        name: str,
        version: str
    }
    """
    retval = {
        'name': '',
        'version': ''
    }
    if has_pyproject_toml():
        x = toml.load(pathlib.Path(_find_root(), "pyproject.toml"))
        retval = {
            'name': x['tool']['poetry']['name'],
            'version': x['tool']['poetry']['version']
        }
    else:
        warn("No pyproject.toml file")
    return retval
