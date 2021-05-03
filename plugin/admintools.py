
"""
✘ Commands Available -

• `{i}promote <reply to user/userid/username>`
    Promover al usuario en el chat.

• `{i}demote <reply to user/userid/username>`
    Degradar al usuario en el chat.

• `{i}ban <reply to user/userid/username> <reason>`
    Prohibir al usuario del chat.

• `{i}unban <reply to user/userid/username> <reason>`
    Desbancar al usuario del chat.

• `{i}kick <reply to user/userid/username> <reason>`
    Kick al usuario del chat.

• `{i}pin <reply to message>`
    Fijar el mensaje en el chat
    para uso silencioso use ({i}pin silent).

• `{i}unpin (all) <reply to message>`
    Desanclar el mensaje(s) en el chat.

• `{i}pinned`
   Obtener mensaje anclado en el chat actual.

• `{i}listpinned`
   Obtener todos los mensajes anclados en el chat actual.

• `{i}purge <reply to message>`
    Purgar todos los mensajes del mensaje respondido.

• `{i}purgeme <reply to message>`
    Purgar solo sus mensajes del mensaje respondido.

• `{i}purgeall <reply to message>`
    Eliminar todos los mensajes del usuario .

• `{i}del <reply to message>`
    Delete the replied message.

• `{i}edit <new message>`
    Edita tu último mensaje.
"""

import asyncio

from telethon.errors import BadRequestError
from telethon.errors.rpcerrorlist import UserIdInvalidError
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights, InputMessagesFilterPinned

from . import *


@ultroid_cmd(
    pattern="promote ?(.*)",
    groups_only=True,
    admins_only=True,
)
async def prmte(ult):
    xx = await eor(ult, get_string("com_1"))
    await ult.get_chat()
    user, rank = await get_user_info(ult)
    if not rank:
        rank = "Admin"
    if not user:
        return await xx.edit("`Responder a un usuario para promocionarlo!`")
    try:
        await ultroid_bot(
            EditAdminRequest(
                ult.chat_id,
                user.id,
                ChatAdminRights(
                    add_admins=False,
                    invite_users=True,
                    change_info=False,
                    ban_users=True,
                    delete_messages=True,
                    pin_messages=True,
                ),
                rank,
            ),
        )
        await xx.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `ahora es administrador en {ult.chat.title} con titulo {rank}.`",
        )
    except BadRequestError:
        return await xx.edit("`No tengo derecho a promocionarte.`")
    await asyncio.sleep(5)
    await xx.delete()


@ultroid_cmd(
    pattern="demote ?(.*)",
    groups_only=True,
    admins_only=True,
)
async def dmote(ult):
    xx = await eor(ult, get_string("com_1"))
    await ult.get_chat()
    user, rank = await get_user_info(ult)
    if not rank:
        rank = "Not Admin"
    if not user:
        return await xx.edit("`Responder a un usuario para degradarlo!`")
    try:
        await ultroid_bot(
            EditAdminRequest(
                ult.chat_id,
                user.id,
                ChatAdminRights(
                    add_admins=None,
                    invite_users=None,
                    change_info=None,
                    ban_users=None,
                    delete_messages=None,
                    pin_messages=None,
                ),
                rank,
            ),
        )
        await xx.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `ya no es un administrador en {ult.chat.title}`",
        )
    except BadRequestError:
        return await xx.edit("`No tengo derecho a degradarte.`")
    await asyncio.sleep(5)
    await xx.delete()


