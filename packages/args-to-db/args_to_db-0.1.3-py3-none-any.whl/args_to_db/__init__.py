# import configparser
from .control.commands.args import arg, flag, option
from .control.commands.combine import combine
from .control.run import run
from .control.commands.to_commands import to_commands
from .runtime.result import config_from_args, write_results

__all__ = [
    'arg',
    'combine',
    'config_from_args',
    'flag',
    'option',
    'run',
    'to_commands',
    'write_results',
]


# import os.path
# from configparser import ConfigParser
# if not os.path.isfile('config.ini'):
#     config_parser = ConfigParser()
#     config_parser['RUN'] = {
#         'thread_count': 1,
#         'data_file': 'data.pkl',
#         'write_data': True,
#         'remove_cache_dir': True,
#         'cache_dir': 'args_to_db_cache/'
#     }
#     with open('config.ini', 'w') as file:
#         config_parser.write(file)
# else:
#     pass
