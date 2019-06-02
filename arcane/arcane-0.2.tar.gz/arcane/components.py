import sys

from .system import error
from .core import Interactive


class Component(Interactive):
    tag = ""
    js = ""
    style = ""
    render_tag = False
    data = {}

    def __init__(self, style="", data={}):
        Interactive.__init__(self)
        self.parameters = {}
        self.style = self.style + style
        self.class_name = ""
        self.data = {**self.data, **data}
        self._pre_render()

    def _build_css(self):
        if self.style == "":
            return ""
        return ";".join(filter(lambda x: len(x) != 1, self.style.split(";")))

    def _parse_parameters(self):
        return " ".join(["{}='{}'".format(key, self.parameters[key]) for key in list(self.parameters)])

    def _parse_tag(self, scripts):
        return "<{} class='{}' {} id='{}' style='{}'>{}</{}>".format(self.tag, self.class_name, self._parse_parameters(), self._id, self._build_css(), self._html(scripts=scripts), self.tag)

    def _build(self, scripts=None):
        if scripts is not None:
            scripts.text += self.js

        if self.tag == "":
            return self._html(scripts)
        else:
            return self._parse_tag(scripts)

    def _html(self, scripts=None):
        return self.child._build(scripts)

    def _pre_render(self):
        self.child = self.render()

    def render(self):
        return None

    @classmethod
    def Styled(cls, style):
        clas = type(str(cls), cls.__bases__, dict(cls.__dict__))
        clas.style = style
        return clas


class Paragraph(Component):
    def __init__(self, text="", style="", tag="p"):
        Component.__init__(self, style=style)
        self.tag = tag
        self.text = text

    def _html(self, scripts):
        return self.text


class Title(Component):
    def __init__(self, text="", size=1, style=""):
        Component.__init__(self, style=style)
        self.tag = "h" + str(size)
        self.text = text
        self.render_tag = True

    def _html(self, scripts):
        return self.text


class Container(Component):
    def __init__(self, childs=[], style="", tag="div"):
        Component.__init__(self, style=style)
        self.childs = []
        self.append_childs(childs)
        self.tag = tag

    def _html(self, scripts):
        return "".join([child._build(scripts) for child in self.childs])

    def append_childs(self, child):
        if type(child) == type([]):
            self.childs = self.childs + child
        else:
            self.childs.append(child)


class Button(Component):
    def __init__(self, text, style=""):
        Component.__init__(self, style=style)
        self.tag = "button"
        self.text = text

    def _html(self, scripts):
        return self.text


class Link(Component):
    def __init__(self, text="", link="", style=""):
        Component.__init__(self, style=style)
        self.tag = "a"
        self.parameters["href"] = link
        self.text = text

    def _html(self, scripts):
        return self.text


class HeaderLink(Component):
    def __init__(self, link="", rel=""):
        Component.__init__(self)
        self.parameters["href"] = link
        self.parameters["rel"] = rel
        self.tag = "link"

    def _parse_tag(self, scripts):
        return "<link {}>".format(self._parse_parameters())

    def _html(self):
        return ""


class Script(Component):
    def __init__(self, src=""):
        Component.__init__(self)
        self.parameters["src"] = src
        self.tag = "script"

    def _parse_tag(self, scripts):
        return "<script {}></script>".format(self._parse_parameters())

    def _html(self):
        return ""


class Meta(Component):
    def __init__(self, name="", content=""):
        Component.__init__(self)
        self.parameters["name"] = name
        self.parameters["content"] = content
        self.tag = "meta"

    def _parse_tag(self, scripts):
        return "<meta {}>".format(self._parse_parameters())

    def _html(self):
        return ""
