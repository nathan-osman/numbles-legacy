from django.http import HttpResponse
from reportlab.lib.colors import black
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table

from .exporter import Exporter


class PDFExporter(Exporter):
    """
    Export to PDF
    """

    _MARGIN = inch / 2

    def export(self, transactions):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="numbles.pdf"'
        doc = SimpleDocTemplate(
            response,
            pagesize=letter,
            leftMargin=self._MARGIN,
            rightMargin=self._MARGIN,
            topMargin=self._MARGIN,
            bottomMargin=self._MARGIN,
        )
        data = [
            [self.TITLES[c] for c in self.COLUMNS],
        ]
        for t in transactions:
            row = []
            for c in self.COLUMNS:
                row.append(self.column(c, t))
            data.append(row)
        style = (
            ('ALIGNMENT', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGNMENT', (-1, 0), (-1, -1), 'RIGHT'),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('LINEABOVE', (0, 1), (-1, -1), 0.25, black),
        )
        doc.build([Table(data, style=style)])
        return response
