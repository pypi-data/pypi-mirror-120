"""Checks Module.

This module defines objects common across checks.
"""
from dataclasses import dataclass
import functools
import pathlib
from typing import Callable, Any, Iterator, List, Tuple
from rich.live import Live
from rich.table import Table
from rich.console import Console
from .cli.cat import random_phrase, cat
from .utils import ensure_directory, _find_root

console: Console = Console()
"""Console object for printing output to terminal."""

CORRECT: str = "[green]:heavy_check_mark:[/green]"
"""Constant representing a pass."""

INCORRECT: str = "[red]:x:[/red]"
"""Constant representing a fail."""


@dataclass
class CheckResponse:
    """Check Reponse.

    A dataclass defining what the response of
    an individual checking function should return.

    Parameters
    ==========
        - name: str, a label for the checking function output.
        - result: bool, should be True if check function passes, False
        otherwise.
        - info: str, further information, typically about the reason for
        failure of a check function.
    """

    name: str
    """str, a label for the checking function output."""
    result: bool
    """bool, should be True if check function passes, False
        otherwise."""
    info: str
    """str, further information, typically about the reason for
        failure of a check function."""


@dataclass
class CollectionResponse:
    """Collection Response.

    A dataclass defining what the response from
    a collection of checks should return. Effectively
    adding a label to an individual CheckResponse
    that informs which group/category the function
    belongs to.

    Parameters
    ==========
        - group: str, a label for the group that a check function belongs to
        - result: CheckResponse, result from the checking function
    """

    group: str
    """str, a label for the group that a check function belongs to"""
    result: CheckResponse
    """CheckResponse, result from the checking function"""


def as_CheckResponse(func: Callable[[Any], Tuple[bool, str]]) -> Callable:
    """Create a CheckResponse.

    Wrap the Tuple[bool, str] result of
    a callable with a CheckResponse type output.

    This is convenient for allowing the function name
    at definition to be used as the name for the CheckResponse
    object.

    @param func: A Callable object that takes any arguments
        and returns a Tuple[bool, str]

    @returns: A Callable, original function definition with wrapped
        return value.
    """
    @functools.wraps(func)
    def inner_as_CheckResponse():
        x, y = func()
        return CheckResponse(func.__name__, x, y)
    return inner_as_CheckResponse


class CheckCollection:
    """Check Collection.

    A class that defines an object whose primary function is to
    allow grouping of one of more check functions into a topic.

    Objects of class CheckCollection are themselves Callable, returning
    a generator for the results of individual check functions within the
    collection.

    Methods
    =======
        - register: function closure (decorator) to add an additional
        Callable to the collection
        - unregister: remove Callable from collection by name
        - get_registered: return a list of the names of registered
        Callables

    Attributes
    ==========

    @ivar name: str a label for the collection
    @ivar __name__: see name, for compatibility with other functions
    @ivar collection: dictionary str -> Callable containing functions
       registered in the collection
    @ivar logging: bool, should output be logged to file
    @ivar issues: int, increments whenever a check function fails
    @ivar message: str, accumulates all messages from check functions
    """

    def __init__(self, name: str, logging: bool = True) -> None:
        """Initialise CheckCollection.

        @param name: str, a label for the collection
        @param logging: bool, should output be logged to file on calling
            check functions
        """
        self.name: str = name
        self.__name__: str = name
        self.collection: dict = dict()
        self.logging: bool = logging
        self.issues: int = 0
        self.message: str = ""

    def register(
        self, func: Callable[[Any], CheckResponse]
    ) -> Callable[[Any], CheckResponse]:
        """Add Callable to collection.

        Function closure, to be used as decorator::

            # e.g
            @GROUP.register
            def f(): pass

        Add a Callable, typically a function, to self.collection,
        associating the function with the group of similar checks.

        @param func: Callable that returns a CheckResponse

        @returns: Callable, after adding it to the self.collection dictionary.
        """
        self.collection[func.__name__] = func

        @functools.wraps(func)
        def inner_register():
            return func()
        return inner_register

    def unregister(self, name: str) -> None:
        """Unregister Callable from collection.

        Remove a Callable from the self.collection dictionary,
        on running checks the removed function will no longer
        be tested by grumpy.

        @param name: str, name of Callable to remove, see
            self.get_registered()

        @returns: None
        """
        if name not in self.collection.keys():
            raise ValueError(f"""{name} is not a registered function in this.collection.
            Registered functions are
            {self.get_registered()}
            """)
        self.collection.pop(name)
        return None

    def get_registered(self) -> List[str]:
        """Get registered function names.

        Get names of Callables in self.collection,
        equivalent to list(self.collection.keys())

        @returns: List[str]: list of names of functions in self.collection
        """
        return list(self.collection.keys())

    def __call__(self) -> Iterator[CollectionResponse]:
        """Call checks in self.collection.

        @returns Generator object yielding results of each check
        in self.collection.
        """
        if self.logging:
            ensure_directory("grumpy_report")
            fname = pathlib.Path(
                _find_root(),
                "grumpy_report",
                f"{self.name}.txt"
            )
            if fname.exists():
                fname.unlink()
        for k, v in self.collection.items():
            res = v()
            if self.logging:
                if not res.result:
                    with open(fname, "a") as f:
                        f.write(f"{res.name}\n\n, {res.info}\n\n")
            yield CollectionResponse(self.name, res)


