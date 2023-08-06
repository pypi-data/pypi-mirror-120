import telewrapper
import re
import json
import sqlq
import datetime
from base64 import b64encode
import requests


numbering = "⒈⒉⒊⒋⒌⒍⒎⒏⒐⒑⒒⒓⒔⒕⒖⒗⒘⒙⒚⒛"


class AccountBtn(telewrapper.TeleBtn):
    label = "Account"
    data = b"account"

    async def callback(self, event: telewrapper.CallbackQuery.Event, **kwargs):
        msg = await event.get_message()
        await event.edit(msg.text, buttons=self.tree)


class AccountBtn_order(telewrapper.TeleBtn):
    label = "Order"
    data = b"/order"

    async def callback(self, event: telewrapper.CallbackQuery.Event, **kwargs):
        ori_msg = await event.get_message()
        await ori_msg.edit("Please wait")
        sql = kwargs["sql"]
        result = sql(
            '''
            SELECT *
            FROM `order`
            JOIN `customer`
            ON `order`.`username` = `customer`.`username`
            WHERE `customer`.`telegram` = ?;
            ''',
            (event.sender_id,),
            "list"
        )

        response = self.label+"\n\n"+json.dump(result)
        await ori_msg.edit(response, buttons=self.parent.tree)


class AccountBtn_wishlist(telewrapper.TeleBtn):
    label = "Wishlist"
    data = b"/wishlist"

    async def callback(self, event: telewrapper.CallbackQuery.Event, **kwargs):
        ori_msg = await event.get_message()
        await ori_msg.edit("Please wait")
        sql = kwargs["sql"]
        result = sql(
            '''
            SELECT *
            FROM `wishlist`
            JOIN `customer`
            ON `wishlist`.`username` = `customer`.`username`
            WHERE `customer`.`telegram` = ?;
            ''',
            (event.sender_id,),
            "list"
        )

        response = self.label+"\n\n"+json.dumps(result)
        await ori_msg.edit(response, buttons=self.parent.tree)


class ItemBtn(telewrapper.TeleBtn):
    label = "Item"
    data = b"item"

    async def callback(self, event: telewrapper.CallbackQuery.Event, **kwargs):
        msg = await event.get_message()
        await event.edit(msg.text, buttons=self.tree)


class ItemBtn_search(telewrapper.TeleUrlBtn):
    label = "Search"
    url = "https://foxe6.github.io/shop/search"


class ItemBtn_info(telewrapper.TeleBtn):
    label = "Info"
    data = b"/item"

    async def callback(self, event: telewrapper.CallbackQuery.Event, **kwargs):
        await event.respond("Enter item link or ID:")

    @staticmethod
    async def execute(event: telewrapper.NewMessage.Event, **kwargs):
        try:
            msg = kwargs["msg"]
            msg = re.search(r"[0-9]{6,}", msg)[0]
            sql = kwargs["sql"]
            session = kwargs["session"]
            item_info = msg
            return item_info
        except Exception as e:
            print(e)
            return "Sorry! I found nothing about:\n{}".format(msg)


# to trigger this function: visit https://t.me/<your bot name>?start=member_<head of passhash>
class member(telewrapper.TeleBtn):
    label = "member"
    data = b"/member"

    @staticmethod
    async def execute(event: telewrapper.NewMessage.Event, **kwargs):
        user_id = event.peer_id.user_id
        sql = kwargs["sql"]
        msg = kwargs["msg"]
        result = sql(
            '''
            SELECT `username`, `telegram`
            FROM `customer`
            WHERE `passhash` LIKE ?;
            ''',
            ("{}%".format(msg),),
            "list"
        )[0]
        if result[1] == 0:
            sql(
                '''UPDATE `customer` SET `telegram` = ? WHERE `username` = ?;''',
                (user_id, result[0])
            )
            return "You have subscribed!"
        else:
            sql(
                '''UPDATE `customer` SET `telegram` = 0 WHERE `username` = ?;''',
                (result[0],)
            )
            return "You have unsubscribed!"


class CartBtn(telewrapper.TeleBtn):
    label = "Cart"
    data = b"/cart"

    async def callback(self, event: telewrapper.CallbackQuery.Event, **kwargs):
        ori_msg = await event.get_message()
        await ori_msg.edit("Please wait")
        sql = kwargs["sql"]
        result = sql(
            '''
            SELECT *
            FROM `cart`
            JOIN `customer`
            ON `cart`.`username` = `customer`.`username`
            WHERE `customer`.`telegram` = ?;
            ''',
            (event.sender_id,),
            "list"
        )
        response = self.label+"\n\n"+json.dumps(result)
        await ori_msg.edit(response, buttons=self.parent.tree)


class NewsBtn(telewrapper.TeleUrlBtn):
    label = "News"
    url = "https://t.me/foxe6_shop"


class ShopBtn(telewrapper.TeleUrlBtn):
    label = "Shop"
    url = "https://foxe6.github.io/shop"


class DonateBtn(telewrapper.TeleUrlBtn):
    label = "Donate"
    url = "https://foxe6.github.io/donation"


