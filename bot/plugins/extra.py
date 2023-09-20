import os, random, time, sys
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Bot import TRIGGERS as trg, OWNER_ID

@Client.on_message(filters.user(OWNER_ID) & filters.command(['restart']))
async def restart_bot(client: Client, message: Message):  
    msg = await message.reply("Restarting", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Dev', url='https://t.me/nobody_ismy_name')]]))
    os.execl(sys.executable, sys.executable, "-m", "Bot")  
    msg.edit_text("successfully restarted ")