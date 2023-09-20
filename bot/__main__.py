from Bot import OWNER_ID, API_ID, APP_HASH, BOT_NAME, BOT_TOKEN
from pyrogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB
import asyncio
from pyrogram import Client

class MyClient(Client):
    def __init__(self):
        super().__init__(BOT_NAME, api_id=API_ID, api_hash=APP_HASH, bot_token=BOT_TOKEN, plugins=dict(root="Bot/plugins"))
    async def on_start(self, client):
        # Perform actions when the client starts
        await send_message(OWNER_ID, text='Bot Started')
        #await client.send_message(chat_id="CHAT_ID", text="Hello, world!")

# Create an instance of the client
app = MyClient()

# Run the client
app.run()




'''
try:
    encoder.send_message(OWNER_ID, text='Bot Started', reply_markup=IKM([[IKB('ʜᴇʟᴘ', 'answer_help'), IKB('ᴅᴇᴠᴇʟᴏᴘᴇʀ', 'answer_about_dev')]]))
except:
    pass    

loop = asyncio.get_event_loop()
loop.run_forever()
'''