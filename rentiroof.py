# -*- coding:utf-8 -*-

from re import U

from typing import Counter

from telegram import replymarkup

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

import telegram

from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, Update, ForceReply

import random

import logging

import random

import mysql.connector

import datetime as dt

import json

from telegram.replymarkup import ReplyMarkup


mydb = mysql.connector.connect(
    host="localhost", user="root", passwd="f123456f", database="Heimsucher")

cursor = mydb.cursor()


# postgres://jhzokfbhvvyzsa:3ff5c0f5fe3bdc4a154911344a601c46c59c4e80c7916d19a0b101596735aac9@ec2-107-20-24-247.compute-1.amazonaws.com:5432/d2bje9go7r7e4d

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


global code, code_2, L, L1, not_allowed, ma_list, loc_list

x = '@'

code = 'YN-10'

cnt_1 = 0

cnt_2 = 0

se = 0

# ------------------------

loc = None

major_slot = None

un_slot = None

sgn = None

loc_validator = None

maj_validator = None

slot = None

numer1 = 0

numer2 = 0

con = None

rand1 = None

# ------------------------

L = ['درخواست دهنده', 'انجام دهنده', 'فروشنده',
     'خریدار', 'پیشنهاد شغلی', 'مشخصات کاربر']

L1 = ['منوی اصلی', 'بازگشت', '@', 'ثبت آگهی جدید', 'ثبت آگهی رایگان']

not_allowed = ['کثافت', 'عوضی', 'هرزه', 'حرام زاده', 'پفیوز']

loc_list = ['تهران', 'اصفهان', 'فارس', 'خراسان رضوی', 'آذربایجان شرقی', 'آذربایجان غربی', 'اردبیل', 'البرز', 'ایلام', 'بوشهر', 'چهارمحال و بختیاری', 'خراسان جنوبی', 'خراسان رضوی', 'خراسان شمالی',
            'خوزستان', 'زنجان', 'سمنان', 'سیستان و بلوچستان', 'قزوین', 'قم', 'کردستان', 'کرمان', 'کرمانشاه', 'کهگیلویه و بویراحمد', 'گلستان', 'گیلان', 'لرستان', 'مازندران', 'مرکزی', 'هرمزگان', 'همدان', 'یزد']

ma_list = ['دروس عمومی', 'دروس پایه', 'مهندسی', 'هوافضا', 'معماری', 'عمران', 'مکانیک', 'کامپیوتر', 'برق', 'نساجی', 'پزشکی', 'شیمی', 'صنایع', 'فناوری اطلاعات', 'شهرسازی', 'نفت', 'کشاورزی', 'متالورژی', 'مکاترونیک', 'علوم کامپیوتر', 'آمار', 'حسابداری', 'برنامه نویسی', 'پزشکی', 'دندانپزشکی', 'داروسازی', 'دامپزشکی', 'فیزیوتراپی', 'پرستاری',
           'مامایی', 'علوم آزمایشگاهی', 'علوم تغذیه', 'علوم و صنایع غذایی', 'هوشبری', 'حقوق', 'روان‌شناسی', 'الهیات', 'علوم اقتصادی', 'مدیریت  بازرگانی', 'علوم سیاسی', 'علوم اجتماعی', 'زبان و ادبیات فارسی', 'مدیریت', 'زبان و ادبیات عربی', 'روابط عمومی', 'سینما', 'عکاسی', 'زبان انگلیسی', 'گرافیک', 'تایپ', 'نرم افزار', 'آموزش', 'سایر موارد']

myRecord1 = json.load(open('MyRecord.json'))

user_dict = {
    'ID': {int(k): (v) for k, v in myRecord1.items()}
}

myRecord2 = json.load(open('MyRecord_2.json'))

user_dict_L = {
    'ID': {int(k): (v) for k, v in myRecord2.items()}
}

myRecord3 = json.load(open('MyRecord_3.json'))

rand_main = {
    'ID': {int(k): (v) for k, v in myRecord3.items()}
}

myRecord4 = json.load(open('MyRecord_4.json'))

Signal_main = {
    'ID': {int(k): (v) for k, v in myRecord4.items()}
}

myRecord5 = json.load(open('MyRecord_5.json'))

Majloc_main = {
    'ID': {int(k): (v) for k, v in myRecord5.items()}
}

myRecord6 = json.load(open('MyRecord_6.json'))

UserName_main = {
    'ID': {int(k): (v) for k, v in myRecord6.items()}
}

myRecord7 = json.load(open('MyRecord_7.json'))

Type_main = {
    'ID': {int(k): (v) for k, v in myRecord7.items()}
}

myRecord8 = json.load(open('MyRecord_8.json'))

Context_main = {
    'ID': {int(k): (v) for k, v in myRecord8.items()}
}

# ===================================================================================


def start(update: Update, context: CallbackContext):

    global rand, rand1, slot, cnt_1, cnt_2, loc, major_slot, un_slot, user_dict, user_dict2, Numerator, Majloc, UserName, Signal, Type, Context, entry, myRecord_1, loc_validator, maj_validator, majval, locval, sgn

    start_key = [['ثبت آگهی جدید', 'ثبت آگهی رایگان'],
                 ['پروفایل کاربر', 'پشتیبانی']]

    start_key_2 = ReplyKeyboardMarkup(start_key, resize_keyboard=True)

    cursor.execute('SELECT * FROM users WHERE chatId = %s',
                   (update.effective_chat.id, ))
    entry = cursor.fetchone()

    # if update.message.from_user.username !=None:

    if entry is None:

        update.message.reply_text('سلام {} به ربات یاب نیز خوش آمدید'.format(
            update.message.from_user.first_name), reply_markup=start_key_2)

        user_dict2 = {
            update.effective_chat.id: cnt_1
        }

        user_dict_2_L = {
            update.effective_chat.id: cnt_2
        }

        rand = {
            update.effective_chat.id: rand1
        }

        Signal = {
            update.effective_chat.id: sgn
        }

        Majloc = {
            update.effective_chat.id: major_slot
        }

        UserName = {
            update.effective_chat.id: un_slot
        }

        Type = {
            update.effective_chat.id: slot
        }

        Context = {
            update.effective_chat.id: con
        }


