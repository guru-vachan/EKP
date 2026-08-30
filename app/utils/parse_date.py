from datetime import datetime


def parse_pdf_date(value: str) -> datetime:
    """

        PyMuPDF commonly returns PDF dates like:
            D:20240825153000+05'30'
    """
    if not value:
        return None

    value = value.removeprefix("D:")

    try:
        return datetime.strptime(value[:14], "%Y%m%d%H%M%S")
    except ValueError:
        return None