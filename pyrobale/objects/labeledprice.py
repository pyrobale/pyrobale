class LabeledPrice:
    def __init__(self, label: str, amount: int) -> None:
        self.label = label
        self.amount = amount

    @property
    def json(self):
        return {"label": self.label, "amount": self.amount}
