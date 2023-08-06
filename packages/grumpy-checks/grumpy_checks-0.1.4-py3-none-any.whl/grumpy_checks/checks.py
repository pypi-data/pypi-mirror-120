from dataclasses import dataclass
import functools
from pathlib import Path
from typing import Callable, Any, Iterator, List, Tuple
from rich.live import Live
from rich.table import Table
from rich.console import Console
from .cli.cat import random_phrase, cat
from .utils import ensure_directory

console = Console()

CORRECT = "[green]:heavy_check_mark:[/green]"
INCORRECT = "[red]:x:[/red]"


@dataclass
class CheckResponse:
    name: str
    result: bool
    info: str


@dataclass
class CollectionResponse:
    group: str
    result: CheckResponse


def as_CheckResponse(func: Callable[[Any], Tuple[bool, str]]):
    """Wrap the Tuple[bool, str] result of
    a callable with a CheckResponse type output.

    This is convenient for allowing the function name
    at definition to be used as the name for the CheckResponse
    object
    """
    @functools.wraps(func)
    def inner_as_CheckResponse():
        x, y = func()
        return CheckResponse(func.__name__, x, y)
    return inner_as_CheckResponse


class CheckCollection:
    def __init__(self, name: str, logging: bool = True) -> None:
        self.name = name
        self.__name__ = name
        self.collection = dict()
        self.logging = logging
        self.issues = 0
        self.message = ""

    def register(
        self, func: Callable[[Any], CheckResponse]
    ) -> Callable[[Any], CheckResponse]:
        self.collection[func.__name__] = func

        @functools.wraps(func)
        def inner_register():
            return func()
        return inner_register

    def unregister(self, name: str) -> None:
        if name not in self.collection.keys():
            raise ValueError(f"""{name} is not a registered function in this.collection.
            Registered functions are
            {self.get_registered()}
            """)
        self.collection.pop(name)
        return None

    def get_registered(self) -> List[str]:
        return list(self.collection.keys())

    def __call__(self) -> Iterator[CollectionResponse]:
        if self.logging:
            ensure_directory("grumpy_report")
            fname = Path("grumpy_report", f"{self.name}.txt")
            if fname.exists():
                fname.unlink()
        for k, v in self.collection.items():
            res = v()
            if self.logging:
                if not res.result:
                    with open(fname, "a") as f:
                        f.write(f"{res.name}\n\n, {res.info}\n\n")
            yield CollectionResponse(self.name, res)
#             if not res.result:
#                 issues += 1
#                 message += f"""
# {res.name}

# {res.info}
#                 """
#         self.issues += issues
#         self.message += message


class CheckCollectionGroup:
    def __init__(self):
        self.collection = dict()
        self.issues = 0

    def register(self, collection: CheckCollection):
        self.collection[collection.name] = collection

        @functools.wraps(collection)
        def inner_register():
            return collection()
        return inner_register

    def __call__(self):
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


def call_check_collection(collection: CheckCollection):
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
    else:
        console.print(cat, style="black on white")
        console.print("Great Work, I hate it.")


class RunnableChecks:
    def __init__(self, checks: dict, fstub: str, name: str = None) -> None:
        self.fstub = fstub
        self.checks = checks
        self.results = dict()
        self.strings = dict()
        self.issues = 0
        self.name = name or fstub

    def __call__(self, *args, **kwargs):
        for k, v in self.checks.items():
            res, string = v()
            self.issues += not res
            self.strings[k] = string
            self.results[k] = res
            yield self.name, k, res, string, self.fstub
