import argparse


class NoOpAction(argparse.Action):
    def __init__(
            self,
            option_strings,
            dest,
            default=None,
            required=False,
            help=None,
            metavar=None,
    ):
        super(NoOpAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=0,
            const=None,
            default=default,
            required=required,
            help=help,
        )

    def __call__(
            self,
            parser,
            namespace,
            values,
            option_string=None,
    ):
        pass
