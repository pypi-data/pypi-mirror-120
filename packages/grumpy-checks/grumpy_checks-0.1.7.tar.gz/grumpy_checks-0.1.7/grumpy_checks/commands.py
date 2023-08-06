"""Centralise all commands.

This module looks to centralise all commands
that are intended to be exposed by the CLI
application.

Objects
=======
    - COMMANDS: dict, collection of commands
"""

from grumpy_checks.docs import check_docs
from .everything import check_everything
from .lint import check_lint
from .news import check_news

COMMANDS = {
    'everything': check_everything,
    'lint': check_lint,
    'news': check_news,
    'docs': check_docs
}
"""Collection of commands to expose to grumpy about <command>"""
