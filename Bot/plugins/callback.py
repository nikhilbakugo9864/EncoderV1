import random, os
from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM, Message
from Bot import OWNER_ID, TRIGGERS, BOT_NAME
from Bot.plugins.database.mongo_db import users as mongp_user,check_user_mdb,check_vcodec_settings,update_vcodec_settings,check_preset_settings,update_preset_settings,check_resolution_settings,check_audio_type_mdb, update_audio_type_mdb,update_resolution_settings, check_crf_mdb, update_crf
from Bot.utils.user_info import  user_check_template, get_users
walls=["https://graph.org/file/bd0cc1cb7d254570a3d95.jpg", "https://graph.org/file/35f8b362519ff570377bd.jpg","https://graph.org/file/b8d4f05888c98fd5cd059.jpg", "https://graph.org/file/14125303a93c33d5eb7fa.jpg"]



BUTTONS_RESOLUTIONS = IKM(
    [
        [
            IKB("ₐᵦₒᵤₜ 𝒹ₑᵥ 👓", 'answer_about_dev'),
            IKB('ᵇᵃᶜᵏ 🚶 ', 'answer_help'),
        ],
        [
            IKB('sᴇᴛ 𝟺𝟾𝟶ᴘ', 'settings_encoding_480p'),
            IKB('sᴇᴛ 𝟽𝟸𝟶ᴘ', 'settings_encoding_720p'),
            IKB('ѕєт 1080ρ', 'settings_encoding_1080p'),
        ]
    ]
)

BUTTONS_CRF = IKM(
    [
        [
            IKB("ₐᵦₒᵤₜ 𝒹ₑᵥ 👓", 'answer_about_dev'),
            IKB('ᵇᵃᶜᵏ 🚶', 'answer_help')
        ],
        [
            IKB('ᴄʀғ + 𝟷', 'settings_crf_plus'),
            IKB('ᴄʀғ - 𝟷', 'settings_crf_minus'),
        ]
    ]
)

BUTTONS_AUDIO = IKM(
    [
        [
            IKB("ₐᵦₒᵤₜ 𝒹ₑᵥ 👓", 'answer_about_dev'),
            IKB('ᵇᵃᶜᵏ 🚶', 'answer_help')
        ],
        [
            IKB('sᴇᴛ ᴀᴀᴄ', 'settings_encoding_aac'),
            IKB('ѕєт ᴏᴘᴜs', 'settings_encoding_opus'),
            IKB('sᴇᴛ ʟɪʙᴏᴘᴜs', 'settings_encoding_libopus'),
        ]
    ]
)

BUTTONS_PRESET = IKM(
    [
        [
            IKB("ₐᵦₒᵤₜ 𝒹ₑᵥ 👓", 'answer_about_dev'),
            IKB('ᵇᵃᶜᵏ 🚶', 'answer_help')
        ],
        [
            IKB('sᴇᴛ ғᴀsᴛ', 'settings_encoding_fast'),
            IKB('ѕєт sʟᴏᴡ', 'settings_encoding_slow'),
        ]
    ]
)

BUTTONS_VCODEC = IKM(
    [
        [
            IKB("ₐᵦₒᵤₜ 𝒹ₑᵥ 👓", 'answer_about_dev'),
            IKB('ᵇᵃᶜᵏ 🚶', 'answer_help')
        ],
        [
            IKB('sᴇᴛ x𝟸𝟼𝟺', 'settings_encoding_x264'),
            IKB('ѕєт x𝟸𝟼𝟻', 'settings_encoding_x265'),
        ]
    ]
)

#_______NON REPEATING BUTTONS_____________
BUTTONS_DEV = IKM(
    [
        [
            IKB('ₜ𝓰 ᵤₛₑᵣₙₐₘₑ ✉️', url='https://t.me/nobody_ismy_name'),
            IKB('ɢɪᴛʜᴜʙ', url = 'https://github.com/shootinstar000')
        ],
        [
            IKB('ᴄʜᴀɴɴᴇʟ', url='https://t.me/OG_bratflix'),
        ],
        [
            IKB('⚙️ₛₑₜₜᵢₙ𝓰ₛ⚙️', 'answer_help')
        ]
    ]
)

BUTTONS_HELP = IKM(
    [
        [
            IKB("ₐᵦₒᵤₜ 𝒹ₑᵥ 👓", 'answer_about_dev'),
        ], 
        [
            IKB('ʀᴇsᴏʟᴜᴛɪᴏɴ', 'answer_resolution'),
            IKB('ᴀᴜᴅɪᴏ', 'answer_audio'),
            IKB('ᴄʀғ', 'answer_crf')
        ],
        [
           IKB('ᴠᴄᴏᴅᴇᴄ', 'answer_vcodec'),
           IKB('ᴘʀᴇsᴇᴛ', 'answer_preset'), 
        ]
    ]
)


