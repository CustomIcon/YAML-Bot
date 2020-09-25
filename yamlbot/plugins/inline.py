from yamlbot import YamlBot
from yamlbot.plugins.yamler import aexec
from io import StringIO
import sys
from pyrogram.errors.exceptions.bad_request_400 import UserIsBlocked

@YamlBot.on_inline_query()
async def inline_query_handler(client, message):
    answers = []
    cmd = f'p(message, stream=sys.stdout)'
    redirected_output = sys.stdout = StringIO()
    await aexec(cmd, client, message)
    evaluation = redirected_output.getvalue()
    final_output = f"```{evaluation.strip()}```"
    try:
        await client.send_message(message.from_user.id, final_output)
        await client.answer_inline_query(message.id,
                                        results=answers,
                                        switch_pm_text="Your Yaml was sent to pm",
                                        switch_pm_parameter="start"
                                        )
    except UserIsBlocked:
        await client.answer_inline_query(message.id,
                                        results=answers,
                                        switch_pm_text="Unblock me to get InlineQuery Yaml",
                                        switch_pm_parameter="start"
                                        )
    