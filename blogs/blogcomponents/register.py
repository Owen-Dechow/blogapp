from django.conf import settings

_BASE_DIR = settings.BASE_DIR
_PATH = _BASE_DIR / "blogs" / "blogcomponents"

files = [
    "header1.html",
    "header2.html",
    "header3.html",
    "paragraph.html",
]

PATHS = [_PATH / f for f in files]
PROPERTY_TABLE_PATH = _PATH / "property_list.html"
