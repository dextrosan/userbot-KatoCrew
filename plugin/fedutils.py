

"""
✘ Commands Available -

• `{i}superfban <reply to user/userid/username>`
    FBanear a la persona en todos los campos en los que es administrador.

• `{i}superunfban <reply to user/userid/username>`
    Un-FBan la persona en todos los campos en los que es administradorn.

Especifique el grupo y los federales para excluir en el asistente.

• `{i}fstat <username/id/reply to user>`
    Collect fed stat of the person in Rose.

• `{i}fedinfo <(fedid)>`
    Recopile información de la federación de la identificación del fed dada, o del fed que usted posee, de Rose.
"""

import asyncio
import os

from telethon.errors.rpcerrorlist import YouBlockedUserError

from . import *

bot = "@MissRose_bot"


@ultroid_cmd(pattern="superfban ?(.*)")
async def _(event):
    msg = await eor(event, "Starting a Mass-FedBan...")
    fedList = []
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await ultroid_bot.download_media(
                previous_message,
                "fedlist",
            )
            file = open(downloaded_file_name, encoding="utf8")
            lines = file.readlines()
            for line in lines:
                try:
                    fedList.append(line[:36])
                except BaseException:
                    pass
            arg = event.text.split(" ", maxsplit=2)
            if len(arg) > 2:
                FBAN = arg[1]
                REASON = arg[2]
            else:
                FBAN = arg[1]
                REASON = " #TBMassBanned "
        else:
            FBAN = previous_message.sender_id
            try:
                REASON = event.text.split(" ", maxsplit=1)[1]
            except BaseException:
                REASON = ""
            if REASON.strip() == "":
                REASON = " #TBMassBanned "
    else:
        arg = event.text.split(" ", maxsplit=2)
        if len(arg) > 2:
            try:
                FBAN = arg[1]
                REASON = arg[2]
            except BaseException:
                return await msg.edit("`Ningún usuario designado!`")
        else:
            try:
                FBAN = arg[1]
                REASON = " #TBMassBanned "
            except BaseException:
                return await msg.edit("`Ningún usuario designado!`")
    try:
        if str(FBAN) in DEVLIST:
            await msg.edit("No puedes prohibir mi desarrollo, novato!!")
            return
        elif FBAN.startswith("@"):
            try:
                x = await ultroid_bot(GetFullUserRequest(FBAN))
                uid = x.user.id
                if str(uid) in DEVLIST:
                    await msg.edit("No puedes prohibir mi desarrollo, novato!!")
                    return
            except Exception as e:
                print(str(e))
                return await msg.edit(str(e))
    except Exception as e:
        print(str(e))
        return await msg.edit(str(e))
    if udB.get("FBAN_GROUP_ID"):
        chat = int(udB.get("FBAN_GROUP_ID"))
    else:
        chat = await event.get_chat()
    if not len(fedList):
        for a in range(3):
            async with ultroid_bot.conversation("@MissRose_bot") as bot_conv:
                await bot_conv.send_message("/start")
                await asyncio.sleep(3)
                await bot_conv.send_message("/myfeds")
                await asyncio.sleep(3)
                try:
                    response = await bot_conv.get_response()
                except asyncio.exceptions.TimeoutError:
                    return await msg.edit(
                        "`Parece que Rose no responde o que el complemento no funciona correctamente.`",
                    )
                await asyncio.sleep(3)
                if "make a file" in response.text or "Looks like" in response.text:
                    await response.click(0)
                    await asyncio.sleep(3)
                    fedfile = await bot_conv.get_response()
                    await asyncio.sleep(3)
                    if fedfile.media:
                        downloaded_file_name = await ultroid_bot.download_media(
                            fedfile,
                            "fedlist",
                        )
                        await asyncio.sleep(6)
                        file = open(downloaded_file_name, errors="ignore")
                        lines = file.readlines()
                        for line in lines:
                            try:
                                fedList.append(line[:36])
                            except BaseException:
                                pass
                    elif "Solo puede usar los comandos alimentados una vez cada 5 minutos" in (
                        await bot_conv.get_edit
                    ):
                        await msg.edit("Vuelve a intentarlo después de 5 minutos.")
                        return
                if len(fedList) == 0:
                    await msg.edit(
                        f"No se puede recopilar FedAdminList. Reintentando ({a+1}/3)...",
                    )
                else:
                    break
        else:
            await msg.edit("Error")
        In = False
        tempFedId = ""
        for x in response.text:
            if x == "`":
                if In:
                    In = False
                    fedList.append(tempFedId)
                    tempFedId = ""
                else:
                    In = True
            elif In:
                tempFedId += x
        if len(fedList) == 0:
            await msg.edit("No se puede recopilar FedAdminList.")
            return
    await msg.edit(f"FBaning in {len(fedList)} feds.")
    try:
        await ultroid_bot.send_message(chat, f"/start")
    except BaseException:
        await msg.edit("El ID de grupo de FBan especificado es incorrecto.")
        return
    await asyncio.sleep(3)
    if udB.get("EXCLUDE_FED"):
        excludeFed = udB.get("EXCLUDE_FED").split(" ")
        for n in range(len(excludeFed)):
            excludeFed[n] = excludeFed[n].strip()
    exCount = 0
    for fed in fedList:
        if udB.get("EXCLUDE_FED") and fed in excludeFed:
            await ultroid_bot.send_message(chat, f"{fed} Excluded.")
            exCount += 1
            continue
        await ultroid_bot.send_message(chat, f"/joinfed {fed}")
        await asyncio.sleep(3)
        await ultroid_bot.send_message(chat, f"/fban {FBAN} {REASON}")
        await asyncio.sleep(3)
    try:
        os.remove("fedlist")
    except Exception as e:
        print(f"Error al eliminar el archivo FedAdmin.\n{str(e)}")
    await msg.edit(
        f"SuperFBan Completed.\nTotal Feds - {len(fedlist)}.\nExcluded - {exCount}.\n Affected {len(fedList) - exCount} feds.\n#TB",
    )


