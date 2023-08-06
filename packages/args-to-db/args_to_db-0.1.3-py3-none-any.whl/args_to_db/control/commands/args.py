from .command import Command
from .commandlist import CommandList


def arg(args):
    """Creates a single or multiple value argument object for command
       contruction.

    Args:
        options (str, list): Command or list of commands

    Returns:
        _Arg: 2D array of commands.
    """
    is_list = isinstance(args, list)
    is_str = isinstance(args, str)

    assert is_list or is_str, 'Passed argument must be a list or string.'
    if is_list:
        assert all(isinstance(option, str) for option in args), \
            'All argument options must be strings.'
    else:
        args = [args]

    return CommandList([Command(arg) for arg in args])


def flag(identifier, vary=True):
    """Creates a flag object for command construction.

    Args:
        identifier (str): string of the actual flag to be added to the command
        vary (bool, optional): Wether this flag is to be understood as an
            optional one. Defaults to True.

    Returns:
        _Arg: 2D array of commands.
    """
    assert isinstance(identifier, str), 'Flag identifier must be of type str.'
    assert isinstance(vary, bool), 'Vary argument takes a bool as parameter.'

    options = [Command([identifier])]
    if vary:
        options.insert(0, Command([]))

    return CommandList(options)


def option(identifier, values):
    """Creates a option object for command construction.

    Args:
        identifier (str): String of the option identifier.
        values (list): Possible values of the option.

    Returns:
        _Arg: 2D array of commands.
    """
    assert isinstance(identifier, str), 'Identifier must be of type str.'

    is_list = isinstance(values, list)
    is_str = isinstance(values, str)
    assert is_list or is_str, 'Values type must be either str or list.'
    if is_list:
        assert all(isinstance(option, str) for option in values), \
            'All possible values must be of type str.'

    if is_list and len(values) == 0:
        return CommandList([])

    return CommandList([Command([identifier])]) + \
        CommandList([Command(value) for value in values])
