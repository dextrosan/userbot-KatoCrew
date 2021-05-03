

"""
✘ Commands Available -

• `{i}blacklist <word/all words with a space>`
    poner en lista negra la palabra elegida en ese chat.

• `{i}remblacklist <word>`
    Eliminar la palabra de la lista negra..

• `{i}listblacklist`
    enumerar todas las palabras de la lista negra.

  'si una persona usa Word de lista negra, su mensaje será eliminado'
  'Y debes ser administrador en ese chat'
"""

import re

from pyUltroid.functions.blacklist_db import *
from telethon.tl.types import ChannelParticipantsAdmins

from . import *


@ultroid_cmd(pattern="blacklist ?(.*)")
async def af(e):
    if e.is_group:
        if not e._chat.admin_rights:
            return await eod(e, "`No eres administrador aquí`")
    wrd = (e.pattern_match.group(1)).lower()
    chat = e.chat_id
    if not (wrd):
        return await eod(e, "`Dar la palabra a la lista negra..`")
    wrd = e.text[10:]
    add_blacklist(int(chat), wrd)
    await eor(e, f"Done : `{wrd}` Incluido aquí.")


@ultroid_cmd(pattern="remblacklist ?(.*)")
async def rf(e):
    if e.is_group:
        if not e._chat.admin_rights:
            return await eod(e, "`No eres administrador aquí`")
    wrd = (e.pattern_match.group(1)).lower()
    chat = e.chat_id
    if not wrd:
        return await eod(e, "`Dar la palabra para eliminar de la lista negra..`")
    rem_blacklist(int(chat), wrd)
    await eor(e, f"Done : `{wrd}` Eliminado de la lista negra.")


@ultroid_cmd(pattern="listblacklist")
async def lsnote(e):
    if e.is_group:
        if not e._chat.admin_rights:
            return await eod(e, "`No eres administrador aquí`")
    x = list_blacklist(e.chat_id)
    if x:
        sd = "Lista negra encontrada en estos chats son\n\n"
        await eor(e, sd + x)
    else:
        await eor(e, "No se ha encontrado ninguna palabra de la lista negra aquí")


@ultroid_bot.on(events.NewMessage(incoming=True))
async def bl(e):
    chat = e.chat_id
    x = get_blacklist(int(chat))
    xx = (e.text).lower()
    if x and xx:
        if " " in xx:
            xx = xx.split(" ")
            kk = ""
            for c in xx:
                kk = re.search(str(c), str(x), flags=re.IGNORECASE)
            if kk:
                async for l in ultroid_bot.iter_participants(
                    e.chat_id, filter=ChannelParticipantsAdmins
                ):
                    if l.id == e.sender_id:
                        return
                await e.delete()
        else:
            k = re.search(xx, x, flags=re.IGNORECASE)
            if k:
                async for l in ultroid_bot.iter_participants(
                    e.chat_id, filter=ChannelParticipantsAdmins
                ):
                    if l.id == e.sender_id:
                        return
                await e.delete()


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