@ultroid_cmd(pattern="superunfban ?(.*)")
async def _(event):
    msg = await eor(event, "Starting a Mass-UnFedBan...")
    fedList = []
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await ultroid_bot.download_media(
                previous_message,
                "fedlist",
            )
            file = open(downloaded_file_name, encoding="utf8")
            lines = file.readlines()
            for line in lines:
                try:
                    fedList.append(line[:36])
                except BaseException:
                    pass
            arg = event.text.split(" ", maxsplit=2)
            if len(arg) > 2:
                FBAN = arg[1]
                REASON = arg[2]  # rose unbans now can have reasons
            else:
                FBAN = arg[1]
                REASON = ""
        else:
            FBAN = previous_message.sender_id
            try:
                REASON = event.text.split(" ", maxsplit=1)[1]
            except BaseException:
                REASON = ""
            if REASON.strip() == "":
                REASON = ""
    else:
        arg = event.text.split(" ", maxsplit=2)
        if len(arg) > 2:
            try:
                FBAN = arg[1]
                REASON = arg[2]
            except BaseException:
                return await msg.edit("`Ningún usuario designado!`")
        else:
            try:
                FBAN = arg[1]
                REASON = " #TBMassUnBanned "
            except BaseException:
                return await msg.edit("`No user designated!`")
    try:
        if str(FBAN) in DEVLIST:
            await msg.edit("No puedes prohibir mi desarrollo, novato!!")
            return
    except Exception as e:
        print(str(e))
        return await msg.edit(str(e))
    if udB.get("FBAN_GROUP_ID"):
        chat = int(udB.get("FBAN_GROUP_ID"))
    else:
        chat = await event.get_chat()
    if not len(fedList):
        for a in range(3):
            async with ultroid_bot.conversation("@MissRose_bot") as bot_conv:
                await bot_conv.send_message("/start")
                await asyncio.sleep(3)
                await bot_conv.send_message("/myfeds")
                await asyncio.sleep(3)
                try:
                    response = await bot_conv.get_response()
                except asyncio.exceptions.TimeoutError:
                    return await msg.edit(
                        "`Parece que Rose no responde o que el complemento no funciona correctamente.`",
                    )
                await asyncio.sleep(3)
                if "make a file" in response.text or "Looks like" in response.text:
                    await response.click(0)
                    await asyncio.sleep(3)
                    fedfile = await bot_conv.get_response()
                    await asyncio.sleep(3)
                    if fedfile.media:
                        downloaded_file_name = await ultroid_bot.download_media(
                            fedfile,
                            "fedlist",
                        )
                        await asyncio.sleep(6)
                        file = open(downloaded_file_name, errors="ignore")
                        lines = file.readlines()
                        for line in lines:
                            try:
                                fedList.append(line[:36])
                            except BaseException:
                                pass
                    elif "Solo puede usar los comandos alimentados una vez cada 5 minutos" in (
                        await bot_conv.get_edit
                    ):
                        await msg.edit("Vuelve a intentarlo después de 5 minutos.")
                        return
                if len(fedList) == 0:
                    await msg.edit(
                        f"No se puede recopilar FedAdminList. Reintentando ({a+1}/3)...",
                    )
                else:
                    break
        else:
            await msg.edit("Error")
        In = False
        tempFedId = ""
        for x in response.text:
            if x == "`":
                if In:
                    In = False
                    fedList.append(tempFedId)
                    tempFedId = ""
                else:
                    In = True
            elif In:
                tempFedId += x
        if len(fedList) == 0:
            await msg.edit("No se puede recopilar FedAdminList.")
            return
    await msg.edit(f"UnFBaning in {len(fedList)} feds.")
    try:
        await ultroid_bot.send_message(chat, f"/start")
    except BaseException:
        await msg.edit("Specified FBan Group ID is incorrect.")
        return
    await asyncio.sleep(3)
    if udB.get("EXCLUDE_FED"):
        excludeFed = udB.get("EXCLUDE_FED").split(" ")
        for n in range(len(excludeFed)):
            excludeFed[n] = excludeFed[n].strip()
    exCount = 0
    for fed in fedList:
        if udB.get("EXCLUDE_FED") and fed in excludeFed:
            await ultroid_bot.send_message(chat, f"{fed} Excluded.")
            exCount += 1
            continue
        await ultroid_bot.send_message(chat, f"/joinfed {fed}")
        await asyncio.sleep(3)
        await ultroid_bot.send_message(chat, f"/unfban {FBAN} {REASON}")
        await asyncio.sleep(3)
    try:
        os.remove("fedlist")
    except Exception as e:
        print(f"Error in removing FedAdmin file.\n{str(e)}")
    await msg.edit(
        f"SuperUnFBan Completed.\nTotal Feds - {len(fedlist)}.\nExcluded - {exCount}.\n Affected {len(fedList) - exCount} feds.\n#TB",
    )


