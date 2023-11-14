from django import template
from django.utils.html import format_html
from bs4 import BeautifulSoup
from django.templatetags.static import static
from ..blogcomponents.register import PATHS, PROPERTY_TABLE_PATH

register = template.Library()


@register.simple_tag
def tools_list(attrs):
    formatted_html = []
    for path in PATHS:
        with open(path) as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")
        template = soup.find("template")

        formatted_html.append(
            format_html(
                r"<li id={} tooltype={} %attrs>{}</li>".replace(r"%attrs", attrs),
                template.attrs["id"],
                template.attrs["tooltype"],
                template.attrs["verbose-name"],
            )
        )

    return format_html("".join(formatted_html))


@register.simple_tag
def templates(attrs=""):
    formatted_html = []
    for path in PATHS:
        with open(path) as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")
        template = soup.find("template")
        template.attrs["for"] = template.attrs["id"]
        template.attrs["id"] = template.attrs["id"].replace("tool", "element-template")

        if attrs:
            attrs_list = attrs.replace("'", "").replace('"', "").strip().split()
            child = template.findChild()
            child.attrs |= {a.split("=")[0]: a.split("=")[1] for a in attrs_list}

        formatted_html.append(template.__str__())

    return format_html("".join(formatted_html))


@register.simple_tag
def property_list(update_method):
    with open(PROPERTY_TABLE_PATH) as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("li")
    formatted_html = []
    for li_item in items:
        for html_input in li_item.find_all("input") + li_item.find_all("select"):
            html_input.attrs["oninput"] = update_method

        formatted_html.append(li_item.__str__())

    return format_html("".join(formatted_html))
