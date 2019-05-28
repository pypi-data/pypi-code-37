from pyramid.config import Configurator

from flatfilecms.resources import root_factory


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings.setdefault('pages_path', 'pages')
    settings.setdefault('data_path', 'data')
    default_jinja2_filters = """markdown = flatfilecms.filters:markdown2html
        fileglob = flatfilecms.filters:fileglob
        merge_dict = flatfilecms.filters.merge_dict
        join_url = flatfilecms.filters.join_url"""
    settings['jinja2.filters'] = default_jinja2_filters + settings.get(
        'jinja2.filters', '')

    config = Configurator(settings=settings, root_factory=root_factory)
    config.include('pyramid_jinja2')
    config.include('.routes')
    config.scan()
    return config.make_wsgi_app()