@Client.on_callback_query(filters.regex('users'))
async def callback_authroize(client:Client, callback_query): 
    #print (callback_query.data)
    if 'unauth' in callback_query.data:
        if callback_query.from_user.id != OWNER_ID:
            await callback_query.answer("Oops You're not authorized to do this")
            return
        id = callback_query.data.split('-')[1]
        id = int(id)
        get_us= await client.get_users(id)
        get_u = await get_users(get_us)
        mongp_user.find_one_and_delete({'user_id':int(id)})
        try:
            pic_user = await client.download_media(get_u[5], file_name=f"user.png")
        except:
            pass    
        TEXTS = await user_check_template(get_u[0],get_u[1],get_u[2],get_u[3],get_u[4],get_u[6])
        try:
            notify = await client.send_photo(OWNER_ID, pic_user,caption="`-------`**ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**`-------`\n\n"+ TEXTS,reply_markup=IKM([[IKB('ᴀᴜᴛʜᴏʀɪᴢᴇ',f'users_auth-{id}'), IKB('ʜᴇʟᴘ', 'answer_help')]]))
        except:
            notify = await client.send_message(OWNER_ID, text="`-------`**ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ**`-------`\n\n"+ TEXTS,reply_markup=IKM([[IKB('ᴀᴜᴛʜᴏʀɪᴢᴇ',f'users_auth-{id}'), IKB('ʜᴇʟᴘ', 'answer_help')]]))    
        await callback_query.answer("❌unAuthorized Successfully ")
        try:
            await client.send_message (id, "❌You have been unauthorized to use the bot ❌")
        except:
            pass  
        
    elif 'auth' in callback_query.data:
        if callback_query.from_user.id != OWNER_ID:
            await callback_query.answer("Oops You're not authorized to do this")
            return
        id = callback_query.data.split('-')[1]
        id = int(id)
        get_us= await client.get_users(id)
        get_u = await get_users(get_us)
        print (get_u)
        mongp_user.insert_one({'user_id':id,'resolution':'480p','preset':'fast','audio_type':'aac','vcodec':'x264', 'crf':26})               
        try:
            pic_user = await client.download_media(get_u[5], file_name=f"user.png")
        except:
            pass   
             
        TEXTS = await user_check_template(get_u[0],get_u[1],get_u[2],get_u[3],get_u[4],get_u[6])
        try:
            notify = await client.send_photo(OWNER_ID, pic_user,caption="`-------`**ᴀᴜᴛʜᴏʀɪᴢᴇᴅ**`-------`\n\n"+ TEXTS,reply_markup=IKM([[IKB('ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇ',f'users_unauth-{id}'), IKB('ʜᴇʟᴘ', 'answer_help')]]))
        except:
            notify = await client.send_message(OWNER_ID,text="`-------`**ᴀᴜᴛʜᴏʀɪᴢᴇᴅ**`-------`\n\n"+ TEXTS,reply_markup=IKM([[IKB('ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇ',f'users_unauth-{id}'), IKB('ʜᴇʟᴘ', 'answer_help')]]))
        await callback_query.answer("✅authorized successfully")
        try:
            await client.send_message(id, "✅Your Request to to access the bot has been accepted, \n Now u can Use the bot")
        except:
            pass    
        
    elif 'request' in callback_query.data:
        
        id_ = callback_query.data.split('-')[1]
        
        get_us= await client.get_users(id_)
        get_u = await get_users(get_us)
        pic_user = await client.download_media(get_u[5], file_name=f"user.png")
        TEXTS = await user_check_template(get_u[0],get_u[1],get_u[2],get_u[3],get_u[4],get_u[6])
        print (TEXTS)
        try:
          notify = await client.send_photo(OWNER_ID , pic_user,caption="`-------`**ʀᴇǫᴜᴇsᴛᴇᴅ ᴀᴜᴛʜᴏʀɪᴢᴇ**`-------`\n\n"+ TEXTS,reply_markup=IKM([[IKB('ᴀᴜᴛʜᴏʀɪᴢᴇ',f'users_auth-{id_}'), IKB('ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇ',f'users_unauth-{id_}')]]))  
          await callback_query.message.edit('Request sent')
        except Exception as e :
          print (e)

