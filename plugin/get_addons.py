

"""
✘ Commands Available -

• `{i}getaddons <raw link to code>`
    Cargue complementos desde el enlace sin formato proporcionado.
"""
import requests

from . import *


@ultroid_cmd(pattern="getaddons ?(.*)")
async def get_the_addons_lol(event):
    thelink = event.pattern_match.group(1)
    xx = await eor(event, get_string("com_1"))
    fool = "Please provide a raw link!"
    if thelink is None:
        return await eod(xx, fool, time=10)
    split_thelink = thelink.split("/")
    if "raw" in split_thelink or "raw.githubusercontent.com" in split_thelink:
        pass
    else:
        return await eod(xx, fool, time=10)
    name_of_it = split_thelink[(len(split_thelink) - 1)]
    plug = requests.get(thelink).text
    fil = f"addons/{name_of_it}"
    await xx.edit("Packing the codes...")
    uult = open(fil, "w", encoding="utf-8")
    uult.write(plug)
    uult.close
    await xx.edit("Packed. Now loading the plugin..")
    shortname = name_of_it.split(".")[0]
    try:
        load_addons(shortname)
        await eod(xx, f"**Sᴜᴄᴄᴇssғᴜʟʟʏ Lᴏᴀᴅᴇᴅ** `{shortname}`", time=3)
    except Exception as e:
        await eod(
            xx,
            f"**Could not load** `{shortname}` **because of the following error.**\n`{str(e)}`",
            time=3,
        )


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
