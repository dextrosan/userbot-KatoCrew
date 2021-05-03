

import re

from telethon import Button
from telethon.errors.rpcerrorlist import BotInlineDisabledError as dis
from telethon.errors.rpcerrorlist import BotResponseTimeoutError as rep
from telethon.errors.rpcerrorlist import MessageNotModifiedError as np
from telethon.tl.functions.users import GetFullUserRequest as gu
from telethon.tl.types import UserStatusEmpty as mt
from telethon.tl.types import UserStatusLastMonth as lm
from telethon.tl.types import UserStatusLastWeek as lw
from telethon.tl.types import UserStatusOffline as off
from telethon.tl.types import UserStatusOnline as on
from telethon.tl.types import UserStatusRecently as rec

from . import *

snap = {}
buddhhu = []


@ultroid_cmd(
    pattern="wspr ?(.*)",
)
async def _(e):
    if e.reply_to_msg_id:
        okk = (await e.get_reply_message()).sender_id
        try:
            zyx = await ultroid_bot(gu(id=okk))
            put = zyx.user.username
        except ValueError as ex:
            return await eor(e, str(ex))
        except AttributeError:
            return await eor(e, "No se encontró el nombre de usuario del usuario que respondió.")
    else:
        put = e.pattern_match.group(1)
    if put:
        try:
            results = await ultroid_bot.inline_query(Var.BOT_USERNAME, f"msg {put}")
        except rep:
            return await eor(
                e,
                get_string("help_2").format(HNDLR),
            )
        except dis:
            return await eor(e, get_string("help_3"))
        await results[0].click(e.chat_id, reply_to=e.reply_to_msg_id, hide_via=True)
        await e.delete()
    else:
        await eor(e, "Agregue también alguna identificación o nombre de usuario")


@in_pattern("msg")
async def _(e):
    vvv = e.text
    zzz = vvv.split(" ", maxsplit=1)
    try:
        ggg = zzz[1]
        sed = ggg.split(" wspr ", maxsplit=1)
        query = sed[0]
    except IndexError:
        return
    meme = e.query.user_id
    try:
        desc = sed[1]
    except IndexError:
        desc = "Touch me"
    if "wspr" not in vvv:
        try:
            logi = await ultroid_bot(gu(id=query))
            name = logi.user.first_name
            ids = logi.user.id
            username = logi.user.username
            x = logi.user.status
            bio = logi.about
            if isinstance(x, on):
                status = "Online"
            if isinstance(x, off):
                status = "Desconectado"
            if isinstance(x, rec):
                status = "Visto por última vez recientemente"
            if isinstance(x, lm):
                status = "Visto por última vez hace meses"
            if isinstance(x, lw):
                status = "Visto por última vez hace semanas"
            if isinstance(x, mt):
                status = "No puedo decir"
            text = f"**Name:**    `{name}`\n"
            text += f"**Id:**    `{ids}`\n"
            text += f"**Username:**    `{username}`\n"
            text += f"**Status:**    `{status}`\n"
            text += f"**About:**    `{bio}`"
            button = [
                Button.url("Private", url=f"t.me/{username}"),
                Button.switch_inline(
                    "Secret msg",
                    query=f"msg {query} wspr ",
                    same_peer=True,
                ),
            ]
            sur = e.builder.article(
                title=f"{name}",
                description=desc,
                text=text,
                buttons=button,
            )
        except BaseException:
            name = f"User {query} No encontrado\nBuscar nuevamente"
            sur = e.builder.article(
                title=name,
                text=name,
            )
    else:
        try:
            logi = await ultroid_bot.get_entity(query)
            button = [
                Button.inline("Secret Msg", data=f"dd_{logi.id}"),
                Button.inline("Delete Msg", data=f"del"),
            ]
            us = logi.username
            sur = e.builder.article(
                title=f"{logi.first_name}",
                description=desc,
                text=get_string("wspr_1").format(us),
                buttons=button,
            )
            buddhhu.append(meme)
            buddhhu.append(logi.id)
            snap.update({logi.id: desc})
        except ValueError:
            sur = e.builder.article(
                title="Escriba su mensaje",
                text=f"No escribiste tu mensaje",
            )
    await e.answer([sur])


@callback(
    re.compile(
        "dd_(.*)",
    ),
)
async def _(e):
    ids = int(e.pattern_match.group(1).decode("UTF-8"))
    if e.sender_id in buddhhu:
        await e.answer(snap[ids], alert=True)
    else:
        await e.answer("No es para ti", alert=True)


@callback("del")
async def _(e):
    if e.sender_id in buddhhu:
        for k in buddhhu:
            try:
                del snap[k]
                buddhhu.clear()
            except KeyError:
                pass
            try:
                await e.edit(get_string("wspr_2"))
            except np:
                pass
    else:
        await e.answer("No puedes hacer esto", alert=True)
