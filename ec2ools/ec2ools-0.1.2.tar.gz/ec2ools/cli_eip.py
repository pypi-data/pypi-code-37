# -*- coding: utf-8 -*-

"""Console script for ec2ools."""
import sys
import click


@click.group()
def main(args=None):
    pass


@main.command(name='allocate')
def eip_allocate():
    click.echo("HERERERE")

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
