# Engine development scaffolding (Python)

Scaffolding project to support engine development in Python.

This subproject provides a Python library to facilitate test-driven development
of engines.

## Test cases generation

In order to develop an engine and to be able to check if the engine
works as expected, a test-driven development approach proved to be
valuable. Test cases might be very well understood by both the content
designer and engine developer.

This project contains DSL (domain-specific language) written in Python 
to help generate test cases. 

Before starting using Python it's recommended to create a virtual environment 
to avoid conflicts.

```sh
python3 -m venv .venv-local
```
This command will create a new virtual environment in the folder `.venv-local`.
Then in a new terminal it needs to be activated:

```sh
source .venv-local/bin/activate
```

To generate test cases for ambulance:

```sh
python ambulance.py
```