@Client.on_callback_query(filters.regex('settings'))
async def settings_callback(client:Client, callback_query): 
    check = check_user_mdb(callback_query.from_user.id)  
    if check is None:
        text= "You're not authorized to use this bot. Request Admins to approve you."
        await callback_query.message.edit(text, reply_markup=IKM([[IKB('ʀᴇǫᴜᴇsᴛ', f'users_request-{callback_query.from_user.id}')]]))
        return
    if 'encoding_480p' in callback_query.data:
        update_resolution_settings(callback_query.from_user.id, '480p')
        await callback_query.message.edit('ᴜᴘᴅᴀᴛᴇᴅ ᴠɪᴅᴇᴏ ʀᴇsᴏʟᴜᴛɪᴏɴn ᴛᴏ 480p',reply_markup=BUTTONS_RESOLUTIONS)
    elif 'encoding_720p' in callback_query.data:
        update_resolution_settings(callback_query.from_user.id, '720p')
        await callback_query.message.edit('ᴜᴘᴅᴀᴛᴇᴅ ᴠɪᴅᴇᴏ ʀᴇsᴏʟᴜᴛɪᴏɴ ᴛᴏ 720p',reply_markup=BUTTONS_RESOLUTIONS)  
    elif 'encoding_1080p' in callback_query.data:
        update_resolution_settings(callback_query.from_user.id, '1080p')
        await callback_query.message.edit('ᴜᴘᴅᴀᴛᴇᴅ ᴠɪᴅᴇᴏ ʀᴇsᴏʟᴜᴛɪᴏɴ ᴛᴏ 1080p',reply_markup=BUTTONS_RESOLUTIONS)          
    elif 'encoding_aac' in callback_query.data:
        update_audio_type_mdb(callback_query.from_user.id, 'aac')
        await callback_query.message.edit('ᴜᴘᴅᴀᴛᴇᴅ ᴀᴜᴅɪᴏ ᴛʏᴘᴇ ᴛᴏ ᴀᴀᴄ', reply_markup=BUTTONS_AUDIO)  
    elif 'encoding_opus' in callback_query.data:
        update_audio_type_mdb(callback_query.from_user.id, 'opus')
        await callback_query.message.edit('ᴜᴘᴅᴀᴛᴇᴅ ᴀᴜᴅɪᴏ ᴛʏᴘᴇ ᴛᴏ ᴏᴘᴜs', reply_markup=BUTTONS_AUDIO) 
    elif 'encoding_libopus' in callback_query.data:
        update_audio_type_mdb(callback_query.from_user.id, 'libopus')
        await callback_query.message.edit('ᴜᴘᴅᴀᴛᴇᴅ ᴀᴜᴅɪᴏ ᴛʏᴘᴇ ᴛᴏ ʟɪʙᴏᴘᴜs', reply_markup=BUTTONS_AUDIO) 
    elif 'encoding_x264' in callback_query.data:
        update_vcodec_settings(callback_query.from_user.id, 'x264')
        await callback_query.message.edit('ᴜᴘᴅᴀᴛᴇᴅ ᴠɪᴅᴇᴏ ᴄᴏᴅᴇᴄ ᴛᴏ x𝟸𝟼𝟺', reply_markup=BUTTONS_VCODEC)       
    elif 'encoding_x265' in callback_query.data:
        update_vcodec_settings(callback_query.from_user.id, 'x265')
        await callback_query.message.edit('ᴜᴘᴅᴀᴛᴇᴅ ᴠɪᴅᴇᴏ ᴄᴏᴅᴇᴄ ᴛᴏ x𝟸𝟼𝟻', reply_markup=BUTTONS_VCODEC)    
    elif 'encoding_slow' in callback_query.data:
        update_preset_settings(callback_query.from_user.id, 'slow')
        await callback_query.message.edit('ᴜᴘᴅᴀᴛᴇᴅ ᴠɪᴅᴇᴏ ᴘʀᴇsᴇᴛ ᴛᴏ sʟᴏᴡ', reply_markup=BUTTONS_PRESET)  
    elif 'encoding_fast' in callback_query.data:
        update_preset_settings(callback_query.from_user.id, 'fast')
        await callback_query.message.edit('ᴜᴘᴅᴀᴛᴇᴅ ᴠɪᴅᴇᴏ ᴘʀᴇsᴇᴛ ᴛᴏ ғᴀsᴛ', reply_markup=BUTTONS_PRESET) 
    elif 'crf_plus' in callback_query.data:
        crf_current = check_crf_mdb(callback_query.from_user.id)
        update = crf_current+1
        crf_plus = update_crf(callback_query.from_user.id, update)
        await callback_query.message.edit(f'ᴜᴘᴅᴀᴛᴇᴅ ᴠɪᴅᴇᴏ ᴄʀғ ᴛᴏ {update}', reply_markup=BUTTONS_CRF) 
    elif 'crf_minus' in callback_query.data:
        crf_current = check_crf_mdb(callback_query.from_user.id)
        update = crf_current-1
        crf_plus = update_crf(callback_query.from_user.id, update)
        await callback_query.message.edit(f'ᴜᴘᴅᴀᴛᴇᴅ ᴠɪᴅᴇᴏ ᴄʀғ ᴛᴏ {update}', reply_markup=BUTTONS_CRF)    
            

