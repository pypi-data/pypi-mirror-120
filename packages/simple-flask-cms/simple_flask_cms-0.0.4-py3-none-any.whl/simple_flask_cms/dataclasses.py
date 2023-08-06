import pydantic


class StrippedPage(pydantic.BaseModel):
    path: str
    title: str
    nav_title: str
    sort_order: int
    subpages: list = []


class Page(StrippedPage):
    content: str
    html: str = ""


class Image(pydantic.BaseModel):
    file: str
    page: str
    mime_type: str
    size: int
