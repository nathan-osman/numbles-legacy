from __future__ import absolute_import

import csv

from django.http import HttpResponse

from .exporter import Exporter


class CSVExporter(Exporter):
    """
    Create a CSV file
    """

    def export(self, transactions):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="numbles.csv"'
        writer = csv.writer(response)
        writer.writerow([self.TITLES[c] for c in self.columns()])
        for t in transactions:
            writer.writerow([self.column(c, t) for c in self.columns()])
        return response
