
"""
✘ Commands Available -

• `{i}save <reply message>`
    Guarde ese mensaje de respuesta en su casilla de mensajes guardados.

"""
from . import *


@ultroid_cmd(pattern="save$")
async def saf(e):
    x = await e.get_reply_message()
    if not x:
        return await eod(
            e, "Reply to Any Message to save it to ur saved messages", time=5
        )
    await ultroid_bot.send_message("me", x)
    await eod(e, "Message saved at saved messages", time=5)


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
