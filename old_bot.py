import mysql.connector
import datetime
import time
from dateutil import relativedelta


WELCOME = 0
BOOK_NAIL = 1
CHECK_NAIL_DATE = 2
BOOKED = 3
BOOKING = 4

now = datetime.datetime.now()
now1= now + datetime.timedelta(days=1)
now2= now + datetime.timedelta(days=2)
now3= now + datetime.timedelta(days=3)
now4= now + datetime.timedelta(days=4)
now5= now + datetime.timedelta(days=5)
now6= now + datetime.timedelta(days=6)


# Define the messages

welcome_message = """
Hi! I am your personal assistance.
How may I help you?
Currently, we have 3 services:
1) nails
2) eyelashes
3) facial
"""

select_date_message = """
Okay, Please tell me which date.
1) %s
2) %s
3) %s
4) %s
5) %s
6) %s
7) %s
"""  % (now.strftime("%Y-%m-%d"),now1.strftime("%Y-%m-%d"),now2.strftime("%Y-%m-%d"),now3.strftime("%Y-%m-%d"),now4.strftime("%Y-%m-%d"),now5.strftime("%Y-%m-%d"),now6.strftime("%Y-%m-%d"))

sorry_recommend_message = """
Sorry, This day is not available.
I recommend that you schedule an appointment for %s
"""

available_recommend_message = """
This day is available !!!
However, I recommend that you schedule an appointment for %s
"""
confirm_date_message = """
Please confirm your booking date.
"""
exit_message = """
Your appointment is booked.
I hope to see you soon.
"""

booking_message = """
Booking your appointment.
Please Wait.
"""
confirm_sorry_message = """
Sorry, This day is not available.
Please choose another date.
"""


# Define the policy rules
policy = {
    (WELCOME, "nails"): (BOOK_NAIL, select_date_message),
    (BOOK_NAIL, "confirm"): (BOOKED, exit_message),
}


mydb = mysql.connector.connect(
                               host="localhost",
                               user="root",
                               passwd="12345678",
                               database="test"
                               )
mycursor = mydb.cursor()

def check_nail_availability(date):
    
    available = 0
    
    date_time_str = str(date)
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
    date_format = date_time_obj.strftime("%Y-%m-%d")
    
    date_tuple = (date_format, )
    sql = "SELECT score FROM nails WHERE date = %s"
    mycursor.execute(sql,date_tuple)
    myresult_list = mycursor.fetchall()
    myresult_tuple = myresult_list[0]
    myresult = myresult_tuple[0]
    #print(date_format)
    #print(myresult)
    
    if myresult < 50:
        #print("available")
        available = 1
    
    next = []

    for x in range(1,7):
        next.append(date_time_obj + datetime.timedelta(days=x))
        
        #print(next)
        least = 100
        least_day = date_format
    
    for i in range(0,6):
        #print(next[i])
        new_date_format = next[i].strftime("%Y-%m-%d")
        #print(new_date_format)
        
        new_date_tuple = (new_date_format, )
        sql = "SELECT score FROM nails WHERE date = %s"
        mycursor.execute(sql,new_date_tuple)
        new_myresult_list = mycursor.fetchall()
        #print(new_myresult_list)
        new_myresult_tuple = new_myresult_list[0]
        #print(new_myresult_tuple)
        new_myresult = new_myresult_tuple[0]
        #print(new_date_format)
        #print(new_myresult)
        if new_myresult < least:
            least = new_myresult
            least_day = new_date_format

    #print("Availability:" + str(available))
    #print("Least Day:" + least_day)

    return available,least_day

#check_nail_availability('2019-05-15')







def send_message(sm_policy,sm_state,sm_message):
    tuple = (sm_state,sm_message)
    value = sm_policy[(tuple)]
    new_state = value[0]
    new_message = value[1]
    response = input(new_message)
    return new_state,response

state = WELCOME
message = input(welcome_message)

while state != BOOKED:
    state,message = send_message(policy,state,message)
    
    if state == BOOK_NAIL:
        
        availability,recommended = check_nail_availability(message)

        if availability == 0:
                        print(sorry_recommend_message % recommended)
        else:
            print(available_recommend_message % recommended)
        
        confirm_date = input(confirm_date_message)
        message = "confirm"

    """
    if state == BOOKING:

        availability,recommended = check_nail_availability(message)

        if availability == 0:
            print(confirm_sorry_message)
            state = BOOK_NAIL
        else:
            print("Done")
    """





        
        
    #state = BOOKED




