import warnings


def _is_list_of_str(obj):
    if obj == []:
        return True

    if not isinstance(obj, (tuple, list)):
        return False

    return all((isinstance(elem, str) for elem in obj))


class Command():
    def __init__(self, args, dependencies=None):

        if isinstance(args, str):
            args = [args]

        assert _is_list_of_str(args)
        self._args = args

        if dependencies is None:
            dependencies = []

        assert _is_list_of_str(dependencies)
        self._dependencies = dependencies

        if dependencies != []:
            warnings.warn("Dependencies are currently only placeholders.")

    def args(self):
        return self._args

    def dependencies(self):
        return self._dependencies

    def __add__(self, other):
        assert isinstance(other, Command)
        # how shoudl dependencies get 'added'?
        return Command([*self.args(), *other.args()])

    def __eq__(self, other) -> bool:
        assert isinstance(other, Command)

        args_eq = (self.args() == other.args())
        dependencies_eq = (self.dependencies() == other.dependencies())
        return args_eq and dependencies_eq

    def __repr__(self) -> str:
        return ' '.join(self._args)
