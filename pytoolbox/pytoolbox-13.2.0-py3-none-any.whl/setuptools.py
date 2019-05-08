# -*- encoding: utf-8 -*-



import setuptools, sys


class Disabled(setuptools.Command):

    description = 'Do not run this.'
    user_options = [('dummy=', 'd', 'dummy option to make setuptools happy')]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        sys.exit('This command is disabled!')
