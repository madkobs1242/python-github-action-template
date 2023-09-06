from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
import tgcrypto
import time
import re
import asyncio
import random
import aiomysql
import httpx

#--------------------------------------------------------------------------------------------------------------------#

API_ID = 16438239
API_HASH = '91354720e00d5c9af4b8752cb271ddc4'

gpdel = '-1001904111237'

bot = Client('bot', API_ID, API_HASH)
print('bot is online!')

lock = asyncio.Lock()

#--------------------------------------------------------------------------------------------------------------------#

Main_Keyboard = ReplyKeyboardMarkup([['📞 خرید شماره مجازی'], ['🧾 قوانین و راهنما', '⚙️ حساب کاربری'], ['💸 افزایش موجودی']], resize_keyboard = True)
Admin_Keyboard = ReplyKeyboardMarkup([['📊 وضعیت ربات'], ['⛔️ مسدود کردن', '✅ رفع مسدودی'], ['📈 کاهش موجودی', '📉 افزودن موجودی'], ['✖️ حذف شماره ها', '➕ افزودن شماره'], ['💵 تنظیم قیمت', '👤 اطلاعات کاربر'], ['🔙 بازگشت']], resize_keyboard = True)
admin = [1627944341]

#--------------------------------------------------------------------------------------------------------------------#

async def Start(Client, message, pool) :

    try :

        chat_id = message.chat.id

        async with pool.acquire() as db :
            async with db.cursor() as cursor :

                await cursor.execute('SELECT step FROM users WHERE user_id = %s' %chat_id)
                data = await cursor.fetchone()

        if data[0] != 'BAN' :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    chg = ('HOME', chat_id)
                    await cursor.execute('UPDATE users SET step = %s WHERE user_id = %s', chg)
                    await db.commit()

                    await message.reply(f'''🌐 به فونیکس نامبر خوش آمدید 💝

👇🏻 برای ادامه یکی از دکمه های زیر را انتخاب نمایید :''', quote = True, reply_markup = Main_Keyboard)

    except Exception as er_Start :
        async with pool.acquire() as db :
            await db.rollback()
        print(f'Start Error : {er_Start}')

#-------------------------------------------------------------#

async def Back(Client, message, pool) :

    try :

        chat_id = message.chat.id

        async with pool.acquire() as db :
            async with db.cursor() as cursor :

                await cursor.execute('SELECT step FROM users WHERE user_id = %s' %chat_id)
                data = await cursor.fetchone()

        if data[0] not in ['HOME', 'BAN'] :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    chg = ('HOME', chat_id)
                    await cursor.execute('UPDATE users SET step = %s WHERE user_id = %s', chg)
                    await db.commit()

                    await message.reply('🔙 به منوی اصلی برگشتید!', quote = True, reply_markup = Main_Keyboard)

    except Exception as er_Back :
        async with pool.acquire() as db :
            await db.rollback()
        print(f'Back Error : {er_Back}')

#-------------------------------------------------------------#

async def UserAccount(Client, message, pool) :

    try :

        chat_id = message.chat.id

        async with pool.acquire() as db :
            async with db.cursor() as cursor :

                await cursor.execute('SELECT step, wallet, num FROM users WHERE user_id = %s' %chat_id)
                data = await cursor.fetchone()

        if data[0] == 'HOME' :

            bot_info = await bot.get_me()

            await message.reply(f'''🔐 اطلاعات حساب کاربری شما در فونیکس نامبر :

 👤 شناسه : {chat_id}
 💳 موجودی : {int(data[1]):,} تومان
🛍 تعداد شماره های خریداری شده : {data[2]} عدد

🤖 @{bot_info.username}''', quote = True)

    except Exception as er_UserAccount :
        print(f'UserAccount Error : {er_UserAccount}')

#-------------------------------------------------------------#

async def RulesGuide(Client, message, pool) :

    try :

        chat_id = message.chat.id

        async with pool.acquire() as db :
            async with db.cursor() as cursor :

                await cursor.execute('SELECT step FROM users WHERE user_id = %s' %chat_id)
                data = await cursor.fetchone()

        if data[0] == 'HOME' :

            await message.reply('''🪖 به فونیکس نامبر خوش اومدید 🪖

به طور تغریبی 99 درصد شماره های ربات سالم هستن نه بن هستن نه سشن دارن و نه مشکلی در کد دهی دارن✅

در صورت کد ندادن یک شماره میتونید اون رو لغو کنید و پول به حسابتون برمیگرده و میتونید شماره دیگری بخرید❤️‍🔥

در صورت مایل بودن به خرید عمده تعداد و قیمت پیشنهادی خود را به پیوی من ارسال کنید☎️

جهت راهنمایی,بروز مشکل و شارژ حساب به پیویم مراجعه کنید.

🆔 | @Mad_Kings''', quote = True)

    except Exception as er_RulesGuide :
        print(f'RulesGuide Error : {er_RulesGuide}')

#-------------------------------------------------------------#

async def Support(Client, message, pool) :

    try :

        chat_id = message.chat.id

        async with pool.acquire() as db :
            async with db.cursor() as cursor :

                await cursor.execute('SELECT step FROM users WHERE user_id = %s' %chat_id)
                data = await cursor.fetchone()

        if data[0] == 'HOME' :

            await message.reply('''به قسمت شارژ  حساب خوش اومدید💗

برای شارژ حساب کاربری جهت خرید شماره به پیوی من مراجعه کنید🎁

پیام های شما ضرف کمتر از 1 ساعت جواب داده میشن,از صبوری شما متشکریم❤️

🆔 | @Mad_Kings''', quote = True)

    except Exception as er_Support :
        print(f'Support Error : {er_Support}')

#-------------------------------------------------------------#

async def BuyNumber(Client, message, pool) :

    try :

        chat_id = message.chat.id

        async with pool.acquire() as db :
            async with db.cursor() as cursor :

                await cursor.execute('SELECT step, wallet FROM users WHERE user_id = %s' %chat_id)
                data = await cursor.fetchone()

        if data[0] == 'HOME' :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    chg = ('BUY NUMBER', chat_id)
                    await cursor.execute('UPDATE users SET step = %s WHERE user_id = %s', chg)
                    await db.commit()

                    await cursor.execute('SELECT * FROM information')
                    prices = await cursor.fetchone()

                    await message.reply(f'''☎️ لطفا نوع شماره را انتخاب کنید :

✔️ قیمت شماره ها :
• شماره کانادا : {int(prices[1]):,} تومان
• شماره آمریکا : {int(prices[0]):,} تومان
• شماره سشن دار : {int(prices[2]):,} تومان''', quote = True, reply_markup = ReplyKeyboardMarkup([[f'نشست دار {prices[2]} تومان 🔐'], [f'آمریکا {prices[0]} تومان 🇺🇸', f'کانادا {prices[1]} تومان 🇨🇦'], ['🔙 بازگشت']], resize_keyboard = True))

    except Exception as er_BuyNumber :
        async with pool.acquire() as db :
            await db.rollback()
        print(f'BuyNumber Error : {er_BuyNumber}')

#-------------------------------------------------------------#

