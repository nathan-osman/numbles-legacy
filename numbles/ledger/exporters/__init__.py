from .csv import write_csv


class InvalidFormatError(Exception):
    def __init__(self, fmt):
        super(InvalidFormatError, self).__init__(
            "Invalid format '{}' supplied.".format(fmt),
        )


formats = {
    'csv': write_csv,
}


def export(format, transactions):
    """
    Export the list of transactions in the specified format.
    """
    if format in formats:
        return formats[format](transactions)
    raise InvalidFormatError(format)
