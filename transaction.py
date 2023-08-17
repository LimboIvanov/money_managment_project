class Transaction:
    def __init__(self, date, category, subcategory, text, amount, balance, status, reconciled):
        self.date = date
        self.category = category
        self.subcategory = subcategory
        self.text = text
        self.amount = amount
        self.balance = balance
        self.status = status
        self.reconciled = reconciled
