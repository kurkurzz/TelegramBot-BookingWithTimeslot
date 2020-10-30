from datetime import timedelta
from telebot import types
from telebot.types import Message
import datetime as dt

#show 4 usages of the bot
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    itembtna = types.KeyboardButton('/register')
    itembtnv = types.KeyboardButton('/bookinglist')
    itembtnc = types.KeyboardButton('/withdraw')
    itembtnd = types.KeyboardButton('/help')
    markup.row(itembtna, itembtnv)
    markup.row(itembtnc, itembtnd)
    return markup

#show date choices. from today's date until +14 days
def date_keyboard():
    now = dt.datetime.now()
    dates = []
    itembtns = []
    itembtns.clear()
    markup = types.ReplyKeyboardMarkup(row_width=5,one_time_keyboard=True)

    #get list of 14 dates from now
    for i in range(0,14):
        dates.append((now + timedelta(days=i)))

    #get list of buttons from the the list of dates
    for date in dates:
        itembtn = types.KeyboardButton(str(date.date().day)+'/'+str(date.date().month))
        itembtns.append(itembtn)
    
    #insert buttons to markup
    markup.add(itembtns[0],itembtns[1],itembtns[2],itembtns[3],itembtns[4],
    itembtns[5],itembtns[6],itembtns[7],itembtns[8],itembtns[9],
    itembtns[10],itembtns[11],itembtns[12],itembtns[13])
    return markup

#show timeslots to choose, 8-5 interval 30 min
def time_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=6,one_time_keyboard=True)
    itembtns = []
    #list of time slots
    time_slots = ['8:00','8:30','9:00','9:30','10:00','10:30','11:00','11:30','12:00','12:30','13:00','13:30'
    ,'14:00','14:30','15:00','15:30','16:00','16:30']
    itembtns.clear()

    #get list of buttons from the the list of timeslots
    for time_slot in time_slots:
        itembtn = types.KeyboardButton(time_slot)
        itembtns.append(itembtn)

    #insert buttons into markup
    markup.add(itembtns[0],itembtns[1],itembtns[2],itembtns[3],itembtns[4],
    itembtns[5],itembtns[6],itembtns[7],itembtns[8],itembtns[9],
    itembtns[10],itembtns[11],itembtns[12],itembtns[13],itembtns[14],
    itembtns[15],itembtns[16],itembtns[17])
    return markup

def remove_keyboard():
    markup = types.ReplyKeyboardRemove()
    return markup

