from . import *


@asst_cmd("ban")
async def banhammer(event):
    x = await event.get_reply_message()
    if x is None:
        return await event.edit("Responde a alguien para que lo banee.")
    target = int(udB.get(str(x.id)))
    if not is_blacklisted(target):
        blacklist_user(target)
        await asst.send_message(event.chat_id, f"#BAN\nUser - {target}")
        await asst.send_message(
            target,
            "`¡Adiós! Has sido baneado.`\n**No se reenviarán más mensajes que envíe.**",
        )
    else:
        return await asst.send_message(event.chat_id, f"El usuario ya está prohibido!")


@asst_cmd("unban")
async def banhammer(event):
    x = await event.get_reply_message()
    if x is None:
        return await event.edit("Responde a alguien para que lo banee.")
    target = int(udB.get(str(x.id)))
    if is_blacklisted(target):
        rem_blacklist(target)
        await asst.send_message(event.chat_id, f"#UNBAN\nUser - {target}")
        await asst.send_message(target, "`¡Felicitaciones! Has sido desbaneado.`")
    else:
        return await asst.send_message(event.chat_id, f"El usuario nunca fue baneado!")
