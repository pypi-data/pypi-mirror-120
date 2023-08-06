# ABle
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Type checking: mypy](https://camo.githubusercontent.com/59eab954a267c6e9ff1d80e8055de43a0ad771f5e1f3779aef99d111f20bee40/687474703a2f2f7777772e6d7970792d6c616e672e6f72672f7374617469632f6d7970795f62616467652e737667)](https://mypy.readthedocs.io/en/stable/)

Able stands for Allthenticate's BLE Peripheral Library.
It serves the purpose of enabling the abstraction of using a BLE Peripheral on Ubuntu, MacOs and Windows based systems
without having to adapt your software to have platform specific support.

# In Progress

Note that this project is still undergoing work by the development team, the main things we are working on are:

- Cleaning up some bugs in the bluezdbus and macos backend
- Making the gitlab/github repo public for contributions
- Setup a slack for developers to reach out to us about issues or ideas
- Make logging/use clearer and update our documentation (for example we require a fork of bluez) and moving things from this readme to our docs
- Get our docs on read the docs
- Some more surprises :)

# How To's

## Quick Start
To get started just run `get_started.sh`. This will install poetry and all of the project's dependencies, and drop you into the projects virtual environment.

```
bash get_started.sh
```
Whenever you pull new updates we recommend running a quick `poetry install` to get any updates. From there, please check out our examples to get started with the project!

## Upgrading Poetry Installer

It may be the case that the current version of your Poetry package is outdated. Run `scripts/check_poetry.sh` to check if there is a newer version of the poetry installer.

```
bash scripts/check_poetry.sh
```

# Documentation

## Writing Docs
We follow the Sphinx docstring format for our docstrings, see the following [site](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html) on the complete specification, but the
general docstring will look like:

```
"""
[Summary]

:param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
:type [ParamName]: [ParamType](, optional)
...
:raises [ErrorType]: [ErrorDescription]
...
:return: [ReturnDescription]
:rtype: [ReturnType]
"""
```

## Generating Docs
To generate the docs for local use you should just have to run the following inside of the poetry shell:

```
make html
```
Then open the html produced by Sphinx.

## Auto-Generating Docs

If you want to have docs magically update as you are writing them, run the following command:

```
sphinx-autobuild source/ build/html/
```

# Testing Able

## How To Test?
Running tests are easy, you need to only do a few things as a developer. First track down the IP of the companion you
plan to be using, we recommend a raspberry pi. Once you have that IP, export it as an environment variable as so:

```
export ABLE_CENTRAL_IP="<IP>"
```

Now, we can run the tests with the following command:

```
poetry install && poetry run pytest tests
```

## Rigorous Testing
If you want to do more rigorous testing over a long period of time and check for flaky tests, you will
have to modify the `pyproject.toml`. We already have the dependencies you need to run tests multiple times
to detect flakiness, all you need to do is modify the following line:

```
addopts = "--flake-finder --flake-runs=1 --reruns 5 --reruns-delay 5"
```
Into:
```
addopts = "--flake-finder --flake-runs=10 --reruns 5 --reruns-delay 5"
```
This will run each test 10 times, you can even modify it to be greater should you choose. You can also
modify the `reruns` and `reruns-delay` parameters to change how much time you should wait between failed tests,
maybe to let things simmer and how many reruns you will accept.

### Speedy Tests
Our dependencies include `pytest-fast-first` which will locally track which tests are quicker and will use AI and
deep learning (a json dictionary of times) to track and run tests that go faster first! Neat!

## Coming Soon To Testing
We are hoping to have unit tests coming soon for Able but right now are relying solely on hardware in the loop tests
to get things off the ground. Eventually we will detect if you have a companion set and if not, we will only run
the unit tests.

# Support
If you have any questions on the use of this library feel free to reach out the head
maintainer <bernie@allthenticate.com> or submit an issue on the repository.

## Contributing
Contributing is not currently enabled but once the repository is licensed we will be opening the project up for public contributions.


# Acknowledgements

This project was inspired by the great work done by the developer team for [Bleak](https://github.com/hbldh/bleak)
which is a fantastic platform agnostic bluetooth framework for a BLE client/central we would highly reccomend!

We also took notes from the work done by Kevin Car with his companion library [Bless](https://github.com/kevincar/bless),
who made a great server supplement to Bleak whose work saved us from countless hours from fighting dbus and pyobjc!
