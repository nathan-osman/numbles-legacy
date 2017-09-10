from __future__ import absolute_import

import csv

from django.http import HttpResponse


def write_csv(transactions):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="numbles.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'ID',
        'Date',
        'Account',
        'Summary',
        'Tags',
        'Reconciled',
        'Amount',
    ])
    for t in transactions:
        writer.writerow([
            t.id,
            t.date,
            t.account.name,
            t.summary,
            ', '.join([x.name for x in t.tags.all()]),
            t.reconciled,
            t.amount,
        ])
    return response
