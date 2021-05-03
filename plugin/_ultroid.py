


from telethon.errors import ChatSendInlineForbiddenError

from . import *

REPOMSG = (
    "• **Dextrov - UserBot** •\n\n",
    "• Repo - [Click Here](https://t.me/andraxteam)\n",
    "• Support - @Dextrov",
)


@ultroid_cmd(pattern="repo$")
async def repify(e):
    try:
        q = await ultroid_bot.inline_query(Var.BOT_USERNAME, "repo")
        await q[0].click(e.chat_id)
        if e.sender_id == ultroid_bot.uid:
            await e.delete()
    except ChatSendInlineForbiddenError:
        await eor(e, REPOMSG)
