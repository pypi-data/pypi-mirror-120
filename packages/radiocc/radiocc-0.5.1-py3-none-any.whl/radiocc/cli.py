#!/usr/bin/env python3
# type: ignore [misc]

"""
radiocc CLI.
"""


from typing import Any

import click
from pudb import set_trace as bp  # noqa: F401

from radiocc import NAME, VERSION, config, core

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


def version(ctx: Any, param: Any, value: Any) -> None:
    if not value or ctx.resilient_parsing:
        return
    click.echo(VERSION)
    ctx.exit()


@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.pass_context
@click.option(
    "-v",
    "--version",
    is_flag=True,
    callback=version,
    expose_value=False,
    is_eager=True,
    help="Show version.",
)
@click.option(
    "--generate-config",
    is_flag=True,
    help="Generate a config file `config.yaml` in the current directory.",
)
def cli(ctx: click.Context, generate_config: bool) -> None:
    """Radio occultations."""
    # Share default command options.
    ctx.ensure_object(dict)
    # ctx.obj["var"] = var

    if generate_config:
        config.generate_config()
        ctx.exit()

    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
        ctx.exit()


@cli.command()
@click.option(
    "-g", "--gui", is_flag=True, help="Start the program with the graphical interface."
)
@click.pass_context
def run(
    ctx: click.Context,
    gui: bool,
) -> None:
    """Run radiocc."""
    if not gui:
        core.run()
    else:
        ctx.exit("the graphical interface is not implemented yet.")


def main() -> None:
    cli(prog_name=NAME)


if __name__ == "__main__":
    main()
