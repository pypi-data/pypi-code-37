import click


class Output(object):

    LEN_DEFAULT = 120

    @staticmethod
    def error(msg, highlight=False):
        Output._echo(msg, "red", highlight)

    @staticmethod
    def warn(msg, highlight=False):
        Output._echo(msg, "yellow", highlight)

    @staticmethod
    def highlight(msg, highlight=False):
        Output._echo(msg, "blue", highlight)

    @staticmethod
    def notice(msg, highlight=False):
        Output._echo(msg, "green", highlight)

    @staticmethod
    def debug(msg, highlight=False):
        Output._echo(msg, "white", highlight)

    @staticmethod
    def _echo(msg, fg, highlight):
        boundary_len = len(msg) if len(msg) < Output.LEN_DEFAULT else Output.LEN_DEFAULT
        if highlight:
            click.echo(click.style(text="=" * boundary_len, fg=fg))

        click.echo(click.style(text=msg, fg=fg))

        if highlight:
            click.echo(click.style(text="=" * boundary_len, fg=fg))
