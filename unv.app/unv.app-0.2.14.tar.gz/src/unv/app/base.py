import inspect
import asyncio

from .settings import SETTINGS


class Application:
    """Used for setup in other components to provide universal way
    of decomposing apps."""

    def __init__(self, setup: bool = True):
        self.apps = {type(self): self}
        self.run_tasks = []
        self.async_run_tasks = []
        self.setup_tasks = []

        if setup:
            self.setup()

    def register(self, app):
        type_ = type(app)
        if type_ in self.apps:
            raise ValueError(f'App type: "{type_}" already registered')
        self.apps[type_] = app

    def unregister(self, app):
        type_ = type(app)
        if type_ == type(self):
            raise ValueError(f'Do not unregister self-app: "{type_}"')
        self.apps.pop(type_, None)

    @property
    def components(self):
        return SETTINGS.get_components()

    def add_run_task(self, func):
        if inspect.iscoroutinefunction(func):
            self.async_run_tasks.append(func)
        else:
            self.run_tasks.append(func)

    def add_setup_task(self, func):
        self.setup_tasks.append(func)

    def setup(self):
        for component in self.components:
            annotations = inspect.getfullargspec(component.setup).annotations
            kwargs = {
                name: self.apps[type_]
                for name, type_ in annotations.items()
                if type_ in self.apps
            }
            component.setup(**kwargs)

        for task in self.setup_tasks:
            task(self)

    def run(self):
        for task in self.run_tasks:
            task()

        if not self.async_run_tasks:
            return

        async def async_tasks():
            await asyncio.gather(*[
                task() for task in self.async_run_tasks
            ], return_exceptions=True)

        asyncio.run(async_tasks())
