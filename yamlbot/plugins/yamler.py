from pyrogram import filters
import sys
import re
from io import StringIO
import os
import traceback

from yamlbot import YamlBot
from bprint import bprint as p


async def aexec(code, client, message):
    exec(
        f"async def __aexec(client, message): "
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


@YamlBot.on_message(~filters.private & filters.command('yaml'))
@YamlBot.on_message(filters.private)
async def prettyprint(client, message):
    cmd = f'p(message, stream=sys.stdout)'
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = f"```{evaluation.strip()}```"
    await message.reply_text(final_output)