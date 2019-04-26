# blender-evolution

## Installation

You will need Python 3.6 installed. (On my system, this was installed as part of Visual Studio). Note that this specific version of Python is required -- Python 3.7 will not work.

(Python 3.7 won't work -- see [this issue](https://github.com/TylerGubala/blenderpy/issues/15).)

The system uses `pipenv` to manage dependencies. Install it using:

```
pip install pipenv
```

Next, install the dependencies:

```
pipenv install
```

Run with:

```
pipenv run python -m src.launcher
```
