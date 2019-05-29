import kivy.resources as _kr
import os.path as _op

# to make sure the local 'data' folder is searchable within Kivy
_kr.resource_add_path(_op.dirname(__file__))

import kivymt.fix_kivy as _kf # to fix kivy