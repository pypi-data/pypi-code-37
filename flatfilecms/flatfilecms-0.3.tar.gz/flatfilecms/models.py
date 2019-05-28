from pathlib import PurePath
import yaml
import frontmatter
import markdown
from datetime import datetime
from pyramid.path import AssetResolver
from zope.interface import (Interface, implementer)
from pyramid.threadlocal import get_current_registry

from flatfilecms.filters import IgnoreExtension


class Loader(yaml.Loader):
    def __init__(self, stream):
        super(Loader, self).__init__(stream)
        Loader.add_constructor('!include', Loader.include)
        Loader.add_constructor('!markdown', Loader.markdown)

    def include(self, node):
        if isinstance(node, yaml.ScalarNode):
            return self.extractFile(self.construct_scalar(node))

        elif isinstance(node, yaml.SequenceNode):
            return [self.extractFile(filename)
                    for filename in self.construct_sequence(node)]

        elif isinstance(node, yaml.MappingNode):
            result = {}
            for k, v in self.construct_mapping(node).items():
                result[k] = self.extractFile(v)
            return result

        else:
            raise yaml.constructor.ConstructorError(
                    "Error:: unrecognised node type in !include statement")

    def markdown(self, node):
        if not isinstance(node, yaml.ScalarNode):
            raise yaml.constructor.ConstructorError(
                    "Error:: unrecognised node type in !markdown statement")
        m = self.construct_scalar(node)
        return markdown.markdown(
            m,
            extensions=[IgnoreExtension(), 'markdown.extensions.extra'],
            output_format='html5',
            tab_length=2)

    def extractFile(self, filename):
        path = PurePath(self.data_path) / filename
        f = AssetResolver().resolve(str(path)).stream()
        if f:
            if path.suffix in ['.yaml', '.yml', '.json']:
                return yaml.load(f, Loader)
            return f.read().decode()


def LoaderFactory(data_path):
    cl = Loader
    cl.data_path = data_path
    return cl


class CustomYAMLHandler(frontmatter.YAMLHandler):
    def __init__(self, data_path):
        self.loader = LoaderFactory(data_path)

    def load(self, fm, **kwargs):
        return yaml.load(fm, self.loader)


def load_yaml(path, data=False):
    registry = get_current_registry()
    settings = registry.settings
    data_path = settings['data_path']
    if data:
        path = str(PurePath(data_path) / path)
    return yaml.load(
        AssetResolver().resolve(path).stream(),
        LoaderFactory(data_path))


def load_frontmatter(path):
    registry = get_current_registry()
    settings = registry.settings
    data_path = settings['data_path']
    return frontmatter.load(
        AssetResolver().resolve(path).stream(),
        handler=CustomYAMLHandler(data_path),
    ).to_dict()


class HiddenFile(Exception):
    pass


class Folder(dict):
    def __init__(self, name, parent, path):
        self.path = path
        self.name = name
        self.__parent__ = parent
        for entry in AssetResolver().resolve(path).listdir():
            asset = f"{path}/{entry}"
            if AssetResolver().resolve(asset).isdir():
                self.create_dir(asset)
            else:
                self.create_file(asset)

    def create_file(self, asset):
        path = PurePath(asset)
        try:
            if path.suffix == '.md':
                self[path.stem] = Markdown(path.stem, self, asset)
            elif path.suffix == '.yaml':
                self[path.stem] = YAML(path.stem, self, asset)
            elif path.suffix == '.j2' or path.suffix == '.jinja2':
                self[path.stem] = Jinja2(path.stem, self, asset)
            else:
                name = path.name
                # Если имя файла не index.html,
                # то отдавать по имени файла
                if name == 'index.html':
                    name = 'index'
                self[name] = Document(name, self, asset)
        except HiddenFile:
            # Do nothing, file was not added to self
            pass

    def create_dir(self, asset):
        path = PurePath(asset)
        self[path.name] = Folder(path.name, self, asset)

    def walk(self):
        for name, item in self.items():
            if name == 'index':
                name = ''
            yield name, item
            if isinstance(item, Folder):
                for subname, subitem in item.walk():
                    yield f"{name}/{subname}", subitem


class Document(object):
    def __init__(self, name, parent, path):
        self.name = name
        self.__parent__ = parent
        self.path = path


class IMarkdown(Interface):
    """ Интерфейс-маркер для генератора markdown """


@implementer(IMarkdown)
class Markdown(Document):
    def __init__(self, name, parent, path):
        super(Markdown, self).__init__('', parent, path)
        self.page = load_frontmatter(path)
        if 'published' in self.page and \
                self.page['published'] > datetime.now():
            raise HiddenFile


@implementer(IMarkdown)
class YAML(Document):
    def __init__(self, name, parent, path):
        super(YAML, self).__init__('', parent, path)
        self.page = load_yaml(path)
        if 'published' in self.page and \
                self.page['published'] > datetime.now():
            raise HiddenFile


class Jinja2(Document):
    pass