async def AdminPanel(Client, message, pool) :

    try :

        chat_id = message.chat.id

        async with pool.acquire() as db :
            async with db.cursor() as cursor :

                await cursor.execute('SELECT step FROM users WHERE user_id = %s' %chat_id)
                data = await cursor.fetchone()

        if chat_id in admin and data[0] == 'HOME' :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    chg = ('ADMIN PANEL', chat_id)
                    await cursor.execute('UPDATE users SET step = %s WHERE user_id = %s', chg)
                    await db.commit()

                    await message.reply(f'''✅ به پنل ادمین خوش آمدید.
◀️ برای شروع یکی از گزینه های زیر را انتخاب کنید :''', quote = True, reply_markup = Admin_Keyboard)

    except Exception as er_AdminPanel :
        print(f'AdminPanel Error : {er_AdminPanel}')

#-------------------------------------------------------------#

async def AdminPanelBack(Client, message, pool) :

    try :

        chat_id = message.chat.id

        async with pool.acquire() as db :
            async with db.cursor() as cursor :

                await cursor.execute('SELECT step FROM users WHERE user_id = %s' %chat_id)
                data = await cursor.fetchone()

        if chat_id in admin and data[0] in ['BAN USER', 'UNBAN USER', 'SUB BALANCE', 'ADD BALANCE', 'DEL NUMBERS', 'ADD NUMBERS', 'SET PRICE', 'USER INFO'] :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    chg = ('ADMIN PANEL', chat_id)
                    await cursor.execute('UPDATE users SET step = %s WHERE user_id = %s', chg)
                    await db.commit()

                    await message.reply(f'''✅ به پنل ادمین خوش آمدید.
◀️ برای شروع یکی از گزینه های زیر را انتخاب کنید :''', quote = True, reply_markup = Admin_Keyboard)

    except Exception as er_AdminPanelBack :
        print(f'AdminPanelBack Error : {er_AdminPanelBack}')

#-------------------------------------------------------------#

async def BotStatus(Client, message, pool) :

    try :

        chat_id = message.chat.id

        async with pool.acquire() as db :
            async with db.cursor() as cursor :

                await cursor.execute('SELECT step FROM users WHERE user_id = %s' %chat_id)
                data = await cursor.fetchone()

        if chat_id in admin and data[0] == 'ADMIN PANEL' :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    await cursor.execute('SELECT user_id FROM users')
                    users = await cursor.fetchall()

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    await cursor.execute('SELECT * FROM usa')
                    usa = await cursor.fetchall()
                    await cursor.execute('SELECT * FROM canada')
                    canada = await cursor.fetchall()
                    await cursor.execute('SELECT * FROM session')
                    session = await cursor.fetchall()

                    await message.reply(f'''📊 وضعیت ربات به صورت زیر می باشد :

👥 تعداد اعضای ربات : <code>{len(users)}</code> نفر

🔋 تعداد شماره های موجود در ربات :

🇺🇸 America : <code>{len(usa) - 1}</code>
🇨🇦 Canada : <code>{len(canada) - 1}</code>
🔐 Session : <code>{len(session) - 1}</code>''', quote = True)

    except Exception as er_BotStatus :
        print(f'BotStatus Error : {er_BotStatus}')

#-------------------------------------------------------------#

async def BanUser(Client, message, pool) :

    try :

        chat_id = message.chat.id

        async with pool.acquire() as db :
            async with db.cursor() as cursor :

                await cursor.execute('SELECT step FROM users WHERE user_id = %s' %chat_id)
                data = await cursor.fetchone()

        if chat_id in admin and data[0] == 'ADMIN PANEL' :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    chg = ('BAN USER', chat_id)
                    await cursor.execute('UPDATE users SET step = %s WHERE user_id = %s', chg)
                    await db.commit()

                    await message.reply('◀️ شناسه کاربری شخص مورد نظر را ارسال کنید :', quote = True, reply_markup = ReplyKeyboardMarkup([['🔙 بازگشت به پنل ادمین']], resize_keyboard = True))

    except Exception as er_BanUser :
        async with pool.acquire() as db :
            await db.rollback()
        print(f'BanUser Error : {er_BanUser}')

#-------------------------------------------------------------#

async def UnbanUser(Client, message, pool) :

    try :

        chat_id = message.chat.id

        async with pool.acquire() as db :
            async with db.cursor() as cursor :

                await cursor.execute('SELECT step FROM users WHERE user_id = %s' %chat_id)
                data = await cursor.fetchone()

        if chat_id in admin and data[0] == 'ADMIN PANEL' :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    chg = ('UNBAN USER', chat_id)
                    await cursor.execute('UPDATE users SET step = %s WHERE user_id = %s', chg)
                    await db.commit()

                    await message.reply('◀️ شناسه کاربری شخص مورد نظر را ارسال کنید :', quote = True, reply_markup = ReplyKeyboardMarkup([['🔙 بازگشت به پنل ادمین']], resize_keyboard = True))

    except Exception as er_UnbanUser :
        async with pool.acquire() as db :
            await db.rollback()
        print(f'UnbanUser Error : {er_UnbanUser}')

#-------------------------------------------------------------#

async def SubBalance(Client, message, pool) :

    try :

        chat_id = message.chat.id

        async with pool.acquire() as db :
            async with db.cursor() as cursor :

                await cursor.execute('SELECT step FROM users WHERE user_id = %s' %chat_id)
                data = await cursor.fetchone()

        if chat_id in admin and data[0] == 'ADMIN PANEL' :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    chg = ('SUB BALANCE', chat_id)
                    await cursor.execute('UPDATE users SET step = %s WHERE user_id = %s', chg)
                    await db.commit()

                    await message.reply(f'''◀️ شناسه کاربری شخص مورد نظر را به صورت فرمت زیر ارسال کنید :

[ <code>104955254 10000</code> ]''', quote = True, reply_markup = ReplyKeyboardMarkup([['🔙 بازگشت به پنل ادمین']], resize_keyboard = True))

    except Exception as er_SubBalance :
        async with pool.acquire() as db :
            await db.rollback()
        print(f'SubBalance Error : {er_SubBalance}')

#-------------------------------------------------------------#

async def AddBalance(Client, message, pool) :

    try :

        chat_id = message.chat.id

        async with pool.acquire() as db :
            async with db.cursor() as cursor :

                await cursor.execute('SELECT step FROM users WHERE user_id = %s' %chat_id)
                data = await cursor.fetchone()

        if chat_id in admin and data[0] == 'ADMIN PANEL' :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    chg = ('ADD BALANCE', chat_id)
                    await cursor.execute('UPDATE users SET step = %s WHERE user_id = %s', chg)
                    await db.commit()

                    await message.reply(f'''◀️ شناسه کاربری شخص مورد نظر را به صورت فرمت زیر ارسال کنید :

[ <code>104955254 10000</code> ]''', quote = True, reply_markup = ReplyKeyboardMarkup([['🔙 بازگشت به پنل ادمین']], resize_keyboard = True))

    except Exception as er_AddBalance :
        async with pool.acquire() as db :
            await db.rollback()
        print(f'AddBalance Error : {er_AddBalance}')

#-------------------------------------------------------------#