# ----------------------------------------------------

        user_dict['ID'].update(user_dict2)
        user_dict_L['ID'].update(user_dict_2_L)
        rand_main['ID'].update(rand)
        Signal_main['ID'].update(Signal)
        Majloc_main['ID'].update(Majloc)
        UserName_main['ID'].update(UserName)
        Type_main['ID'].update(Type)
        Context_main['ID'].update(Context)

        j = json.dumps(user_dict['ID'])
        with open('MyRecord.json', 'w') as f:
            f.write(j)
            f.close()

        j2 = json.dumps(user_dict_L['ID'])
        with open('MyRecord_2.json', 'w') as f2:
            f2.write(j2)
            f2.close()

        j3 = json.dumps(rand_main['ID'])
        with open('MyRecord_3.json', 'w') as f3:
            f3.write(j3)
            f3.close()

        j4 = json.dumps(Signal_main['ID'])
        with open('MyRecord_4.json', 'w') as f4:
            f4.write(j4)
            f4.close()

        j5 = json.dumps(Majloc_main['ID'])
        with open('MyRecord_5.json', 'w') as f5:
            f5.write(j5)
            f5.close()

        j6 = json.dumps(UserName_main['ID'])
        with open('MyRecord_6.json', 'w') as f6:
            f6.write(j6)
            f6.close()

        j7 = json.dumps(Type_main['ID'])
        with open('MyRecord_7.json', 'w') as f7:
            f7.write(j7)
            f7.close()

        j8 = json.dumps(Context_main['ID'])
        with open('MyRecord_8.json', 'w') as f8:
            f8.write(j8)
            f8.close()

        Type_main['ID'][update.effective_chat.id] = None
        Majloc_main['ID'][update.effective_chat.id] = None
        UserName_main['ID'][update.effective_chat.id] = None
        Context_main['ID'][update.effective_chat.id] = None
        Signal_main['ID'][update.effective_chat.id] = None
        rand_main['ID'][update.effective_chat.id] = None

        Dcode = 'NONE'

        j3 = json.dumps(rand_main['ID'])
        with open('MyRecord_3.json', 'w') as f3:
            f3.write(j3)
            f3.close()

        j4 = json.dumps(Signal_main['ID'])
        with open('MyRecord_4.json', 'w') as f4:
            f4.write(j4)
            f4.close()

        j5 = json.dumps(Majloc_main['ID'])
        with open('MyRecord_5.json', 'w') as f5:
            f5.write(j5)
            f5.close()

        j6 = json.dumps(UserName_main['ID'])
        with open('MyRecord_6.json', 'w') as f6:
            f6.write(j6)
            f6.close()

        j7 = json.dumps(Type_main['ID'])
        with open('MyRecord_7.json', 'w') as f7:
            f7.write(j7)
            f7.close()

        j8 = json.dumps(Context_main['ID'])
        with open('MyRecord_8.json', 'w') as f8:
            f8.write(j8)
            f8.close()

        cursor.execute("INSERT INTO users (chatId, name, username, username_org, Time) VALUES(%s, %s, %s, %s, %s)", (update.effective_chat.id,
                       update.message.from_user.first_name, UserName_main['ID'][update.effective_chat.id], update.message.from_user.username, dt.datetime.now()))
        mydb.commit()

        cursor.execute('INSERT INTO ads_info (ChatId, Counter, Counter_total, discount_code, Time) VALUES (%s, %s, %s, %s, %s)', (
            update.effective_chat.id, user_dict['ID'][update.effective_chat.id], user_dict_L['ID'][update.effective_chat.id], Dcode, dt.datetime.now()))
        mydb.commit()

    else:
        if update.message != None:
            update.message.reply_text(
                'منوی اصلی یاب نیز', reply_markup=start_key_2)
        else:
            query = update.callback_query
            context.bot.send_message(
                chat_id=query.message.chat_id, text='منوی اصلی یاب نیز', reply_markup=start_key_2)

    rand = {
        update.effective_chat.id: rand1
    }

    Majloc = {
        update.effective_chat.id: major_slot
    }

    UserName = {
        update.effective_chat.id: un_slot
    }

    Signal = {
        update.effective_chat.id: sgn
    }

    Type = {
        update.effective_chat.id: slot
    }

    Context = {
        update.effective_chat.id: con
    }

    rand_main['ID'].update(rand)
    Signal_main['ID'].update(Signal)
    Majloc_main['ID'].update(Majloc)
    UserName_main['ID'].update(UserName)
    Type_main['ID'].update(Type)
    Context_main['ID'].update(Context)

    j3 = json.dumps(rand_main['ID'])
    with open('MyRecord_3.json', 'w') as f3:
        f3.write(j3)
        f3.close()

    j4 = json.dumps(Signal_main['ID'])
    with open('MyRecord_4.json', 'w') as f4:
        f4.write(j4)
        f4.close()

    j5 = json.dumps(Majloc_main['ID'])
    with open('MyRecord_5.json', 'w') as f5:
        f5.write(j5)
        f5.close()

    j6 = json.dumps(UserName_main['ID'])
    with open('MyRecord_6.json', 'w') as f6:
        f6.write(j6)
        f6.close()

    j7 = json.dumps(Type_main['ID'])
    with open('MyRecord_7.json', 'w') as f7:
        f7.write(j7)
        f7.close()

    j8 = json.dumps(Context_main['ID'])
    with open('MyRecord_8.json', 'w') as f8:
        f8.write(j8)
        f8.close()

    Type_main['ID'][update.effective_chat.id] = None
    Majloc_main['ID'][update.effective_chat.id] = None
    UserName_main['ID'][update.effective_chat.id] = None
    Context_main['ID'][update.effective_chat.id] = None
    Signal_main['ID'][update.effective_chat.id] = None
    rand_main['ID'][update.effective_chat.id] = None

    j3 = json.dumps(rand_main['ID'])
    with open('MyRecord_3.json', 'w') as f3:
        f3.write(j3)
        f3.close()

    j4 = json.dumps(Signal_main['ID'])
    with open('MyRecord_4.json', 'w') as f4:
        f4.write(j4)
        f4.close()

    j5 = json.dumps(Majloc_main['ID'])
    with open('MyRecord_5.json', 'w') as f5:
        f5.write(j5)
        f5.close()

    j6 = json.dumps(UserName_main['ID'])
    with open('MyRecord_6.json', 'w') as f6:
        f6.write(j6)
        f6.close()

    j7 = json.dumps(Type_main['ID'])
    with open('MyRecord_7.json', 'w') as f7:
        f7.write(j7)
        f7.close()

    j8 = json.dumps(Context_main['ID'])
    with open('MyRecord_8.json', 'w') as f8:
        f8.write(j8)
        f8.close()

    # else:
    #     update.message.reply_text('کاربر گرامی شما نام کاربری ندارید ❗ \n ابتدا یک نام کاربری بسازید و دوباره برای استفاده از ربات تلاش کنید')

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def Function(update: Update, context: CallbackContext):
    global Discount
    try:

        if update.message.text:

            if update.message.text == 'ثبت آگهی جدید':

                key = [['انجام دهنده', 'درخواست دهنده'], [
                    'خریدار', 'فروشنده'], ['پیشنهاد شغلی']]

                key_2 = ReplyKeyboardMarkup(key, resize_keyboard=True)

                rand_main['ID'][update.effective_chat.id] = code + \
                    str(random.randint(10000, 900000))

                j3 = json.dumps(rand_main['ID'])
                with open('MyRecord_3.json', 'w') as f3:
                    f3.write(j3)
                    f3.close()

                update.message.reply_text('🔶لطفا نوع اگهی خودتو از بین موارد زیر انتخاب کن \n \n🔹اگر درخواستی داری میتونی از گزینه درخواست دهنده استفاده کنی \n مثال:کمک در حل تمرین یا پروژه\n \n🔹اگر حرفه ای بلدی که فکر میکنی میتونه مفید باشه برای بقیه میتونی از گزینه انجام دهنده استفاده کنی\n مثال:مسلط به فوتوشاپ هستم و میتونم هر کاری در این زمینه رو انجام بدم \n یا فردی هستم مسلط به زبان انگلیسی میتونم اشکالات شمارو رفع کنم.\n \n🔹اگر چیزی میخوای بفروشی میتونی از گزینه فروشنده استفاده کنی\n مثال:کتاب،ماشین حساب و... \n \n🔹اگر چیزی میخوای بخری میتونی از گزینه خریدار استفاده کنی \n مثال:کتاب،ماشین حساب و... \n \n🔹اگر کسب و کاری داری و احتیاج به شخصی با حرفه خاصی داری یا اگر حرفه خاصی داری و احتیاج به کسب و کاری داری میتونی از گزینه پیشنهاد شغلی استفاده کنی', reply_markup=key_2)

            elif update.message.text == 'ثبت آگهی رایگان':

                try:
                    context.bot.sendPhoto(chat_id=update.message.chat.id, photo='https://ibb.co/47mjffF',
                                          caption='لطفا کد تخفیفی که پس از ثبت آگهی پنجم دریافت کردید را مانند عکس وارد کنید')
                except:
                    update.message.reply_text('لطفا کد تخفیف خود را وارد کنید')
                    Dis_Count(update, context)

            elif update.message.text == 'پروفایل کاربر':

                cursor.execute(
                    'SELECT * FROM ads_info WHERE chatId = %s', (update.effective_chat.id, ))
                entry_c = cursor.fetchone()

                cursor.execute('SELECT * FROM users WHERE ChatId= %s',
                               (update.effective_chat.id, ))
                entry_cc = cursor.fetchone()

                update.message.reply_text('🟢نام: {} \n ➖➖➖➖➖➖➖➖➖➖➖➖➖\n🔵نام کاربری: {} \n ➖➖➖➖➖➖➖➖➖➖➖➖➖ \n🟠تعداد آگهی لازم برای ثبت رایگان: {}/3 \n➖➖➖➖➖➖➖➖➖➖➖➖➖\n🔴تعداد کل آگهی های شما: {} \n➖➖➖➖➖➖➖➖➖➖➖➖➖\n🟡کد تخفیف: {} \n➖➖➖➖➖➖➖➖➖➖➖➖➖\n'.format(
                    entry_cc[1], entry_cc[2], entry_c[2], entry_c[3], entry_c[4]))

            elif update.message.text == 'پشتیبانی':

                support(update, context)

        if update.message.text != 'ثبت آگهی جدید' or update.message.text != 'ثبت آگهی رایگان':

            prv_pol = [
                ['قوانین و مقررات آگهی یاب نیز را میپذیرم🔹'], ['منوی اصلی']]
            prv_pol_2 = ReplyKeyboardMarkup(prv_pol, resize_keyboard=True)

            prv_poll = [
                ['قوانین و مقررات آگهی یاب نیز را میپذیرم🔸'], ['منوی اصلی']]
            prv_pol_3 = ReplyKeyboardMarkup(prv_poll, resize_keyboard=True)

            if update.message.text == 'درخواست دهنده':

                Type_main['ID'][update.effective_chat.id] = '#درخواست_دهنده'

                j7 = json.dumps(Type_main['ID'])
                with open('MyRecord_7.json', 'w') as f7:
                    f7.write(j7)
                    f7.close()

                update.message.reply_text('⛔قوانین و مقررات آگهی #درخواست_دهنده در یاب نیز :\n \n \n 1-استفاده از لینک و یا تبلیغ در متن اگهی ممنوع می باشد. \n \n 2- توهین و به کار بردن الفاظ رکیک در آگهی ممنوع می باشد. \n \n 3- به کار بردن ایموجی در متن آگهی ممنوع می باشد. \n \n 4- آگهی با موضوع امتحان , پروپوزال , پایان نامه و پروژه آماده ممنوع می باشد. \n \n 5- برای درج آگهی ققط از یک آیدی میتوانید استفاده کنید. \n \n 6- 🔸هزینه ثبت آگهی درخواست دهنده در کانال یاب نیز 6000 تومان میباشد. \n \n پذیرش قوانین و مقررات یابنیز به منزله موافقت با قوانین ذکر شده است \n اگر موارد ذکر شده در آگهی ثبت شده رعایت نشده باشد آگهی شما از کانال حذف شده و تضمینی برای بازگشت وجه پرداخت شده نمی باشد. \n ', reply_markup=prv_pol_2)

            elif update.message.text == 'انجام دهنده':

                Type_main['ID'][update.effective_chat.id] = '#انجام_دهنده'

                j7 = json.dumps(Type_main['ID'])
                with open('MyRecord_7.json', 'w') as f7:
                    f7.write(j7)
                    f7.close()

                update.message.reply_text('⛔قوانین و مقررات آگهی #انجام_دهنده در یاب نیز :\n \n \n 1- استفاده از لینک و یا تبلیغ در متن اگهی ممنوع می باشد. \n \n 2- کالا یا خدمات مورد نیاز نباید به هیچ وجه ناقض حقوق مولفان و ناشران آن باشد. \n \n 3- توهین و به کار بردن الفاظ رکیک در آگهی ممنوع می باشد. \n \n 4 - به کار بردن ایموجی در متن آگهی ممنوع می باشد. \n \n 5 - آگهی با موضوع امتحان , پروپوزال , پایان نامه و پروژه آماده ممنوع می باشد. \n \n 6- برای درج آگهی ققط از یک آیدی میتوانید استفاده کنید. \n \n 7- 🔸هزینه ثبت آگهی انجام دهنده در کانال یاب نیز 15000 تومان میباشد. \n \n پذیرش قوانین و مقررات یابنیز به منزله موافقت با قوانین ذکر شده است \n اگر موارد ذکر شده در آگهی ثبت شده رعایت نشده باشد آگهی شما از کانال حذف شده و تضمینی برای بازگشت وجه پرداخت شده نمی باشد. \n ', reply_markup=prv_pol_2)

            elif update.message.text == 'فروشنده':

                Type_main['ID'][update.effective_chat.id] = '#فروشنده'

                j7 = json.dumps(Type_main['ID'])
                with open('MyRecord_7.json', 'w') as f7:
                    f7.write(j7)
                    f7.close()

                update.message.reply_text('⛔قوانین و مقررات آگهی #فروشنده در یاب نیز :\n \n \n 1- استفاده از لینک و یا تبلیغ در متن اگهی ممنوع می باشد. \n \n 2- کالا یا خدماتی که قرار است آگهی شود از جانب شما نباشد به هیچ وجه ناقض حقوق مولفان و ناشران آن باشد. \n \n 3- توهین و به کار بردن الفاظ رکیک در آگهی ممنوع می باشد. \n \n 4- به کار بردن ایموجی در متن آگهی ممنوع می باشد. \n \n 5- آگهی با موضوع امتحان , پروپوزال , پایان نامه و پروژه آماده ممنوع می باشد. \n \n 6- برای درج آگهی ققط از یک آیدی میتوانید استفاده کنید. \n \n 7- 🔸هزینه ثبت آگهی در کانال یاب نیز 6000 تومان میباشد. \n \n پذیرش قوانین و مقررات یابنیز به منزله موافقت با قوانین ذکر شده است \n اگر موارد ذکر شده در آگهی ثبت شده رعایت نشده باشد آگهی شما از کانال حذف شده و تضمینی برای بازگشت وجه پرداخت شده نمی باشد. \n ', reply_markup=prv_pol_3)

            elif update.message.text == 'خریدار':

                Type_main['ID'][update.effective_chat.id] = '#خریدار'

                j7 = json.dumps(Type_main['ID'])
                with open('MyRecord_7.json', 'w') as f7:
                    f7.write(j7)
                    f7.close()

                update.message.reply_text('⛔قوانین و مقررات آگهی #خریدار در یاب نیز :\n \n \n 1- استفاده از لینک و یا تبلیغ در متن اگهی ممنوع می باشد. \n \n 2- توهین و به کار بردن الفاظ رکیک در آگهی ممنوع می باشد. \n \n 3- به کار بردن ایموجی در متن آگهی ممنوع می باشد. \n \n 4- آگهی با موضوع امتحان , پروپوزال , پایان نامه و پروژه آماده ممنوع می باشد. \n \n 5- برای درج آگهی ققط از یک آیدی میتوانید استفاده کنید. \n \n 6- از به کاربردن ایموجی در متن آگهی خود داری کنید. \n \n 7- 🔸هزینه ثبت آگهی در کانال یاب نیز 6000 تومان میباشد. \n \n پذیرش قوانین و مقررات یابنیز به منزله موافقت با قوانین ذکر شده است \n اگر موارد ذکر شده در آگهی ثبت شده رعایت نشده باشد آگهی شما از کانال حذف شده و تضمینی برای بازگشت وجه پرداخت شده نمی باشد. \n ', reply_markup=prv_pol_3)

            elif update.message.text == 'پیشنهاد شغلی':

                Type_main['ID'][update.effective_chat.id] = '#پیشنهاد_شغلی'

                j7 = json.dumps(Type_main['ID'])
                with open('MyRecord_7.json', 'w') as f7:
                    f7.write(j7)
                    f7.close()

                update.message.reply_text('⛔قوانین و مقررات آگهی #پیشنهاد_شغلی در یاب نیز :\n \n \n 1- استفاده از لینک و یا تبلیغ در متن اگهی ممنوع می باشد. \n \n 2- توهین و به کار بردن الفاظ رکیک در آگهی ممنوع می باشد. \n \n 3- به کار بردن ایموجی در متن آگهی ممنوع می باشد. \n \n 4- برای درج آگهی ققط از یک آیدی میتوانید استفاده کنید. \n \n 5- هزینه ثبت آگهی در کانال یاب نیز 6000 تومان میباشد. \n \n پذیرش قوانین و مقررات یابنیز به منزله موافقت با قوانین ذکر شده است \n اگر موارد ذکر شده در آگهی ثبت شده رعایت نشده باشد آگهی شما از کانال حذف شده و تضمینی برای بازگشت وجه پرداخت شده نمی باشد. \n ', reply_markup=prv_pol_3)

        if update.message.text == 'قوانین و مقررات آگهی یاب نیز را میپذیرم🔹':

            major = [['منوی اصلی', 'بازگشت'], ['دروس عمومی', 'دروس پایه'], ['مهندسی'], ['هوافضا', 'معماری', 'عمران', 'مکانیک'], ['کامپیوتر', 'برق', 'نساجی', 'پزشکی'], ['شیمی', 'صنایع', 'فناوری اطلاعات', 'شهرسازی'], ['نفت', 'کشاورزی', 'متالورژی', 'مکاترونیک'], ['علوم کامپیوتر', 'آمار', 'حسابداری', 'برنامه نویسی'], ['فیزیک', 'شیمی', 'ریاضی', 'زیست شناسی'], ['پزشکی'], ['دندان پزشکی', 'داروسازی'], [
                'دامپزشکی', 'فیزیوتراپی', 'پرستاری', 'مامایی'], ['علوم آزمایشگاهی', 'علوم تغذیه', 'علوم و صنایع غذایی', 'هوشبری'], ['حقوق', 'روانشناسی'], ['الهیات', 'علوم اقتصادی', 'مدیریت  بازرگانی', 'علوم سیاسی'], ['علوم اجتماعی', 'زبان و ادبیات فارسی', 'مدیریت', 'زبان و ادبیات عربی'], ['روابط عمومی', 'سینما', 'عکاسی', 'زبان انگلیسی'], ['گرافیک', 'تایپ', 'نرم افزار', 'آموزش'], ['ابتدایی', 'متوسطه اول', 'متوسطه دوم'], ['سایر موارد']]
            major_2 = ReplyKeyboardMarkup(major, resize_keyboard=True)

            Signal_main['ID'][update.effective_chat.id] = 0

            j4 = json.dumps(Signal_main['ID'])
            with open('MyRecord_4.json', 'w') as f4:
                f4.write(j4)
                f4.close()
            update.message.reply_text(
                'حالا لطفا موضوع اگهی خود را از بین موارد زیر انتخاب کنید.', reply_markup=major_2)

        if update.message.text == 'قوانین و مقررات آگهی یاب نیز را میپذیرم🔸':

            loc_key = [['منوی اصلی', 'بازگشت'], ['تهران', 'اصفهان', 'فارس', 'خراسان رضوی'], ['آذربایجان شرقی', 'آذربایجان غربی', 'اردبیل', 'البرز'], ['ایلام', 'بوشهر', 'چهارمحال و بختیاری', 'خراسان جنوبی'], [
                'خراسان رضوی', 'خراسان شمالی', 'خوزستان', 'زنجان'], ['سمنان', 'سیستان و بلوچستان', 'قزوین', 'قم'], ['کردستان', 'کرمان', 'کرمانشاه', 'کهگیلویه و بویراحمد'], ['گلستان', 'گیلان', 'لرستان', 'مازندران'], ['مرکزی', 'هرمزگان', 'همدان', 'یزد']]
            loc_key_2 = ReplyKeyboardMarkup(loc_key, resize_keyboard=True)

            Signal_main['ID'][update.effective_chat.id] = 0

            j4 = json.dumps(Signal_main['ID'])
            with open('MyRecord_4.json', 'w') as f4:
                f4.write(j4)
                f4.close()

            update.message.reply_text(
                'حالا لطفا نام استانی که در آن ساکن هستید را وارد کنید', reply_markup=loc_key_2)

        if update.message.text not in L and update.message.text != 'قوانین و مقررات آگهی یاب نیز را میپذیرم🔹':
            restart_key = [['بازگشت'], ['منوی اصلی']]
            rstart_key_2 = ReplyKeyboardMarkup(
                restart_key, resize_keyboard=True)

            if update.message.text == 'خراسان رضوی' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#خراسان_رضوی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'فارس' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#فارس'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'تهران' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#تهران'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'اصفهان' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#اصفهان'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'البرز' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#البرز'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'اردبیل' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#اردبیل'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'آذربایجان غربی' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#آذربایجان_غربی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'آذربایجان شرقی' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#آذربایجان_شرقی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'خراسان جنوبی' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#خراسان_جنوبی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'چهارمحال و بختیاری' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#چهارمحال_و_بختیاری'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'ایلام' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#ایلام'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'بوشهر' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#بوشهر'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'زنجان' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#زنجان'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'خوزستان' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#خوزستان'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'خراسان شمالی' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#خراسان_شمالی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'خراسان رضوی' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#خراسان_رضوی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'قم' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#قم'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'قزوین' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#قزوین'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'سیستان و بلوچستان' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#سیستان_و_بلوچستان'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'سمنان' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#سمنان'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'کرمانشاه' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#کرمانشاه'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'کرمان' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#کرمان'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'کردستان' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#کردستان'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'کهگیلویه و بویراحمد' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#کهکیلویه_و_بویراحمد'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'مازندران' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#مازندران'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'لرستان' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#لرستان'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'گیلان' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#گیلان'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'گلستان' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#گلستان'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'یزد' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#یزد'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'همدان' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#همدان'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'هرمزگان' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#هرمزگان'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'مرکزی' and Signal_main['ID'][update.effective_chat.id] != None:

                Majloc_main['ID'][update.effective_chat.id] = '#مرکزی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)


