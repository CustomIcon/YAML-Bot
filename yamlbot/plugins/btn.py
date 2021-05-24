from yamlbot import YamlBot
from pyrogram import filters
import asyncio


@YamlBot.on_callback_query(filters.regex('^remove'))
async def remove_btn(_, query):
    user_id = query.data.split('_')[1]
    if query.from_user.id == int(user_id):
        return await asyncio.gather(
            query.message.delete(),
            query.message.reply_to_message.delete()
        )
    await query.answer('This button is not for you', show_alert=True)