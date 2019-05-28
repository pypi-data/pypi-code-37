from pyramid.view import (
    view_config,
    render_view_to_response,
)
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import FileResponse
from pyramid.path import (DottedNameResolver, AssetResolver)

from flatfilecms.models import (Folder, Document, IMarkdown, Jinja2)


class PagesView:
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(context=Folder)
    def folder(self):
        if 'index' not in self.context:
            raise HTTPNotFound
        return render_view_to_response(self.context['index'], self.request)

    @view_config(context=Document)
    def document(self):
        return FileResponse(
            AssetResolver().resolve(self.context.path).abspath(),
            request=self.request)

    @view_config(context=IMarkdown)
    def process_yaml(self):
        if 'view' in self.context.page:
            r = DottedNameResolver()
            if isinstance(self.context.page['view'], str):
                response = r.resolve(self.context.page['view'])(self)
                if response:
                    return response
            elif isinstance(self.context.page['view'], dict):
                for name, options in self.context.page['view'].items():
                    response = r.resolve(name)(self, options)
                    if response:
                        return response
            else:
                for view in self.context.page['view']:
                    if isinstance(view, str):
                        response = r.resolve(view)(self)
                        if response:
                            return response
                    else:
                        for name, options in view.items():
                            response = r.resolve(name)(self, options)
                            if response:
                                return response
        post = self.context.page
        return render_to_response(
            '{0}.jinja2'.format(post.get('template', 'default')),
            post,
            request=self.request,
            response=self.request.response)

    @view_config(context=Jinja2)
    def jinja2(self):
        return render_to_response(self.context.path, {}, request=self.request)
