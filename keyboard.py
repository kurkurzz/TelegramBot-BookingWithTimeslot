from datetime import timedelta
from telebot import types
from telebot.types import Message
import datetime as dt

def main_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    itembtna = types.KeyboardButton('/register')
    itembtnv = types.KeyboardButton('/bookinglist')
    itembtnc = types.KeyboardButton('/withdraw')
    itembtnd = types.KeyboardButton('/help')
    markup.row(itembtna, itembtnv)
    markup.row(itembtnc, itembtnd)
    return markup
    # bot.send_message(message.chat.id, "Welcome to PetCare. click /register to make a booking.", reply_markup=markup)

def date_keyboard():
    now = dt.datetime.now()
    end = now + timedelta(days=14)
    dates = []
    itembtns = []

    for i in range(0,14):
        dates.append((now + timedelta(days=i)))
    
    markup = types.ReplyKeyboardMarkup(row_width=7,one_time_keyboard=True)
    itembtns.clear()
    for date in dates:
        itembtn = types.KeyboardButton(str(date.date().day)+'/'+str(date.date().month))
        itembtns.append(itembtn)
        
    markup.add(itembtns[0],itembtns[1],itembtns[2],itembtns[3],itembtns[4],
    itembtns[5],itembtns[6],itembtns[7],itembtns[8],itembtns[9],
    itembtns[10],itembtns[11],itembtns[12],itembtns[13])
    return markup

def time_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=9,one_time_keyboard=True)
    itembtns = []
    timeslots = ['8:00','8:30','9:00','9:30','10:00','10:30','11:00','11:30','12:00','12:30','13:00','13:30'
    ,'14:00','14:30','15:00','15:30','16:00','16:30']
    itembtns.clear()
    for timeslot in timeslots:
        itembtn = types.KeyboardButton(timeslot)
        itembtns.append(itembtn)

    markup.add(itembtns[0],itembtns[1],itembtns[2],itembtns[3],itembtns[4],
    itembtns[5],itembtns[6],itembtns[7],itembtns[8],itembtns[9],
    itembtns[10],itembtns[11],itembtns[12],itembtns[13],itembtns[14],
    itembtns[15],itembtns[16],itembtns[17])
    return markup

def remove_keyboard():
    markup = types.ReplyKeyboardRemove()
    return markup

