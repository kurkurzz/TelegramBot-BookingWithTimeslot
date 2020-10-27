from datetime import datetime, timedelta
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
                newBooking.name = message.text
                bot.send_message(chat_id=message.chat.id, text='Please enter your pet\'s name.')
                bot.register_next_step_handler(message,get_petname)
            except:
                bot.send_message(chat_id=message.chat.id, text='Something is wrong, please try again.',reply_markup=keyboard.main_keyboard())

        def get_petname(message):
            try:
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
                hour = message.text
                convertedtime = methods.convert_string_to_datetime(date,hour)
                print(convertedtime)
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
        # def get_date(message):
        #     try:
        #         timeslot = message.text
        #         convertedTime = dt.datetime.strptime(timeslot,r'%d/%m/%Y %I:%M %p')
        #         timenow = dt.datetime.now()
        #         if convertedTime.hour>8 and convertedTime.hour<17 and (convertedTime.minute==0 or convertedTime.minute==30) :
        #             if convertedTime>timenow and convertedTime<timenow+timedelta(days=14):
        #                 exist = False
        #                 sameTime = 0
        #                 for booking in bookingList:

        #                     if(booking.userid==message.from_user.id):
        #                         exist = True
        #                         break
        #                     # print(booking.timeslot+' '+convertedTime)
        #                     if booking.timeslot == convertedTime.timestamp():
        #                         sameTime +=1

        #                 if not exist:
            #                 if(sameTime < 3):
            #                     newBooking.timeslot = convertedTime.timestamp()
            #                     newBooking.userid = message.from_user.id
            #                     firestore_service.add_booking(newBooking)
            #                     bot.send_message(chat_id=message.chat.id, text='Registration successful.')
            #                 else:
            #                     bot.send_message(chat_id=message.chat.id, text='Booking for that time is full. please try other time.')                    
            #             else:
            #                 bot.send_message(chat_id=message.chat.id, text='Registration failed. You already made a booking.')
            #         else:
            #             bot.send_message(chat_id=message.chat.id, text='Booking failed. Please insert valid time and no gap longer than 14 days from now.')
            #     else:
            #         bot.send_message(chat_id=message.chat.id, text='Booking failed. Please insert time within 08:00 AM - 05:00 PM with 30 minutes interval.')
            # except:
            #      bot.send_message(chat_id=message.chat.id, text='Booking failed. Please insert correct time format.')
                

        bot.send_message(chat_id=message.chat.id, text='Please enter your name.')
        bot.register_next_step_handler(message,get_name)
        
    except:
        bot.send_message(chat_id=message.chat.id,
        text='Something is wrong, please try again.'
        )
        

@bot.message_handler(commands=['bookinglist'])
def send_booking_list(message):
    try:
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
        print(message.contact)
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
        canDelete = firestore_service.delete_booking(message.from_user.id)
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