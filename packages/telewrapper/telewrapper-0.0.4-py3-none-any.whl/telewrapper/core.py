from telethon import TelegramClient, Button
from telethon.events.callbackquery import CallbackQuery
from telethon.events.newmessage import NewMessage
from telethon.events import StopPropagation
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
import asyncio
import time
import threading
import abc


class TeleMsgTemplate(abc.ABC):
    commands = {}


class TeleBaseCmd(TeleMsgTemplate):
    command = None

    @abc.abstractmethod
    async def execute(self, event: NewMessage.Event, **kwargs):
        pass


class TeleBaseMsg(TeleMsgTemplate):
    pattern = None

    @abc.abstractmethod
    async def execute(self, event: NewMessage.Event, _cmd: str, **kwargs):
        pass


class TeleBaseBtn(abc.ABC):
    label = None
    data = None
    tree = []
    parent = None

    @abc.abstractmethod
    async def callback(self, event: CallbackQuery.Event, **kwargs):
        pass


class TeleUrlBtn(object):
    label = None
    url = None


class BackBtn(TeleBaseBtn):
    label = "Back"

    async def callback(self, event: CallbackQuery.Event, **kwargs):
        msg = await event.get_message()
        await event.edit(msg.text, buttons=self.parent.parent.tree)


class TeleBtn(TeleBaseBtn):
    _telewrapper = None

    def add_tree(self, tree: list, back=True):
        if back:
            backbtn = BackBtn()
            backbtn.data = "{}_back".format(self.__class__.__name__).encode()
            tree.append([backbtn])
        for btns in tree:
            for btn in btns:
                btn.parent = self
        self.tree = tuple(self._telewrapper.new_btns_event(tree))
        return self

    async def callback(self, event: CallbackQuery.Event, **kwargs):
        pass


class Telewrapper(object):
    terminate = False
    terminated = False
    interaction = {}

    def __init__(
            self,
            session_name: str,
            api_id: int, api_hash: str, phone: str,
            chat_id: int = None, channel_id: int = None,
            bot_tk: str = None,
            commands: dict = None,
            passthrough: dict = None
    ):
        self.me = None
        self.session_name = session_name
        self.api_id = api_id
        self.api_hash = api_hash
        self.bot_tk = bot_tk
        self.phone = phone
        self.chat_id = None
        self.channel_id = None
        self.client = None
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        if chat_id:
            self.chat_id = PeerChannel(chat_id)
        if channel_id:
            self.channel_id = PeerChannel(channel_id)
        self.client = self.get_telegram_client()
        TeleBtn._telewrapper = self
        TeleMsgTemplate.commands = commands
        self.passthrough = passthrough

    def get_telegram_client(self):
        _ = TelegramClient(self.session_name, self.api_id, self.api_hash, loop=self.loop)
        if self.session_name.endswith("bot"):
            return _.start(bot_token=self.bot_tk)
        else:
            _.start(phone=self.phone)
            return _

    def stop_loop(self):
        self.terminate = True
        while not self.terminated:
            time.sleep(1/10)

    async def job(self):
        self.me = await self.client.get_me()
        print(self.me)
        while not self.terminate:
            await asyncio.sleep(1/1000, loop=self.loop)
        self.terminated = True

    def disconnect(self):
        self.client.disconnect()

    def _start(self):
        asyncio.set_event_loop(self.loop)
        self.client.loop.run_until_complete(self.job())

    def start_loop(self):
        p = threading.Thread(target=self._start)
        p.daemon = True
        p.start()

    def on(self, *args, **kwargs):
        def wrapper(function):
            return self.client.on(*args, **kwargs)(function)

        return wrapper

    @staticmethod
    def msg_cb(*args, **kwargs):
        return NewMessage(*args, **kwargs)

    def new_cmd_event(self, cmd: TeleBaseCmd):
        async def handler(event):
            self.interaction[event.peer_id.user_id] = cmd.command
            return await cmd.execute(event, **self.passthrough)

        self.on(self.msg_cb(pattern=cmd.command))(handler)

    def new_msg_event(self, msg: TeleBaseMsg):
        async def handler(event):
            try:
                _cmd = self.interaction[event.peer_id.user_id]
            except KeyError:
                _cmd = None
            self.interaction[event.peer_id.user_id] = None
            return await msg.execute(event, _cmd, **self.passthrough)

        self.on(self.msg_cb(pattern=msg.pattern))(handler)

    @staticmethod
    def btn_cb(*args, **kwargs):
        return CallbackQuery(*args, **kwargs)

    def new_btn(self, btn):
        if hasattr(btn, "label") and hasattr(btn, "url"):
            return Button.url(btn.label, btn.url)
        if btn.data and btn.callback:
            def handler(event: CallbackQuery.Event):
                self.interaction[event.sender_id] = btn.data.decode()
                return btn.callback(event, **self.passthrough)

            self.on(self.btn_cb(data=btn.data))(handler)
        return Button.inline(btn.label, data=btn.data)

    def new_btns_event(self, btns: list):
        return [[self.new_btn(btn) for btn in _btns] for _btns in btns]


class TeleCmd_start(TeleBaseCmd):
    command = "/start"

    def get_welcome_msg(self, event: NewMessage.Event):
        return "Hi, {}! How can I help you?".format(event.sender.username)

    async def respond(self, event: NewMessage.Event, msg):
        if msg:
            await event.respond(msg)
            await event.respond(
                "I hope that is your answer!\n\nHow can I help you?"
            )
        else:
            await event.respond(
                self.get_welcome_msg(event)
            )

    def get_args(self, event: NewMessage.Event):
        return event.message.text.replace(self.command, "")[1:].split("_")

    async def execute(self, event: NewMessage.Event, **kwargs):
        args = self.get_args(event)
        msg = None
        if len(args):
            _cmd = args[0]
            if _cmd in self.commands:
                msg = await self.commands[_cmd](event, msg=args[1], **kwargs)
        await self.respond(event, msg)
        raise StopPropagation


class TeleMsg_Echo(TeleBaseMsg):
    pattern = None
    unknown_command_msg = "Unknown command!\nPress /start to restart."
    next_command_msg = "I hope that is your answer!\n\nHow can I help you?"

    async def respond(self, event: NewMessage.Event, msg, **kwargs):
        await event.respond(msg)
        await event.respond(self.next_command_msg)

    async def respond_unknown(self, event: NewMessage.Event, **kwargs):
        await event.respond(self.unknown_command_msg)

    async def execute(self, event: NewMessage.Event, _cmd: str, **kwargs):
        if _cmd is None:
            return await event.respond(self.unknown_command_msg)
        if _cmd in self.commands:
            if self.commands[_cmd]:
                msg = await self.commands[_cmd](event, msg=event.message.text, **kwargs)
            else:
                return
            if msg:
                await self.respond(event, msg, **kwargs)
        else:
            await self.respond_unknown(event, **kwargs)


