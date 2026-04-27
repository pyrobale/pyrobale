from .enums import TransactionStatus
from typing import Union
from ..exceptions import PyroBaleException

class Transaction:
    def __init__(self,
    id: str,
    status: Union[str, TransactionStatus],
    userID: int,
    amount: int,
    provider_payment_charge_id: str,
    createdAt: int):
        self.id = id
        
        if isinstance(status, str):
            try:
                self.status = TransactionStatus(status)
            except Exception as e:
                raise PyroBaleException(f"Unexpected error : {e}")
        else:
            self.status = status

        self.userID = userID
        self.amount = amount
        self.provider_payment_charge_id = provider_payment_charge_id
        self.createdAt = createdAt