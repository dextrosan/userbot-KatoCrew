

"""
✘ Commands Available -

• `{i}addfilter <word><reply to a message>`
    agregue la palabra usada como filtro relacionado con el mensaje respondido.

• `{i}remfilter <word>`
    Eliminar el usuario filtrado..

• `{i}listfilter`
    enumerar todos los filtros.
"""

import os

from pyUltroid.functions.filter_db import *
from telegraph import upload_file as uf
from telethon.utils import pack_bot_file_id

from . import *


@ultroid_cmd(pattern="addfilter ?(.*)")
async def af(e):
    wrd = (e.pattern_match.group(1)).lower()
    wt = await e.get_reply_message()
    chat = e.chat_id
    if not (wt and wrd):
        return await eor(e, "`Utilice esta palabra de comando para establecer como filtro y responder...`")
    if wt and wt.media:
        wut = mediainfo(wt.media)
        if wut.startswith(("pic", "gif")):
            dl = await bot.download_media(wt.media)
            variable = uf(dl)
            m = "https://telegra.ph" + variable[0]
        elif wut == "video":
            if wt.media.document.size > 8 * 1000 * 1000:
                return await eod(x, "`Unsupported Media`")
            else:
                dl = await bot.download_media(wt.media)
                variable = uf(dl)
                os.remove(dl)
                m = "https://telegra.ph" + variable[0]
        else:
            m = pack_bot_file_id(wt.media)
        if wt.text:
            add_filter(int(chat), wrd, wt.text, m)
        else:
            add_filter(int(chat), wrd, None, m)
    else:
        add_filter(int(chat), wrd, wt.text, None)
    await eor(e, f"Done : Filter `{wrd}` Saved.")


@ultroid_cmd(pattern="remfilter ?(.*)")
async def rf(e):
    wrd = (e.pattern_match.group(1)).lower()
    chat = e.chat_id
    if not wrd:
        return await eor(e, "`Give the filter to remove..`")
    rem_filter(int(chat), wrd)
    await eor(e, f"Done : Filter `{wrd}` Removed.")


@ultroid_cmd(pattern="listfilter$")
async def lsnote(e):
    x = list_filter(e.chat_id)
    if x:
        sd = "Filters Found In This Chats Are\n\n"
        await eor(e, sd + x)
    else:
        await eor(e, "No Filters Found Here")


@ultroid_bot.on(events.NewMessage())
async def fl(e):
    xx = (e.text).lower()
    chat = e.chat_id
    x = get_filter(int(chat))
    if x:
        if " " in xx:
            xx = xx.split(" ")
            kk = ""
            for c in xx:
                if c in x:
                    k = get_reply(int(chat), c)
                    if k:
                        kk = k
            if kk:
                msg = k["msg"]
                media = k["media"]
                await e.reply(msg, file=media)

        else:
            k = get_reply(chat, xx)
            if k:
                msg = k["msg"]
                media = k["media"]
                await e.reply(msg, file=media)


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