# ============================================================================================================================================================

        if update.message.text not in L and update.message.text != 'قوانین و مقررات آگهی یاب نیز را میپذیرم🔸':

            restart_key = [['بازگشت'], ['منوی اصلی']]
            rstart_key_2 = ReplyKeyboardMarkup(
                restart_key, resize_keyboard=True)

            if update.message.text == 'دروس پایه' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#پایه'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'دروس عمومی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#عمومی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'مهندسی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#مهندسی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'هوافضا' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#هوافضا'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'معماری' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#معماری'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'عمران' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#عمران'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'مکانیک' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#مکانیک'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'پزشکی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#پزشکی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'نساجی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#نساجی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'برق' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#برق'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'کامپیوتر' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#کامپیوتر'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'شهرسازی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#شهرسازی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'فناوری اطلاعات' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#فناوری_اطلاعات'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'صنایع' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#صنایع'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'شیمی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#شیمی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'نفت' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#نفت'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'کشاورزی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#کشاوزی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'متالورژی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#متالورژی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'مکاترونیک' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#مکاترونیک'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'علوم کامپیوتر' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#علوم_کامپیوتر'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'آمار' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#آمار'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'حسابداری' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#حسابداری'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'برنامه نویسی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#برنامه_نویسی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'پزشکی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#پزشکی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'داروسازی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#داروسازی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'دندان پزشکی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#دندان_پزشکی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'مامایی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#مامایی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'پرستاری' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#پرستاری'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'فیزیوتراپی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#فیزیوتراپی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'دامپزشکی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#دامپزشکی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'هوشبری' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#هوشبری'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'علوم و صنایع غذایی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#علوم_و_صنایع_غدایی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'علوم تغذیه' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#علوم_تغذیه'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'علوم آزمایشگاهی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#علوم_آزمایشگاهی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'روانشناسی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#روانشناسی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'حقوق' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#حقوق'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'علوم سیاسی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#علوم_سیاسی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'مدیریت بازرگانی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#مدیریت_بازرگانی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'علوم اقتصادی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#علوم_اقتصادی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'الهیات' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#الهیات'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'زبان و ادبیات عربی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#زبان_عربی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'زبان و ادبیات فارسی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#زبان_و_ادبیات_فارسی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'زبان انگلیسی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#زبان_انگلیسی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'مدیریت' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#مدیریت'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'علوم_اجتماعی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#علوم_اجتماعی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'عکاسی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#عکاسی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'سینما' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#سینما'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'روابط عمومی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#روابط_عمومی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'گرافیک' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#گرافیک'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'تایپ' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#تایپ'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'نرم افزار' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#نرم_افزار'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'آموزش' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#آموزش'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'ابتدایی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#ابتدایی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'متوسطه اول' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#متوسطه_اول'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'متوسطه دوم' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#متوسطه_دوم'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'سایر موارد' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = ''

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'ریاضی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#ریاضی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'فیزیک' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#فیزیک'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'شیمی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#شیمی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

            elif update.message.text == 'زیست شناسی' and Signal_main['ID'][update.effective_chat.id] != None:
                Majloc_main['ID'][update.effective_chat.id] = '#زیست_شناسی'

                j5 = json.dumps(Majloc_main['ID'])
                with open('MyRecord_5.json', 'w') as f5:
                    f5.write(j5)
                    f5.close()

                update.message.reply_text(
                    'حالا لطفا نام کاربری خود را وارد کنید. \n 🔺توجه داشته باشید که حتما اول نام کاربری خود @ داشته باشد در غیر این صورت نمیتوانید ادامه مراحل را طی کنید \n مثال : @yabniz_admin', reply_markup=rstart_key_2)

        if update.message.text:

            if x in update.message.text and update.message.text != 'بازگشت' and update.message.text != 'قوانین و مقررات آگهی یاب نیز را میپذیرم' and Signal_main['ID'].get(update.effective_chat.id) != None and Majloc_main['ID'].get(update.effective_chat.id) != None:

                add_main = [['منوی اصلی']]
                add_main2 = ReplyKeyboardMarkup(add_main, resize_keyboard=True)

                UserName_main['ID'][update.effective_chat.id] = update.message.text

                j6 = json.dumps(UserName_main['ID'])
                with open('MyRecord_6.json', 'w') as f6:
                    f6.write(j6)
                    f6.close()

                cursor.execute("UPDATE users SET username=%s WHERE chatId=%s ", (
                    UserName_main['ID'][update.effective_chat.id], update.effective_chat.id))
                mydb.commit()

            # add username row to ads table and update that row except from users: DO NOT UPDATE USERNAME FROM USERS*
                update.message.reply_text('🔹حالا لطفا متن آگهی خود را وارد کنید. \n \n🔸مثال درخواست دهنده :\nبه یک نفر برای کمک در حل تمرین یا پروژه نیازمندم \n \n🔸مثال انجام دهنده : \n مسلط به فوتوشاپ هستم و میتونم هر کاری در این زمینه رو انجام بدم یا فردی هستم مسلط به زبان انگلیسی میتونم اشکالات شمارو رفع کنم.\n \n🔸مثال خریدار : \n خریدار کتاب و لوازم تحریر و... \n \n🔸مثال فروشنده : \n یه سری لوازم و کتاب دارم به قیمت خوبی میفروشم \n \n🔸مثال پیشنهاد شغلی : \n به یک نفر مسلط به فوتوشاپ برای استخدام در شرکت نیازمندم \n . ', reply_markup=add_main2)

        if update.message.text not in L1 and update.message.text != UserName_main['ID'].get(update.effective_chat.id) and update.message.text not in L and update.message.text not in loc_list and UserName_main['ID'].get(update.effective_chat.id) != None and Signal_main['ID'].get(update.effective_chat.id) != None:

            key = [[InlineKeyboardButton(text='ارتباط با آگهی دهنده 💬', url=f'https://t.me/{update.message.from_user.username}')], [InlineKeyboardButton(
                text='ارتباط با ادمین 👤', url='https://t.me/yabniz_admin'), InlineKeyboardButton(text='ثبت آگهی با ربات 🤖', url='https://t.me/yabniz_bot')]]
            key_2 = InlineKeyboardMarkup(key)

            key_admin = [[InlineKeyboardButton(text='لینک کانال 🔗', url='https://t.me/yabniz')], [InlineKeyboardButton(
                text='پروفایل کاربر 👤', callback_data='A1'), InlineKeyboardButton(text='منوی اصلی🟡', callback_data='B1')]]
            key_admin_2 = InlineKeyboardMarkup(key_admin)

            Context_main['ID'][update.effective_chat.id] = update.message.text

            j8 = json.dumps(Context_main['ID'])
            with open('MyRecord_8.json', 'w') as f8:
                f8.write(j8)
                f8.close()

            Signal_main['ID'][update.effective_chat.id] += 1

            user_dict['ID'][update.effective_chat.id] += 1

            user_dict_L['ID'][update.effective_chat.id] += 1

            j = json.dumps(user_dict['ID'])
            with open('MyRecord.json', 'w') as f:
                f.write(j)
                f.close()

            j2 = json.dumps(user_dict_L['ID'])
            with open('MyRecord_2.json', 'w') as f2:
                f2.write(j2)
                f2.close()

                cursor.execute("UPDATE ads_info SET Counter=%s, Counter_total=%s WHERE chatId=%s ", (
                    user_dict['ID'][update.effective_chat.id], user_dict_L['ID'][update.effective_chat.id],  update.effective_chat.id))
                mydb.commit()

                cursor.execute("INSERT INTO ads (ChatId, Code, Type, Maj_Loc, UserName, Context, Time) VALUES(%s, %s, %s, %s, %s, %s, %s)", (update.effective_chat.id, rand_main['ID'][update.effective_chat.id], Type_main[
                               'ID'][update.effective_chat.id], Majloc_main['ID'][update.effective_chat.id], UserName_main['ID'][update.effective_chat.id], Context_main['ID'][update.effective_chat.id],  dt.datetime.now()))
                mydb.commit()

                cursor.execute(
                    'SELECT * FROM ads_info WHERE chatId = %s', (update.effective_chat.id, ))
                entry_c = cursor.fetchone()

                context.bot.send_chat_action(
                    chat_id=update.effective_message.chat_id, action=telegram.ChatAction.TYPING)
                update.message.reply_text(
                    f"✅ آگهی شما بعد از تأیید در کانال ثبت میشود \n \n \n شرح آگهی:\n \n کد آگهی :{rand_main['ID'][update.effective_chat.id]} \n \n {Type_main['ID'][update.effective_chat.id]} \n \n {Majloc_main['ID'][update.effective_chat.id]}\n \n {Context_main['ID'][update.effective_chat.id]} \n \n {UserName_main['ID'][update.effective_chat.id]} \n \n➖➖➖➖➖➖➖➖➖➖➖➖➖ \n \n 🔹شما {entry_c[2]} آگهی از 3  آگهی را برای دریافت آگهی رایگان ثبت کردید. \n \n 🔸تعداد کل آگهی های ثبت شده توسط شما: {entry_c[3]} \n ➖➖➖➖➖➖➖➖➖➖➖➖➖ \n", reply_markup=key_admin_2)

                context.bot.send_message(
                    text=f"🟩کد آگهی :{rand_main['ID'][update.effective_chat.id]} \n نوع آگهی: {Type_main['ID'][update.effective_chat.id]} \n➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n {Majloc_main['ID'][update.effective_chat.id]} \n متن آگهی : \n {Context_main['ID'][update.effective_chat.id]} \n \n \n 📥 ID: {UserName_main['ID'][update.effective_chat.id]} \n➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n ✅ @Yabniz", chat_id='@yabnest', reply_markup=key_2)

        else:
            update.message.reply_text(
                'به علت استفاده از کلمات ممنوعه یا تلاش برای ثبت مجدد آگهی قبلی خود اگهی شما مجاز به ثبت نمیباشد \n لطفا به منوی اصلی بازگشته و مراحل را از اول شروع کنید', reply_markup=key_admin_2)

        if user_dict['ID'][update.effective_chat.id] >= 3 and Context_main['ID'][update.effective_chat.id] != None:

            user_dict['ID'][update.effective_chat.id] = 0

            j = json.dumps(user_dict['ID'])
            with open('MyRecord.json', 'w') as f:
                f.write(j)
                f.close()

            lower = "abcdefghijklmnopqrstvwxyz"
            upper = "ABCDEFGHIJKLMNOPQRSTVWXYZ"
            number = "1234567890"
            all = lower + upper + number
            length = 11
            Discount = {
                update.effective_chat.id: "".join(random.sample(all, length))
            }
            Context_main['ID'][update.effective_chat.id] = None

            cursor.execute("UPDATE ads_info SET Counter=%s, discount_code=%s WHERE chatId=%s ", (
                user_dict['ID'][update.effective_chat.id], Discount[update.effective_chat.id], update.effective_chat.id))
            mydb.commit()
            update.message.reply_text(
                f'✅کاربر گرامی اکنون میتوانید یک آگهی رایگان ثبت کنید \n با استفاده از کد تخیف 100 درصدی زیر آگهی خود را به صورت رایگان ثبت کنید \n \n \n ➖➖➖➖➖➖➖➖➖➖➖➖➖ \n {Discount[update.effective_chat.id]} \n ➖➖➖➖➖➖➖➖➖➖➖➖➖ \n')

        if update.message.text == 'منوی اصلی':
            start(update, context)

        if update.message.text == 'بازگشت':
            callme(update, context)
    except:
        start(update, context)


