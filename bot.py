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
Hi! I am Mirai 
I am your personal assistant.
"""

get_name_message = """
Tell me your name.
"""
empty_name_message = """
I am pretty sure you have a wonderful name.
Please tell me. I won't tell anyone.
"""

get_phone_message = """
Please let me know your phone number.
"""

empty_phone_message = """
I need your phone number to serve you better.
Don't worry I won't call you in odd hours. 
"""

get_service_message = """
Currently, we have 3 services:
1) Nails
2) Beauty treatment
3) Eye lashes
What would you like?
"""

wrong_service_message = """
Please choose a correct option from 1 to 3.
"""


get_date_message = """
What date would you like to visit our salon?

Example: enter 21-06-2019 for 21 June 2019
"""

wrong_date_message = """
Please enter the correct date in a format I understand.

Example: enter 21-06-2019 for 21 June 2019
"""


get_time_message = """
Alright!
    
What time would be convenient for you?

Example: enter 13:00 for 1pm
"""

wrong_time_message = """
Please enter the correct time in a format I understand.
    
Example: enter 13:00 for 1pm
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
                               host="34.85.64.241",
                               user="jts",
                               passwd="Jts5678?",
                               database="jtsboard_jts"
                               )
mycursor = mydb.cursor()

slot_list = ["00:00:00","00:30:00","01:00:00","01:30:00","02:00:00","02:30:00","03:00:00","03:30:00",
             "04:00:00","04:30:00","05:00:00","05:30:00","06:00:00","06:30:00","07:00:00","07:30:00",
             "08:00:00","08:30:00","09:00:00","09:30:00","10:00:00","10:30:00","11:00:00","11:30:00",
             "12:00:00","12:30:00","13:00:00","13:30:00","14:00:00","14:30:00","15:00:00","15:30:00",
             "16:00:00","16:30:00","17:00:00","17:30:00","18:00:00","18:30:00","19:00:00","19:30:00",
             "20:00:00","20:30:00","21:00:00","21:30:00","22:00:00","22:30:00","23:00:00","23:30:00"]


def find_employees_for_service(service_id):
    
    sql = "select service_id,id from employees where user_id = 102 and is_technician = 1 order by service_id"
    mycursor.execute(sql)
    
    
    myresult_list = mycursor.fetchall()
    
    service_dict = dict()
    
    for tuple in myresult_list:
        if tuple[0] in service_dict:
            service_dict[tuple[0]].append(tuple[1])
        else:
            service_dict[tuple[0]] = [tuple[1]]

    #service_dict[4] = [49]
    #service_dict[5] = [74,49,43]
    #service_dict[6] = [74,49,43]

    return service_dict[service_id]


