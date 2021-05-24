from yamlbot import YamlBot
from yamlbot.plugins.yamler import aexec
from io import StringIO
import sys
from pyrogram import types
from pyrogram.errors.exceptions.bad_request_400 import UserIsBlocked


@YamlBot.on_inline_query()
async def inline_query_handler(client: YamlBot, message: types.InlineQuery):
    cmd = 'p(message, stream=sys.stdout)'
    redirected_output = sys.stdout = StringIO()
    await aexec(cmd, client, message)
    evaluation = redirected_output.getvalue()
    final_output = f"```{evaluation.strip()}```"
    try:
        await client.send_message(message.from_user.id, final_output)
        await client.answer_inline_query(message.id,
                                        results=[],
                                        switch_pm_text="Output was sent to pm",
                                        switch_pm_parameter="start",
                                        cache_time=0
                                        )
    except UserIsBlocked:
        await client.answer_inline_query(message.id,
                                        results=[],
                                        switch_pm_text="Unblock me to get InlineQuery Yaml",
                                        switch_pm_parameter="start",
                                        cache_time=0
                                        )
    