async def DelNumbers(Client, message, pool) :

    try :

        chat_id = message.chat.id

        async with pool.acquire() as db :
            async with db.cursor() as cursor :

                await cursor.execute('SELECT step FROM users WHERE user_id = %s' %chat_id)
                data = await cursor.fetchone()

        if chat_id in admin and data[0] == 'ADMIN PANEL' :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    chg = ('DEL NUMBERS', chat_id)
                    await cursor.execute('UPDATE users SET step = %s WHERE user_id = %s', chg)
                    await db.commit()

                    await message.reply('''◀️ برای حذف شماره ها کافیست کشور مورد نظر را با فرمت زیر ارسال کنید :

[ <code>del usa</code> | <code>del canada</code> | <code>del session</code>]''', quote = True, reply_markup = ReplyKeyboardMarkup([['🔙 بازگشت به پنل ادمین']], resize_keyboard = True))

    except Exception as er_DelNumbers :
        async with pool.acquire() as db :
            await db.rollback()
        print(f'DelNumbers Error : {er_DelNumbers}')

#-------------------------------------------------------------#

async def AddNumbers(Client, message, pool) :

    try :

        chat_id = message.chat.id

        async with pool.acquire() as db :
            async with db.cursor() as cursor :

                await cursor.execute('SELECT step FROM users WHERE user_id = %s' %chat_id)
                data = await cursor.fetchone()

        if chat_id in admin and data[0] == 'ADMIN PANEL' :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    chg = ('ADD NUMBERS', chat_id)
                    await cursor.execute('UPDATE users SET step = %s WHERE user_id = %s', chg)
                    await db.commit()

                    await message.reply('◀️ شماره هارا به صورت یک فایل txt ارسال کنید :', quote = True, reply_markup = ReplyKeyboardMarkup([['🔙 بازگشت به پنل ادمین']], resize_keyboard = True))

    except Exception as er_AddNumbers :
        async with pool.acquire() as db :
            await db.rollback()
        print(f'Add Numbers Error : {er_AddNumbers}')

#-------------------------------------------------------------#

async def SetPrice(Client, message, pool) :

    try :

        chat_id = message.chat.id

        async with pool.acquire() as db :
            async with db.cursor() as cursor :

                await cursor.execute('SELECT step FROM users WHERE user_id = %s' %chat_id)
                data = await cursor.fetchone()

        if chat_id in admin and data[0] == 'ADMIN PANEL' :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    chg = ('SET PRICE', chat_id)
                    await cursor.execute('UPDATE users SET step = %s WHERE user_id = %s', chg)
                    await db.commit()

                    await message.reply('''◀️ برای تعیین قیمت شماره ها یا قیمت دلار کافیست قیمت شماره یا دلار را به صورت فرمت زیر ارسال کنید :

[ <code>usa_price 6000</code> | <code>canada_price 6000</code> | <code>session_price 3000</code>]''', quote = True, reply_markup = ReplyKeyboardMarkup([['🔙 بازگشت به پنل ادمین']], resize_keyboard = True))

    except Exception as er_SetPrice :
        async with pool.acquire() as db :
            await db.rollback()
        print(f'SetPrice Error : {er_SetPrice}')

#-------------------------------------------------------------#

async def UserInfo(Client, message, pool) :

    try :

        chat_id = message.chat.id

        async with pool.acquire() as db :
            async with db.cursor() as cursor :

                await cursor.execute('SELECT step FROM users WHERE user_id = %s' %chat_id)
                data = await cursor.fetchone()

        if chat_id in admin and data[0] == 'ADMIN PANEL' :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    chg = ('USER INFO', chat_id)
                    await cursor.execute('UPDATE users SET step = %s WHERE user_id = %s', chg)
                    await db.commit()

                    await message.reply('◀️ شناسه کاربری شخص مورد نظر را ارسال کنید :', quote = True, reply_markup = ReplyKeyboardMarkup([['🔙 بازگشت به پنل ادمین']], resize_keyboard = True))

    except Exception as er_UserInfo :
        async with pool.acquire() as db :
            await db.rollback()
        print(f'UserInfo Error : {er_UserInfo}')

#-------------------------------------------------------------#

Message_Mapping = {

    '/start' : Start,
    '🔙 بازگشت' : Back,
    '🔙 بازگشت به پنل ادمین' : AdminPanelBack,
    'p' : AdminPanel,
    'P' : AdminPanel,
    '📊 وضعیت ربات' : BotStatus,
    '⛔️ مسدود کردن' : BanUser,
    '✅ رفع مسدودی' : UnbanUser,
    '📈 کاهش موجودی' : SubBalance,
    '📉 افزودن موجودی' : AddBalance,
    '✖️ حذف شماره ها' : DelNumbers,
    '➕ افزودن شماره' : AddNumbers,
    '💵 تنظیم قیمت' : SetPrice,
    '👤 اطلاعات کاربر' : UserInfo,
    '🧾 قوانین و راهنما' : RulesGuide,
    '⚙️ حساب کاربری' : UserAccount,
    '💸 افزایش موجودی' : Support,
    '📞 خرید شماره مجازی' : BuyNumber

}

#--------------------------------------------------------------------------------------------------------------------#

