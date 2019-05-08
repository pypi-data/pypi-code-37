#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------
""" The interface for a dialog that allows the user to open/save files etc. """


# Standard library imports.
import sys

# Enthought library imports.
from traits.api import Enum, Unicode, Int

# Local imports.
from pyface.i_dialog import IDialog
import six


class IFileDialog(IDialog):
    """ The interface for a dialog that allows the user to open/save files etc.
    """

    #### 'IFileDialog' interface ##############################################

    #: The 'action' that the user is peforming on the directory.
    action = Enum('open', 'save as')

    #: The default directory.
    default_directory = Unicode

    #: The default filename.
    default_filename = Unicode

    #: The default path (directory and filename) of the chosen file.  This is
    #: only used when the *default_directory* and *default_filename* are not set
    #: and is equivalent to setting both.
    default_path = Unicode

    #: The directory containing the chosen file.
    directory = Unicode

    #: The name of the chosen file.
    filename = Unicode

    #: The path (directory and filename) of the chosen file.
    path = Unicode

    #: The wildcard used to restrict the set of files.
    wildcard = Unicode

    #: The index of the selected wildcard.
    wildcard_index = Int(0)


class MFileDialog(object):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IFileDialog interface.

    Implements: create_wildcard()
    """

    # FIXME v3: These are referenced elsewhere so maybe should be part of the
    # interface. The format is toolkit specific and so shouldn't be exposed.
    # The create_wildcard() class method (why isn't it a static method?) should
    # be the basis for this - but nothing seems to use it.  For now the PyQt
    # implementation will convert the wx format to its own.  Actually we need
    # the format to be portable between toolkits - so stick with PyQt
    # supporting the wx format or invent a data structure.

    #: A file dialog wildcard for Python files.
    WILDCARD_PY = "Python files (*.py)|*.py|"

    #: A file dialog wildcard for text files.
    WILDCARD_TXT = "Text files (*.txt)|*.txt|"

    #: A file dialog wildcard for all files.
    if sys.platform == 'win32':
        WILDCARD_ALL = "All files (*.*)|*.*|"
    else:
        WILDCARD_ALL = "All files (*)|*"

    #: A file dialog wildcard for Zip archives.
    WILDCARD_ZIP = "Zip files (*.zip)|*.zip|"

    ###########################################################################
    # 'MFileDialog' *CLASS* interface.
    ###########################################################################

    @classmethod
    def create_wildcard(cls, description, extension):
        """ Creates a wildcard for a given extension.

        Parameters
        ----------
        description : str
            A human-readable description of the pattern.
        extenstion : list
            The wildcard patterns for the extension.
        """

        if isinstance(extension, six.string_types):
            pattern = extension

        else:
            pattern = ';'.join(extension)

        return "%s (%s)|%s|" % (description, pattern, pattern)