@ultroid_cmd(
    pattern="ban ?(.*)",
    groups_only=True,
    admins_only=True,
)
async def bban(ult):
    xx = await eor(ult, get_string("com_1"))
    await ult.get_chat()
    user, reason = await get_user_info(ult)
    if not user:
        return await xx.edit("`Responder a un usuario o dar un nombre de usuario para bloquearlo!`")
    if str(user.id) in DEVLIST:
        return await xx.edit(" `LoL, no puedo prohibir a mi desarrollador 😂`")
    try:
        await ultroid_bot.edit_permissions(ult.chat_id, user.id, view_messages=False)
    except BadRequestError:
        return await xx.edit("`No tengo derecho a prohibir a un usuario.`")
    except UserIdInvalidError:
        await xx.edit("`No pude entender quien es el!`")
    try:
        reply = await ult.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        return await xx.edit(
            f"[{user.first_name}](tg://user?id={user.id}) **Fue baneado por** [{OWNER_NAME}](tg://user?id={OWNER_ID}) **en** `{ult.chat.title}`\n**Razon**: `{reason}`\n**Mensajes eliminados**: `False`",
        )
    if reason:
        await xx.edit(
            f"[{user.first_name}](tg://user?id={user.id}) **Fue baneado por** [{OWNER_NAME}](tg://user?id={OWNER_ID}) **en** `{ult.chat.title}`\n**Razon**: `{reason}`",
        )
    else:
        await xx.edit(
            f"[{user.first_name}](tg://user?id={user.id}) **Fue baneado por** [{OWNER_NAME}](tg://user?id={OWNER_ID}) **en** `{ult.chat.title}`",
        )


@ultroid_cmd(
    pattern="unban ?(.*)",
    groups_only=True,
    admins_only=True,
)
async def uunban(ult):
    xx = await eor(ult, get_string("com_1"))
    await ult.get_chat()
    user, reason = await get_user_info(ult)
    if not user:
        return await xx.edit("`Responder a un usuario o dar un nombre de usuario para desbloquearlo!`")
    try:
        await ultroid_bot.edit_permissions(ult.chat_id, user.id, view_messages=True)
    except BadRequestError:
        return await xx.edit("`No tengo derecho a desbanear a un usuario.`")
    except UserIdInvalidError:
        await xx.edit("`No pude entender quien es el!`")
    if reason:
        await xx.edit(
            f"[{user.first_name}](tg://user?id={user.id}) **Ha sido Eliminado por** [{OWNER_NAME}](tg://user?id={OWNER_ID}) **enn** `{ult.chat.title}`\n**Razon**: `{reason}`",
        )
    else:
        await xx.edit(
            f"[{user.first_name}](tg://user?id={user.id}) **Ha sido Eliminado por** [{OWNER_NAME}](tg://user?id={OWNER_ID}) **en** `{ult.chat.title}`",
        )


@ultroid_cmd(
    pattern="kick ?(.*)",
    groups_only=True,
    admins_only=True,
)
async def kck(ult):
    if ult.text == f"{HNDLR}kickme":
        return
    xx = await eor(ult, get_string("com_1"))
    await ult.get_chat()
    user, reason = await get_user_info(ult)
    if not user:
        return await xx.edit("`¿Kick? ¿Quién? No pude conseguir su información...`")
    if str(user.id) in DEVLIST:
        return await xx.edit(" `Lol, no puedo sacar a mi desarrollador`😂")
    if user.id == ultroid_bot.uid:
        return await xx.edit("`No puedes kickearte solo`")
    try:
        await ultroid_bot.kick_participant(ult.chat_id, user.id)
        await asyncio.sleep(0.5)
    except BadRequestError:
        return await xx.edit("`No tengo derecho a dar Kick a un usuario.`")
    except Exception as e:
        return await xx.edit(
            f"`No tengo derecho a dar Kick a un usuario.`\n\n**ERROR**:\n`{str(e)}`",
        )
    if reason:
        await xx.edit(
            f"[{user.first_name}](tg://user?id={user.id})` Ha sido Eliminado` [{OWNER_NAME}](tg://user?id={OWNER_ID}) `in {ult.chat.title}`\n**Razon**: `{reason}`",
        )
    else:
        await xx.edit(
            f"[{user.first_name}](tg://user?id={user.id})` Ha sido Eliminado` [{OWNER_NAME}](tg://user?id={OWNER_ID}) `in {ult.chat.title}`",
        )


