from pyrogram import filters
import sys
import re
from io import StringIO
import os
import traceback

from yamlbot import YamlBot
from bprint import bprint as p
from yamlbot.plugins.nekobin import nekobin


async def aexec(code, client, message):
    exec(
        f"async def __aexec(client, message): "
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


@YamlBot.on_message(~filters.private & filters.command(['yaml', 'yaml@pyrogramyamlbot']))
@YamlBot.on_message(filters.private)
async def prettyprint(client, message):
    cmd = f'p(message, stream=sys.stdout)'
    redirected_output = sys.stdout = StringIO()
    await aexec(cmd, client, message)
    evaluation = redirected_output.getvalue()
    final_output = f"```{evaluation.strip()}```"
    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(evaluation.strip()))
            data = await nekobin(message, out_file.read())
        await message.reply_document(document=filename, caption=data)
        os.remove(filename)
    else:
        await message.reply_text(final_output)