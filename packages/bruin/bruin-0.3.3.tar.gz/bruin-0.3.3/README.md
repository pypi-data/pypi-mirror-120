# Bruin CLI

A toolbox for UCLA students in various events

Project published on PyPi: https://pypi.org/project/bruin/

Author: Oswald He <zifanhe1202@g.ucla.edu>

## Installation:
```sh
pip install bruin
```
or download this repo and run
```sh
python setup.py install
```

## Simple Usages:

### Meal
Print today's dining menu

```sh
bruin meal
```
Print hour of operations:
```sh
bruin meal --hour=['', 'all', 'De Neve', etc.]
```

Print detail menu:
```sh
bruin meal --detail=['Breakfast', 'Lunch', 'Dinner']
```

### Calendar
Print today's events/classes
```sh
bruin calendar
```

### Tasks
Print your remaining tasks:
```sh
bruin tasks
```

Add a new task (it will pop several prompts):
```sh
bruin task --add
```

Complete a task and move to review later:
```sh
bruin task --complete=[%d]
```

Terminate a task (or finish your review):
```sh
bruin task --terminate=[('t'|'r'|'d')(%d)]
```

Remove a daily recurring tasks:
```sh
bruin task --remove=[%d]
```

## Troubleshooting

1. *Cannot find certain packages*: Make sure you install Python 3.6 or higher and use it throughout your system.
2. *ModuleError: No module <module_name>*: Check whether the path you are running python is the same as where `pip` install all the dependencies. The root should be in the output log when you run either commands.

## Contribute
You can directly create a PR on a branch, but please create an issue first and after we talked about whether this improvement is needed, you can start your development.
   