@ultroid_cmd(
    pattern="pin ?(.*)",
)
async def pin(msg):
    if not msg.is_private:
        # for pin(s) in private messages
        await msg.get_chat()
    cht = await ultroid_bot.get_entity(msg.chat_id)
    xx = msg.reply_to_msg_id
    tt = msg.text
    try:
        kk = tt[4]
        if kk:
            return
    except BaseException:
        pass
    if not msg.is_reply:
        return
    ch = msg.pattern_match.group(1)
    if ch != "silent":
        slnt = True
        x = await eor(msg, get_string("com_1"))
        try:
            await ultroid_bot.pin_message(msg.chat_id, xx, notify=slnt)
        except BadRequestError:
            return await x.edit("`Hmm, no tengo derechos aquí...`")
        except Exception as e:
            return await x.edit(f"**ERROR:**`{str(e)}`")
        await x.edit(f"`Pinned` [this message](https://t.me/c/{cht.id}/{xx})!")
    else:
        try:
            await ultroid_bot.pin_message(msg.chat_id, xx, notify=False)
        except BadRequestError:
            return await eor(msg, "`Hmm, no tengo derechos aquí...`")
        except Exception as e:
            return await eor(msg, f"**ERROR:**`{str(e)}`")
        try:
            await msg.delete()
        except BaseException:
            pass


@ultroid_cmd(
    pattern="unpin($| (.*))",
)
async def unp(ult):
    xx = await eor(ult, get_string("com_1"))
    if not ult.is_private:
        # for (un)pin(s) in private messages
        await ult.get_chat()
    ch = (ult.pattern_match.group(1)).strip()
    msg = ult.reply_to_msg_id
    if msg and not ch:
        try:
            await ultroid_bot.unpin_message(ult.chat_id, msg)
        except BadRequestError:
            return await xx.edit("`Hmm, no tengo derechos aquí...`")
        except Exception as e:
            return await xx.edit(f"**ERROR:**\n`{str(e)}`")
    elif ch == "all":
        try:
            await ultroid_bot.unpin_message(ult.chat_id)
        except BadRequestError:
            return await xx.edit("`Hmm, no tengo derechos aquí...`")
        except Exception as e:
            return await xx.edit(f"**ERROR:**`{str(e)}`")
    else:
        return await xx.edit(f"Responda a un mensaje o utilice `{hndlr}unpin all`")
    if not msg and ch != "all":
        return await xx.edit(f"Responda a un mensaje o utilice `{hndlr}unpin all`")
    await xx.edit("`Unpinned!`")


@ultroid_cmd(
    pattern="purge$",
)
async def fastpurger(purg):
    chat = await purg.get_input_chat()
    msgs = []
    count = 0
    if not purg.reply_to_msg_id:
        return await eod(purg, "`Responder a un mensaje para depurar.`", time=10)
    async for msg in ultroid_bot.iter_messages(chat, min_id=purg.reply_to_msg_id):
        msgs.append(msg)
        count = count + 1
        msgs.append(purg.reply_to_msg_id)
        if len(msgs) == 100:
            await ultroid_bot.delete_messages(chat, msgs)
            msgs = []

    if msgs:
        await ultroid_bot.delete_messages(chat, msgs)
    done = await ultroid_bot.send_message(
        purg.chat_id,
        "__Fast purge complete!__\n**Purged** `"
        + str(len(msgs))
        + "` **of** `"
        + str(count)
        + "` **messages.**",
    )
    await asyncio.sleep(5)
    await done.delete()