def check_availability(service_int, date_time_obj,employee_list,time_duration):

    result_list = list()
    date_format = date_time_obj.strftime("%Y-%m-%d")
    time_format = date_time_obj.strftime("%H:%M:%S")
    for employee in employee_list:
        #print("Employee ID: " + str(employee))

        employee_schedule = []
        for i in range(48):
            employee_schedule.append(0)

        sql = "select service_id, employee_ids, start_date, start_time, end_time from reservations where user_id = 102 and reservation_type='1' and start_date = %s and employee_ids = %s"


        tuple = (date_format,employee)
        mycursor.execute(sql,tuple)

        appointments = mycursor.fetchall()

        for appointment in appointments:

            #print("--- appointment ---")
            
            service_id = appointment[0]
            employee_id = appointment[1]
            date = appointment[2]
            start_time = appointment[3]
            end_time = appointment[4]
            #print("Service ID: " + str(service_id))
            # print("Employee ID " + str(employee_id))
            #print("Date: " + str(date))

            #print("Start Time: " + str(start_time))

            #print("End Time: " + str(end_time))
            start_hour = start_time.seconds//3600
            start_minute = (start_time.seconds//60) % 60
            #print("Start Hour:" + str(start_hour))
            #print("Start Minute:" + str(start_minute))

            start_slot_number = start_hour * 2
            if start_minute >= 30 and start_minute <= 59:
                start_slot_number += 1

            #print("Start slot number:" + str(start_slot_number))



            #print("End Time: " + str(end_time))
            
            end_hour = end_time.seconds//3600
            end_minute = (end_time.seconds//60) % 60
            #print("End Hour:" + str(end_hour))
            #print("End Minute:" + str(end_minute))

            end_slot_number = end_hour * 2

            if end_minute == 0:
                end_slot_number -= 1
            if end_minute > 30 and end_minute <= 59:
                end_slot_number += 1


            #print("End slot number:" + str(end_slot_number))

            for i in range(start_slot_number,end_slot_number+1):
                employee_schedule[i] = 1


        #print("Employee Schedule")
        #for i in range(0,48):
           #print(str(slot_list[i]) + " " + str(employee_schedule[i]))

        num_of_slots_needed = time_duration * 2
        request_hour = int(date_time_obj.strftime("%H"))
        request_minute = int(date_time_obj.strftime("%M"))


        request_start_slot = request_hour * 2
        if request_minute >= 30 and request_minute <= 59:
                request_start_slot += 1

        """
        employee_unavailable = 0
        slot_iter_var = request_start_slot

        for i in range(num_of_slots_needed):
            if employee_schedule[slot_iter_var] != 0:
                employee_unavailable = 1
            slot_iter_var += 1
        
        if employee_unavailable == 1:
            print("Employee " + str(employee) + " Unavailable")
        else:
            print("Employee " + str(employee) + " Available")
        """
        #print("Request Start Slot: " + str(request_start_slot))


        zero_count = 0


        for slot_i in range (request_start_slot,48):
            #print("Employee Schedule: " + str(employee_schedule[slot_i]))

            if employee_schedule[slot_i] == 1:
                zero_count = 0
            else:
                zero_count += 1
            #print("Count after end of iteration " + str(slot_i) + " = " + str(zero_count))

            if zero_count == num_of_slots_needed:
                break

        avail_end_slot = slot_i
        avail_start_slot = avail_end_slot - num_of_slots_needed + 1

        avail_next_slot = avail_end_slot + 1

        #print("slot number:" + str(slot_i))

        #print("Employee " + str(employee) + " is available from " + str(slot_list[avail_start_slot]) + " to " + str(slot_list[avail_net_slot]))
        row_list = [employee,avail_start_slot,avail_next_slot]
        #print(row_list)
        result_list.append(row_list)

        #print("")
        #print("")
    #print("HI")
    #print("result List:")
    #print(result_list) 
    return result_list



    

"""
def check_availability(service_int, date_time_obj):

    date_format = date_time_obj.strftime("%Y-%m-%d")
    time_format = date_time_obj.strftime("%H:%M:%S")


    sql = "select service_id,employee_ids,start_date,start_time,end_time from reservations where user_id = 102 and reservation_type='1' and start_date = %s and start_time = %s and service_id = %s"

    date_tuple = (date_format,time_format,service_int)

    mycursor.execute(sql,date_tuple)

    myresult_list = mycursor.fetchall()

    myresult_first_tuple = myresult_list[0]

    service_id = myresult_first_tuple[0]
    employee_id = myresult_first_tuple[1]
    date = myresult_first_tuple[2]
    start_time = myresult_first_tuple[3]
    end_time = myresult_first_tuple[4]

    #print(myresult_list)
    print(service_id)
    print(employee_id)
    print(date)
    print(start_time)
    print(end_time)

"""


def service_numbers_to_strings(argument):
    switcher = {
        1: "nails",
        2: "beauty_treatment",
        3: "eye_lashes"
        #4: "body",
        #5: "hair_removal",
        #6: "facial"
    }
    return switcher.get(argument, "nothing")

"""
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
    tuple_ = (sm_state,sm_message)
    value = sm_policy[(tuple_)]
    new_state = value[0]
    new_message = value[1]
    response = input(new_message)
    return new_state,response
"""
def welcome_the_user():
    print(welcome_message)

def ask_name():
    name = input(get_name_message)
    while not name:
        name = input(empty_name_message)
    return name

def ask_phone():
    phone = input(get_phone_message)
    while not phone:
        phone = input(empty_phone_message)
    return phone


def ask_service():
    service_name = "nothing"
    print(get_service_message)

    while service_name == "nothing":
        service_input = input(wrong_service_message)
        
        service_int = None

        while service_int is None:
            try:
                service_int = int(service_input)
            except:
                service_input = input(wrong_service_message)

        service_name = service_numbers_to_strings(service_int)
        #print("Service:" + service)
    #print("Service:" + service)
    return service_int


def ask_date():
    date_str = input(get_date_message)
    date_obj = None

    while date_obj is None:

        try:
            date_obj = datetime.datetime.strptime(date_str, '%d-%m-%Y')
            #print ("DateObject:" + str(date_obj))
        except:
            #print(wrong_date_message)
            date_str = input(wrong_date_message)
    return date_obj

def ask_time():
    time_str = input(get_time_message)
    dummy_time_str = "01-01-2000 " + time_str

    time_obj = None

    while time_obj is None:
        
        try:
            time_obj = datetime.datetime.strptime(dummy_time_str, '%d-%m-%Y %H:%M')
            #print ("DateTimeObject:" + str(date_time_obj))
        except:
            #print(wrong_date_message)
            time_str = input(wrong_time_message)
            dummy_time_str = "01-01-2000 " + time_str
    return time_obj

def calc_date_time(date_obj,time_obj):
    inp_hour = time_obj.hour
    inp_minute = time_obj.minute
    date_time_obj = date_obj.replace(hour=inp_hour, minute=inp_minute)
    return date_time_obj


# PROGRAM STARTS HERE

welcome_the_user()
name = ask_name()
phone = ask_phone()
service_int = ask_service()
date_obj = ask_date()
time_obj = ask_time()
date_time_obj = calc_date_time(date_obj,time_obj)
relevant_employee_list = find_employees_for_service(service_int)
duration = 2
avail_emp_list = check_availability(service_int, date_time_obj,relevant_employee_list,duration)


 
print("")
for employee in avail_emp_list:
    emp_id = employee[0]
    start_slot = employee[1]
    next_slot = employee[2]
    time_start = slot_list[start_slot]
    time_end = slot_list[next_slot]
    
    print("Employee " + str(emp_id) + " is available from " + str(time_start) + " to " + str(time_end) )
    print(" ")



"""
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

    if state == BOOKING:

        availability,recommended = check_nail_availability(message)

        if availability == 0:
            print(confirm_sorry_message)
            state = BOOK_NAIL
        else:
            print("Done")
"""
