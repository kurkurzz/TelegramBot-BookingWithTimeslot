from booking import Booking
import threading
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from booking import Booking

cred = credentials.Certificate("firebase-adminsdk.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()
booking_collection = db.collection(u'booking')
booking_list = []
display = 'There is a problem showing booking list.'

def add_booking(new_booking):
    print(new_booking.to_dict())
    booking_collection.document().set(new_booking.to_dict())

def delete_booking_by_userid(user_id):
    global booking_list
    for booking in booking_list:
        if(booking.user_id==user_id):
            booking_collection.document(booking.id).delete()
            return True
    return False

def delete_booking_by_documentid(id):
    booking_collection.document(id).delete()
    
def get_booking_list():
    # sorted_list = sorted(booking_list,key=lambda booking: booking.datetime)
    booking_list.sort(key=lambda booking: booking.datetime)
    dates = []
    to_display = 'List of booking.\n\n'
    dates.clear()
    for sorted_booking in booking_list:
        if not sorted_booking.datetime.date() in dates:
            dates.append(sorted_booking.datetime.date())

    for date in dates:
        to_display += str(date.day) +'/'+str(date.month) +'/'+str(date.year) +'\n'
        for sorted_booking in booking_list:
            if(sorted_booking.datetime.date()==date):
                to_display += sorted_booking.name +'   '+str(sorted_booking.datetime.hour)+':'+str(sorted_booking.datetime.minute)+'\n'
        to_display += '\n'
    return to_display


callback_done = threading.Event()
def on_snapshot(doc_snapshot, changes, read_time):
    global booking_list
    global display
    booking_list.clear()
    for doc in doc_snapshot:
        booking = Booking()
        booking.from_dict(doc.to_dict(),doc.id)
        booking_list.append(booking)
        print('id: ',booking,' ',doc.to_dict())
    print('\n')
    display = get_booking_list()
    callback_done.set()
# Watch the document
doc_watch = booking_collection.on_snapshot(on_snapshot)




        