@ultroid_cmd(
    pattern="purgeme$",
)
async def fastpurgerme(purg):
    chat = await purg.get_input_chat()
    msgs = []
    count = 0
    if not purg.reply_to_msg_id:
        return await eod(purg, "`Responder a un mensaje para depurar.`", time=10)
    async for msg in ultroid_bot.iter_messages(
        chat,
        from_user="me",
        min_id=purg.reply_to_msg_id,
    ):
        msgs.append(msg)
        count = count + 1
        msgs.append(purg.reply_to_msg_id)
        if len(msgs) == 100:
            await ultroid_bot.delete_messages(chat, msgs)
            msgs = []

    if msgs:
        await ultroid_bot.delete_messages(chat, msgs)
    done = await ultroid_bot.send_message(
        purg.chat_id,
        "__Fast purge complete!__\n**Purged** `" + str(count) + "` **messages.**",
    )
    await asyncio.sleep(5)
    await done.delete()


@ultroid_cmd(
    pattern="purgeall$",
)
async def _(e):
    xx = await eor(e, get_string("com_1"))
    if e.reply_to_msg_id:
        input = (await e.get_reply_message()).sender_id
        name = (await e.client.get_entity(input)).first_name
        try:
            nos = 0
            async for x in e.client.iter_messages(e.chat_id, from_user=input):
                await e.client.delete_messages(e.chat_id, x)
                nos += 1
            await xx.edit(
                f"**Purged **`{nos}`** msgs of **[{name}](tg://user?id={input})",
            )
        except ValueError:
            return await eod(xx, str(er), time=5)
    else:
        return await eod(
            xx,
            "`Responder al mensaje de alguien para eliminar.`",
            time=5,
        )


@ultroid_cmd(
    pattern="del$",
)
async def delete_it(delme):
    msg_src = await delme.get_reply_message()
    if delme.reply_to_msg_id:
        try:
            await msg_src.delete()
            await delme.delete()
        except BaseException:
            await eod(
                delme,
                f"No se pudo borrar el mensaje.\n\n**ERROR:**\n`{str(e)}`",
                time=5,
            )


@ultroid_cmd(
    pattern="edit",
)
async def editer(edit):
    message = edit.text
    chat = await edit.get_input_chat()
    self_id = await ultroid_bot.get_peer_id("me")
    string = str(message[6:])
    i = 1
    async for message in ultroid_bot.iter_messages(chat, self_id):
        if i == 2:
            await message.edit(string)
            await edit.delete()
            break
        i = i + 1


@ultroid_cmd(pattern="pinned")
async def get_pinned(event):
    x = await eor(event, get_string("com_1"))
    chat_id = (str(event.chat_id)).replace("-100", "")
    chat_name = (await event.get_chat()).title
    tem = ""
    c = 0

    async for i in ultroid.iter_messages(
        event.chat_id, filter=InputMessagesFilterPinned
    ):
        c += 1
        tem += f"El mensaje anclado en {chat_name} puede ser encontrado <a href=https://t.me/c/{chat_id}/{i.id}>Aquí.</a>"
        if c == 1:
            return await x.edit(tem, parse_mode="html")

    if tem == "":
        return await eod(x, "No hay ningún mensaje anclado en el chat!", time=5)


@ultroid_cmd(pattern="listpinned")
async def get_all_pinned(event):
    x = await eor(event, get_string("com_1"))
    chat_id = (str(event.chat_id)).replace("-100", "")
    chat_name = (await event.get_chat()).title
    a = ""
    c = 1
    async for i in ultroid.iter_messages(
        event.chat_id, filter=InputMessagesFilterPinned
    ):
        a += f"{c}. <a href=https://t.me/c/{chat_id}/{i.id}>Ir al mensaje.</a>\n"
        c += 1

    if c == 1:
        m = f"<b>El mensaje anclado en {chat_name}:</b>\n\n"
    else:
        m = f"<b>Lista de mensajes fijados(s) en {chat_name}:</b>\n\n"

    if a == "":
        return await eod(x, "No hay ningún mensaje fijado en este grupo!", time=5)

    await x.edit(m + a, parse_mode="html")


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
