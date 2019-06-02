from fpdf import FPDF
from typing import Tuple, List
from . import PageOrientation


class PDF:
    image_path: str
    title: str
    orientation: PageOrientation
    pdf: FPDF

    scale: str
    scale_unit: int
    scale_labels: List[str]

    title_height: float
    page_width: float
    margin_top: float
    margin_side: float
    body_width: float
    image_margin_side: float
    image_width: float
    image_height: float

    def __init__(self, image_path: str, scale: str, scale_unit: int, scale_labels: List[str],
                 pdf_size: Tuple[float, float], box_mm: int, orientation: PageOrientation = PageOrientation.LANDSCAPE,
                 title: str = None):
        self.image_path = image_path
        self.scale = scale
        self.scale_unit = scale_unit
        self.scale_labels = scale_labels
        self.orientation = orientation
        self.pdf = FPDF(orientation='P' if orientation == PageOrientation.PORTRAIT else 'L')
        if title is None:
            title = ""
        self.title = title
        self.image_margin_side = 2
        self.margin_top = 10

        if orientation == PageOrientation.PORTRAIT:
            self.pdf = FPDF(orientation='P')
            self.title_height = 15
            self.page_width = 210

        else:
            self.pdf = FPDF(orientation='L')
            self.title_height = 10
            self.page_width = 297

        self.image_width = pdf_size[0] * box_mm
        self.image_height = pdf_size[1] * box_mm
        self.margin_side = (self.page_width - self.image_width - self.image_margin_side * 2) / 2
        self.body_width = self.page_width - self.margin_side * 2

    def _draw_scale(self, x: float, y: float, u: float) -> None:
        self.pdf.rect(x=x, y=y,  w=u * 10, h=2)
        self.pdf.line(x1=x,      y1=y + 1, x2=x + u, y2=y + 1)  # Horizontal
        self.pdf.line(x1=x + u * 1, y1=y,     x2=x + u * 1, y2=y + 2)  # Vertical
        self.pdf.line(x1=x + u * 2, y1=y,     x2=x + u * 2, y2=y + 2)  # Vertical
        self.pdf.line(x1=x + u * 2, y1=y + 1, x2=x + u * 3, y2=y + 1)  # Horizontal
        self.pdf.line(x1=x + u * 3, y1=y,     x2=x + u * 3, y2=y + 2)  # Vertical
        self.pdf.line(x1=x + u * 4, y1=y,     x2=x + u * 4, y2=y + 2)  # Vertical
        self.pdf.line(x1=x + u * 4, y1=y + 1, x2=x + u * 5, y2=y + 1)  # Horizontal
        self.pdf.line(x1=x + u * 5, y1=y,     x2=x + u * 5, y2=y + 2)  # Vertical
        self.pdf.line(x1=x + u * 6, y1=y,     x2=x + u * 6, y2=y + 2)  # Vertical
        self.pdf.line(x1=x + u * 6, y1=y + 1, x2=x + u * 7, y2=y + 1)  # Horizontal
        self.pdf.line(x1=x + u * 7, y1=y,     x2=x + u * 7, y2=y + 2)  # Vertical
        self.pdf.line(x1=x + u * 8, y1=y,     x2=x + u * 8, y2=y + 2)  # Vertical
        self.pdf.line(x1=x + u * 8, y1=y + 1, x2=x + u * 9, y2=y + 1)  # Horizontal
        self.pdf.line(x1=x + u * 9, y1=y,     x2=x + u * 9, y2=y + 2)  # Vertical

    def _draw_scale_text(self, x: float):

        self.pdf.set_font(family="", size=8)
        self.pdf.cell(x - (self.scale_unit/2 + self.margin_side), 3)
        self.pdf.cell(self.scale_unit, 3, txt=self.scale_labels[0], align="C")
        self.pdf.set_font(family="", size=6)
        self.pdf.cell(self.scale_unit, 3, txt=self.scale_labels[1], align="C")
        self.pdf.cell(self.scale_unit, 3, txt=self.scale_labels[2], align="C")
        self.pdf.cell(self.scale_unit, 3, txt=self.scale_labels[3], align="C")
        self.pdf.cell(self.scale_unit, 3, txt=self.scale_labels[4], align="C")
        self.pdf.cell(self.scale_unit, 3, txt=self.scale_labels[5], align="C")
        self.pdf.cell(self.scale_unit, 3, txt=self.scale_labels[6], align="C")
        self.pdf.cell(self.scale_unit, 3, txt=self.scale_labels[7], align="C")
        self.pdf.cell(self.scale_unit, 3, txt=self.scale_labels[8], align="C")
        self.pdf.cell(self.scale_unit, 3, txt=self.scale_labels[9], align="C")
        self.pdf.set_font(family="", size=8)
        self.pdf.cell(self.scale_unit, 3, txt=self.scale_labels[10], align="C")
        self.pdf.cell(0, 0, ln=1)

    def _draw_cell_padding(self, h: float):
        self.pdf.cell(0, h, ln=1)

    def draw(self):

        # Initialise page
        self.pdf.set_auto_page_break(False)
        self.pdf.set_margins(left=self.margin_side, right=self.margin_side, top=self.margin_top)
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)

        # Page Title
        self.pdf.cell(self.body_width, self.title_height, txt=self.title, ln=1, align="C")

        # Map Image
        self.pdf.cell(self.body_width, self.image_height + 2, ln=1)
        self.pdf.image(self.image_path, x=self.margin_side + self.image_margin_side,
                       y=self.margin_top + self.title_height, w=self.image_width, h=self.image_height)

        # Surrounding Rectangles
        self.pdf.rect(x=self.margin_side + self.image_margin_side, y=self.margin_top + self.title_height,
                      w=self.image_width, h=self.image_height)
        self.pdf.rect(x=self.margin_side, y=self.margin_top, w=self.image_width + self.image_margin_side * 2,
                      h=self.image_height + self.margin_top + self.title_height + 10)

        # Map Scale Text
        self.pdf.set_font("", size=8)
        self.pdf.cell(self.body_width, 4, txt="Scale " + self.scale, ln=1, align="C")

        # Map Scale
        self._draw_scale(x=self.page_width / 2 - (self.scale_unit * 5), y=self.image_height + self.margin_top + self.title_height + 10, u=self.scale_unit)
        self._draw_cell_padding(h=0.5)
        self._draw_scale_text(self.page_width / 2 - (self.scale_unit * 5))
        self._draw_cell_padding(h=6.75)

        # Projection
        self.pdf.cell(self.body_width, 5, txt="Projection: British National Grid", ln=1, align="C")

    def save(self, filename: str):
        self.pdf.output(filename)
