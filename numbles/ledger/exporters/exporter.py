class Exporter:
    """
    Base class for all exporters
    """

    COLUMN_ID = 'id'
    COLUMN_DATE = 'date'
    COLUMN_ACCOUNT = 'account'
    COLUMN_SUMMARY = 'summary'
    COLUMN_TAGS = 'tags'
    COLUMN_RECONCILED = 'reconciled'
    COLUMN_AMOUNT = 'amount'

    COLUMNS = (
        COLUMN_ID,
        COLUMN_DATE,
        COLUMN_ACCOUNT,
        COLUMN_SUMMARY,
        COLUMN_TAGS,
        COLUMN_RECONCILED,
        COLUMN_AMOUNT,
    )

    TITLES = {
        COLUMN_ID: "ID",
        COLUMN_DATE: "Date",
        COLUMN_ACCOUNT: "Account",
        COLUMN_SUMMARY: "Summary",
        COLUMN_TAGS: "Tags",
        COLUMN_RECONCILED: "Reconciled",
        COLUMN_AMOUNT: "Amount",
    }

    def column(self, column, transaction):
        """
        Return the raw value for a column
        """
        if column == self.COLUMN_ID:
            return transaction.id
        elif column == self.COLUMN_DATE:
            return transaction.date
        elif column == self.COLUMN_ACCOUNT:
            return transaction.account.name
        elif column == self.COLUMN_SUMMARY:
            return transaction.summary
        elif column == self.COLUMN_TAGS:
            return ', '.join([x.name for x in transaction.tags.all()])
        elif column == self.COLUMN_RECONCILED:
            return transaction.reconciled
        elif column == self.COLUMN_AMOUNT:
            return transaction.amount
