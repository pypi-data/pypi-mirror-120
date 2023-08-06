"""Define CLI grumpy about <command>."""

from cleo import Command
from rich.table import Table
from ..commands import COMMANDS
from ..checks import console


class AboutCommand(Command):
    """
    Grumpily runs a check.

    about
        {command : What are you grumpy about?}
        {--topic=? : For asking about a specific topic}
    """

    def handle(self):
        """Handle command."""
        if self.argument('command') == "what":
            return self._handle_what()
        command = COMMANDS[self.argument('command')]
        command()

    def _handle_what(self):
        #  what_option = self.option('topic')
        available_commands = list(COMMANDS.keys())
        table = Table(show_header=True)
        table.add_column("Command")
        table.add_column("Description")
        for com in available_commands:
            table.add_row(com, "")
        console.print(table)