class CsBtn(telewrapper.TeleUrlBtn):
    label = "Customer Services"
    url = "https://t.me/foxe6_owner"


class CommonTemplate(object):
    WELCOME_BTNS = None

    @staticmethod
    def get_welcome_msg(event):
        msg = "\n".join([
            '''**Hello, **@{username}**!**
I am a helper (a bot).
How can I help you?'''
        ])
        matches = re.findall(r"\{[a-z]+\}(?!\})", msg)
        for key in matches:
            if hasattr(event.sender, key[1:-1]):
                msg = msg.replace(key, getattr(event.sender, key[1:-1]))
        msg = msg.replace("{{", "{").replace("}}", "}")
        return msg


class Cmd_start(telewrapper.TeleCmd_start, CommonTemplate):
    def get_args(self, event: telewrapper.NewMessage.Event):
        args = super().get_args(event)
        if len(args):
            if args[0]:
                args[0] = "/"+args[0]
        return args

    async def respond(self, event: telewrapper.NewMessage.Event, msg):
        if msg:
            please_wait = await event.respond("Please wait")
            if isinstance(msg, str):
                await event.respond(msg)
            elif isinstance(msg, tuple):
                if len(msg) == 2:
                    if isinstance(msg[0], tuple) and isinstance(msg[1], dict):
                        await event.respond(*msg[0], **msg[1])
            await please_wait.delete()
            await event.respond(
                "I hope that is your answer! How can I help you?",
                buttons=self.WELCOME_BTNS
            )
        else:
            await event.respond(
                self.get_welcome_msg(event),
                buttons=self.WELCOME_BTNS
            )


class Cmd_help(telewrapper.TeleBaseCmd, CommonTemplate):
    command = "/help"

    async def execute(self, event: telewrapper.NewMessage.Event, **kwargs):
        await event.respond(
            self.get_welcome_msg(event),
            buttons=self.WELCOME_BTNS
        )


class Msg_echo(telewrapper.TeleMsg_Echo, CommonTemplate):
    pattern = None

    async def respond(self, event: telewrapper.NewMessage.Event, msg, **kwargs):
        if isinstance(msg, str):
            await event.respond(msg)
        elif isinstance(msg, tuple):
            if len(msg) == 2:
                if isinstance(msg[0], tuple) and isinstance(msg[1], dict):
                    await event.respond(*msg[0], **msg[1])
        await event.respond(
            self.next_command_msg,
            buttons=self.WELCOME_BTNS
        )

    async def respond_unknown(self, event: telewrapper.NewMessage.Event, **kwargs):
        await event.respond(self.unknown_command_msg+"\nDo you require online customer services?", buttons=telewrapper.TeleBtn().add_tree(
            [
                [
                    CsBtn(),
                ]
            ],
            back=False
        ).tree)


def gen_commands(_locals):
    commands = {}
    _locals_k = list(_locals.keys())
    for _k in _locals_k:
        try:
            if hasattr(_locals[_k], "__class__"):
                k = None
                v = None
                if issubclass(_locals[_k], telewrapper.TeleBtn):
                    if hasattr(_locals[_k], "execute"):
                        k = getattr(_locals[_k], "data").decode()
                        v = getattr(_locals[_k], "execute")
                elif issubclass(_locals[_k], telewrapper.TeleBaseCmd):
                    if hasattr(_locals[_k], "execute"):
                        k = getattr(_locals[_k], "command")
                        v = ""
                commands[k] = v
        except:
            pass
    print(commands)
    return commands


if __name__ == "__main__":
    def sqlqueue(*args, **kwargs):
        return sqlq.SqlQueueU(db_port=39292+0).sql(*args, **kwargs)

    session = requests.Session()
    telebot = telewrapper.Telewrapper(
        session_name="session_name",
        # https://my.telegram.org
        api_id=...,
        api_hash="...",
        # https://t.me/botfather
        bot_tk="...",
        chat_id=...,
        channel_id=...,
        phone="+...",
        commands=gen_commands(locals()),
        passthrough=dict(
            sql=sqlqueue,
            session=session
        )
    )
    import asyncio
    asyncio.set_event_loop(telebot.loop)
    async def test():
        my_account_id = ...
        return await telebot.client.send_message(my_account_id, "bot started")
    telebot.client.loop.create_task(test())
    CommonTemplate.WELCOME_BTNS = telewrapper.TeleBtn().add_tree([
        [
            AccountBtn().add_tree([
                [
                    AccountBtn_order(),
                    AccountBtn_wishlist(),
                ],
            ]),
            ItemBtn().add_tree([
                [
                    ItemBtn_search(),
                    ItemBtn_info(),
                ],
            ])
        ],
        [
            CartBtn(),
            NewsBtn(),
        ],
        [
            DonateBtn(),
            ShopBtn(),
        ],
        [
            CsBtn(),
        ],
    ], back=False).tree


    telebot.new_cmd_event(Cmd_start())
    telebot.new_cmd_event(Cmd_help())
    telebot.new_msg_event(Msg_echo())


    telebot.start_loop()
    input("stop?")
    telebot.stop_loop()