async def StepBuynumber(Clinet, message, pool) :

    try :

        chat_id = message.chat.id

        async with pool.acquire() as db :
            async with db.cursor() as cursor :

                await cursor.execute('SELECT wallet, num_limit FROM users WHERE user_id = %s' %chat_id)
                data = await cursor.fetchone()

                await cursor.execute('SELECT * FROM information')
                prices = await cursor.fetchone()

                await cursor.execute('SELECT * FROM session')
                session = await cursor.fetchall()
                await cursor.execute('SELECT * FROM canada')
                canada = await cursor.fetchall()
                await cursor.execute('SELECT * FROM usa')
                usa = await cursor.fetchall()

        #-----------------------------#

        if data[1] < 100 and len(session) > 1 and message.text == f'نشست دار {prices[2]} تومان 🔐' and data[0] >= prices[2] :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    chg = (prices[2], chat_id)
                    await cursor.execute('UPDATE users SET wallet = wallet - %s, num = num + 1, num_limit = num_limit + 1 WHERE user_id = %s', chg)
                    number_index = random.randint(1, len(session) - 1)
                    await cursor.execute('DELETE FROM session WHERE number = %s' %session[number_index])
                    chg = (time.time(), session[number_index])
                    await cursor.execute('UPDATE numbers_info SET timer = %s, bool = 0 WHERE number = %s', chg)
                    await db.commit()

                    await message.reply(f'''🔐 <code>{session[number_index][0]}</code>
📊 وضعیت : ✅ #فعال
⏱ زمان انقضا : <code>900</code> ثانیه''', reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('🔢 دریافت کد', callback_data = f'S {session[number_index][0]}'), InlineKeyboardButton('❗️ لغو خرید', callback_data = f'CS {session[number_index][0]}')]]))

        #-----------------------------#

        if data[1] < 100 and len(canada) > 1 and message.text == f'کانادا {prices[1]} تومان 🇨🇦' and data[0] >= prices[1] :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    chg = (prices[1], chat_id)
                    await cursor.execute('UPDATE users SET wallet = wallet - %s, num = num + 1, num_limit = num_limit + 1 WHERE user_id = %s', chg)
                    number_index = random.randint(1, len(canada) - 1)
                    await cursor.execute('DELETE FROM canada WHERE number = %s' %canada[number_index])
                    chg = (time.time(), canada[number_index])
                    await cursor.execute('UPDATE numbers_info SET timer = %s, bool = 0 WHERE number = %s', chg)
                    await db.commit()

                    await message.reply(f'''🇨🇦 <code>{canada[number_index][0]}</code>
📊 وضعیت : ✅ #فعال
⏱ زمان انقضا : <code>900</code> ثانیه''', reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('🔢 دریافت کد', callback_data = f'C {canada[number_index][0]}'), InlineKeyboardButton('❗️ لغو خرید', callback_data = f'CC {canada[number_index][0]}')]]))

        #-----------------------------#

        if data[1] < 100 and len(usa) > 1 and message.text == f'آمریکا {prices[0]} تومان 🇺🇸' and data[0] >= prices[0] :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    chg = (prices[0], chat_id)
                    await cursor.execute('UPDATE users SET wallet = wallet - %s, num = num + 1, num_limit = num_limit + 1 WHERE user_id = %s', chg)
                    number_index = random.randint(1, len(usa) - 1)
                    await cursor.execute('DELETE FROM usa WHERE number = %s' %usa[number_index])
                    chg = (time.time(), usa[number_index])
                    await cursor.execute('UPDATE numbers_info SET timer = %s, bool = 0 WHERE number = %s', chg)
                    await db.commit()

                    await message.reply(f'''🇺🇸 <code>{usa[number_index][0]}</code>
📊 وضعیت : ✅ #فعال
⏱ زمان انقضا : <code>900</code> ثانیه''', reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('🔢 دریافت کد', callback_data = f'U {usa[number_index][0]}'), InlineKeyboardButton('❗️ لغو خرید', callback_data = f'CU {usa[number_index][0]}')]]))

        elif data[1] >= 100 :

            await message.reply(f'❗️ شما درحال حاضر {data[1]} شماره فعال دارید!', quote = True)

        elif message.text == f'نشست دار {prices[2]} تومان 🔐' and len(session) == 1 or message.text == f'کانادا {prices[1]} تومان 🇨🇦' and len(canada) == 1 or message.text == f'آمریکا {prices[0]} تومان 🇺🇸' and len(usa) == 1 :

            await message.reply('❗️ شماره ای در ربات موجود نمی باشد!', quote = True)

        elif message.text == f'نشست دار {prices[2]} تومان 🔐' and data[0] < prices[2] or message.text == f'کانادا {prices[1]} تومان 🇨🇦' and data[0] < prices[1] or message.text == f'آمریکا {prices[0]} تومان 🇺🇸' and data[0] < prices[0] :

            await message.reply('❗️ موجودی شما کافی نمی باشد!', quote = True)

    except Exception as er_StepBuynumber :
        async with pool.acquire() as db :
            await db.rollback()
        print(f'StepBuynumber Error : {er_StepBuynumber}')

#-------------------------------------------------------------#

async def StepBanUser(Client, message, pool) :

    try :

        async with pool.acquire() as db :
            async with db.cursor() as cursor :

                await cursor.execute('SELECT user_id FROM users')
                users = await cursor.fetchall()

        if message.text.isdigit() is True and (int(message.text),) in users :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    chg = ('BAN', int(message.text))
                    await cursor.execute('UPDATE users SET step = %s WHERE user_id = %s', chg)
                    await db.commit()

                    await bot.send_message(int(message.text), '⛔️ کاربر گرامی شما از ربات مسدود شدید!', reply_markup = ReplyKeyboardRemove())
                    await message.reply(f'⛔️ کاربر <code>{message.text}</code> با موفقیت از ربات مسدود شد!', quote = True)

        elif message.text.isdigit() is False :

            await message.reply('❗️ لطفا به صورت عدد وارد کنید!', quote = True)

        elif (int(message.text),) not in users :

            await message.reply('❗️ شناسه کاربری اشتباه است!', quote = True)

    except Exception as er_StepBanUser :
        async with pool.acquire() as db :
            await db.rollback()
        print(f'StepBanUser Error : {er_StepBanUser}')

#-------------------------------------------------------------#

async def StepUnbanUser(Client, message, pool) :

    try :

        async with pool.acquire() as db :
            async with db.cursor() as cursor :

                await cursor.execute('SELECT user_id FROM users')
                users = await cursor.fetchall()

        if message.text.isdigit() is True and (int(message.text),) in users :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    chg = ('HOME', int(message.text))
                    await cursor.execute('UPDATE users SET step = %s WHERE user_id = %s', chg)
                    await db.commit()

                    await bot.send_message(int(message.text), '✅ کاربر گرامی شما از ربات رفع مسدود شدید.', reply_markup = Main_Keyboard)
                    await message.reply(f'✅ کاربر <code>{message.text}</code> با موفقیت از ربات رفع مسدود شد.', quote = True)

        elif message.text.isdigit() is False :

            await message.reply('❗️ لطفا به صورت عدد وارد کنید!', quote = True)

        elif (int(message.text),) not in users :

            await message.reply('❗️ شناسه کاربری اشتباه است!', quote = True)

    except Exception as er_StepUnbanUser :
        async with pool.acquire() as db :
            await db.rollback()
        print(f'StepUnbanUser Error : {er_StepUnbanUser}')

#-------------------------------------------------------------#

async def StepSubbalance(Client, message, pool) :

    try :

        async with pool.acquire() as db :
            async with db.cursor() as cursor :

                await cursor.execute('SELECT user_id FROM users')
                users = await cursor.fetchall()

        if len(message.text.split()) == 2 and (int(message.text.split()[0]),) in users and message.text.split()[1].isdigit() is True :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    chg = (int(message.text.split()[1]), int(message.text.split()[0]))
                    await cursor.execute('UPDATE users SET wallet = wallet - %s WHERE user_id = %s', chg)
                    await db.commit()

                    await bot.send_message(int(message.text.split()[0]), f'📈 کاربر گرامی از حساب شما به مقدار <code>{int(message.text.split()[1]):,}</code> تومان کسر شد.')
                    await message.reply(f'📈 از حساب کاربری <code>{message.text.split()[0]}</code> به مقدار <code>{int(message.text.split()[1]):,}</code> تومان با موفقیت کسر شد.', quote = True)

        elif len(message.text.split()) != 2 :

            await message.reply('❗️ فرمت ارسال شده اشتباه است!', quote = True)

        elif (int(message.text.split()[0]),) not in users :

            await message.reply('❗️ شناسه کاربری اشتباه است!', quote = True)

        elif message.text.split()[1].isdigit() is False :

            await message.reply('❗️ لطفا به صورت عدد وارد کنید!', quote = True)

    except Exception as er_StepSubbalance :
        async with pool.acquire() as db :
            await db.rollback()
        print(f'StepSubbalance Error : {er_StepSubbalance}')

#-------------------------------------------------------------#

