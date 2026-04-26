class Transaction:
    def __init__(self,
    id: str,
    status: str,
    userID: int,
    amount: int,
    provider_payment_charge_id: str,
    createdAt: int):
        self.id = id
        self.status = status
        self.userID = userID
        self.amount = amount
        self.provider_payment_charge_id = provider_payment_charge_id
        self.createdAt = createdAt