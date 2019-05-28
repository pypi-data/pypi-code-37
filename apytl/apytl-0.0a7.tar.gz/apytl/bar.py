#!/usr/bin/env python

"""
A logging module implementation of another progress bar I have seen
floating around the web. One advantage of this implementation is that
the progress bar will be correctly piped to STDOUT even if it is called
via a shell script.

I haven't checked how this behaves when logging to a file. Caveat 
emptor, or something.
"""

import logging
import random
import sys

class Bar:
    def __init__(self):
        self.barsize = 50
        self.decimal = 1
        self.fill = '#'
        self.fillfactor = 1
        self.first_iteration = True
        self.prefix = 'Progress'
        self.suffix = 'Complete'
        self._EMOJI = {
            'dash'         : '\\U0001F4A8',
            'eggplant'     : '\\U0001F346',
            'grimace'      : '\\U0001F62C',
            'middlefinger' : '\\U0001F595',
            'peach'        : '\\U0001F351',
            'poop'         : '\\U0001F4A9',
            'pufferfish'   : '\\U0001F421',
            'skullnbones'  : '\\u2620',
            'sweat'        : '\\U0001F4A6',
            'taco'         : '\\U0001F32E',
            'trex'         : '\\U0001F996',
        }

    def parse_unicode(self, userstring):
        """
        Parse a unicode string of the form UXXXXXXXX or uXXXX

        Parameters
        ----------
        userstring : str

        Returns
        -------
        fill : str
        """
        fill = (userstring
                .encode('utf-8')
                .decode('raw_unicode_escape'))
        return fill

    def reset_bar(self):
        """Reset progress bar attributes to their default values"""
        self.__init__()
        return

    def setup_bar(self, **kwargs):
        """
        Format the progress bar and perform initial setup.

        Parameters
        ----------
        prefix : str
            An string to place at the left side of the bar. Default is
            'Progress'.
        suffix : str
            A string to place at the right side of the bar, Default is
            'Complete'.
        decimal : int
            The number of decimal places to which the completion progress
            should be calculated. Default it 1.
        barsize : int
            The size of the progress bar in units of characters. Default is
            50.
        fill : str
            The character to use to fill the bar and represent completion.
            Any single-width alphanumeric or punctuation character may be
            passed. Some stock options are provided and may be accessed
            through the keys of `apytl.Bar()._EMOJI`. User-supplied unicode
            is also acceptable. See `Notes`. Default is `#`.

        Notes
        -----
        USE THE FOLLOWING AT YOUR OWN PERIL:
        Choose from a preselected set of unicode emojis (N.B., this list may
        not be completely up-to-date. Inspect the `._EMOJI` attribute for the
        authoritative version.):
          'dash'
          'eggplant'
          'grimace'
          'middlefinger'
          'peach'
          'poop'
          'pufferfish'
          'skullnbones'
          'sweat'
          'taco'
          'trex'
        or pass your own unicode. Pass 'random' to randomly select one of
        the above options.

        Due to the variety of terminal emulators, font support, and display
        and window managers it's impossible to know how well (if at all) this
        will function on your system. If passing a custom emoji, you will have
        to use a format Python will recognize. For instance:
          `\\U0001F4A9` --> poop emoji
          `\\u2620`     --> skull and crossbones emoji
        Note the difference in capitalization and the zero-padding.
        """
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        self.logginghandler = logging.StreamHandler()
        self.logginghandler.terminator = ''

        for attr, value in kwargs.items():
            if hasattr(self, attr):
                if attr == 'fill':
                    self.check_fill(value)
                else:
                    self.__setattr__(attr, value)
            else:
                raise AttributeError('The progress bar has no attribute: "{}"'.format(attr))
        self.first_iteration = False
        return

    def teardown_bar(self):
        """Clean up the logging handler after completion"""
        self.logginghandler.terminator = '\n'
        endrecord = logging.LogRecord('end', 2, '.', 1, '%s', (' '), None)
        self.logginghandler.emit(endrecord)
        self.logginghandler.terminator = ''
        self.first_iteration = True
        return

    def check_fill(self, fill):
        """
        Check the fill passed by the user and parse it accordingly.

        Parameters
        ----------
        fill : string

        Returns
        -------
        fill_params : tuple; two elements: string and int
        """
        ubytes = False
        if fill.casefold() == 'random':
            # The user doesn't care what shows up, so we choose for them
            choice = random.choice(list(self._EMOJI.keys()))
            fill = self._EMOJI[choice]
            ubytes = True
        elif fill in self._EMOJI.keys():
            # The user has selected an entry in the provided emoji dictionary
            fill = self._EMOJI[fill]
            ubytes = True
        elif len(fill) > 1:
            # The user has passed their own input
            ubytes = True
        # Now we just need to adjust the buffer width to accommodate the
        # greater-than-single-width emojis
        fillfactor = 1
        if ubytes and len(fill) > 7:
            fillfactor = 2
        if ubytes:
            fill = self.parse_unicode(fill)
        self.fill = fill
        self.fillfactor = fillfactor
        return

    def drawbar(self, iteration, total, **kwargs):
        """
        Draw a progress bar on the terminal.

        Parameters
        ----------
        iteration : int
            The current iteration number. Note that it is assumed that your
            counter starts at zero.
        total : int
            The total number of iterations that will be executed.

        Other parameters
        ----------------
        **kwargs
            All keyword arguments are passed to `apytl.Bar().setup_bar()`.
            Keyword arguments are responsible for the initial setup of the
            progress bar.
          prefix : str
              An string to place at the left side of the bar. Default is
              'Progress'.
          suffix : str
              A string to place at the right side of the bar, Default is
              'Complete'.
          decimal : int
              The number of decimal places to which the completion progress
              should be calculated. Default it 1.
          barsize : int
              The size of the progress bar in units of characters. Default is
              50.
          fill : str
              The character to use to fill the bar and represent completion.
              Any single-width alphanumeric or punctuation character may be
              passed. Some stock options are provided and may be accessed
              through the keys of `apytl.Bar()._EMOJI`. User-supplied unicode
              is also acceptable. See `Notes`. Default is `#`.

        Notes
        -----
        USE THE FOLLOWING AT YOUR OWN PERIL:
        Choose from a preselected set of unicode emojis (N.B., this list may
        not be completely up-to-date. Inspect the `._EMOJI` attribute for the
        authoritative version.):
          'dash'
          'eggplant'
          'grimace'
          'middlefinger'
          'peach'
          'poop'
          'pufferfish'
          'skullnbones'
          'sweat'
          'taco'
          'trex'
        or pass your own unicode. Pass 'random' to randomly select one of
        the above options.

        Due to the variety of terminal emulators, font support, and display
        and window managers it's impossible to know how well (if at all) this
        will function on your system. If passing a custom emoji, you will have
        to use a format Python will recognize. For instance:
          `\\U0001F4A9` --> poop emoji
          `\\u2620`     --> skull and crossbones emoji
        Note the difference in capitalization and the zero-padding.
        """
        if self.first_iteration:
            self.setup_bar(**kwargs)
        iteration = iteration + 1
        str_format = '{0:.' + str(self.decimal) + 'f}'
        percent = str_format.format(100 * (iteration / float(total)))
        filled_length = int(round(self.barsize * iteration / float(total * self.fillfactor)))
        bar = self.fill * filled_length + '-' * \
              ((self.barsize - int(filled_length * self.fillfactor)))
        # Note that most of the arguments passed to LogRecord are filler. We only
        # really care about the last three.
        msg = '\r{} |{}| {}{} {}'.format(self.prefix, bar, percent, '%', self.suffix)
        record = logging.LogRecord('bar', 2, '.', 1, msg, None, None)
        self.logginghandler.emit(record)
        if iteration == total:
            self.teardown_bar()
        return
