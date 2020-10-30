import telebot
import time
import firestore_service
from booking import Booking
from firestore_service import booking_list
import keyboard
# import methods
import emoji
from credentials import TOKEN
import datetime as dt

bot = telebot.TeleBot(token=TOKEN)

#triggered when '/start'
#bot send intro message
@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        bot.send_message(chat_id=message.chat.id,
        text='Welcome to PetCare Reservation.\nTo make reservation please click /register.',
        reply_markup=keyboard.main_keyboard()
        )
    except:
        bot.send_message(chat_id=message.chat.id,
        text='Something is wrong, please try again.'
        )

#triggered when '/register'
@bot.message_handler(commands=['register'])
def register(message):
    date = ''
    try:
        new_booking = Booking()
        #code starts below
        #bot.register_next_step_handler is to wait for next input
        
        def get_name(message):
            try:
                check_input(message.text)
                new_booking.name = message.text
                bot.send_message(chat_id=message.chat.id, text='Please enter your phone number.')
                #if triggered, go to get_phonenumber method
                bot.register_next_step_handler(message,get_phonenumber)
            except:
                bot.send_message(chat_id=message.chat.id, text='Something is wrong, please try again.',reply_markup=keyboard.main_keyboard())

        def get_phonenumber(message):
            try:
                check_input(message.text)
                new_booking.phone_number = message.text
                bot.send_message(chat_id=message.chat.id, text='Please enter your pet\'s name.')
                #if triggered, go to get_petname method
                bot.register_next_step_handler(message,get_petname)
            except:
                bot.send_message(chat_id=message.chat.id, text='Something is wrong, please try again.',reply_markup=keyboard.main_keyboard())

        def get_petname(message):
            try:
                check_input(message.text)
                new_booking.pet_name = message.text
                bot.send_message(chat_id=message.chat.id, 
                text='Please select a date.',
                reply_markup=keyboard.date_keyboard()
                )
                #if triggered, go to get_date method
                bot.register_next_step_handler(message,get_date)
            except:
                bot.send_message(chat_id=message.chat.id, text='Something is wrong, please try again.',reply_markup=keyboard.main_keyboard())

        def get_date(message):
            try:
                check_input(message.text)
                nonlocal date
                date = message.text
                bot.send_message(chat_id=message.chat.id,text='Please select a time slot.',reply_markup=keyboard.time_keyboard())
                #if triggered, go to get_time method
                bot.register_next_step_handler(message,get_time)
            except:
                bot.send_message(chat_id=message.chat.id, text='Something is wrong, please try again.',reply_markup=keyboard.main_keyboard())

        def get_time(message):
            try:
                check_input(message.text)
                hour = message.text
                converted_time = convert_string_to_datetime(date,hour)
                exist = False
                same_time = 0
                #check if user_id already exist. if exist, cannot register
                for booking in booking_list:
                    if booking.user_id==message.from_user.id:
                        exist = True
                        break
                    if booking.time_slot == converted_time.timestamp():
                        same_time +=1
                if not exist:
                    #check if timeslot is full (default value is 3). if full, cannot register
                    if(same_time < 3):
                        new_booking.time_slot = int(converted_time.timestamp())
                        new_booking.user_id = message.from_user.id
                        firestore_service.add_booking(new_booking)
                        bot.send_message(chat_id=message.chat.id, text='Registration successful.',reply_markup=keyboard.main_keyboard())
                    else:
                        bot.send_message(chat_id=message.chat.id, text='Booking for that time is full. please try other time.',reply_markup=keyboard.main_keyboard())
                else:
                    bot.send_message(chat_id=message.chat.id, text='Registration failed. You already made a booking.',reply_markup=keyboard.main_keyboard())
            except:
                bot.send_message(chat_id=message.chat.id, text='Something is wrong, please try again.',reply_markup=keyboard.main_keyboard())
        
        #code start here
        bot.send_message(chat_id=message.chat.id, text='Please enter your name.')
        #go to get_name method
        bot.register_next_step_handler(message,get_name)
        
    except:
        bot.send_message(chat_id=message.chat.id,
        text='Something is wrong, please try again.'
        )
        
#triggered when '/bookinglist'
@bot.message_handler(commands=['bookinglist'])
def send_booking_list(message):
    try:
        delete_past_booking()
        bot.send_message(chat_id=message.chat.id,text=firestore_service.display,
        reply_markup=keyboard.main_keyboard())
    except:
        bot.send_message(chat_id=message.chat.id,
        text='Something is wrong, please try again.',
        reply_markup=keyboard.main_keyboard()
        )

#triggered when '/withdraw'
@bot.message_handler(commands=['withdraw'])
def send_Message(message):
    try:
        #check if booking connected to the user_id exist. return true if exist
        can_delete = firestore_service.delete_booking_by_userid(message.from_user.id)
        if can_delete:
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

#triggered when '/help'
@bot.message_handler(commands=['help'])
def send_help(message):
    try:
        bot.send_message(chat_id=message.chat.id,text=
        '''
        Guide to use this bot.\n
    to book a slot, click /register
    to check booked slot list, click /bookinglist
    to withdraw, click /withdraw
        ''',
        reply_markup=keyboard.main_keyboard()
        )
    except:
        bot.send_message(chat_id=message.chat.id,
        text='Something is wrong, please try again.',
        reply_markup=keyboard.main_keyboard()
            )  

#convert string of date and time to datetime format
def check_input(text):
    #check if emoji
    if(text=='' or text[0][:1]=='/' or bool(emoji.get_emoji_regexp().search(text))):
        print('raising')
        raise Exception

#delete booking that already past time now
def delete_past_booking():
    time_now = dt.datetime.now()
    for booking in booking_list:
        if booking.datetime < time_now:
            firestore_service.delete_booking_by_documentid(booking.id)

#check text input from gif/emoji/empty string to prevent any error
#throw exception if false
def convert_string_to_datetime(date,hour):
    time_now = dt.datetime.now()       
    year = ''
    prob_date = dt.datetime.strptime(date+'/'+str(time_now.year),r'%d/%m/%Y')
    if(prob_date<time_now):
        year = str(time_now.year+1)
    else:
        year = str(time_now.year)
    date += '/'+ str(year)
    time = date + ' ' + hour
    converted_time = dt.datetime.strptime(time,r'%d/%m/%Y %H:%M')
    return converted_time

while True:
    try:
        bot.polling(none_stop=False)
    except Exception:
        print('crash')
        time.sleep(1)