"""
    The command line goes here
"""

import click
import os

from perm.validator import get_valid_emails, create_and_concat_csv


@click.group()
@click.option('-d', '--debug', default=False)
@click.option('-s', '--save', default=False)
@click.pass_context
def cli(ctx, debug, save):
    if ctx.obj is None:
        ctx.obj = {}
    ctx.obj['DEBUG'] = debug
    ctx.obj['SAVE'] = save

@cli.command()
@click.pass_context
@click.argument('first')
@click.argument('last')
@click.argument('domain')
@click.option('-m', '--middle', default=None)
def names(ctx, first, last, domain, middle):
    valid_emails = get_valid_emails(first, last, domain, middle=middle, debug=ctx.obj["DEBUG"])
    if ctx.obj['SAVE']:
        value = click.prompt('Please enter a valid email name', type=str, default="emails.csv")
        desired_file = os.getcwd()+f"/{value}"
        create_and_concat_csv(desired_file, valid_emails, first, middle, last, domain)
