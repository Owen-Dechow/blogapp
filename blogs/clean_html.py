from bleach import clean, linkify, Cleaner
from bleach.css_sanitizer import CSSSanitizer
from bs4 import BeautifulSoup


def clean_post(html):
    allowed_tags = [
        "a",
        "br",
        "p",
        "h1",
        "h2",
        "h3",
        "span",
        "code",
        "pre",
        "blockquote",
        "img",
        "li",
    ]

    allowed_attributes = {x: ["class", "style"] for x in allowed_tags}
    allowed_attributes["a"] += ["href", "target", "rel"]
    allowed_attributes["img"] += ["src"]
    allowed_attributes["span"] += ["content-editable"]
    allowed_attributes["pre"] += ["spellcheck"]

    schemas = ["https", "data"]

    styles = [
        "color",
        "background-color",
        "top",
        "margin-right",
        "font-size",
    ]

    cleaner = Cleaner(
        tags=allowed_tags,
        attributes=allowed_attributes,
        css_sanitizer=CSSSanitizer(allowed_css_properties=styles),
        protocols=schemas,
    )

    html = cleaner.clean(html)

    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all("a"):
        a.attrs["target"] = "_blank"

    return soup.__str__()
