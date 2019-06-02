from .components import *
from flask import Flask
import threading
import sys


class Page():
    title = ""
    css = ""
    js = ""
    body_style = """"""

    def header():
        return Paragraph("")

    def render():
        return ""

    @staticmethod
    def load_scripts(elements):
        return " ".join([element._load_events() for element in elements])

    @classmethod
    def build(cls):
        html = Container(tag="html")

        bootstrap_css = HeaderLink(
            "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css", "stylesheet")

        charset = Meta()
        charset.parameters["charset"] = "utf-8"

        viewport = Meta(
            name="viewport", content="width=device-width, initial-scale=1, shrink-to-fit=no")

        title = Paragraph(cls.title, tag="title")
        head = Container(
            [charset, viewport, title, cls.header(), bootstrap_css], tag="head")

        script = Paragraph(tag="script")
        script._id = "arcane_scripts"

        jquery = Script("https://code.jquery.com/jquery-3.3.1.slim.min.js")
        popper = Script(
            "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js")
        bootstrap_script = Script(
            "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js")

        body = Container([cls.render(), jquery, popper,
                          bootstrap_script], tag="body", style=cls.body_style)

        html.append_childs([head, body, script])

        return html._build(script)
