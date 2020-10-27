import datetime as dt
import firestore_service
from firestore_service import bookingList

def convert_string_to_datetime(date,hour):
    timenow = dt.datetime.now()       
    year = ''
    probdate = dt.datetime.strptime(date+'/'+str(timenow.year),r'%d/%m/%Y')
    if(probdate<timenow):
        year = str(timenow.year+1)
    else:
        year = str(timenow.year)
    date += '/'+ str(year)
    time = date + ' ' + hour
    timeconverted = dt.datetime.strptime(time,r'%d/%m/%Y %H:%M')
    return timeconverted

def delete_past_booking():
    timenow = dt.datetime.now()
    for booking in bookingList:
        if booking.datetime < timenow:
            firestore_service.delete_booking_by_documentid(booking.id)
    
