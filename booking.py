import datetime as dt

class Booking:
    def __init__(self):
        self.user_id = ''
        self.name =''
        self.pet_name = ''
        self.time_slot = 0
        self.id = ''
        self.phone_number = ''

    def to_dict(self):
        return {
            'name' : self.name,
            'petname' : self.pet_name,
            'timeslot' : self.time_slot,
            'userid' : self.user_id,
            'phonenumber' : self.phone_number
        }

    #convert data from db to class
    def from_dict(self,dict,id):
        self.name = dict['name']
        self.pet_name = dict['petname']
        self.time_slot = int(dict['timeslot'])    
        self.user_id = dict['userid']  
        self.phone_number = dict['phonenumber']  
        self.id = id
        self.datetime = dt.datetime.fromtimestamp(self.time_slot)
        return self

    def __str__(self):
        return self.id + " - " + str(self.time_slot)