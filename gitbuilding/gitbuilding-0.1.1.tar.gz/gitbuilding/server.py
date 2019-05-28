
import os
import socket
import flask
import codecs
import yaml
from markdown import markdown
import gitbuilding as gb
import datetime


class GBServer(flask.Flask):
    """
    GBServer is the Git Building server it uses Flask to render documentation
    """
    def __init__(self,homepage):

        self.homepage = homepage
        self.homepath = os.path.dirname(homepage)
        self.gbpath = os.path.dirname(gb.__file__)
        with open(os.path.join(self.homepath,'_data','project.yaml'), 'r') as stream:
            self.project_data = yaml.load(stream, Loader=yaml.FullLoader)
            
        super(GBServer, self).__init__( __name__,static_folder=self.homepath)
        # set page rendering
        self.add_url_rule('/', 'render', self._render_page)
        self.add_url_rule('/<path:subpath>', 'render', self._render_page) 
        
        self.renderer = GBRenderer(self.project_data)
    
    def _render_page(self, subpath=None):
        # define special page for missing
        if subpath == 'missing':
            return self.renderer.missing_page()
        if subpath is None:
            page=self.homepage
        else:
            page = os.path.join(self.homepath,subpath)
        
        if os.path.isfile(page):
            if page.endswith('.md'):
                return self.renderer.render_md_file(page,subpath)
            else:
                return flask.send_file(os.path.abspath(page))
            
        page = os.path.join(self.gbpath,subpath)
        if os.path.isfile(page):
            return flask.send_file(page)
        flask.abort(404)

    def run(self, host='localhost', port=6178, debug=None):
        # Run local server
        super(GBServer, self).run(host, port)


class GBRenderer():
    
    def __init__(self,project_data):
        self.gbpath = os.path.dirname(gb.__file__)
        self.project_data = project_data
        self.link = None
    
    def header(self):
        return f"""<!DOCTYPE html>
<html>
<head>
    <title>{self.project_data['Title']}</title>
    <link rel="shortcut icon" href="/static/Logo/favicon.ico" />
    <link rel="icon" type="image/png" href="/static/Logo/favicon-32x32.png" sizes="32x32" />
    <link rel="icon" type="image/png" href="/static/Logo/favicon-16x16.png" sizes="16x16" />
    <link href="/static/style.css" rel="stylesheet">
</head>
<body>
<header class="site-header">
<div class="wrapper">
{self.project_header()}
</div>
</header>
<div class="page-content">

<nav class="sidebar">
    <a href="#" class="menu-icon">
    <svg viewBox="0 0 18 15">
        <path fill="#424242" d="M18,1.484c0,0.82-0.665,1.484-1.484,1.484H1.484C0.665,2.969,0,2.304,0,1.484l0,0C0,0.665,0.665,0,1.484,0 h15.031C17.335,0,18,0.665,18,1.484L18,1.484z"/>
        <path fill="#424242" d="M18,7.516C18,8.335,17.335,9,16.516,9H1.484C0.665,9,0,8.335,0,7.516l0,0c0-0.82,0.665-1.484,1.484-1.484 h15.031C17.335,6.031,18,6.696,18,7.516L18,7.516z"/>
        <path fill="#424242" d="M18,13.516C18,14.335,17.335,15,16.516,15H1.484C0.665,15,0,14.335,0,13.516l0,0 c0-0.82,0.665-1.484,1.484-1.484h15.031C17.335,12.031,18,12.696,18,13.516L18,13.516z"/>
    </svg>
    </a>
    <div class="trigger">
    {self.page_links()}
    </div>
</nav>
<div class="wrapper">"""

    def page_links(self):
        html=f'<a class="navhome" href="/">{self.project_data["Title"]}</a>'
        for page in self.project_data['PageList']:
            if page["Link"] == self.link:
                class_txt = 'class="active" '
            else:
                class_txt = ''
            html+=f'<a {class_txt}href="/{page["Link"]}">{page["Title"]}</a>'
        return html


    def authorlist(self):
        text = ''
        for i,author in enumerate(self.project_data['Authors']):
            if i==0:
                pass
            elif i==Nauth-1:
                text+=', and '
            else:
                text+=', '
            text+=f'{author}'
        return text
        
    def project_header(self):
        html = ''
        if self.project_data['Title'] is not None:
            html+=f'<a class="site-title" href="/">{self.project_data["Title"]}</a>'
        if self.project_data['Authors'] is not None:
            html+='<p class="author">by '
            Nauth = len(self.project_data['Authors'])
            html+=self.authorlist()
            html+='</p>'
        if self.project_data['Affiliation'] is not None:
            html+=f'<p class="affiliation">{self.project_data["Affiliation"]}</p>'
        return html
    
    def footer(self):
        return f"""</div>
</div>
<footer class="site-footer">
<div class="wrapper">
<span class="icon">{codecs.open(os.path.join(self.gbpath,'static','Logo','GitBuilding.svg'), mode="r", encoding="utf-8").read()}</span>
<span class="info">Documentation powered by Git Building</span>
{self.project_footer()}
</div>
</footer>
</body>
</html>"""

    def project_footer(self):
        html=''
        if self.project_data['Authors'] is not None:
            html+='<p class="author">© '
            Nauth = len(self.project_data['Authors'])
            html+=self.authorlist()
            html+=f' {datetime.datetime.now().year}</p>'
        if self.project_data['Email'] is not None:
            html+=f'<p class="email">Contact: <a href="mailto:{self.project_data["Email"]}">{self.project_data["Email"]}</a></p>'
        if self.project_data['License'] is not None:
            html+=f'<p class="license">{self.project_data["Title"]} is released under {self.project_data["License"]}</p>'
        return html

    def render_md_file(self,page,link):
        return self.render(markdown(codecs.open(page, mode="r", encoding="utf-8").read(),extensions=['tables']),link)
        
    def render(self,html,link):
        self.link = link
        output = self.header()
        output+=html
        output+=self.footer()
        return output
    
    def missing_page(self):
        return self.render('<h1>Git Building Missing Part</h1>')