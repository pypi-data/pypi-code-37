import click


@click.group()
def hello():
    click.echo("hello")


@hello.command()
def world():
    click.echo("world")
