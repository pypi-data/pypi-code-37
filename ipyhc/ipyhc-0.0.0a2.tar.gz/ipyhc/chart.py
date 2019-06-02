from copy import copy, deepcopy
import random
import os
import pandas as pd
import simplejson as json

import ipywidgets as wg

from traitlets import observe, Unicode, Dict, List, Int, Bool

from .util import Util
from .builder_param import BuilderParams
from .display import export_html_code
from .__meta__ import __version_js__

_semver_range_frontend_ = '~' + __version_js__


class Chart(wg.DOMWidget):
    """
    HighCharts Widget.

    -----
    Attributes:

    TBD
    """
    _model_name = Unicode('ChartModel').tag(sync=True)
    _view_name = Unicode('ChartView').tag(sync=True)
    _model_module = Unicode('ipyhc').tag(sync=True)
    _view_module = Unicode('ipyhc').tag(sync=True)
    _view_module_version = Unicode(_semver_range_frontend_).tag(sync=True)
    _model_module_version = Unicode(_semver_range_frontend_).tag(sync=True)

    _id = Int(0).tag(sync=True)

    theme = Unicode('').tag(sync=True)
    width = Unicode('').tag(sync=True)
    height = Unicode('').tag(sync=True)
    stock = Bool(False).tag(sync=True)
    update_data = Int(0).tag(sync=True)

    _options_down = Unicode('').tag(sync=True, to_json=Util.compress)
    _data_down = Unicode('').tag(sync=True, to_json=Util.compress)
    _data_up = Unicode('').tag(sync=True, from_json=Util.data_from_json)

    def __init__(self,
                 width='100%',
                 height=0,
                 theme='',
                 stock=False,
                 options={},
                 data=[],
                 unsync=False):
        """
        Instantiates the widget. See TBD
        for more details.
        """

        self._id = random.randint(0, int(1e9))
        self.width_in = width
        self.height_in = height
        self.theme = theme
        self.stock=stock
        self._options_dict = options
        self.data_in = deepcopy(data)
        self.update_data = 0
        self.data_out = {'counter':0}
        self.unsync=unsync

        bp = BuilderParams(self)
        bp.valid()
        bp.build()

        super().__init__()
    
    @observe('_data_up')
    def export(self, change):
        if not self.unsync:
            self.data_out = json.loads(self._data_up)
            self.update_data +=1

    def export_html(self, build=False):
        """
        If build==True, returns a str containing HTML code 
        for embedding as a standalone widget.
        If build==False, returns a dict containing 4 parts necessary
        to put several embed widgets in the same page.
        """
        if build:
            html = export_html_code(self)
            return (html['script_tags'] +
                    (html['html_state']).format(manager_state=json.dumps(html['manager_state'])) +
                    html['grid_div'])
        return export_html_code(self)
    
    def dump(self, path, mode='standalone'):
        """
        Similar as export_html, but create the files in the in the 'path' directory.
        """
        if mode == 'standalone':
            with open(path+"/export_grid_standalone"+str(self._id)+".html", 'w+') as f:
                f.write(self.export_html(build=True))
        elif mode == 'all':
            widget_export = self.export_html(build=False)
            with open(path+"/export_scripts.html", "w+") as f:
                f.write(widget_export['script_tags'])
            with open(path+"/export_html_state.html", "w+") as f:
                f.write(widget_export['html_state'])
            with open(path+"/export_state_"+str(self._id)+".json", "w+") as f:
                f.write(json.dumps(widget_export['manager_state']))
            with open(path+"/export_grid_"+str(self._id)+".html", "w+") as f:
                f.write(widget_export['grid_div'])