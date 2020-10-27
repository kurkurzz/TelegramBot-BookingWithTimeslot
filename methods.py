import datetime as dt

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