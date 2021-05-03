# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

"""
✘ Commands Available -

• `{i}install <reply to plugin>`
    Para instalar el complemento,
   `{i}install f`
    Para forzar la instalación.

• `{i}uninstall <plugin name>`
    Para descargar y eliminar el complemento.

• `{i}load <plugin name>`
    Para cargar un complemento no oficial descargado.

• `{i}unload <plugin name>`
    Para descargar un complemento no oficial.

• `{i}help <plugin name>`
Te muestra un menú de ayuda (like this) para cada complemento.
"""

import os

from telethon import Button

from . import *


@in_pattern(
    "send ?(.*)",
)
@in_owner
async def inline_handler(event):
    builder = event.builder
    input_str = event.pattern_match.group(1)
    plug = [*PLUGINS]
    plugs = []
    if input_str is None or input_str == "":
        for i in plug:
            try:
                plugs.append(
                    await event.builder.document(
                        f"./plugins/{i}.py",
                        title=f"{i}.py",
                        description=f"Módulo encontrado",
                        text=f"{i}.py use .paste para pegar en neko y raw..",
                        buttons=[
                            [
                                Button.switch_inline(
                                    "Busca de nuevo..?",
                                    query="send ",
                                    same_peer=True,
                                ),
                            ],
                        ],
                    ),
                )
            except BaseException:
                pass
        await event.answer(plugs)
    else:
        try:
            ultroid = builder.document(
                f"./plugins/{input_str}.py",
                title=f"{input_str}.py",
                description=f"Module {input_str} Found",
                text=f"{input_str}.py usa .paste para pegar en neko y raw..",
                buttons=[
                    [
                        Button.switch_inline(
                            "Busca de nuevo..?",
                            query="send ",
                            same_peer=True,
                        ),
                    ],
                ],
            )
            await event.answer([ultroid])
            return
        except BaseException:
            ultroidcode = builder.article(
                title=f"Modulo {input_str}.py No encontrado",
                description=f"No existe tal módulo",
                text=f"Ningún módulo nombrado {input_str}.py",
                buttons=[
                    [
                        Button.switch_inline(
                            "Busca de nuevo",
                            query="send ",
                            same_peer=True,
                        ),
                    ],
                ],
            )
            await event.answer([ultroidcode])
            return


@ultroid_cmd(
    pattern="install",
)
async def install(event):
    await safeinstall(event)


@ultroid_cmd(
    pattern=r"unload ?(.*)",
)
async def unload(event):
    shortname = event.pattern_match.group(1)
    if not shortname:
        await eor(event, "`Dar el nombre del complemento que desea descargar`")
        return
    lsd = os.listdir("addons")
    lst = os.listdir("plugins")
    zym = shortname + ".py"
    if zym in lsd:
        try:
            un_plug(shortname)
            await eod(event, f"**Uɴʟᴏᴀᴅᴇᴅ** `{shortname}` **Sᴜᴄᴄᴇssғᴜʟʟʏ.**", time=3)
        except Exception as ex:
            return await eor(event, str(ex))
    elif zym in lst:
        return await eod(event, "**Yᴏᴜ Cᴀɴ'ᴛ Uɴʟᴏᴀᴅ Oғғɪᴄɪᴀʟ Pʟᴜɢɪɴs**", time=3)
    else:
        return await eod(event, f"**Nᴏ Pʟᴜɢɪɴ Nᴀᴍᴇᴅ** `{shortname}`", time=3)


@ultroid_cmd(
    pattern=r"uninstall ?(.*)",
)
async def uninstall(event):
    shortname = event.pattern_match.group(1)
    if not shortname:
        await eor(event, "`Dar el nombre del complemento que desea desinstalar`")
        return
    lsd = os.listdir("addons")
    lst = os.listdir("plugins")
    zym = shortname + ".py"
    if zym in lsd:
        try:
            un_plug(shortname)
            await eod(event, f"**Uɴɪɴsᴛᴀʟʟᴇᴅ** `{shortname}` **Sᴜᴄᴄᴇssғᴜʟʟʏ.**", time=3)
            os.remove(f"addons/{shortname}.py")
        except Exception as ex:
            return await eor(event, str(ex))
    elif zym in lst:
        return await eod(event, "**Yᴏᴜ Cᴀɴ'ᴛ Uɴɪɴsᴛᴀʟʟ Oғғɪᴄɪᴀʟ Pʟᴜɢɪɴs**", time=3)
    else:
        return await eod(event, f"**Nᴏ Pʟᴜɢɪɴ Nᴀᴍᴇᴅ** `{shortname}`", time=3)


@ultroid_cmd(
    pattern=r"load ?(.*)",
)
async def load(event):
    shortname = event.pattern_match.group(1)
    if not shortname:
        await eor(event, "`Dar el nombre del complemento que desea cargar`")
        return
    try:
        try:
            un_plug(shortname)
        except BaseException:
            pass
        load_addons(shortname)
        await eod(event, f"**Sᴜᴄᴄᴇssғᴜʟʟʏ Lᴏᴀᴅᴇᴅ** `{shortname}`", time=3)
    except Exception as e:
        await eod(
            event,
            f"**No puede cargar** `{shortname}` **debido al siguiente error.**\n`{str(e)}`",
            time=3,
        )


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
