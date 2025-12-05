from ... import pyrobale
import json
import time
import datetime
import jdatetime
import importlib.util
import asyncio


class PyroJsonBale:
    def __init__(self, file_name_or_content):
        if isinstance(file_name_or_content, str):
            with open(file_name_or_content, encoding="utf-8") as f:
                self.json = json.load(f)
        else:
            self.json = file_name_or_content

        self.bot = pyrobale.Client(self.json.get("TOKEN"))
        self.custom_functions = {}
        self._load_custom_functions()
        self._setup_handlers()

    def _load_custom_functions(self):
        if "custom_functions" in self.json:
            for func_path in self.json["custom_functions"]:
                try:
                    spec = importlib.util.spec_from_file_location(
                        "custom_module", func_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if callable(attr) and not attr_name.startswith("_"):
                            self.custom_functions[attr_name] = attr
                except Exception as e:
                    print(f"Error loading {func_path}: {e}")

    def _format_text(self, obj, text):
        if isinstance(obj, pyrobale.Message):
            user = obj.user
            chat = obj.chat
            message_text = obj.text or ""
            message_id = obj.id
        else:
            user = obj.user
            chat = obj.message.chat if obj.message else None
            message_text = obj.data or ""
            message_id = obj.message.id if obj.message else ""

        replacements = {
            "$TEXT": message_text,
            "$UID": str(user.id),
            "$CHATID": str(chat.id) if chat else "",
            "$FIRSTNAME": str(user.first_name or ""),
            "$LASTNAME": str(user.last_name or ""),
            "$FULLNAME": f"{user.first_name or ''} {user.last_name or ''}".strip(),
            "$USERNAME": f"@{user.username}" if user.username else "",
            "$MENTION": f"@{user.username}" if user.username else user.first_name,
            "$EPOCH": str(time.time()),
            "$TIME": time.strftime("%H:%M:%S"),
            "$DATE": datetime.datetime.now().strftime("%Y/%m/%d"),
            "$JDATE": jdatetime.datetime.now().strftime("%Y/%m/%d"),
            "$MESSAGEID": str(message_id),
            "$DATA": message_text if isinstance(obj, pyrobale.CallbackQuery) else ""
        }

        for key, value in replacements.items():
            text = text.replace(key, value)

        return text

    def _check_filters(self, obj, filters):
        for fltr in filters:
            if fltr in ["pv", "private"]:
                chat = obj.chat if isinstance(
                    obj, pyrobale.Message) else (
                    obj.message.chat if obj.message else None)
                if not chat or chat.type != "private":
                    return False
            elif fltr in ["gp", "group"]:
                chat = obj.chat if isinstance(
                    obj, pyrobale.Message) else (
                    obj.message.chat if obj.message else None)
                if not chat or chat.type != "group":
                    return False
            elif fltr in ["ch", "channel"]:
                chat = obj.chat if isinstance(
                    obj, pyrobale.Message) else (
                    obj.message.chat if obj.message else None)
                if not chat or chat.type != "channel":
                    return False
            elif fltr == "text":
                if not getattr(obj, 'text', None):
                    return False
            elif fltr.startswith("text:"):
                if not getattr(obj, 'text', None) or obj.text != fltr[5:]:
                    return False
            elif fltr.startswith("text_contains:"):
                if not getattr(obj, 'text', None) or fltr[14:] not in obj.text:
                    return False
            elif fltr.startswith("text_startswith:"):
                if not getattr(obj, 'text', None) or not obj.text.startswith(
                        fltr[16:]):
                    return False
            elif fltr == "data":
                if not getattr(obj, 'data', None):
                    return False
            elif fltr.startswith("data:"):
                if not getattr(obj, 'data', None) or obj.data != fltr[5:]:
                    return False
            elif fltr == "digit":
                text = getattr(obj, 'text', None) or getattr(obj, 'data', None)
                if not text or not text.isdigit():
                    return False
            elif fltr.startswith("user_id:"):
                if obj.user.id != int(fltr[8:]):
                    return False
            elif fltr.startswith("username:"):
                if not obj.user.username or obj.user.username.lower(
                ) != fltr[9:].lower():
                    return False
            elif fltr == "admin":
                if obj.user.id not in self.json.get("admins", []):
                    return False

        return True

    def _create_keyboard(self, hand):
        if hand.get('keyboard'):
            mkb = pyrobale.ReplyKeyboardMarkup()
            mkb.keyboard = hand.get('keyboard')
            return mkb

        if hand.get('inline_keyboard'):
            mkb = pyrobale.InlineKeyboardMarkup()
            mkb.inline_keyboard = hand.get('inline_keyboard')
            return mkb

    async def _do_action(self, obj, act, keyboard):
        action_type = act.get("type")

        try:
            chat_id = None
            if isinstance(obj, pyrobale.Message):
                chat_id = obj.chat.id
            elif isinstance(obj, pyrobale.CallbackQuery) and obj.message:
                chat_id = obj.message.chat.id

            if action_type == "reply":
                if isinstance(obj, pyrobale.Message):
                    await obj.reply(self._format_text(obj, act.get("text", "")), reply_markup=keyboard)

            elif action_type == "send":
                if chat_id:
                    await self.bot.send_message(chat_id, self._format_text(obj, act.get("text", "")), reply_markup=keyboard)

            elif action_type == "edit":
                if hasattr(obj, 'edit_text'):
                    await obj.edit_text(self._format_text(obj, act.get("text", "")), reply_markup=keyboard)

            elif action_type == "answer":
                if isinstance(obj, pyrobale.CallbackQuery):
                    await obj.answer(act.get("text", ""), show_alert=act.get("alert", False))

            elif action_type == "delete":
                if hasattr(obj, 'delete'):
                    await obj.delete()

            elif action_type == "forward":
                if isinstance(obj, pyrobale.Message):
                    await obj.forward(act.get("chat_id"))

            elif action_type == "copy":
                if isinstance(obj, pyrobale.Message):
                    await obj.copy(act.get("chat_id"))

            elif action_type == "custom_function":
                func_name = act.get("function")
                if func_name in self.custom_functions:
                    try:
                        result = await self.custom_functions[func_name](obj, self.bot, act.get("params", {}))
                        if act.get("send_result") and result and chat_id:
                            await self.bot.send_message(chat_id, str(result))
                    except Exception as e:
                        print(f"Error in {func_name}: {e}")

            elif action_type == "sleep":
                await asyncio.sleep(act.get("seconds", 1))

        except Exception as e:
            print(f"Error in {action_type}: {e}")

    def _setup_handlers(self):
        for hand in self.json.get('handlers', []):
            if hand.get("type") == "message":
                async def message_handler(message, hand=hand):
                    if not self._check_filters(
                            message, hand.get("filters", [])):
                        return
                    keyboard = self._create_keyboard(hand)
                    for act in hand.get('actions', []):
                        await self._do_action(message, act, keyboard)

                self.bot.on_message()(message_handler)

            elif hand.get("type") == "callback":
                async def callback_handler(callback, hand=hand):
                    if not self._check_filters(
                            callback, hand.get("filters", [])):
                        return
                    keyboard = self._create_keyboard(hand)
                    for act in hand.get('actions', []):
                        await self._do_action(callback, act, keyboard)

                self.bot.on_callback_query()(callback_handler)

    def run(self):
        self.bot.run()