@Client.on_callback_query(filters.regex('blankquery'))
async def blankcallback_answer(client:Client, callback_query): 
    await callback_query.answer('Oops Empty')
        
@Client.on_callback_query(filters.regex('answer'))
async def callback_answer(client:Client, callback_query): 
    check = check_user_mdb(callback_query.from_user.id)
    if check is None:
        text= "You're not authorized to use this bot. Request Admins to approve you."
        await callback_query.message.edit(text, reply_markup=IKM([[IKB('ʀᴇǫᴜᴇsᴛ', f'users_request-{callback_query.from_user.id}')]]))
        return
    if 'help' in callback_query.data:
        text = f'**Hi There** `{callback_query.from_user.first_name}`,\n\nI am a video encoder bot, which reduces the size of the video and gives it in good quality.\n\nTo see all my features, click the buttons below'
        await callback_query.message.edit(text, reply_markup=BUTTONS_HELP) 
    elif 'crf' in callback_query.data:
        text = '**To change the video crf of this bot, use the buttons given below**.\n\n'
        text += f'**Your current video crf  is** : `{check_crf_mdb(callback_query.from_user.id)}`\n\n**[Created By Mr.Nobody](https://t.me/nobody_ismy_name)**'
        await callback_query.message.edit(text, reply_markup=BUTTONS_CRF) 
    elif 'resolution' in callback_query.data:
        text = '**To change the video resolution of this bot, use the buttons given below**.\n\n'
        text += f'**Your current video resolution is** : `{check_resolution_settings(callback_query.from_user.id)}`\n\n**[Created By Mr. Nobody ](https://t.me/nobody_ismy_name)**'
        await callback_query.message.edit(text, reply_markup=BUTTONS_RESOLUTIONS) 
    elif 'audio' in callback_query.data:  
        text = '**To change the audio type of this bot, use the buttons given below**.\n\n'
        text += f'**Your current audio type is** : `{check_audio_type_mdb(callback_query.from_user.id)}`\n\n**[Created By Mr. Nobody ](https://t.me/nobody_ismy_name)**'  
        await callback_query.message.edit(text, reply_markup=BUTTONS_AUDIO) 
    elif 'vcodec' in callback_query.data:  
        text = '**To change the video codec of this bot, use the buttons given below**.\n\n'
        text += f'**Your current video codec is** : `{check_vcodec_settings(callback_query.from_user.id)}`\n\n**[Created By Mr. Nobody ](https://t.me/nobody_ismy_name)**'  
        await callback_query.message.edit(text, reply_markup=BUTTONS_VCODEC)  
    elif 'preset' in callback_query.data:  
        text = '**To change the video preset of this bot, use the buttons given below**.\n\n'
        text += f'**Your current video preset is** : `{check_preset_settings(callback_query.from_user.id)}`\n\n**[Created By Mr. Nobody ](https://t.me/nobody_ismy_name)**'  
        await callback_query.message.edit(text, reply_markup=BUTTONS_PRESET) 
    elif 'about_dev' in callback_query.data:
        text = f'Hello `{callback_query.from_user.first_name}`,\n\n'
        text += "The bot is modified by me, Mr.Nobody😉\nTo connect with me, Click Below Buttons"
        await callback_query.message.edit(text,reply_markup=BUTTONS_DEV)    
    await callback_query.answer('Your Query Processed.')   
              
@Client.on_message(filters.command(['start', 'help']) & filters.private)
async def start_(client: Client, message: Message):
    
    if message.reply_to_message:
        reply = message.reply_to_message
        user_id = reply.from_user.id  
    else:
        user_id = message.from_user.id  
    await message.reply_photo(
        photo =random.choice(walls), 
        caption = f'**Hi There** `{message.from_user.first_name}`,\n\nI am a video encoder bot, which reduces the size of the video and gives it in good quality.\nTo see all my features, click the buttons below',
        reply_markup=IKM(
            [
                [
                    IKB(
                        "ₐᵦₒᵤₜ 𝒹ₑᵥ👓",
                        "answer_about_dev"
                    ),
                    IKB(
                        "⚙️ₛₑₜₜᵢₙ𝓰ₛ⚙️",
                        "answer_help"
                    )
                ],
            ],
        ),
    ) 
