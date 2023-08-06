from typing import Optional

import click

from anyscale.controllers.project_controller import ProjectController
from anyscale.project import validate_project_name


@click.command(
    name="clone",
    short_help="Clone a project that exists on anyscale, to your local machine.",
    help="""Clone a project that exists on anyscale, to your local machine.
This command will create a new folder on your local machine inside of
the current working directory and download the most recent snapshot.

This is frequently used with anyscale push or anyscale pull to download, make
changes, then upload those changes to a currently running cluster.""",
)
@click.argument("project-name", required=True)
@click.option(
    "--owner",
    help="Username or email of the user who owns the project. Defaults to the current user.",
    required=False,
)
def anyscale_clone(project_name: str, owner: Optional[str]) -> None:
    project_controller = ProjectController()
    project_controller.clone(project_name, owner=owner)


def _validate_project_name(ctx, param, value) -> str:
    if not validate_project_name(value):
        raise click.BadParameter(
            '"{}" contains spaces. Please enter a project name without spaces'.format(
                value
            )
        )

    return value


def _default_project_name() -> str:
    import os

    cur_dir = os.getcwd()
    return os.path.basename(cur_dir)


@click.command(
    name="init",
    help="Create a new project or attach this directory to an existing project.",
)
@click.option(
    "--name",
    help="Project name.",
    required=True,
    callback=_validate_project_name,
    prompt=True,
    default=_default_project_name(),
)
@click.option(
    "--config",
    help="[DEPRECATED] Path to autoscaler yaml. Created by default.",
    type=click.Path(exists=True),
    required=False,
)
@click.option(
    "--requirements",
    help="Path to requirements.txt. Created by default.",
    required=False,
)
def anyscale_init(
    name: str, config: Optional[str], requirements: Optional[str],
) -> None:

    project_controller = ProjectController()
    project_controller.init(name, config, requirements)