class CheckCollectionGroup:
    """Check Collection Group.

    A class that defines an object whose primary function is to
    allow grouping of one of more CheckCollections (groups of check
    functions) into a topic.

    Objects of class CheckCollectionGroup are themselves Callable, creating
    and displaying a table as individual checks run.

    Methods
    =======

    register: function closure (decorator) to add an additional
        Callable to the collection
    unregister: remove Callable from collection by name
    get_registered: return a list of the names of registered
        Callables

    Attributes
    ==========

    @ivar collection: dictionary str -> Callable containing functions
        registered in the collection
    @ivar issues: int, increments whenever a check function fails
    """

    def __init__(self):
        """Initialse CheckCollectionGroup."""
        self.collection = dict()
        self.issues = 0

    def register(self, collection: CheckCollection):
        """Add Callable to collection.

        Add a Callable, typically a CheckCollection, to self.collection.

        @param collection: CheckCollection object.

        @returns: Callable (CheckCollection), after adding it
        to the self.collection dictionary.
        """
        self.collection[collection.name] = collection

        @functools.wraps(collection)
        def inner_register():
            return collection()
        return inner_register

    def unregister(self, name: str) -> None:
        """Unregister Callable from collection.

        Remove a Callable from the self.collection dictionary,
        on running checks the removed function will no longer
        be tested by grumpy.

        @param name: str, name of Callable to remove, see
            self.get_registered()
        @returns None
        """
        if name not in self.collection.keys():
            raise ValueError(f"""{name} is not a registered function in this.collection.
            Registered functions are
            {self.get_registered()}
            """)
        self.collection.pop(name)
        return None

    def get_registered(self) -> List[str]:
        """Get registered function names.

        Get names of Callables in self.collection,
        equivalent to list(self.collection.keys())

        @returns: List[str], list of names of functions in self.collection
        """
        return list(self.collection.keys())

    def __call__(self):
        """Call CheckCollectionGroup.

        Run all checks within the groups, drawing out a table
        in the console as the checks run.

        If any checks fail, exit with exitcode=1, else 0.
        """
        table = Table()
        table.add_column("Group")
        table.add_column("Check")
        table.add_column("Result")
        with Live(table, refresh_per_second=30):
            for _, collection in self.collection.items():
                gen = collection()
                for res in gen:
                    # res = func()
                    self.issues += not res.result.result
                    table.add_row(
                        res.group,
                        res.result.name,
                        (res.result.result and CORRECT) or INCORRECT
                    )
        if self.issues:
            console.print(random_phrase())
        else:
            console.print(cat, style="black on white")
            console.print("Great Work, I hate it.")
        if self.issues:
            exit(1)


def call_check_collection(collection: CheckCollection):
    """Run a CheckCollection group of checks.

    Created to allow the same table drawing output interface
    to be runnable for individual groups of check functions
    (a single CheckCollection object).

    @param collection: CheckCollection object

    Exits with exitcode = 1 if any checks fail, else 0.
    """
    issues = 0
    table = Table()
    table.add_column("Group")
    table.add_column("Check")
    table.add_column("Result")
    with Live(table, refresh_per_second=30):
        gen = collection()
        for res in gen:
            # res = func()
            issues += not res.result.result
            table.add_row(
                res.group,
                res.result.name,
                (res.result.result and CORRECT) or INCORRECT
            )
    if issues:
        console.print(random_phrase())
        exit(1)
    else:
        console.print(cat, style="black on white")
        console.print("Great Work, I hate it.")