async def StepAddbalance(Client, message, pool) :

    try :

        async with pool.acquire() as db :
            async with db.cursor() as cursor :

                await cursor.execute('SELECT user_id FROM users')
                users = await cursor.fetchall()

        if len(message.text.split()) == 2 and (int(message.text.split()[0]),) in users and message.text.split()[1].isdigit() is True :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    chg = (int(message.text.split()[1]), int(message.text.split()[0]))
                    await cursor.execute('UPDATE users SET wallet = wallet + %s WHERE user_id = %s', chg)
                    await db.commit()

                    await bot.send_message(int(message.text.split()[0]), f'📉 کاربر گرامی حساب شما به مقدار <code>{int(message.text.split()[1]):,}</code> تومان شارژ شد.')
                    await message.reply(f'📉 حساب کاربری <code>{message.text.split()[0]}</code> به مقدار <code>{int(message.text.split()[1]):,}</code> تومان با موفقیت شارژ شد.', quote = True)

        elif len(message.text.split()) != 2 :

            await message.reply('❗️ فرمت ارسال شده اشتباه است!', quote = True)

        elif (int(message.text.split()[0]),) not in users :

            await message.reply('❗️ شناسه کاربری اشتباه است!', quote = True)

        elif message.text.split()[1].isdigit() is False :

            await message.reply('❗️ لطفا به صورت عدد وارد کنید!', quote = True)

    except Exception as er_StepAddbalance :
        async with pool.acquire() as db :
            await db.rollback()
        print(f'StepAddbalance Error : {er_StepAddbalance}')

#-------------------------------------------------------------#

async def StepDelnumbers(Client, message, pool) :

    try :

        if len(message.text.split()) == 2 and message.text.split()[0] == 'del' and message.text.split()[1] in ['usa', 'canada', 'session'] :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    await cursor.execute('DELETE FROM %s WHERE number > 0' %message.text.split()[1])
                    await db.commit()

                    await message.reply(f'✅ شماره های {message.text.split()[1]} با موفقیت حذف شدند.', quote = True)

        elif len(message.text.split()) != 2 :

            await message.reply('❗️ فرمت ارسال شده اشتباه است!', quote = True)

        elif message.text.split()[0] != 'del' :

            await message.reply('❗️ فرمت ارسال شده اشتباه است!', quote = True)

        elif message.text.split()[1] not in ['usa', 'canada', 'session'] :

            await message.reply('❗️ فرمت ارسال شده اشتباه است!', quote = True)

    except Exception as er_StepDelnumbers :
        async with pool.acquire() as db :
            await db.rollback()
        print(f'StepDelnumbers Error : {er_StepDelnumbers}')

#-------------------------------------------------------------#

async def StepAddnumbers(Client, message, pool) :

    try :

        if message.document and str(message.caption) in ['usa', 'canada', 'session'] :

            mess = await message.reply('♻️ درحال پردازش . . .', quote = True)

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    await cursor.execute('SELECT * FROM %s' %message.caption)
                    nums_list = await cursor.fetchall()

            file = await bot.download_media(message.document.file_id)
            with open(f'{file}', 'r') as ff :
                txt = ff.read()

            text = txt.split()
            nl = []
            count = 0

            for n in list(nums_list) :

                nl.append(n[0])

            for i in text:

                if int(i.split('*')[0]) not in nl :

                    async with pool.acquire() as db :
                        async with db.cursor() as cursor :

                            val = (i.split('*')[0], i.split('*')[1], 0, 0, 0, 0)
                            await cursor.execute('INSERT INTO numbers_info (number, api, timer, status, cancel_count, bool) VALUES (%s, %s, %s, %s, %s, %s)', val)
                            table_name = message.caption
                            await cursor.execute('INSERT INTO {} (number) VALUES (%s)'.format(table_name) %i.split('*')[0])
                            await db.commit()

                            count += 1

            await mess.edit_text(f'✅ به تعداد {count} شماره به ربات افزوده شد!')

        elif not message.document :

            await message.reply('❗️ لطفا فقط فایل ارسال کنید!', quote = True)

        elif str(message.caption) not in ['usa', 'canada', 'session'] :

            await message.reply('❗️ کپشن به درستی وارد نشده است!', quote = True)

    except Exception as er_StepAddnumbers :
        async with pool.acquire() as db :
            await db.rollback()
        print(f'StepAddnumbers Error : {er_StepAddnumbers}')

#-------------------------------------------------------------#

async def StepSetprice(Client, message, pool) :

    try :

        if len(message.text.split()) == 2 and message.text.split()[0] in ['usa_price', 'canada_price', 'session_price'] and message.text.split()[1].isdigit() is True :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    field = message.text.split()[0]
                    await cursor.execute('UPDATE information SET {} = %s'.format(field) %int(message.text.split()[1]))
                    await db.commit()

                    await message.reply(f'✅ قیمت {message.text.split()[0]} با موفقیت به {message.text.split()[1]} اپدیت شد!', quote = True)

        elif len(message.text.split()) != 2 :

            await message.reply('❗️ فرمت ارسال شده اشتباه است!', quote = True)

        elif message.text.split()[0] not in ['usa_price', 'canada_price', 'session_price'] :

            await message.reply('❗️ فرمت ارسال شده اشتباه است!', quote = True)

        elif message.text.split()[1].isdigit() is False :

            await message.reply('❗️ لطفا به صورت عدد وارد کنید!', quote = True)

    except Exception as er_StepSetprice :
        async with pool.acquire() as db :
            await db.rollback()
        print(f'StepSetprice Error : {er_StepSetprice}')

#-------------------------------------------------------------#

async def StepUserinfo(Client, message, pool) :

    try :

        async with pool.acquire() as db :
            async with db.cursor() as cursor :

                await cursor.execute('SELECT user_id FROM users')
                users = await cursor.fetchall()

        if message.text.isdigit() is True and (int(message.text),) in users :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    await cursor.execute('SELECT wallet, num FROM users WHERE user_id = %s' %message.text)
                    info = await cursor.fetchone()

                    await message.reply(f'''👤 اطلاعات کاربر <code>{message.text}</code> به صورت زیر می باشد :

💳 Wallet : <code>{int(str(info[0])):,}</code> تومان
🔢 Num : <code>{info[1]}</code> شماره''', quote = True)

        elif message.text.isdigit() is False :

            await message.reply('❗️ لطفا به صورت عدد وارد کنید!', quote = True)

        elif (int(message.text),) not in users :

            await message.reply('❗️ شناسه کاربری اشتباه است!', quote = True)

    except Exception as er_StepUserinfo :
        async with pool.acquire() as db :
            await db.rollback()
        print(f'StepSetprice Error : {er_StepUserinfo}')

#-------------------------------------------------------------#

Step_Mapping = {

    'BUY NUMBER' : StepBuynumber,
    'BAN USER' : StepBanUser,
    'UNBAN USER' : StepUnbanUser,
    'SUB BALANCE' : StepSubbalance,
    'ADD BALANCE' : StepAddbalance,
    'DEL NUMBERS' : StepDelnumbers,
    'ADD NUMBERS' : StepAddnumbers,
    'SET PRICE' : StepSetprice,
    'USER INFO' : StepUserinfo

}

#--------------------------------------------------------------------------------------------------------------------#

