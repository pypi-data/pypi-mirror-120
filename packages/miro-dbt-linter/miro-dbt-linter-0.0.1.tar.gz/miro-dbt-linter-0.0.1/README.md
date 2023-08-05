# Miro dbt linter

An extensible linter for dbt projects.

## Development

Clone this project.

```
git clone https://github.com/tjwaterman99/miro-dbt-linter.git
```

Install a Python virtual environment.

```
python -m pip install virtualenv
python -m virtualenv venv
source venv/bin/activate
venv/bin/pip install -r requirements.txt
```

Install the package in development mode.

```
pip install --editable .
```

## Deploying

Build the wheels.

```
python setup.py sdist bdist_wheel
```