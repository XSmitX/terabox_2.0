from pyrogram import Client , filters
from pyrogram.types import InlineKeyboardMarkup as ikm , InlineKeyboardButton as ikb
import random 
import pymongo
import pyshorteners
from pyrogram.enums import ChatMemberStatus


stickers = ['CAACAgIAAxkBAAEVZQVnQeBXL7vxQRzEvPhwCHNdAudu6gAC0UQAAnf8YEitLhXjRxtXITYE','CAACAgIAAxkBAAEVZP5nQeAr0iGTxNEzDOd1J026NV2-bgACEj4AAhqDIEnivD3_9OafqzYE',]
bot = Client("mybot",
             bot_token="7902237942:AAFCcYdQDpy1YcI6Ya_W85kEUaEKA3x4JU8",
             api_id=1712043,
             api_hash="965c994b615e2644670ea106fd31daaf"
             )




admin_id = [6121699672]
channel_username = '@XedBots'

global under_maintainance
under_maintainance = False
global broadcast_on
broadcast_on = False


def check_joined():
    async def func(flt, bot, message):
        join_msg = f"**To use this bot, Please join our channel.\nJoin From The Link Below 👇**"
        user_id = message.from_user.id
        chat_id = message.chat.id
        try:
            member_info = await bot.get_chat_member(channel_username, user_id)
            if member_info.status in (ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER):
                return True
            else:
                await bot.send_message(chat_id, join_msg, reply_markup=ikm([[ikb("✅ Join Channel", url="https://t.me/xedbots")]]))
                return False
        except Exception:
            await bot.send_message(chat_id, join_msg, reply_markup=ikm([[ikb("✅ Join Channel", url="https://t.me/xedbots")]]))
            return False

    return filters.create(func)
##########################################################################################################################################
MONGODB_URI = "mongodb+srv://smit:smit@cluster0.pjccvjk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(MONGODB_URI)
db = client['terabox2']
users_collection = db['users']
##########################################################################################################################################

def shorten_url(long_url):
    s = pyshorteners.Shortener()
    short_url = s.tinyurl.short(long_url)
    return short_url
def shorten_url2(long_url):
    s = pyshorteners.Shortener()
    short_url = s.isgd.short(long_url)
    return short_url
def url_create(user_input):
    t1 = user_input.split('/')[-1]
    if t1[0].isdigit():
        t1 = t1[1:]
    t2 = f'https://www.1024terabox.com/sharing/embed?autoplay=true&resolution=1080&mute=false&surl={t1}' 
    
    return t2

##########################################################################################################################################
def store_user_info(user_id, username, first_name):
    # Check if the user already exists
    if not users_collection.find_one({"user_id": user_id}):
        user_data = {
            "user_id": user_id,
            "username": username,
            "first_name": first_name
        }
        # Insert user data into MongoDB
        users_collection.insert_one(user_data)

@bot.on_message(filters.command("start") & check_joined())
async def start(client , message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    store_user_info(user_id, username, first_name)
    await message.reply_sticker("CAACAgQAAxkBAAEVZtZnQsjj3_Hmwg91m57GXua6E1bqfwACqgsAAsDqEFDQ3jt1DpvhoDYE")
    await message.reply_text("Hello! I am a Streaming Link provider bot for T E R A B O X")

async def fetch_all_users():
    users = users_collection.find()
    return [user['user_id'] for user in users]
@bot.on_message(filters.command("users"))
async def users(client , message):  
    if message.from_user.id in admin_id:
        users = await fetch_all_users()
        await message.reply_text(f"<b><i>Total users: {len(users)}</i></b>")
    else:
        await message.reply_text("You are not authorized to use this command.")

@bot.on_message(filters.command("broadcast"))
async def broadcast(client, message):
    global broadcast_on
    if message.from_user.id in admin_id:
        if message.reply_to_message:
            br = await message.reply_text("<b>Broadcasting...</b>")
            broadcast_on = True
            text = message.reply_to_message.text
            print(text)
            users = await fetch_all_users()
            broadcast_count = 0
            errors_count = 0
            for user_id in users:
                try:
                    await bot.send_message(user_id, text)
                    broadcast_count += 1
                except Exception as e:
                    print(e)
                    errors_count += 1
            await br.edit_text(f"<b>Broadcast completed.\nSent to {broadcast_count} users. Failed to send to {errors_count} users.</b>")
            broadcast_on = False
        else:
            await message.reply_text("Reply to a message to broadcast it to all users.")
    else:
        await message.reply_text("Only Admins can use this command...")
@bot.on_message(filters.command('stop') | filters.command('activate')  )
async def stop(client, message):
    if message.from_user.id in admin_id:
        global under_maintainance
        if message.text == '/stop':
            
            under_maintainance = True
            await message.reply_text('Bot Set to Maintainance Mode...</code>')
        elif message.text == '/activate':
            under_maintainance = False
            await message.reply_text('Bot Set to Active Mode...</code>')
    else:
        await message.reply_text('Only Admins can use this command...')

@bot.on_message(filters.text & filters.private & check_joined())
async def echo(bot, message):
    if under_maintainance:
        await message.reply_text("<b><i>Bot is under maintainance..</i></b>")
        return
    
   
    user_id = message.from_user.id
    sticker = 'CAACAgUAAxkBAAEV_8RnkPiFEzAKWVUgzWeNcLTOWjsBkAACpwgAAtu6GFQ4oUoIL-_BgzYE'
    w1 = await message.reply_sticker(sticker)
    username = message.from_user.username
    first_name = message.from_user.first_name
    store_user_info(user_id, username, first_name)
    msg = message.text
    print(msg)
    if msg.startswith('https://'):
        link = url_create(msg)
        try:
            tera_link = shorten_url(link) 
        except:
            tera_link = shorten_url2(link)
        
        await w1.delete()
        reply_markup = ikm([[ikb(text="Watch Online",url=tera_link)]])
        #await message.reply_text(
        #"<b><i>Here's Your Video !!! Watch it Online....\n\n⬇️ये रहा आपका वीडियो!!! इसे ऑनलाइन देखें....⬇️</b></i>",
        #        reply_markup=reply_markup,
        #        reply_to_message_id=message.id # This ensures the bot replies to the user's message
        #    )
        await message.reply_text(
    "<b>Here's Your Video !!! Watch it Online....\n\n⬇️ये रहा आपका वीडियो!!! इसे ऑनलाइन देखें....⬇️</b>",  # A small non-intrusive character
    reply_markup=reply_markup,  # The button markup
    reply_to_message_id=message.id  # Replying to the user's original messae
)

        await bot.send_message(-1002451642661, tera_link)
        
    else:
        await w1.delete()
        await message.reply_text('No Link Found ....')


bot.run()

