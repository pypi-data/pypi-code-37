import os

from fxqioccore.stereotype import Component

from fxqgeoffrey.model import Task


@Component
class TaskRunner:

    def run_task(self, task: Task):
        for cmd in task.script_commands:
            print("Running %s" % cmd)
            os.system(cmd)
