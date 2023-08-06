"""Documentation checks.

This module collates check functions related
to checking the quality of documentation in
a project.

Objects
=======
DOCS_CHECKS: CheckCollection, the various functions to check

Functions
=========
check_docs: run all registered doc checking functions
run_pydocstyle: Run pydocstyle documentation style checker
"""

import subprocess
from typing import Iterator
from .checks import (
    CheckCollection, CheckResponse,
    as_CheckResponse, call_check_collection
)
from .utils import _find_root


DOCS_CHECKS: CheckCollection = CheckCollection("docs")
"""CheckCollection object for all documentation checks."""


def check_docs() -> Iterator[CheckResponse]:
    """Run all doc checking functions.

    Returns
    -------
    Generator of results from the DOCS_CHECKS functions
    """
    return call_check_collection(DOCS_CHECKS)


@DOCS_CHECKS.register
@as_CheckResponse
def run_pydocstyle() -> CheckResponse:
    """Run pydocstyle checks.

    Run pydocstyle at the root of the project,
    capturing any documentation style issues.

    Returns
    -------
    CheckResponse object detailing result of check.
    """
    retval = True, ""
    output = subprocess.run(
        'pydocstyle', capture_output=True,
        cwd=_find_root()
    )
    if output.returncode:
        retval = False, '\n'.join(
            [output.stdout.decode("utf8"), output.stderr.decode("utf8")]
        )
    return retval
