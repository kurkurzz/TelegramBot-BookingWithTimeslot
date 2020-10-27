import datetime as dt

class Booking:
    def __init__(self):
        self.userid = ''
        self.name =''
        self.petname = ''
        self.timeslot = 0
        self.id = ''

    def to_dict(self):
        return {
            'name' : self.name,
            'petname' : self.petname,
            'timeslot' : self.timeslot,
            'userid' : self.userid
        }

    #convert data from db to class
    def from_dict(self,dict,id):
        self.name = dict['name']
        self.petname = dict['petname']
        self.timeslot = int(dict['timeslot'])    
        self.userid = dict['userid']  
        self.id = id
        self.datetime = dt.datetime.fromtimestamp(self.timeslot)
        return self

    def __str__(self):
        return self.id + " - " + str(self.timeslot)