async def GetCode_Session(Client, CallBackQuery, pool) :

    try :

        chat_id = CallBackQuery.from_user.id
        callback = CallBackQuery.data

        async with pool.acquire() as db :
            async with db.cursor() as cursor :

                await cursor.execute('SELECT api, timer, status, bool FROM numbers_info WHERE number = %s' %callback.split()[1])
                info = await cursor.fetchone()

        async with httpx.AsyncClient() as req :
            response = await req.get(f'{info[0]}')
            code = re.findall('\d{5,}', response.text)

        if not code and time.time() - info[1] < 900 and info[2] == 0 :

            await CallBackQuery.message.edit_text(f'''🔐 <code>{callback.split()[1]}</code>
📊 وضعیت : ✅ #فعال
⏱ زمان انقضا : <code>{900 - int(time.time() - info[1])}</code> ثانیه''', reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('🔢 دریافت کد', callback_data = f'S {callback.split()[1]}'), InlineKeyboardButton('❗️ لغو خرید', callback_data = f'CS {callback.split()[1]}')]]))

        if info[3] == 0 and code and time.time() - info[1] < 900 and info[2] == 0 :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    await cursor.execute('UPDATE numbers_info SET status = 1, bool = 1 WHERE number = %s' %callback.split()[1])
                    await cursor.execute('UPDATE users SET num_limit = num_limit - 1  WHERE user_id = %s' %chat_id)
                    await db.commit()

                    await CallBackQuery.message.edit_text(f'''🔐 <code>{callback.split()[1]}</code>
🔑 <code>{code[0]}</code>
📊 وضعیت : ✅ #فعال
⏱ زمان انقضا : <code>{900 - int(time.time() - info[1])}</code> ثانیه''', reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('🔢 دریافت مجدد کد', callback_data = f'S {callback.split()[1]}')]]))

        elif not code and time.time() - info[1] < 900 and info[2] == 1 :

            await CallBackQuery.message.edit_text(f'''🔐 <code>{callback.split()[1]}</code>
📊 وضعیت : ✅ #فعال
⏱ زمان انقضا : <code>{900 - int(time.time() - info[1])}</code> ثانیه''', reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('🔢 دریافت مجدد کد', callback_data = f'S {callback.split()[1]}')]]))

        elif code and time.time() - info[1] < 900 and info[2] == 1 :

            await CallBackQuery.message.edit_text(f'''🔐 <code>{callback.split()[1]}</code>
🔑 <code>{code[0]}</code>
📊 وضعیت : ✅ #فعال
⏱ زمان انقضا : <code>{900 - int(time.time() - info[1])}</code> ثانیه''', reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('🔢 دریافت مجدد کد', callback_data = f'S {callback.split()[1]}')]]))

        elif info[3] == 0 and time.time() - info[1] > 900 :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    await cursor.execute('UPDATE numbers_info SET bool = 1 WHERE number = %s' %callback.split()[1])
                    await db.commit()

            if info[2] == 0 :

                async with pool.acquire() as db :
                    async with db.cursor() as cursor :

                        await cursor.execute('UPDATE users SET num_limit = num_limit - 1 WHERE user_id = %s' %chat_id)
                        await db.commit()

                        await CallBackQuery.message.edit_text(f'''🔐 <s>{callback.split()[1]}</s>
📊 وضعیت : ❗️ #منقصی
⏱ زمان انقضا : <code>0</code> ثانیه''')

            else :

                await CallBackQuery.message.edit_text(f'''🔐 <s>{callback.split()[1]}</s>
📊 وضعیت : ❗️ #منقصی
⏱ زمان انقضا : <code>0</code> ثانیه''')

    except Exception as er_GetCode_Session :
        async with pool.acquire() as db :
            await db.rollback()
        print(f'GetCode_Session Error : {er_GetCode_Session}')

#-------------------------------------------------------------#

async def CancelSession(Client, CallBackQuery, pool) :

    try :

        chat_id = CallBackQuery.from_user.id
        callback = CallBackQuery.data

        async with pool.acquire() as db :
            async with db.cursor() as cursor :

                await cursor.execute('SELECT session_price FROM information')
                price = await cursor.fetchone()

                await cursor.execute('SELECT api, timer, status, cancel_count, bool FROM numbers_info WHERE number = %s' %callback.split()[1])
                info = await cursor.fetchone()

        if info[4] == 0 and info[2] == 0 and time.time() - info[1] > 10 and time.time() - info[1] < 900 :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    await cursor.execute('UPDATE numbers_info SET bool = 1 WHERE number = %s' %callback.split()[1])
                    await db.commit()

            if info[3] == 0 :

                async with pool.acquire() as db :
                    async with db.cursor() as cursor :

                        chg = (price[0], chat_id)
                        await bot.send_message(gpdel, f"{number}")
                        await cursor.execute('UPDATE users SET wallet = wallet + %s, num = num - 1, num_limit = num_limit - 1 WHERE user_id = %s', chg)
                        await cursor.execute('DELETE FROM session WHERE number=%s', CallBackQuery.data.split()[1])
                        await db.commit()

                        await CallBackQuery.message.delete()


        elif time.time() - info[1] < 10 :

            await CallBackQuery.answer(text = f'''❗️ امکان لغو خرید وجود ندارد!

◀️ لطفا{10 - int(time.time() - info[1])} ثانیه دیگر امتحان کنید.''', show_alert = True)

        elif info[4] == 0 and time.time() - info[1] > 900 :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    await cursor.execute('UPDATE numbers_info SET bool = 1 WHERE number = %s' %callback.split()[1])
                    await db.commit()

            if info[2] == 0 :

                async with pool.acquire() as db :
                    async with db.cursor() as cursor :

                        await cursor.execute('UPDATE users SET num_limit = num_limit - 1 WHERE user_id = %s' % chat_id)
                        await db.commit()

                        await CallBackQuery.message.edit_text(f'''🔐 <s>{callback.split()[1]}</s>
📊 وضعیت : ❗️ #منقصی
⏱ زمان انقضا : <code>0</code> ثانیه''')

            else :

                await CallBackQuery.message.edit_text(f'''🔐 <s>{callback.split()[1]}</s>
📊 وضعیت : ❗️ #منقصی
⏱ زمان انقضا : <code>0</code> ثانیه''')

    except Exception as er_CancelSession :
        async with pool.acquire() as db :
            await db.rollback()
        print(f'CancelSession Error : {er_CancelSession}')

#-------------------------------------------------------------#

