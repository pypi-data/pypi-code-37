#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
#
# Copyright (c) 2015-2017, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
#
#------------------------------------------------------------------------------
"""
This module provides the toolkit object for the current backend toolkit

See :py_func:`pyface.base_toolkit.find_toolkit` for details on the loading
algorithm.
"""

from .base_toolkit import find_toolkit


# The toolkit function.
toolkit = toolkit_object = find_toolkit('pyface.toolkits')
