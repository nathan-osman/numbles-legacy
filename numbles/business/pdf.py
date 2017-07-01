from reportlab.lib.colors import black
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table
from reportlab.platypus.flowables import HRFlowable


class InvoiceGenerator:
    """
    Generate a PDF for an invoice
    """

    _MARGIN = inch / 2

    def __init__(self, fileobj, invoice):
        self._invoice = invoice
        self._doc = SimpleDocTemplate(
            fileobj,
            pagesize=letter,
            leftMargin=self._MARGIN,
            rightMargin=self._MARGIN,
            topMargin=self._MARGIN,
            bottomMargin=self._MARGIN,
        )

    def _draw_page(self, canvas, doc):
        canvas.saveState()
        canvas.line(
            self._MARGIN,
            letter[1] - self._MARGIN,
            letter[0] - self._MARGIN,
            letter[1] - self._MARGIN,
        )
        canvas.line(
            self._MARGIN,
            self._MARGIN,
            self._MARGIN,
            letter[1] - self._MARGIN,
        )
        canvas.line(
            letter[0] - self._MARGIN,
            letter[1] - self._MARGIN,
            letter[0] - self._MARGIN,
            self._MARGIN,
        )
        canvas.line(
            self._MARGIN,
            self._MARGIN,
            letter[0] - self._MARGIN,
            self._MARGIN,
        )
        canvas.setFont("Helvetica", 10)
        canvas.drawString(
            inch * 0.75,
            inch * 0.75,
            "Invoice amount due in 30 days",
        )
        canvas.restoreState()

    def _header_table(self):
        c = self._invoice.client
        u = self._invoice.user
        data = (
            (
                "Bill From:",
                "{}\n{}".format(
                    u.get_full_name() or u.username,
                    u.profile.address.replace('\r', ''),
                ),
                unicode(self._invoice),
            ),
            ("Bill To:", "{}\n{}\n\n{}\n{}".format(
                c.name,
                c.address.replace('\r', ''),
                c.contact,
                c.email,
            ), "Dated:", self._invoice.date),
        )
        style = (
            ('ALIGNMENT', (2, 0), (2, 0), 'RIGHT'),
            ('ALIGNMENT', (3, 1), (3, 1), 'RIGHT'),
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONT', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (2, 0), (2, 0), 16),
            ('SPAN', (2, 0), (3, 0)),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('VALIGN', (2, 0), (-1, -1), 'BOTTOM'),
        )
        colWidths = (
            inch,
            4 * inch,
            inch,
            inch,
        )
        return Table(data, style=style, colWidths=colWidths)

    def _entry_table(self):
        data = []
        for e in self._invoice.entries.all():
            data.append(
                (
                    Paragraph(
                        e.description.replace('\n', '<br/>'),
                        getSampleStyleSheet()['Normal'],
                    ),
                    "${}".format(e.amount),
                ),
            )
        style = (
            ('ALIGNMENT', (1, 0), (-1, -1), 'RIGHT'),
        )
        colWidths = (
            5 * inch,
            2 * inch,
        )
        return Table(data, style=style, colWidths=colWidths)

    def _total_table(self):
        data = (
            ("Invoice amount:", "${}".format(self._invoice.amount)),
        )
        style = (
            ('ALIGNMENT', (1, 0), (-1, -1), 'RIGHT'),
        )
        colWidths = (
            5 * inch,
            2 * inch,
        )
        return Table(data, style=style, colWidths=colWidths)

    def generate(self):
        content = [
            self._header_table(),
            Spacer(0, inch * 0.1),
            HRFlowable(width='100%', color=black),
            HRFlowable(width='100%', color=black),
            Spacer(0, inch * 0.1),
            self._entry_table(),
            Spacer(0, inch * 0.1),
            HRFlowable(width='100%', color=black),
            Spacer(0, inch * 0.1),
            self._total_table(),
        ]
        self._doc.build(content, onFirstPage=self._draw_page, onLaterPages=self._draw_page)


