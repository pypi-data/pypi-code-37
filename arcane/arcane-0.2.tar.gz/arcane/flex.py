from .components import Container


class Row(Container):
    def __init__(self, childs=[], style=""):
        Container.__init__(self, childs, style=style)
        self.class_name = "row"


class Flex(Container):
    def __init__(self, childs=[], style=""):
        Container.__init__(self, childs, style=style)
        self.class_name = "container"


class Col(Container):
    def __init__(self, childs=[], xs=None, sm=None, md=None, lg=None, xl=None, style=""):
        Container.__init__(self, childs, style=style)

        self.xs = xs
        self.sm = xs if sm is None else sm
        self.md = sm if md is None else md
        self.lg = md if sm is None else lg
        self.xl = lg if sm is None else xl

    def _build_cols(self):
        xs = "" if self.xs is None else "col-" + str(self.xs)
        sm = "" if self.sm is None else "col-sm-" + str(self.sm)
        md = "" if self.md is None else "col-md-" + str(self.md)
        lg = "" if self.lg is None else "col-lg-" + str(self.lg)
        xl = "" if self.xl is None else "col-xl-" + str(self.xl)

        return xs + " " + sm + " " + md + " " + lg + " " + xl

    def _parse_tag(self, scripts):
        return "<{} class='{}' {} id='{}' style='{}'>{}</{}>".format(self.tag, self._build_cols(), self._parse_parameters(), self._id, self._build_css(), self._html(scripts=scripts), self.tag)
