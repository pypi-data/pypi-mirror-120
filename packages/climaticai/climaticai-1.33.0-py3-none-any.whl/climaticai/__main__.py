"""CLI commands."""

import click

from climaticai.utils.cli_utils import print_info


@click.group()
def cli():
    """CLI command with no arguments. Does nothing."""
    pass


@click.command()
def info():
    """CLI command with `info` argument. Prints info about the system, climaticai, and dependencies of climaticai."""
    print_info()


cli.add_command(info)
