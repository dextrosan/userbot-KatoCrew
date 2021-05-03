# Ultroid - UserBot

"""
✘ Commands Available -

**Comandos de base de datos, no los use si no sabe qué es.**

• `{i}redisusage`
    Verificar la capacidad de datos almacenados.

• `{i}setredis key | value`
    Valor establecido de Redis.
    e.g :
    `{i}setredis hi there`
    `{i}setredis hi there | KatoCrew here`

• `{i}getredis key`
    Redis obtiene valor

• `{i}delredis key`
    Eliminar clave de Redis DB

• `{i}renredis old keyname | new keyname`
    Actualizar nombre de clave

• `{i}getkeys`
    Obtenga la lista de claves almacenadas en Redis
"""

import re

from . import *


@ultroid_cmd(
    pattern="setredis ?(.*)",
)
async def _(ult):
    ok = await eor(ult, "`...`")
    try:
        delim = " " if re.search("[|]", ult.pattern_match.group(1)) is None else " | "
        data = ult.pattern_match.group(1).split(delim, maxsplit=1)
        udB.set(data[0], data[1])
        redisdata = Redis(data[0])
        await ok.edit(
            "Redis Key Value Pair Updated\nKey : `{}`\nValue : `{}`".format(
                data[0],
                redisdata,
            ),
        )
    except BaseException:
        await ok.edit("`Something Went Wrong`")


@ultroid_cmd(
    pattern="getredis ?(.*)",
)
async def _(ult):
    ok = await eor(ult, "`Fetching data from Redis`")
    val = ult.pattern_match.group(1)
    if val == "":
        return await ult.edit(f"Please use `{hndlr}getkeys <keyname>`")
    try:
        value = Redis(val)
        await ok.edit(f"Key: `{val}`\nValue: `{value}`")
    except BaseException:
        await ok.edit("`Something Went Wrong`")


@ultroid_cmd(
    pattern="delredis ?(.*)",
)
async def _(ult):
    ok = await eor(ult, "`Deleting data from Redis ...`")
    try:
        key = ult.pattern_match.group(1)
        udB.delete(key)
        await ok.edit(f"`Successfully deleted key {key}`")
    except BaseException:
        await ok.edit("`Something Went Wrong`")


@ultroid_cmd(
    pattern="renredis ?(.*)",
)
async def _(ult):
    ok = await eor(ult, "`...`")
    delim = " " if re.search("[|]", ult.pattern_match.group(1)) is None else " | "
    data = ult.pattern_match.group(1).split(delim)
    if Redis(data[0]):
        try:
            udB.rename(data[0], data[1])
            await ok.edit(
                "Redis Key Rename Successful\nOld Key : `{}`\nNew Key : `{}`".format(
                    data[0],
                    data[1],
                ),
            )
        except BaseException:
            await ok.edit("Something went wrong ...")
    else:
        await ok.edit("Key not found")


@ultroid_cmd(
    pattern="getkeys$",
)
async def _(ult):
    ok = await eor(ult, "`Fetching Keys ...`")
    keys = sorted(udB.keys())
    msg = ""
    for x in keys:
        if x.isdigit() or x.startswith("-"):
            pass
        else:
            msg += f"• `{x}`" + "\n"
    await ok.edit(f"**List of Redis Keys :**\n{msg}")


@ultroid_cmd(
    pattern="redisusage$",
)
async def _(ult):
    ok = await eor(ult, "`Calculating ...`")
    x = 30 * 1024 * 1024
    z = 0
    for n in udB.keys():
        z += udB.memory_usage(n)
    a = humanbytes(z) + "/" + humanbytes(x)
    b = str(round(z / x * 100, 3)) + "%" + "  Used"
    await ok.edit(f"{a}\n{b}")


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
