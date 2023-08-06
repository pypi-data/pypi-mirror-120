"""Check Everything.

This module collates all the package checks
into a single CheckCollectionGroup to facilitate easy running of
all grumpy checks.

Objects
-------
    - ALL_CHECKS: CheckCollectionGroup of all check functions.

Functions
---------
    - check_everything: run all checks in all registered collections.
"""

from grumpy_checks.docs import DOCS_CHECKS
from .lint import LINT_CHECKS
from .news import NEWS_CHECKS
from .checks import CheckCollectionGroup


ALL_CHECKS = CheckCollectionGroup()
"""All checks CheckCollectionGroup object."""


def check_everything():
    """Run all registered checks in all categories.

    This is really just a wrapper for the Callable
    object ALL_CHECKS
    """
    return ALL_CHECKS()


ALL_CHECKS.register(LINT_CHECKS)
ALL_CHECKS.register(NEWS_CHECKS)
ALL_CHECKS.register(DOCS_CHECKS)
