from booking import Booking
import threading
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from booking import Booking

cred = credentials.Certificate("firebase-adminsdk.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()
bookingCollection = db.collection(u'booking')
bookingList = []
display = 'y'

def add_booking(newBooking):
    print(newBooking.to_dict())
    bookingCollection.document().set(newBooking.to_dict())

def delete_booking(userid):
    global bookingList
    for booking in bookingList:
        if(booking.userid==userid):
            bookingCollection.document(booking.id).delete()
            return True
    return False
        

callback_done = threading.Event()
def on_snapshot(doc_snapshot, changes, read_time):
    global bookingList
    global display
    bookingList.clear()
    print('latest snapshot')
    for doc in doc_snapshot:
        booking = Booking()
        booking.from_dict(doc.to_dict(),doc.id)
        bookingList.append(booking)
        print('id: ',booking,' ',doc.to_dict())
    print('\n')
    print(display)
    display = get_booking_list()
    print(display)
    callback_done.set()
# Watch the document
doc_watch = bookingCollection.on_snapshot(on_snapshot)



def get_booking_list():
    sortedList = sorted(bookingList,key=lambda booking: booking.datetime)
    dates = []
    todisplay = 'List of booking.\n\n'
    dates.clear()
    for sortedBooking in sortedList:
        if not sortedBooking.datetime.date() in dates:
            dates.append(sortedBooking.datetime.date())

    for date in dates:
        todisplay += str(date.day) +'/'+str(date.month) +'/'+str(date.year) +'\n'
        for sortedBooking in sortedList:
            if(sortedBooking.datetime.date()==date):
                todisplay += sortedBooking.name +'   '+str(sortedBooking.datetime.hour)+':'+str(sortedBooking.datetime.minute)+'\n'
        todisplay += '\n'

    return todisplay
        