async def GetCode_Canada(Client, CallBackQuery, pool) :

    try :

        chat_id = CallBackQuery.from_user.id
        callback = CallBackQuery.data

        async with pool.acquire() as db :
            async with db.cursor() as cursor :

                await cursor.execute('SELECT api, timer, status, bool FROM numbers_info WHERE number = %s' %callback.split()[1])
                info = await cursor.fetchone()

        async with httpx.AsyncClient() as req :
            response = await req.get(f'{info[0]}')
            code = re.findall('\d{5,}', response.text)

        if not code and time.time() - info[1] < 900 and info[2] == 0 :

            await CallBackQuery.message.edit_text(f'''🇨🇦 <code>{callback.split()[1]}</code>
📊 وضعیت : ✅ #فعال
⏱ زمان انقضا : <code>{900 - int(time.time() - info[1])}</code> ثانیه''', reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('🔢 دریافت کد', callback_data = f'C {callback.split()[1]}'), InlineKeyboardButton('❗️ لغو خرید', callback_data = f'CC {callback.split()[1]}')]]))

        if info[3] == 0 and code and time.time() - info[1] < 900 and info[2] == 0 :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    await cursor.execute('UPDATE numbers_info SET status = 1, bool = 1 WHERE number = %s' %callback.split()[1])
                    await cursor.execute('UPDATE users SET num_limit = num_limit - 1  WHERE user_id = %s' %chat_id)
                    await db.commit()

                    await CallBackQuery.message.edit_text(f'''🇨🇦 <code>{callback.split()[1]}</code>
🔑 <code>{code[0]}</code>
📊 وضعیت : ✅ #فعال
⏱ زمان انقضا : <code>{900 - int(time.time() - info[1])}</code> ثانیه''', reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('🔢 دریافت مجدد کد', callback_data = f'C {callback.split()[1]}')]]))

        elif not code and time.time() - info[1] < 900 and info[2] == 1 :

            await CallBackQuery.message.edit_text(f'''🇨🇦 <code>{callback.split()[1]}</code>
📊 وضعیت : ✅ #فعال
⏱ زمان انقضا : <code>{900 - int(time.time() - info[1])}</code> ثانیه''', reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('🔢 دریافت مجدد کد', callback_data = f'C {callback.split()[1]}')]]))

        elif code and time.time() - info[1] < 900 and info[2] == 1 :

            await CallBackQuery.message.edit_text(f'''🇨🇦 <code>{callback.split()[1]}</code>
🔑 <code>{code[0]}</code>
📊 وضعیت : ✅ #فعال
⏱ زمان انقضا : <code>{900 - int(time.time() - info[1])}</code> ثانیه''', reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('🔢 دریافت مجدد کد', callback_data = f'C {callback.split()[1]}')]]))

        elif info[3] == 0 and time.time() - info[1] > 900 :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    await cursor.execute('UPDATE numbers_info SET bool = 1 WHERE number = %s' %callback.split()[1])
                    await db.commit()

            if info[2] == 0 :

                async with pool.acquire() as db :
                    async with db.cursor() as cursor :

                        await cursor.execute('UPDATE users SET num_limit = num_limit - 1 WHERE user_id = %s' %chat_id)
                        await db.commit()

                        await CallBackQuery.message.edit_text(f'''🇨🇦 <s>{callback.split()[1]}</s>
📊 وضعیت : ❗️ #منقصی
⏱ زمان انقضا : <code>0</code> ثانیه''')

            else :

                await CallBackQuery.message.edit_text(f'''🇨🇦 <s>{callback.split()[1]}</s>
📊 وضعیت : ❗️ #منقصی
⏱ زمان انقضا : <code>0</code> ثانیه''')

    except Exception as er_GetCode_Canada :
        async with pool.acquire() as db :
            await db.rollback()
        print(f'GetCode_Canada Error : {er_GetCode_Canada}')

#-------------------------------------------------------------#

async def CancelCanada(Client, CallBackQuery, pool) :

    try :

        chat_id = CallBackQuery.from_user.id
        callback = CallBackQuery.data

        async with pool.acquire() as db :
            async with db.cursor() as cursor :

                await cursor.execute('SELECT canada_price FROM information')
                price = await cursor.fetchone()

                await cursor.execute('SELECT api, timer, status, cancel_count, bool FROM numbers_info WHERE number = %s' %callback.split()[1])
                info = await cursor.fetchone()

        if info[4] == 0 and info[2] == 0 and time.time() - info[1] > 10 and time.time() - info[1] < 900 :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    await cursor.execute('UPDATE numbers_info SET bool = 1 WHERE number = %s' %callback.split()[1])
                    await db.commit()

            if info[3] == 0 :

                async with pool.acquire() as db :
                    async with db.cursor() as cursor :

                        chg = (price[0], chat_id)
                        await bot.send_message(gpdel, f"{number}")
                        await cursor.execute('UPDATE users SET wallet = wallet + %s, num = num - 1, num_limit = num_limit - 1 WHERE user_id = %s', chg)
                        await cursor.execute('DELETE FROM canada WHERE number=%s', CallBackQuery.data.split()[1])
                        await db.commit()

                        await CallBackQuery.message.delete()


        elif time.time() - info[1] < 10 :

                await CallBackQuery.answer(text = f'''❗️ امکان لغو خرید وجود ندارد!

◀️ لطفا{10 - int(time.time() - info[1])} ثانیه دیگر امتحان کنید.''', show_alert = True)

        elif info[4] == 0 and time.time() - info[1] > 900 :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    await cursor.execute('UPDATE numbers_info SET bool = 1 WHERE number = %s' %callback.split()[1])
                    await db.commit()

            if info[2] == 0 :

                async with pool.acquire() as db :
                    async with db.cursor() as cursor :

                        await cursor.execute('UPDATE users SET num_limit = num_limit - 1 WHERE user_id = %s' %chat_id)
                        await db.commit()

                        await CallBackQuery.message.edit_text(f'''🔐 <s>{callback.split()[1]}</s>
📊 وضعیت : ❗️ #منقصی
⏱ زمان انقضا : <code>0</code> ثانیه''')

            else :

                await CallBackQuery.message.edit_text(f'''🔐 <s>{callback.split()[1]}</s>
📊 وضعیت : ❗️ #منقصی
⏱ زمان انقضا : <code>0</code> ثانیه''')

    except Exception as er_CancelCanada :
        async with pool.acquire() as db :
            await db.rollback()
        print(f'CancelCanada Error : {er_CancelCanada}')

#-------------------------------------------------------------#

