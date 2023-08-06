# <span style="color:#4078c0">args_to_db</span> - Data Generation Tool for Argument Optimisation

```sh
pip install args_to_db
```

You want to analyze a (python) script for different arguments/settings? - Argument optimization is becoming more and more important in many application areas. <span style="color:#4078c0">args_to_db</span> is an attempt to generalize and simplify the process of running a programm in different modes or configurations and combining the resulting datasets to allow for further analysis.

## When should I use <span style="color:#4078c0">args_to_db</span>?
You have a programm which is highly dependent on parameters and arguments, for example a solver framework for linear system of equations. Different inputs vary performance of solving methods dramatically. So we want to optimize the solver and preonditioner used for a specific linear system of equations.

This is performed once and results in preferences which are then to be used automatically by the programm. <span style="color:#4078c0">args_to_db</span> simplifies the process of argument variation and dataset generation.

## How to use <span style="color:#4078c0">args_to_db</span> to run a script?

Argument construction is made easy with the usage of `arg, option, flag`.

```python
from args_to_db import arg, flag, option

py = arg('python')
# > py=[['python']]

script = arg('script.py')
# > py=[['script.py']]

data = option('--input', ['file1.csv', 'file2.csv'])
# > data=[['--input', 'file1.csv'],
#         ['--input', 'file2.csv']]

opt_flags = flag('-O') + flag('-r')
# > opt_flags=[[],
#              ['-r'],
#              ['-O'],
#              ['-O', '-r']]

log_flag = flag('--log', vary=False)
# > log_flag=[['--log']]

cmds = py + script + data + opt_flags + log_flag
# > cmds=[['python', 'script.py', '--input', 'file1.csv', '--log'],
#         ['python', 'script.py', '--input', 'file1.csv', '-r', '--log'],
#         ['python', 'script.py', '--input', 'file1.csv', '-O', '--log'],
#         ['python', 'script.py', '--input', 'file1.csv', '-O', '-r', '--log'],
#         ['python', 'script.py', '--input', 'file2.csv', '--log'],
#         ['python', 'script.py', '--input', 'file2.csv', '-r', '--log'],
#         ['python', 'script.py', '--input', 'file2.csv', '-O', '--log'],
#         ['python', 'script.py', '--input', 'file2.csv', '-O', '-r', '--log']]

```

The container objects are arrays of commands (which themselves are arrays again), they behave like normal python arrays except for the differnt usage of the `+` and `+=` operator.

Such object or any other 2D command array may then be executed.

```python
run(cmds, threads=4)
# runs all specified commands with upto 4 concurrent threads.
```

## How to report (config specific) results of the scripts?
The values of interest on which we want to optimize need to be logged and combined. <span style="color:#4078c0">args_to_db</span> makes this easy.

```python
results = {'key': value}
write_results(__file__, args, results) 
```

This produces an output which is then later on combined with the others by the `run(...)` task.
