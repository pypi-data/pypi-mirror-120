Script that set up boilerplate code for python repositories.
==========================

## Create a Virtual Environment

After cloning or downloading the repo, create a Python virtual environment with:

```
python -m venv .env
```

This will create the virtual environment in the project directory as `.env
## Activate the Virtual Environment

Now activate the virtual environment. on macOS, Linux and Unix systems, use:

```
source .env/bin/activate
```

On Windows with `cmd.exe`:

```
.env\Scripts\activate.bat
```

Or Windows with PowerShell:

```
.\.env\Scripts\activate.ps1
```

## Install the dependencies 

Install pipenv

```
pip install --user pipenv
```

Install py-code library

```
pipenv install py-code
```

## Create boilerplate codes

To create a new project with boilerplate codes

```
pipenv run pycode <project_name>
```

To update boilerplate codes for a project

```
cd <project-directory>
```

```
pipenv run update
```