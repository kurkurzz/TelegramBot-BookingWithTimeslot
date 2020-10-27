from datetime import datetime, timedelta
import threading
import telebot
import time
import datetime as dt
import firestore_service
from booking import Booking
from firestore_service import bookingList
import keyboard
from keyboard import remove_keyboard
import methods
from credentials import TOKEN
import schedule




bot = telebot.TeleBot(token=TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        # keyboard.main_keyboard(message,bot)
        # keyboard.date_keyboard(message,bot)
        # keyboard.time_keyboard(message,bot)
        bot.send_message(chat_id=message.chat.id,
        text='Welcome to PetCare Reservation.\nTo make reservation please click /register.',
        reply_markup=keyboard.main_keyboard()
        )
    except:
        bot.send_message(chat_id=message.chat.id,
        text='Something is wrong, please try again.'
        )

@bot.message_handler(commands=['register'])
def register(message):
    date = ''
    try:
        newBooking = Booking()
        def get_name(message):
            try:
                methods.check_input(message.text)
                newBooking.name = message.text
                bot.send_message(chat_id=message.chat.id, text='Please enter your phone number.')
                bot.register_next_step_handler(message,get_phonenumber)
            except:
                bot.send_message(chat_id=message.chat.id, text='Something is wrong, please try again.',reply_markup=keyboard.main_keyboard())

        def get_phonenumber(message):
            try:
                methods.check_input(message.text)
                newBooking.phonenumber = message.text
                bot.send_message(chat_id=message.chat.id, text='Please enter your pet\'s name.')
                bot.register_next_step_handler(message,get_petname)
            except:
                bot.send_message(chat_id=message.chat.id, text='Something is wrong, please try again.',reply_markup=keyboard.main_keyboard())

        def get_petname(message):
            try:
                methods.check_input(message.text)
                newBooking.petname = message.text
                bot.send_message(chat_id=message.chat.id, 
                text='Please select date.',
                reply_markup=keyboard.date_keyboard()
                )
                bot.register_next_step_handler(message,get_date)
            except:
                bot.send_message(chat_id=message.chat.id, text='Something is wrong, please try again.',reply_markup=keyboard.main_keyboard())

        def get_date(message):
            try:
                methods.check_input(message.text)
                nonlocal date
                date = message.text
                bot.send_message(chat_id=message.chat.id, 
                text='Please time slot date.',
                reply_markup=keyboard.time_keyboard()
                )
                bot.register_next_step_handler(message,get_time)
            except:
                bot.send_message(chat_id=message.chat.id, text='Something is wrong, please try again.',reply_markup=keyboard.main_keyboard())

        def get_time(message):
            try:
                methods.check_input(message.text)
                hour = message.text
                convertedtime = methods.convert_string_to_datetime(date,hour)
                exist = False
                sameTime = 0
                for booking in bookingList:
                    if booking.userid==message.from_user.id:
                        exist = True
                        break
                    if booking.timeslot == convertedtime.timestamp():
                        sameTime +=1
                if not exist:
                    if(sameTime < 3):
                        newBooking.timeslot = convertedtime.timestamp()
                        newBooking.userid = message.from_user.id
                        firestore_service.add_booking(newBooking)
                        bot.send_message(chat_id=message.chat.id, text='Registration successful.',reply_markup=keyboard.main_keyboard())
                    else:
                        bot.send_message(chat_id=message.chat.id, text='Booking for that time is full. please try other time.',reply_markup=keyboard.main_keyboard())
                else:
                    bot.send_message(chat_id=message.chat.id, text='Registration failed. You already made a booking.',reply_markup=keyboard.main_keyboard())
            except:
                bot.send_message(chat_id=message.chat.id, text='Something is wrong, please try again.',reply_markup=keyboard.main_keyboard())

        bot.send_message(chat_id=message.chat.id, text='Please enter your name.')
        bot.register_next_step_handler(message,get_name)
        
    except:
        bot.send_message(chat_id=message.chat.id,
        text='Something is wrong, please try again.'
        )
        

@bot.message_handler(commands=['bookinglist'])
def send_booking_list(message):
    try:
        methods.delete_past_booking()
        bot.send_message(chat_id=message.chat.id,text=firestore_service.display,
        reply_markup=keyboard.main_keyboard())
    except:
        bot.send_message(chat_id=message.chat.id,
        text='Something is wrong, please try again.',
        reply_markup=keyboard.main_keyboard()
        )

@bot.message_handler(commands=['help'])
def send_help(message):
    try:
        print(message)
        bot.send_message(chat_id=message.chat.id,text=
        '''
        Guide to use this bot.\n
    to book a slot, klik /register
    to check booked slot list, klik /bookinglist
    to withdraw, klik /withdraw
        ''',
        reply_markup=keyboard.main_keyboard()
        )
    except:
        bot.send_message(chat_id=message.chat.id,
        text='Something is wrong, please try again.',
        reply_markup=keyboard.main_keyboard()
            )    

@bot.message_handler(commands=['withdraw'])
def send_Message(message):
    try:
        canDelete = firestore_service.delete_booking_by_userid(message.from_user.id)
        if canDelete:
            bot.send_message(chat_id=message.chat.id, text='Booking deleted successfully.',
            reply_markup=keyboard.main_keyboard())
        else:
            bot.send_message(chat_id=message.chat.id, text='There is no booking associated with your account.',
            reply_markup=keyboard.main_keyboard())
    except:
        bot.send_message(chat_id=message.chat.id,
        text='Something is wrong, please try again.',
        reply_markup=keyboard.main_keyboard()
        )


while True:
    try:
        bot.polling(none_stop=False)
    except Exception:
        print('crash')
        time.sleep(1)