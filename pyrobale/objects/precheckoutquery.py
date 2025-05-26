from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class PreCheckoutQuery:
    def __init__(
        self,
        id: str,
        from_user: "User",
        currency: str,
        total_amount: int,
        invoice_payload: str,
        **kwargs
    ) -> None:
        self.id = id
        self.from_user = from_user
        self.currency = currency
        self.total_amount = total_amount
        self.invoice_payload = invoice_payload
