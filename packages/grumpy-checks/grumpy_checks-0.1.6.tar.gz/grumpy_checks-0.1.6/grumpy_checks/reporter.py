from rich.console import Console
from typing import Callable, Tuple
from functools import wraps


console = Console()


def reporter(happy: str, grumpy: str) -> Callable:
    def messenger_inner(func: Callable) -> Callable:
        @wraps
        def eval() -> bool:
            res = func()
            if res:
                console.print(happy)
            else:
                console.print(grumpy)
            return res
        return eval
    return messenger_inner


class Reporter:
    """A decorator class for console reporting

    This class can be used as a decorator to add success and fail
    text to the checking functions. Defaults to a thumbs up or
    thumbs down followed by the function name for pass and fail
    respectively.

    Messages in the text are printed using a rich.Console object
    so colours and emojis are also allowed.
    """

    def __init__(self, func, happy=None, grumpy=None):
        """Create a Reporter object

        Parameters
        ----------
        func: Callable -> Tuple[bool, str]
            Callable object, typically a function definition to be decorated
        happy: str
            Message to display on pass, if None f':thumbs_up: {func.__name__}'
        grumpy: str
            Message to display on fail, if None f':thumbs_up: {func.__name__}'
        """
        self.func = func
        self.happy = happy or f':thumbs_up: {func.__name__}'
        self.grumpy = grumpy or f':thumbs_down: {func.__name__}'
        self.__name__ = func.__name__
        # (happy: str, grumpy: str) -> Callable:

    def __call__(self, *args, **kwargs) -> Tuple[bool, str]:
        res, string = self.func(*args, **kwargs)
        if res:
            console.print(self.happy)
        else:
            console.print(self.grumpy)
        return res, string
