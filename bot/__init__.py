import os, sys, logging
from pyrogram import Client 

if os.path.exists('error.log'):
    os.remove('error.log')
        
#<-----------LOGGING------------>
logging.basicConfig(level=logging.INFO, filename='error.log')
LOG = logging.getLogger("Bot by @nobody_ismy_name")
LOG.setLevel(level=logging.INFO)
#<-----------Variables-------------->
LOG.info('❤️ Checking Bot Variables.....')
TRIGGERS = os.environ.get("TRIGGERS", "/ !").split("/")
BOT_TOKEN = os.environ.get('BOT_TOKEN', '5825664739:AAEf9JUkp914r_GRSzKUFdbBfeUcBQAXAoo') #BOT Token Add
API_ID = int(os.environ.get('API_ID', 25508286)) #Telgram Api id
APP_HASH = os.environ.get('APP_HASH', '40214cc5dd97f8c5833c37be143bdd54')# Telgram App hash  
OWNER_ID = int(os.environ.get('OWNER_ID', 1448721786))
MONGO_DB = os.environ.get("MONGO_DB", 'mongodb+srv://narrutoofans:uu5MUKiquZusbsl2@cluster0.1oq2kqc.mongodb.net/?retryWrites=true&w=majority') #MONGO DB FOR ANIME DATA
FILES_CHANNEL = os.environ.get("FILES_CHANNEL", -1001861228406)
BOT_NAME = os.environ.get('BOT_NAME', 'assistant')
"""
#<---------------Connecting-------------->
if BOT_TOKEN is not None:
    try:
        encoder  = Client('AutoEncoder', api_id=API_ID, api_hash=APP_HASH, bot_token=BOT_TOKEN, plugins=dict(root="Bot/plugins"))
        LOG.info('❤️ Bot Connected Created By Github shootinstar000|| Telegram @nobody_ismy_name ')
    except Exception as e:
        LOG.warn(f'😞 Error While Connecting To Bot\nCheck Errors: {e}')
        sys.exit()       
"""
