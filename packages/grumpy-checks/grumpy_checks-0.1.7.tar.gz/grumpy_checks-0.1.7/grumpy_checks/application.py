"""Application.

This module defines the main entrypoint to grumpy
cli application.

The module defines a cleo.Application object,
adds appropriate commands and defines
a main function that runs the application.
"""

from cleo import Application
from .cli.about import AboutCommand


application = Application()
"""Main Application CLI object from cleo."""
application.add(AboutCommand())


def main():
    """CLI application main function."""
    application.run()


if __name__ == '__main__':
    main()
