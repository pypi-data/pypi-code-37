#!/usr/bin/env python

# Run a standalone AL service

import glob
import json
import logging
import os
import tempfile
import time

import pyinotify
import yaml

from alv3_service.common import log as al_log
from alv3_service.common.mock_modules import modules1, modules2
from alv3_service.common.task import Task
from assemblyline.common.dict_utils import recursive_update
from assemblyline.common.importing import load_module_by_path

modules1()
modules2()

current_task = None
previous_task = None


class EventHandler(pyinotify.ProcessEvent):
    def process_default(self, event):
        global current_task, previous_task
        if event.pathname.endswith('_task.json'):
            if previous_task != os.path.basename(event.pathname):
                current_task = os.path.basename(event.pathname)


def run_service():
    global current_task, previous_task

    service = svc_class(cfg)
    service.start_service()

    folder_path = os.path.join(tempfile.gettempdir(), svc_name, 'received')

    wm = pyinotify.WatchManager()  # Watch Manager
    notifier = pyinotify.ThreadedNotifier(wm, EventHandler())

    try:
        notifier.start()

        while True:
            if not os.path.isdir(folder_path):
                os.makedirs(folder_path)

            # Check if 'received' directory already contains a task
            task_files = glob.glob(folder_path+'/*_task.json')
            if task_files:
                current_task = os.path.basename(task_files[0])
            else:
                wdd = wm.add_watch(folder_path, pyinotify.ALL_EVENTS, rec=True)

            while not current_task:
                # log.info('Waiting for task in: {}'.format(folder_path))
                time.sleep(2)

            previous_task = current_task
            current_task = None

            try:
                wm.rm_watch(list(wdd.values()), rec=True)
                pass
            except:
                pass

            tasks = glob.glob(folder_path+'/*_task.json')
            for task_path in tasks:
                log.info('Task found in: {}'.format(task_path))
                try:
                    with open(task_path, 'r') as f:
                        task = Task(json.load(f))
                    service.handle_task(task)

                    while os.path.exists(task_path):
                        time.sleep(1)
                except IOError:
                    pass
    finally:
        notifier.stop()
        service.stop_service()


def get_service_config(yml_config=None):
    if yml_config is None:
        yml_config = "/etc/assemblyline/service_config.yml"

    default_file = os.path.join(os.path.dirname(__file__), "common", "service_config.yml")
    if os.path.exists(default_file):
        with open(default_file, 'r') as default_fh:
            service_config = yaml.safe_load(default_fh.read())

    # Load modifiers from the service
    service = svc_class()
    service_data = service.get_default_config()
    service_config = recursive_update(service_config, service_data)
    service_config['SERVICE_TOOL_VERSION'] = service.get_tool_version()

    with open(yml_config, 'w') as yml_fh:
        yaml.safe_dump(service_config, yml_fh)

    return service_config['SERVICE_DEFAULT_CONFIG']


if __name__ == '__main__':

    name = os.environ['SERVICE_PATH']

    svc_name = name.split(".")[-1].lower()
    al_log.init_logging(log_level=logging.INFO)
    log = logging.getLogger('assemblyline.svc.%s' % svc_name)

    try:
        svc_class = load_module_by_path(name)
    except:
        log.error('Could not find service in path.')
        raise

    cfg = get_service_config()

    try:
        run_service()
    except Exception as e:
        log.error(str(e))
