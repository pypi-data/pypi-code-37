import re
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPFound
from pyramid.traversal import (find_root, find_resource)

from flatfilecms.models import (Folder, YAML, Markdown)


def redirect(self, url):
    return HTTPFound(location=url)


def set_content_type(self, content_type):
    self.request.response.content_type = content_type


def blog(self, options={}):
    path = options.get('base', '')
    format = options.get('format', 'blogposts')
    root = find_root(self.context)
    tree = find_resource(root, path)
    postlist = []
    for name, item in tree.walk():
        if isinstance(item, (YAML, Markdown)) and 'published' in item.page:
            postlist.append((f"{path}/{name}", item))
    post = self.context.page.copy()
    post['pages'] = sorted(
        postlist, key=lambda t: t[1].page['published'], reverse=True)
    if format == 'atom':
        set_content_type(self, 'application/atom+xml')
    return render_to_response(
        '{0}.jinja2'.format(post.get('template', format)),
        post,
        request=self.request,
        response=self.request.response)


def sitemap(self, options={}):
    ignore = [re.compile(i) for i in options.get('ignore', [])]
    root = find_root(self.context)
    post = self.context.page.copy()
    post['pages'] = []
    for name, item in root.walk():
        if not isinstance(item, Folder) and name != 'sitemap.xml' and not next(
            (True for r in ignore if r.match(name)), False):
            lastmod = None
            if isinstance(item,
                          (YAML, Markdown)) and ('published' in item.page
                                                 or 'updated' in item.page):
                lastmod = (item.page.get('updated')
                           or item.page.get('published')).strftime('%Y-%m-%d')
            post['pages'].append((name, lastmod))
    set_content_type(self, 'text/xml')
    return render_to_response(
        '{0}.jinja2'.format(post.get('template', 'sitemap')),
        post,
        request=self.request,
        response=self.request.response)
