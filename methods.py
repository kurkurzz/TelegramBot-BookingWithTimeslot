import datetime as dt
import emoji
import firestore_service
from firestore_service import booking_list

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

def delete_past_booking():
    time_now = dt.datetime.now()
    for booking in booking_list:
        if booking.datetime < time_now:
            firestore_service.delete_booking_by_documentid(booking.id)
    
def check_input(text):
    #check if emoji
    if(text=='' or text[0][:1]=='/' or bool(emoji.get_emoji_regexp().search(text))):
        print('raising')
        raise Exception