from typing import TYPE_CHECKING, Optional
from .utils import smart_method
if TYPE_CHECKING:
    from .user import User
    from ..client import Client


class PreCheckoutQuery:
    def __init__(
        self,
        id: Optional[str] = None,
        from_user: Optional["User"] = None,
        currency: Optional[str] = None,
        total_amount: Optional[int] = None,
        invoice_payload: Optional[str] = None,
        **kwargs
    ) -> None:
        self.id = id
        self.from_user = from_user
        self.currency = currency
        self.total_amount = total_amount
        self.invoice_payload = invoice_payload
        self.client = kwargs.get("client", None)

    @smart_method
    async def answer(self, ok: bool, error_message: str = None) -> bool:
        """Answers to a 'PreCheckoutQuery' update

        Args:
            ok (bool): True for allowing the payment and False for showing the error message
            error_message (str): Optional: An string to show the user if the `ok` argument is False

        Returns:
            bool: True in success
        """

        return await self.client.answer_pre_checkout_query(self, ok, error_message)
