from .csv import CSVExporter
from .excel import ExcelExporter
from .pdf import PDFExporter


class InvalidFormatError(Exception):
    def __init__(self, fmt):
        super(InvalidFormatError, self).__init__(
            "Invalid format '{}' supplied.".format(fmt),
        )


_formats = {
    'csv': CSVExporter,
    'excel': ExcelExporter,
    'pdf': PDFExporter
}


def export(fmt, transactions):
    """
    Export the list of transactions in the specified format
    """
    if fmt in _formats:
        return _formats[fmt]().export(transactions)
    raise InvalidFormatError(fmt)
