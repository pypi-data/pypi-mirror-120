import os

from spell.shared.dependencies import (
    PipDependencies,
    CondaDependencies,
    in_virtualenv,
    NoEnvFound
)
from spell.cli.exceptions import ExitException


def dependencies_from_env():
    if os.environ.get("CONDA_DEFAULT_ENV"):
        return CondaDependencies.from_env()
    elif in_virtualenv():
        return PipDependencies.from_env()
    raise NoEnvFound


def validate_pip(pip):
    if pip.find("==") != pip.find("="):
        raise ExitException(
            f"Invalid pip dependency {pip}: = is not a valid operator. Did you mean == ?"
        )


def format_pip_versions(pip):
    for x in pip:
        validate_pip(x)
    return [convert_name_version_pair(x, "==") for x in pip]


def format_apt_versions(apt):
    return [convert_name_version_pair(x, "=") for x in apt]


def convert_name_version_pair(package, separator):
    split = package.split(separator)
    return {"name": split[0], "version": split[1] if len(split) > 1 else None}
