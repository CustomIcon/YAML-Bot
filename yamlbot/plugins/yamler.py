from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import sys
from io import StringIO
import os

from yamlbot import YamlBot
from bprint import bprint as p
from yamlbot.plugins.nekobin import nekobin


async def aexec(code, client, message):
    exec("async def __aexec(client, message): "+"".join(f"\n {l}" for l in code.split("\n")))
    return await locals()["__aexec"](client, message)


@YamlBot.on_message(~filters.private & filters.command(['yaml', 'yaml@pyrogramyamlbot']))
@YamlBot.on_message(filters.private)
async def prettyprint(client, message: types.Message):
    if message.sender_chat:
        user_id = message.sender_chat.id
    else:
        user_id = message.from_user.id
    cmd = 'p(message, stream=sys.stdout)'
    redirected_output = sys.stdout = StringIO()
    await aexec(cmd, client, message)
    evaluation = redirected_output.getvalue()
    final_output = f"```{evaluation.strip()}```"
    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(evaluation.strip()))
        with open(filename, "r") as f:
            data = await nekobin(message, f.read())
        await message.reply_document(
            document=filename,
            quote=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('Nekobin', url=data)
                    ],
                    [
                        InlineKeyboardButton('Delete Message', callback_data=f'remove_{user_id}')
                    ]
                ]
            )
        )
        os.remove(filename)
    else:
        await message.reply_text(
            final_output,
            quote=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('Delete Message', callback_data=f'remove_{user_id}')
                    ]
                ]
            )
        )