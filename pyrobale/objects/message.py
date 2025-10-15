from typing import TYPE_CHECKING
from typing import Optional, Union
from ..objects.utils import pythonize

if TYPE_CHECKING:
    from .utils import build_api_url
    from ..objects.user import User
    from ..objects.chat import Chat
    from ..objects.chatphoto import ChatPhoto
    from ..objects.animation import Animation
    from ..objects.audio import Audio
    from ..objects.document import Document
    from ..objects.photosize import PhotoSize
    from ..objects.sticker import Sticker
    from ..objects.video import Video
    from ..objects.voice import Voice
    from ..objects.contact import Contact
    from ..objects.location import Location
    from ..objects.invoice import Invoice
    from ..objects.successfulpayment import SuccessfulPayment
    from ..objects.webappdata import WebAppData
    from ..objects.webappinfo import WebAppInfo
    from ..objects.inlinekeyboardmarkup import InlineKeyboardMarkup
    from ..objects.replykeyboardmarkup import ReplyKeyboardMarkup
    from ..client import Client
from ..objects.chat import Chat
from ..objects.user import User
from ..objects.inlinekeyboardmarkup import InlineKeyboardMarkup


class Message:
    """This class represents a Message object in Telegram.

    A message can contain various types of content like text, media, location, etc.
    It also provides methods to reply, edit, delete, and forward messages.

    Attributes:
        id (int): Unique message identifier
        user (User): Sender of the message
        date (int): Date the message was sent in Unix time
        chat (Chat): Conversation the message belongs to
        text (str): Text content of the message
        forward_from (User): Original sender of a forwarded message
        forward_from_chat (Chat): Original chat of a forwarded message
        forward_from_message_id (int): Message ID in the original chat
        forward_date (int): Date when message was forwarded
        edite_date (int): Date when message was last edited
        animation (Animation): Message is an animation
        audio (Audio): Message is an audio file
        document (Document): Message is a general file
        photo (list[PhotoSize]): Message is a photo
        sticker (Sticker): Message is a sticker
        video (Video): Message is a video
        voice (Voice): Message is a voice message
        caption (str): Caption for media messages
        contact (Contact): Message is a shared contact
        location (Location): Message is a shared location
        new_chat_members (list[User]): New members added to the chat
        left_chat_member (User): Member removed from the chat
        invoice (Invoice): Message is an invoice for payment
        successful_payment (SuccessfulPayment): Message is a service message about successful payment
        web_app_data (WebAppData): Data from a Web App
        reply_markup (InlineKeyboardMarkup): Inline keyboard attached to the message
        client (Client): Client instance associated with this message
    """

    def __init__(
            self,
            message_id: Optional[int] = None,
            from_user: Optional["User"] = None,
            date: Optional[int] = None,
            chat: Optional["Chat"] = None,
            text: Optional[str] = None,
            forward_from: Optional["User"] = None,
            forward_from_chat: Optional["Chat"] = None,
            forward_from_message_id: Optional[int] = None,
            forward_date: Optional[int] = None,
            edite_date: Optional[int] = None,
            animation: Optional["Animation"] = None,
            audio: Optional["Audio"] = None,
            document: Optional["Document"] = None,
            photo: Optional[list["PhotoSize"]] = None,
            sticker: Optional["Sticker"] = None,
            video: Optional["Video"] = None,
            voice: Optional["Voice"] = None,
            caption: Optional[str] = None,
            contact: Optional["Contact"] = None,
            location: Optional["Location"] = None,
            new_chat_members: Optional[list["User"]] = None,
            left_chat_member: Optional["User"] = None,
            invoice: Optional["Invoice"] = None,
            successful_payment: Optional["SuccessfulPayment"] = None,
            web_app_data: Optional["WebAppData"] = None,
            reply_markup: Optional["InlineKeyboardMarkup"] = None,
            reply_to_message: Optional[int] = None,
            client: Optional["Client"] = None,
            **kwargs
    ):
        """Initialize a Message object with the provided attributes.

        Args:
            message_id: Unique message identifier
            from_user: Sender of the message
            date: Date the message was sent in Unix time
            chat: Conversation the message belongs to
            text: Text content of the message
            forward_from: Original sender of a forwarded message
            forward_from_chat: Original chat of a forwarded message
            forward_from_message_id: Message ID in the original chat
            forward_date: Date when message was forwarded in Unix time
            edite_date: Date when message was last edited in Unix time
            animation: Animation content
            audio: Audio content
            document: Document content
            photo: List of photo sizes
            sticker: Sticker content
            video: Video content
            voice: Voice message content
            caption: Caption for media messages
            contact: Contact content
            location: Location content
            new_chat_members: New members added to the chat
            left_chat_member: Member removed from the chat
            invoice: Invoice content
            successful_payment: Successful payment information
            web_app_data: Web App data
            reply_markup: Inline keyboard markup
            reply_to_message: Message ID in the original chat
            client: Client instance associated with this message
            **kwargs: Additional keyword arguments including client instance
        """
        self.client: Client = kwargs.get("kwargs", {}).get("client")
        if not self.client:
            self.client = client
        if reply_to_message != None:
            reply_to_message['client'] = self.client
            self.reply_to_message = Message(**pythonize(reply_to_message))
        else:
            self.reply_to_message = None
        self.id: int = message_id
        self.user: "User" = (
            User(**from_user, kwargs={"client": self.client}) if from_user else None
        )
        self.date: int = date
        if isinstance(chat, Chat):
            self.chat: Chat = chat
        elif chat != None:
            data = chat
            data['client'] = self.client
            chat = data
            self.chat: Chat = Chat(**chat)
        else:
            self.chat: Chat = None

        self.forward_from: Optional["User"] = forward_from
        self.forward_from_chat: Optional["Chat"] = forward_from_chat
        self.forward_from_message_id: Optional[int] = forward_from_message_id
        self.forward_date: Optional[int] = forward_date
        self.edite_date: Optional[int] = edite_date
        self.text: Optional[str] = text
        self.animation: Optional["Animation"] = animation
        self.audio: Optional["Audio"] = audio
        self.document: Optional["Document"] = document
        self.photo: Optional[list["PhotoSize"]] = photo
        self.sticker: Optional["Sticker"] = sticker
        self.video: Optional["Video"] = video
        self.voice: Optional["Voice"] = voice
        self.caption: Optional[str] = caption
        self.contact: Optional["Contact"] = contact
        self.location: Optional["Location"] = location
        self.new_chat_members: Optional[list["User"]] = new_chat_members
        self.left_chat_member: Optional["User"] = left_chat_member
        self.invoice: Optional["Invoice"] = invoice
        self.successful_payment: Optional["SuccessfulPayment"] = successful_payment
        self.web_app_data: Optional["WebAppData"] = web_app_data
        self.reply_markup: Optional["InlineKeyboardMarkup"] = reply_markup
        self.reply_to_message

    @property
    async def is_admin(self):
        """Check if the message sender is an admin in the chat.

        Returns:
            bool: True if user is admin or creator, False otherwise
        """
        if self.client.get_chat_member(self.chat, self.user.id).status in ['administrator', 'creator']:
            return True
        else:
            return False

    async def reply(
            self,
            text: str,
            reply_markup: Union["ReplyKeyboardMarkup", "InlineKeyboardMarkup"] = None,
    ) -> 'Message':
        """Reply to the current message with text.

        Args:
            text: The text to send
            reply_markup: Optional keyboard markup for the message

        Returns:
            Message: The sent message object
        """
        if self.chat and self.chat.id:
            message = await self.client.send_message(
                self.chat.id,
                text,
                reply_to_message_id=self.id,
                reply_markup=reply_markup,
            )
            return message

    async def edit(
            self,
            text: str,
            reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> 'Message':
        """Edit the current message text.

        Args:
            text: The new text
            reply_markup: Optional new keyboard markup

        Returns:
            Message: The edited message object
        """
        if self.chat and self.chat.id and self.id:
            message = await self.client.edit_message(
                self.chat.id, self.id, text, reply_markup=reply_markup
            )
            return message

    async def delete(self) -> bool:
        """Delete the current message.

        Returns:
            bool: True if successful
        """
        if self.chat and self.chat.id and self.id:
            return await self.client.delete_message(self.chat.id, self.id)

    async def forward(self, chat_id: int) -> 'Message':
        """Forward the current message to another chat.

        Args:
            chat_id: Destination chat ID

        Returns:
            Message: The forwarded message object
        """
        if self.chat and self.chat.id and self.id:
            message = await self.client.forward(self.chat.id, chat_id, self.id)
            return message

    async def reply_photo(
            self,
            photo: str,
            caption: Optional[str] = None,
            reply_markup: Union["ReplyKeyboardMarkup", "InlineKeyboardMarkup"] = None,
    ) -> 'Message':
        """Reply with a photo to the current message.

        Args:
            photo: Photo to send (file_id or URL)
            caption: Optional caption for the photo
            reply_markup: Optional keyboard markup

        Returns:
            Message: The sent photo message object
        """
        if self.chat and self.chat.id:
            message = await self.client.send_photo(
                self.chat.id,
                photo=photo,
                caption=caption,
                reply_to_message_id=self.id,
                reply_markup=reply_markup,
            )
            return message

    async def reply_video(
            self,
            video: str,
            caption: Optional[str] = None,
            reply_markup: Union["ReplyKeyboardMarkup", "InlineKeyboardMarkup"] = None,
    ) -> 'Message':
        """Reply with a video to the current message.

        Args:
            video: Video to send (file_id or URL)
            caption: Optional caption for the video
            reply_markup: Optional keyboard markup

        Returns:
            Message: The sent video message object
        """
        if self.chat and self.chat.id:
            message = await self.client.send_video(
                self.chat.id,
                video=video,
                caption=caption,
                reply_to_message_id=self.id,
                reply_markup=reply_markup,
            )
            return message

    async def reply_audio(
            self,
            audio: str,
            caption: Optional[str] = None,
            reply_markup: Union["ReplyKeyboardMarkup", "InlineKeyboardMarkup"] = None,
    ) -> 'Message':
        """Reply with an audio file to the current message.

        Args:
            audio: Audio to send (file_id or URL)
            caption: Optional caption for the audio
            reply_markup: Optional keyboard markup

        Returns:
            Message: The sent audio message object
        """
        if self.chat and self.chat.id:
            message = await self.client.send_audio(
                self.chat.id,
                audio=audio,
                caption=caption,
                reply_to_message_id=self.id,
                reply_markup=reply_markup,
            )
            return message

    async def reply_document(
            self,
            document: str,
            caption: Optional[str] = None,
            reply_markup: Union["ReplyKeyboardMarkup", "InlineKeyboardMarkup"] = None,
    ) -> 'Message':
        """Reply with a document to the current message.

        Args:
            document: Document to send (file_id or URL)
            caption: Optional caption for the document
            reply_markup: Optional keyboard markup

        Returns:
            Message: The sent document message object
        """
        if self.chat and self.chat.id:
            message = await self.client.send_document(
                self.chat.id,
                document=document,
                caption=caption,
                reply_to_message_id=self.id,
                reply_markup=reply_markup,
            )
            return message

    async def reply_sticker(
            self,
            sticker: str,
            reply_markup: Union["ReplyKeyboardMarkup", "InlineKeyboardMarkup"] = None,
    ) -> 'Message':
        """Reply with a sticker to the current message.

        Args:
            sticker: Sticker to send (file_id or URL)
            reply_markup: Optional keyboard markup

        Returns:
            Message: The sent sticker message object
        """
        if self.chat and self.chat.id:
            message = await self.client.send_sticker(
                self.chat.id,
                sticker=sticker,
                reply_to_message_id=self.id,
                reply_markup=reply_markup
            )
            return message

    async def reply_location(
            self,
            latitude: float,
            longitude: float,
            horizontal_accuracy: Optional[float] = None,
            reply_markup: Union["ReplyKeyboardMarkup", "InlineKeyboardMarkup"] = None,
    ) -> 'Message':
        """Reply with a location to the current message.

        Args:
            latitude: Latitude of the location
            longitude: Longitude of the location
            horizontal_accuracy: The radius of uncertainty for the location
            reply_markup: Optional keyboard markup

        Returns:
            Message: The sent location message object
        """
        if self.chat and self.chat.id:
            message = await self.client.send_location(
                self.chat.id,
                latitude=latitude,
                longitude=longitude,
                horizontal_accuracy=horizontal_accuracy,
                reply_to_message_id=self.id,
                reply_markup=reply_markup,
            )
            return message

    async def reply_contact(
            self,
            phone_number: str,
            first_name: str,
            reply_markup: Union["ReplyKeyboardMarkup", "InlineKeyboardMarkup"] = None,
    ) -> 'Message':
        """Reply with a contact to the current message.

        Args:
            phone_number: Contact's phone number
            first_name: Contact's first name
            reply_markup: Optional keyboard markup

        Returns:
            Message: The sent contact message object
        """
        if self.chat and self.chat.id:
            message = await self.client.send_contact(
                self.chat.id,
                phone_number=phone_number,
                first_name=first_name,
                reply_to_message_id=self.id,
                reply_markup=reply_markup,
            )
            return message

    async def reply_invoice(
            self,
            title: str,
            description: str,
            payload: str,
            provider_token: str,
            prices: list,
            reply_markup: Union["ReplyKeyboardMarkup", "InlineKeyboardMarkup"] = None,
    ) -> 'Message':
        """Reply with an invoice to the current message.

        Args:
            title: Product name
            description: Product description
            payload: Bot-defined invoice payload
            provider_token: Payment provider token
            prices: Price breakdown (amount in smallest units)
            reply_markup: Optional keyboard markup

        Returns:
            Message: The sent invoice message object
        """
        if self.chat and self.chat.id:
            message = await self.client.send_invoice(
                self.chat.id,
                title=title,
                description=description,
                payload=payload,
                provider_token=provider_token,
                prices=prices,
                reply_to_message_id=self.id,
                reply_markup=reply_markup
            )
            return message
