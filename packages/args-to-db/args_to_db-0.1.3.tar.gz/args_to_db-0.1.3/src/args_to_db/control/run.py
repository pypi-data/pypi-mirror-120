import itertools
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from os import listdir
from os.path import isdir, isfile
from shutil import rmtree

import cursor
import pandas

from .commands.commandlist import CommandList


class State(Enum):
    QUEUED = 0
    RUNNING = 1
    SUCCESS = 2
    FAILED = 3


class UIThread(threading.Thread):

    _frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    _update_interval = 0.2

    def __init__(self, states):
        super().__init__()
        self._frame_index = 0
        self._states = states
        self._states_lock = threading.Lock()
        self._stopevent = threading.Event()

        self._newly_finished = []

    def update_state(self, cmd, state):
        assert state in State

        with self._states_lock:
            self._states[cmd] = state

            if state in (State.SUCCESS, State.FAILED):
                self._newly_finished.append(cmd)

    def _print_states(self, overwrite=True):

        def _by_state(state):
            return {k: v for k, v in self._states.items() if v == state}

        # Think about how to improve htis...
        queued = _by_state(State.QUEUED)
        running = _by_state(State.RUNNING)
        sucessed = _by_state(State.SUCCESS)
        failed = _by_state(State.FAILED)

        for cmd in self._newly_finished:
            state = self._states[cmd]
            if state == State.SUCCESS:
                icon = '✓'
                color = '\033[92m'
            elif state == State.FAILED:
                icon = '🗙'
                color = '\033[31m'
            else:
                raise Exception('Invalid ProcessState')

            line = ''
            if color is not None:
                line += color
            line += f'{icon} \033[0m {cmd} \n'
            sys.stdout.write(line)

        self._newly_finished = []

        spinner = self._frames[self._frame_index]
        for cmd in running:
            icon = spinner
            color = None
            line = ''
            if color is not None:
                line += color
            line += f'{icon} \033[0m {cmd} \n'
            sys.stdout.write(line)

        line = f'{len(queued)} ⧖\033[0m, '
        line += f'{len(running)} {spinner}\033[0m, '
        line += f'\033[92m{len(sucessed)} ✓\033[0m, '
        line += f'\033[31m{len(failed)} 🗙\033[0m, '
        line += f'{len(self._states)} Total \n'
        sys.stdout.write(line)

        if overwrite:
            sys.stdout.write(f'\033[{len(running) + 1}A')

        sys.stdout.flush()

    def run(self):
        cursor.hide()

        while not self._stopevent.is_set():
            self._frame_index = (self._frame_index + 1) % len(self._frames)
            self._print_states()

            time.sleep(self._update_interval)

        self._print_states(overwrite=False)
        cursor.show()

    def join(self, timeout=None) -> None:
        self._stopevent.set()
        return super().join(timeout=timeout)


def run_shell_command(cmd, uithread):

    uithread.update_state(str(cmd), State.RUNNING)

    with subprocess.Popen(cmd.args(),
                          stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL) as process:
        exit_code = process.wait()

    new_state = State.SUCCESS if exit_code == 0 else State.FAILED
    uithread.update_state(str(cmd), new_state)
    return exit_code


def _run_commands(command_list, threads):
    commands = command_list.commands()

    states = {str(cmd): State.QUEUED for cmd in commands}
    uithread = UIThread(states)
    uithread.start()

    uithreads = itertools.repeat(uithread, len(commands))

    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(run_shell_command, commands, uithreads)

    uithread.join()

    success = all((state == State.SUCCESS for state in states.values()))
    if not success:
        raise Exception('Command Failed!')


def _read_data_file(data_file):
    return pandas.read_pickle(data_file) if isfile(data_file) else None


def _combine_output_data(data_file, cache_dir):
    table = _read_data_file(data_file)

    for filename in listdir(cache_dir):

        row = pandas.read_pickle(f'{cache_dir}/{filename}')

        if table is None:
            table = row
        else:
            if row.iloc[0].name in table.index:
                table = table.update(row)
            else:
                table = table.append(row, verify_integrity=True)

    return table


def run(commands, threads=1, data_file='data.pkl', write_data=True,
        remove_cache_dir=True):
    cache_dir = 'args_to_db_cache'

    assert isinstance(commands, CommandList)
    assert isinstance(threads, int)
    assert isinstance(data_file, str)
    assert isinstance(write_data, bool)
    assert isinstance(cache_dir, str)
    assert isinstance(remove_cache_dir, bool)

    _run_commands(commands, threads)

    if not isdir(cache_dir):
        return None

    table = _combine_output_data(data_file, cache_dir)

    if remove_cache_dir:
        rmtree(cache_dir)

    if write_data:
        table.to_pickle(data_file)
        table.to_csv(f'{data_file}.csv')

    return table
    # FUTURE: return more info -> as specially to allow detailed testing