def call_back(update, context):

    query = update.callback_query

    if query.data == 'B1':

        start(update, context)

    if query.data == 'A1':

        cursor.execute('SELECT * FROM ads_info WHERE chatId = %s',
                       (update.effective_chat.id, ))
        entry_c1 = cursor.fetchone()

        cursor.execute('SELECT * FROM users WHERE chatId = %s',
                       (update.effective_chat.id, ))
        entry_c2 = cursor.fetchone()

        context.bot.send_message(chat_id=query.message.chat_id, text='🟢نام: {} \n ➖➖➖➖➖➖➖➖➖➖➖➖➖ \n🔵نام کاربری: {} \n ➖➖➖➖➖➖➖➖➖➖➖➖➖ \n🟠تعداد آگهی لازم برای ثبت رایگان: {}/3 \n➖➖➖➖➖➖➖➖➖➖➖➖➖\n🔴تعداد کل آگهی های شما: {} \n➖➖➖➖➖➖➖➖➖➖➖➖➖\n🟡کد تخفیف: {} \n➖➖➖➖➖➖➖➖➖➖➖➖➖\n'.format(
            entry_c2[1], entry_c2[2], entry_c1[2], entry_c1[3], entry_c1[4]))


def Dis_Count(update, context):

    cursor.execute('SELECT * FROM ads_info WHERE ChatId= %s',
                   (update.effective_chat.id, ))
    discount_entry = cursor.fetchone()

    try:
        usertext = ' '.join(context.args)
        if usertext != discount_entry[4]:

            update.message.reply_text(
                'کد تخفیف وارد شده اشتباه است ❗ \n \n  لطفا کد تخفیف را مجددا به صورت دقیق وارد کنید')
        else:
            update.message.reply_text('✅کد تخفیف شما تایید شد')
            freead(update, context)

            user_dict['ID'][update.effective_chat.id] = 0

            j = json.dumps(user_dict['ID'])

            with open('MyRecord.json', 'w') as f:
                f.write(j)
                f.close()

            exp = 'EXPIRED'
            cursor.execute("UPDATE ads_info SET Counter=%s, discount_code=%s WHERE chatId=%s ",
                           (user_dict['ID'][update.effective_chat.id], exp, update.effective_chat.id))
            mydb.commit()

    except NameError:
        update.message.reply_text('❗در حال حاضر شما کد تخفیفی ندارید')

    except TypeError:
        context.bot.send_chat_action(
            chat_id=update.effective_message.chat_id, action=telegram.ChatAction.TYPING)


