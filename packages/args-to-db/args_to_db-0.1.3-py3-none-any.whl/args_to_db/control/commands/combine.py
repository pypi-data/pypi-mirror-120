from .commandlist import CommandList


def combine(*lists):
    assert all((isinstance(list, CommandList) for list in lists))

    return CommandList([cmd for list in lists for cmd in list.commands()])
