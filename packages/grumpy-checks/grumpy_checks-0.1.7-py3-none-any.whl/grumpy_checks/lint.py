"""Check lint.

This module defines and registers the various lint checking
functions. By design all checks are registered by default
and must be explicilty unregistered (grumpy.lint.unregister(name: str))
if desired to be skipped.

This module contains the following functions:

    * has_flake8 - ensures that a .flake8 file exists
    * run_flake8 - run the flake8 linter and capture the output

The LINT_CHECKS Callable object is a CheckCollection which contains
the register of the current lint checks, see grumpy.lint.LINT_CHECKS.collection

New functions that return a CheckResponse object can be added to the register
with LINT_CHECKS.register(func: Callable[[Any], CheckResponse])
"""

import pathlib
import subprocess
from typing import Iterator, Tuple

from .checks import (CheckCollection, CheckResponse, as_CheckResponse,
                     call_check_collection)
from .utils import _find_root

LINT_CHECKS = CheckCollection("lint")
"""Test docs"""


def check_lint() -> Iterator[CheckResponse]:
    """Run all registered lint checks.

    This is really just a wrapper for LINT_CHECKS()
    callable object, that adds a table summary of output
    from the resultant generator.
    """
    return call_check_collection(LINT_CHECKS)


@LINT_CHECKS.register
@as_CheckResponse
def has_flake8() -> Tuple[bool, str]:
    """Check for the existence of a flake 8 file.

    @returns: CheckResponse detailing result of test.
    """
    retval = True, ""
    if not pathlib.Path(_find_root(), ".flake8").exists():
        retval = False, "Missing .flake8 file"
    return retval


def _flake8_process():
    """Run flake8.

    Run flake8 from the root of the project.

    Returns
    -------
    CompletedProcess object with
        - stdout
        - stderr
        - returncode
    amongst other attributes.
    """
    return subprocess.run(
            'flake8', capture_output=True,
            cwd=_find_root()
    )


@LINT_CHECKS.register
@as_CheckResponse
def run_flake8() -> Tuple[bool, str]:
    """Run flake8 linter.

    flake8 is run on a subprocess with any output captured and returned.

    Returns
    -------
    CheckResponse detailing result of check.
    """
    # only run if there is a flake8 file
    if not has_flake8().result:
        retval = False, "No flake 8 file"
    else:
        retval = True, ""
        output = _flake8_process()
        if output.returncode:
            retval = False, '\n'.join(
                [output.stdout.decode('utf8'), output.stderr.decode('utf8')])
    return retval