async def GetCode_Usa(Client, CallBackQuery, pool) :

    try :

        chat_id = CallBackQuery.from_user.id
        callback = CallBackQuery.data

        async with pool.acquire() as db :
            async with db.cursor() as cursor :

                await cursor.execute('SELECT api, timer, status, bool FROM numbers_info WHERE number = %s' %callback.split()[1])
                info = await cursor.fetchone()

        async with httpx.AsyncClient() as req :
            response = await req.get(f'{info[0]}')
            code = re.findall('\d{5,}', response.text)

        if not code and time.time() - info[1] < 900 and info[2] == 0 :

            await CallBackQuery.message.edit_text(f'''🇺🇸 <code>{callback.split()[1]}</code>
📊 وضعیت : ✅ #فعال
⏱ زمان انقضا : <code>{900 - int(time.time() - info[1])}</code> ثانیه''', reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('🔢 دریافت کد', callback_data = f'U {callback.split()[1]}'), InlineKeyboardButton('❗️ لغو خرید', callback_data = f'CU {callback.split()[1]}')]]))

        if info[3] == 0 and code and time.time() - info[1] < 900 and info[2] == 0 :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    await cursor.execute('UPDATE numbers_info SET status = 1, bool = 1 WHERE number = %s' %callback.split()[1])
                    await cursor.execute('UPDATE users SET num_limit = num_limit - 1  WHERE user_id = %s' %chat_id)
                    await db.commit()

                    await CallBackQuery.message.edit_text(f'''🇺🇸 <code>{callback.split()[1]}</code>
🔑 <code>{code[0]}</code>
📊 وضعیت : ✅ #فعال
⏱ زمان انقضا : <code>{900 - int(time.time() - info[1])}</code> ثانیه''', reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('🔢 دریافت مجدد کد', callback_data = f'U {callback.split()[1]}')]]))

        elif not code and time.time() - info[1] < 900 and info[2] == 1 :

            await CallBackQuery.message.edit_text(f'''🇺🇸 <code>{callback.split()[1]}</code>
📊 وضعیت : ✅ #فعال
⏱ زمان انقضا : <code>{900 - int(time.time() - info[1])}</code> ثانیه''', reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('🔢 دریافت مجدد کد', callback_data = f'U {callback.split()[1]}')]]))

        elif code and time.time() - info[1] < 900 and info[2] == 1 :

            await CallBackQuery.message.edit_text(f'''🇺🇸 <code>{callback.split()[1]}</code>
🔑 <code>{code[0]}</code>
📊 وضعیت : ✅ #فعال
⏱ زمان انقضا : <code>{900 - int(time.time() - info[1])}</code> ثانیه''', reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('🔢 دریافت مجدد کد', callback_data = f'U {callback.split()[1]}')]]))

        elif info[3] == 0 and time.time() - info[1] > 900 :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    await cursor.execute('UPDATE numbers_info SET bool = 1 WHERE number = %s' %callback.split()[1])
                    await db.commit()

            if info[2] == 0 :

                async with pool.acquire() as db :
                    async with db.cursor() as cursor :

                        await cursor.execute('UPDATE users SET num_limit = num_limit - 1 WHERE user_id = %s' %chat_id)
                        await db.commit()

                        await CallBackQuery.message.edit_text(f'''🇺🇸 <s>{callback.split()[1]}</s>
📊 وضعیت : ❗️ #منقصی
⏱ زمان انقضا : <code>0</code> ثانیه''')

            else :

                await CallBackQuery.message.edit_text(f'''🇺🇸 <s>{callback.split()[1]}</s>
📊 وضعیت : ❗️ #منقصی
⏱ زمان انقضا : <code>0</code> ثانیه''')

    except Exception as er_GetCode_Usa :
        async with pool.acquire() as db :
            await db.rollback()
        print(f'GetCode_Usa Error : {er_GetCode_Usa}')

#-------------------------------------------------------------#

async def CancelUsa(Client, CallBackQuery, pool) :

    try :

        chat_id = CallBackQuery.from_user.id
        callback = CallBackQuery.data

        async with pool.acquire() as db :
            async with db.cursor() as cursor :

                await cursor.execute('SELECT usa_price FROM information')
                price = await cursor.fetchone()

                await cursor.execute('SELECT api, timer, status, cancel_count, bool FROM numbers_info WHERE number = %s' %callback.split()[1])
                info = await cursor.fetchone()

        if info[4] == 0 and info[2] == 0 and time.time() - info[1] > 10 and time.time() - info[1] < 900 :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    await cursor.execute('UPDATE numbers_info SET bool = 1 WHERE number = %s' %callback.split()[1])
                    await db.commit()

            if info[3] == 0 :

                async with pool.acquire() as db :
                    async with db.cursor() as cursor :

                        chg = (price[0], chat_id)
                        await bot.send_message(gpdel, f"{number}")
                        await cursor.execute('UPDATE users SET wallet = wallet + %s, num = num - 1, num_limit = num_limit - 1 WHERE user_id = %s', chg)
                        await cursor.execute('DELETE FROM usa WHERE number=%s', CallBackQuery.data.split()[1])
                        await db.commit()

                        await CallBackQuery.message.delete()


        elif time.time() - info[1] < 10 :

                await CallBackQuery.answer(text = f'''❗️ امکان لغو خرید وجود ندارد!

◀️ لطفا{10 - int(time.time() - info[1])} ثانیه دیگر امتحان کنید.''', show_alert = True)

        elif info[4] == 0 and time.time() - info[1] > 900 :

            async with pool.acquire() as db :
                async with db.cursor() as cursor :

                    await cursor.execute('UPDATE numbers_info SET bool = 1 WHERE number = %s' %callback.split()[1])
                    await db.commit()

            if info[2] == 0 :

                async with pool.acquire() as db :
                    async with db.cursor() as cursor :

                        await cursor.execute('UPDATE users SET num_limit = num_limit - 1 WHERE user_id = %s' %chat_id)
                        await db.commit()

                        await CallBackQuery.message.edit_text(f'''🔐 <s>{callback.split()[1]}</s>
📊 وضعیت : ❗️ #منقصی
⏱ زمان انقضا : <code>0</code> ثانیه''')

            else :

                await CallBackQuery.message.edit_text(f'''🔐 <s>{callback.split()[1]}</s>
📊 وضعیت : ❗️ #منقصی
⏱ زمان انقضا : <code>0</code> ثانیه''')

    except Exception as er_CancelUsa :
        async with pool.acquire() as db :
            await db.rollback()
        print(f'CancelUsa Error : {er_CancelUsa}')

#-------------------------------------------------------------#

Callback_Mapping = {

    'S' : GetCode_Session,
    'C' : GetCode_Canada,
    'U' : GetCode_Usa,
    'CS' : CancelSession,
    'CC' : CancelCanada,
    'CU' : CancelUsa

}

#--------------------------------------------------------------------------------------------------------------------#

@bot.on_message(filters.private)
async def MessageHandler(Client, message) :

    try :

        async with lock :

            pool = await aiomysql.create_pool(host = 'containers-us-west-86.railway.app', user = 'root', password = 'H3jdEzJgnnNhT8kSrvBF', db = 'railway', port = 6433)
            chat_id = message.chat.id

            async with pool.acquire() as db :
                async with db.cursor() as cursor :
                    await cursor.execute('SELECT step FROM users WHERE user_id = %s' %chat_id)
                    data = await cursor.fetchone()

            if bool(data) is False :

                async with pool.acquire() as db :
                    async with db.cursor() as cursor :
                        val = (chat_id, 'HOME', 0, 0, 0, 0)
                        await cursor.execute('INSERT INTO users (user_id, step, wallet, num, num_limit, msg) VALUES (%s, %s, %s, %s, %s, %s)', val)
                        await db.commit()
                        await cursor.execute('SELECT step FROM users WHERE user_id = %s' %chat_id)
                        data = await cursor.fetchone()

            if message.text in Message_Mapping :

                await Message_Mapping[message.text](Client, message, pool)

            elif data[0] in Step_Mapping :

                await Step_Mapping[data[0]](Client, message, pool)

    except Exception as er_MessageHandler :
        async with pool.acquire() as db :
            await db.rollback()
        print(f'MessageHandler Error : {er_MessageHandler}')

#--------------------------------------------------------------------------------------------------------------------#

@bot.on_callback_query()
async def CallbackHandler(Client, CallBackQuery) :

    try :

        async with lock :

            pool = await aiomysql.create_pool(host = 'containers-us-west-86.railway.app', user = 'root', password = 'H3jdEzJgnnNhT8kSrvBF', db = 'railway', port = 6433)
            callback = CallBackQuery.data

            if callback.split()[0] in Callback_Mapping :

                await Callback_Mapping[callback.split()[0]](Client, CallBackQuery, pool)

    except Exception as er_CallbackHandler :
        print(f'CallbackHandler Error : {er_CallbackHandler}')

















bot.run()