@ultroid_cmd(pattern="fstat ?(.*)")
async def _(event):
    ok = await eor(event, "`Checking...`")
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        sysarg = str(previous_message.sender_id)
        user = f"[user](tg://user?id={sysarg})"
        if event.pattern_match.group(1):
            sysarg += f" {event.pattern_match.group(1)}"
    else:
        sysarg = event.pattern_match.group(1)
        user = sysarg
    if sysarg == "":
        await ok.edit(
            "`Dame la identificación de alguien o responde al mensaje de alguien para verificar su estado de fedstat.`",
        )
        return
    else:
        async with ultroid.conversation(bot) as conv:
            try:
                await conv.send_message("/start")
                await conv.get_response()
                await conv.send_message("/fedstat " + sysarg)
                audio = await conv.get_response()
                if audio.message.startswith("Este comando solo se puede usar una vez"):
                    return await ok.edit(
                        "Vaya, puede usar este comando solo una vez por minuto!",
                    )
                elif "Looks like" in audio.text:
                    await audio.click(0)
                    await asyncio.sleep(2)
                    audio = await conv.get_response()
                    await ultroid.send_file(
                        event.chat_id,
                        audio,
                        caption=f"List of feds {user} ha sido prohibido en.\n\nRecopilado usando Kato Crew Bor.",
                        link_preview=False,
                    )
                    await ok.delete()
                else:
                    okk = await conv.get_edit()
                    await ok.edit(okk.message)
                await ultroid.send_read_acknowledge(bot)
            except YouBlockedUserError:
                await ok.edit("**Error**\n `Desatascar` @MissRose_Bot `e intenta de nuevo!")


@ultroid_cmd(pattern="fedinfo ?(.*)")
async def _(event):
    ok = await event.edit("`Extrayendo información...`")
    sysarg = event.pattern_match.group(1)
    async with ultroid.conversation(bot) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message("/fedinfo " + sysarg)
            audio = await conv.get_response()
            await ultroid.send_read_acknowledge(bot)
            await ok.edit(audio.text + "\n\nFedInfo extraído por Kato Crew")
        except YouBlockedUserError:
            await ok.edit("**Error**\n `Desatascar` @MissRose_Bot `e intenta de nuevo!")


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
