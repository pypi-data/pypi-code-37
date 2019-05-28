from flatfilecms.models import Folder


class Root(Folder):
    def __init__(self, path):
        super(Root, self).__init__('', None, path)


roots = {}


def root_factory(request):
    path = request.registry.settings['pages_path']
    return roots.setdefault(path, Root(path))
