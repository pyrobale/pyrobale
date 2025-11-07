class Transaction:
    def __init__(self,
    id: str,
    status: str,
    userID: int,
    amount: int,
    createdAt: int):
        self.id = id
        self.status = status
        self.userID = userID
        self.amount = amount
        self.createdAt = createdAt