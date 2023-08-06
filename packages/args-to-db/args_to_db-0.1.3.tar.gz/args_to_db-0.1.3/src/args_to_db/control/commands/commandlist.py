from .command import Command


class CommandList():
    def __init__(self, commands):
        assert isinstance(commands, (tuple, list))
        assert all((isinstance(cmd, Command) for cmd in commands))

        self._commands = commands

    def __add__(self, other):
        assert isinstance(other, CommandList)

        commands = [s + o for s in self.commands() for o in other.commands()]
        return CommandList(commands)

    def commands(self) -> list:
        return self._commands

    def __eq__(self, other) -> bool:
        assert isinstance(other, CommandList)

        return self._commands == other.commands()

    def __len__(self) -> int:
        return len(self._commands)

    def __repr__(self) -> str:
        return str(self._commands)
