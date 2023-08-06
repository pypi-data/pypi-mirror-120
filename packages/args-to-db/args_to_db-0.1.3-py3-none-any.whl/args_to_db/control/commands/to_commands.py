from .command import Command
from .commandlist import CommandList


def to_commands(commands):
    assert all((isinstance(arg, str) for cmd in commands for arg in cmd))

    return CommandList([Command(cmd) for cmd in commands])
