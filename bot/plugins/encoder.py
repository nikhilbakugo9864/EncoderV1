from enum import auto
import time, os
from pyrogram import filters
from pyrogram import Client as encoder 
from pyrogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB
import wget
from Bot.plugins.database.mongo_db import check_user_mdb,check_vcodec_settings,update_vcodec_settings,check_preset_settings,update_preset_settings,check_resolution_settings,check_audio_type_mdb, update_audio_type_mdb,update_resolution_settings
from Bot.utils.decorators import ffmpeg_settings
from Bot import OWNER_ID, LOG, FILES_CHANNEL
from Bot.utils.progress_pyro import progress_for_pyrogram
from Bot.utils.ffmpeg import ffmpeg_progress
from PIL import Image
encoder_is_on = []
flood = []

async def on_task_complete():
    del encoder_is_on[0]
    if len(encoder_is_on) > 0:
        if encoder_is_on[0]:
            await add_task(encoder_is_on[0])   
        
async def add_task(message):
    try:
        msg = await message.reply_text("<code>╰•★★ Downloading Files... ★★•╯</code>")
        c_time = time.time()
        FT = time.time()
        try:
            filepath = await message.download(progress=progress_for_pyrogram,progress_args=("**▅ ▆ ▇ █ Dᴏᴡɴʟᴏᴀᴅɪɴɢ █ ▇ ▆ ▅ \n\n**", msg, c_time))   
            check_resolution = check_resolution_settings(message.from_user.id)
            
            cmd = ffmpeg_settings(message.from_user.id, filepath, FT)  
            print (cmd)
            await msg.edit_text('**Encoding...**')
            try:
                await ffmpeg_progress(cmd, filepath,f'progress-{FT}.txt',FT, msg, '** ▅ ▆ ▇ █ Eɴᴄᴏᴅɪɴɢ Sᴛᴀʀᴛᴇᴅ█ ▇ ▆ ▅ **\n\n')
            except Exception as e:
                LOG.info(f'ERror while ffmpeg progress\n' +e)  
            output = filepath.rsplit('.',1)[0]
            if '.mkv' in filepath:
                output = output+'_@Aniimes_Nation.mkv'    
            else:
                output = output+'_@Aniimes_Nation.mp4'       
                
            file_name = output.rsplit('/', 1)[1].replace('_@Aniimes_Nation', "")
            sent_name=output.rsplit('/', 1)[1]
            print (output)
            thumbnail_url="https://graph.org/file/a1d45c72e2d93553bd29e.jpg"
            ph_path = wget.download(thumbnail_url)
            print (ph_path)
            Image.open(ph_path).convert("RGB").save(ph_path)
            img = Image.open(ph_path)
            img.resize((320, 320))
            img.save(ph_path, "JPEG")
            try: #MSG EDIT AND EDIT
                await msg.edit(f'**Encoding Completed')   
                file =  await msg.reply_document(output, thumb=ph_path, caption=f"**{check_resolution}\n__{file_name}__**", file_name=sent_name,force_document=True)  
            except Exception as e: 
                LOG.info(f'Error while file sending\n'+e)  
            try:
                await file.copy(FILES_CHANNEL)
            except Exception as e: 
                LOG.info(f'Error while file copy\n'+e)
                
            try: #FILE DELETE
                os.remove(filepath)
                os.remove(output)
                os.remove(f'progress-{FT}.txt')
                os.remove(ph_path)
            except Exception as e: 
                LOG.info(f'Error while removing files\n'+e)      
           
            try: #MSG DELETE
                await msg.delete() 
            except:
                pass       
                       
        except Exception as e: 
            LOG.info(f'Error while line 56\n'+e)    
    except Exception as e: 
        LOG.info(f'Error while Line 58\n'+e)
        
    try:
        await on_task_complete()   
    except Exception as e: 
       # await on_task_complete()   
        LOG.info(f'Error while task complete\n'+e) 
       


video_mimetype = [
    "video/x-flv",
    "video/mp4",
    "application/x-mpegURL",
    'application/zip',
    "video/MP2T",
    "video/3gpp",
    "video/quicktime",
    "video/x-msvideo",
    "video/x-ms-wmv",
    "video/x-matroska",
    "video/webm",
    "video/x-m4v",
    "video/quicktime",
    "video/mpeg"
]      
                  
@encoder.on_message(filters.document | filters.video & filters.private)
async def encoder_process(encoder, message):
    if message.document and message.video and message.document.mime_type and message.video.mime_type not in video_mimetype:
        return 
    check = check_user_mdb(message.from_user.id)
    if check is None:
        text= "You're not authorized to use this bot. Request Admins to approve you."
        await encoder.send_message(message.chat.id, text, reply_markup=IKM([[IKB('ʀᴇǫᴜᴇsᴛ', f'users_request-{message.from_user.id}')]]))
        return
    cancel_but=[[IKB("Clear queue🧹",callback_data="removequ")]]
    msf = await message.reply_text('Added to the queue', quote=True, reply_markup=IKM(cancel_but))
    encoder_is_on.append(message)
    #print (encoder_is_on)
    if len(encoder_is_on) == 1:
        await msf.delete()
        await add_task(message)      
    return 
                         
@encoder.on_callback_query(filters.regex('removequ'))
async def removing_que(bot, callback_query):
  await callback_query.answer("please wait")
  try: 
    message = callback_query.message
    replied_media=message.reply_to_message.id
    for i in encoder_is_on:
      if i.id==replied_media:
        encoder_is_on.remove(i)
    await message.edit("Successfully removed from queue✅")
  except Exception as e:
    await message.edit(e)
  #print (message)
  return 



@encoder.on_message(filters.command('view'))
async def view_que(bot, msg):
  await msg.reply_text(f'Total Queued Files : {str(len(encoder_is_on))}')
  return 