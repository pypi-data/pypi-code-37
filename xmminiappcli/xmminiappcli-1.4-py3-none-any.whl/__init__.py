import json
import os
import shutil
from http.server import *
import fire

from .utils import *


class MiniApp:
    app_rel_path: str
    app_full_path: str
    app_name: str
    app_thumbnail: str

    def __init__(self, root_path):
        self.app_rel_path = os.path.join(root_path.split('/')[-1], 'output')
        self.app_full_path = os.path.join(root_path, 'output')
        self.app_name = self.read_app_name(self.app_full_path)
        self.app_thumbnail = os.path.join(root_path, 'thumbnail.png')

    def read_app_name(self, app_full_path):
        appjson_path = os.path.join(app_full_path, "app.json")
        with open(appjson_path) as file:
            appjson_content = file.read()
            appjson = json.loads(appjson_content)
            if 'window' in appjson:
                window_info = appjson['window']
                if 'navigationBarTitleText' in window_info:
                    return window_info['navigationBarTitleText']
            return '我是谁？'

    def to_dict(self):
        return {
            'name': self.app_name,
            'bundleId': self.app_rel_path,
            'icon_url': '',
            'path': '/' + self.app_rel_path
        }


def gen_app_list_json(input_path):
    sub_dirs = os.listdir(input_path)
    apps = []
    for sub_dir in sub_dirs:
        root_path = os.path.join(input_path, sub_dir)
        appjson_path = os.path.join(root_path, 'output/app.json')
        if os.path.isdir(root_path) and os.path.exists(appjson_path):
            app = MiniApp(root_path)
            apps.append(app.to_dict())
    return apps


def prepare_swan_core(root_path):
    dst_path = os.path.join(root_path, 'swan-core')
    if os.path.exists(dst_path):
        return
    home_dir = os.path.expanduser('~')
    swan_core_root = os.path.join(home_dir, '.swan-cli/vendor/swan-core/')
    swan_core_selected_path = swan_core_root
    sub_dirs = os.listdir(swan_core_root)
    for sub_dir in sub_dirs:
        if sub_dir.startswith('3.'):
            swan_core_selected_path = os.path.join(swan_core_selected_path, sub_dir)
            break
    dst_path = os.path.join(root_path, 'swan-core')
    shutil.copytree(swan_core_selected_path, dst_path)


def gen_test_app_json(root_path):
    prepare_swan_core(root_path)
    json = {}
    json['swan-core-master'] = '/swan-core/master/master.html'
    json['swan-core-slave'] = '/swan-core/slaves/slaves.html'
    json['apps'] = gen_app_list_json(root_path)
    return json


def start_server(server_path):
    os.chdir(server_path)
    httpd = HTTPServer(('', 8000), SimpleHTTPRequestHandler)
    httpd.serve_forever()


class XMMiniAppCli(object):
    def test(self, root_path:str = os.curdir):
        output = os.path.join(root_path, 'testapps.json')
        test_app_json = gen_test_app_json(root_path)
        output_abs_path = os.path.abspath(output)
        with open(output_abs_path, 'w+') as ofile:
            ofile.write(json.dumps(test_app_json))
        print("servering at http://127.0.0.1:8000")
        start_server(root_path)


fire.Fire(XMMiniAppCli)
