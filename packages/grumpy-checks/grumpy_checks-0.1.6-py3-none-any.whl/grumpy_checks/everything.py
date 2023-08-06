from .lint import LINT_CHECKS
from .news import NEWS_CHECKS
from .checks import CheckCollectionGroup


ALL_CHECKS = CheckCollectionGroup()


def check_everything():
    """Run all registered checks in all categories

    This is really just a wrapper for the Callable
    object ALL_CHECKS
    """
    return ALL_CHECKS()


ALL_CHECKS.register(LINT_CHECKS)
ALL_CHECKS.register(NEWS_CHECKS)
