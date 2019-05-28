import pytest


@pytest.fixture
def pages(current_directory, config):
    from flatfilecms.resources import Root
    return Root(
        str(current_directory / 'pages'))


def test_loading(pages):
    assert 'index' in pages


def test_loading_markdown(pages):
    assert pages['index'].page['title'] == 'Заглушка для тестов БД'


def test_generating_markdown(pages, fake_request, config):
    from flatfilecms.views.pages import PagesView
    view = PagesView(pages['index'], fake_request)
    assert view.process_yaml().text == 'Hello World!'


def test_view(pages, fake_request, config):
    from flatfilecms.views.pages import PagesView
    view = PagesView(pages['view'], fake_request)
    assert view.process_yaml().text == 'Hello World! View1'


def test_view_with_options(pages, fake_request, config):
    from flatfilecms.views.pages import PagesView
    view = PagesView(pages['view-with-options'], fake_request)
    assert view.process_yaml().text == 'Hello World! View4(a)'


def test_views(pages, fake_request, config):
    from flatfilecms.views.pages import PagesView
    view = PagesView(pages['views'], fake_request)
    assert view.process_yaml().text == \
        'Hello World! View1 View2 View3(a:1, b:2)'


def test_blogindex(pages, fake_request, config):
    from flatfilecms.views import blog
    from flatfilecms.views.pages import PagesView
    fake_view_object = PagesView(pages['blog']['index'], fake_request)
    response = blog(fake_view_object, {'base': '/blog'})
    assert response.text == '/blog/blogpost2 /blog/blogpost1 '


def test_sitemap(pages, fake_request, config):
    from flatfilecms.views.pages import PagesView
    response = PagesView(pages['sitemap.xml'], fake_request).process_yaml()
    assert response.text == """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
   <url>
     <loc>https://flatfilecms.test/</loc>
   </url>
   <url>
     <loc>https://flatfilecms.test/view</loc>
   </url>
   <url>
     <loc>https://flatfilecms.test/views</loc>
   </url>
   <url>
     <loc>https://flatfilecms.test/view-with-options</loc>
   </url>
   <url>
     <loc>https://flatfilecms.test/menu</loc>
   </url>
</urlset>"""
    assert response.content_type == 'text/xml'


def test_menu(pages, fake_request, config):
    from flatfilecms.views.pages import PagesView
    response = PagesView(pages['menu'], fake_request).process_yaml()
    assert response.text == 'Menu - OK'