def freead(update: Update, context: CallbackContext):

    add_key = [[InlineKeyboardButton(
        text='ارتباط با درخولست دهنده 💬', url=f'https://t.me/{update.message.from_user.username}')]]
    add_key2 = InlineKeyboardMarkup(add_key)

    cursor.execute('SELECT * FROM users WHERE chatId = %s',
                   (update.effective_chat.id, ))
    check_user = cursor.fetchone()

    update.message.reply_text(
        'درخواست ثبت آگهی رایگان شما برای ادمین ارسال شد لطفا منتظر دریافت پیام از ادمین باشید.')
    context.bot.send_message(
        text=f'🔻 کاربر {check_user[1]} با مشخصات زیر درخواست ثبت آگهی رایگان دارد: \n \n ➖➖➖➖➖➖➖➖➖➖➖➖➖ \n Chat Id: {check_user[0]} \n ➖➖➖➖➖➖➖➖➖➖➖➖➖ \n UserName: @{check_user[3]} \n ➖➖➖➖➖➖➖➖➖➖➖➖➖ \n', chat_id=1657739774, reply_markup=add_key2)


def support(update: Update, context: CallbackContext):

    update.message.reply_text('https://t.me/yabniz_admin')


def callme(update: Update, context: CallbackContext):

    key = [['انجام دهنده', 'درخواست دهنده'], [
        'خریدار', 'فروشنده', 'پیشنهاد شغلی'], ['منوی اصلی']]

    key_2 = ReplyKeyboardMarkup(key, resize_keyboard=True)

    Type_main['ID'][update.effective_chat.id] = None
    Majloc_main['ID'][update.effective_chat.id] = None
    UserName_main['ID'][update.effective_chat.id] = None
    Context_main['ID'][update.effective_chat.id] = None
    Signal_main['ID'][update.effective_chat.id] = None
    rand_main['ID'][update.effective_chat.id] = code + \
        str(random.randint(10000, 900000))

    j3 = json.dumps(rand_main['ID'])
    with open('MyRecord_3.json', 'w') as f3:
        f3.write(j3)
        f3.close()

    j4 = json.dumps(Signal_main['ID'])
    with open('MyRecord_4.json', 'w') as f4:
        f4.write(j4)
        f4.close()

    j5 = json.dumps(Majloc_main['ID'])
    with open('MyRecord_5.json', 'w') as f5:
        f5.write(j5)
        f5.close()

    j6 = json.dumps(UserName_main['ID'])
    with open('MyRecord_6.json', 'w') as f6:
        f6.write(j6)
        f6.close()

    j7 = json.dumps(Type_main['ID'])
    with open('MyRecord_7.json', 'w') as f7:
        f7.write(j7)
        f7.close()

    j8 = json.dumps(Context_main['ID'])
    with open('MyRecord_8.json', 'w') as f8:
        f8.write(j8)
        f8.close()

    update.message.reply_text(
        'کاربر گرامی لطفا نوع آگهی خود را از بین موارد زیر انتخاب کنید', reply_markup=key_2)


def main() -> None:

    updater = Updater("5777083251:AAHI1MpzmPMTJuwLlGPMyT4t66rqPnbxKVU")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, Function))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, freead))
    dispatcher.add_handler(CommandHandler("code", Dis_Count))
    dispatcher.add_handler(CallbackQueryHandler(call_back))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
