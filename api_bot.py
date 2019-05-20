import mysql.connector
import datetime
import time
from dateutil import relativedelta
from flask import Flask, session, jsonify, request 
import os
import traceback

STATE = 0 
cust_name = ""
cust_first_name = "" 
cust_phone = ""
service_int = 0
date_obj = 0
time_obj = 0
date_time_obj = 0
duration = 2
emp_serial_id_dict = dict()


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

old_welcome_message = """
Hey There! I am Mirai. 

I am your personal assistant.
I'm pleased to talk to you.

Firstly, I would  want to know a little bit about you.
Please tell me your name. 

"""


welcome_message = """
こんにちは。アプリ登録ありがとうございます。
私の名前はミライです。
私は、あなた専属の美容コンシェルジュです。
サロンの予約受付は私が行います。
さらに、
サロンのこと、
美容のこと、
わからないことがあれば何でも解決策を考えます。
知りたい情報はいち早くお伝えいたします。
あなたの人生が楽しく、そして快適に過ごせるように・・・
全力でお手伝いいたします。
どうぞよろしくお願いいたします。

あなたのお名前は？

Hi, thank you for registering at my application,
my name is Mirai, I will be your personal assistant for beauty,
I will help you to make reservations at your favorite salons,
I will help you to get good deals and I will always find best solutions for you,
I will try to make your life easier and much more fun for you,
I will always try to learn more about you and this will help me to recommend best options for you according to your taste and preferences, also I will help you to find best and newest cosmetics in the market, I will always be on your side trying to find best things for you,

What is your name?

"""


empty_name_message = """
I am pretty sure you have a wonderful name.

Please tell me. I won't tell anyone.

"""

good_name_message = """
That's a nice name, {}. 

Please let me know your phone number as well.

"""

good_phone_message = """
Thanks for the number.

Currently, we have 3 services:

1) Nails
2) Beauty treatment
3) Eye lashes

What would you like?

"""

empty_phone_message = """
I need your phone number to serve you better.
Don't worry I won't call you in odd hours. 

"""


wrong_service_message = """
Please choose a correct option from 1 to 3.

"""

good_service_message = """
Sounds Good.

What date would you like to visit our salon?

Example: enter 21-06-2019 for 21 June 2019.

"""

wrong_date_message = """
Please enter the correct date in a format I understand.

Example: enter 21-06-2019 for 21 June 2019

"""

good_date_message = """
Alright!
    
What time would be convenient for you?

Example: enter 13:00 for 1pm

"""
good_time_message = """
Checking availablity of our staff.

Please wait.

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


policy = {
    (WELCOME, "nails"): (BOOK_NAIL, select_date_message),
    (BOOK_NAIL, "confirm"): (BOOKED, exit_message),
}


local_connection = mysql.connector.connect(
                               host="localhost",
                               user="root",
                               passwd="12345678",
                               database="test"
                               )

local_cursor = local_connection.cursor()



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



def insert_into_chats_db(name,phone,date,start_time,end_time,emp_id):
    sql = "insert into chats values(default,%s,%s,%s,%s,%s,%s)"
    insert_tuple = (name,phone,date,start_time,end_time,emp_id)
    local_cursor.execute(sql,insert_tuple)
    local_connection.commit()
  


def find_employee_name():
    sql = "select id,name from employees where user_id = 102 and is_technician = 1 order by service_id "
    mycursor.execute(sql)
        
    myresult_list = mycursor.fetchall()
    emp_name_dict = dict()
        
    for emp_tuple in myresult_list:
            emp_name_dict[emp_tuple[0]] = [emp_tuple[1]]

    return emp_name_dict


def find_employees_for_service(service_id):
    
    sql = "select service_id,id from employees where user_id = 102 and is_technician = 1 order by service_id"
    mycursor.execute(sql)
    
    
    myresult_list = mycursor.fetchall()
    
    service_dict = dict()
    
    for serv_tuple in myresult_list:
        if serv_tuple[0] in service_dict:
            service_dict[serv_tuple[0]].append(serv_tuple[1])
        else:
            service_dict[serv_tuple[0]] = [serv_tuple[1]]

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
    return welcome_message

def ask_name():
    return get_name_message

def check_name(name):
    name_status = 0 
    if not name:
        name_status = 0 
        return name_status, empty_name_message
    else:
        name_status = 1
        return name_status, good_name_message 

def ask_phone():
    return get_phone_message

def check_phone(phone):
    phone_status = 0 
    if not phone:
        phone_status = 0 
        return phone_status, empty_phone_message
    else:
        phone_status = 1
        return phone_status, good_phone_message 


def check_service(service_inp):
    service_status = 0
    service_name = "nothing"
    service_int = None

    try:
        service_int = int(service_inp)
    except:
        service_status = 0
        return service_status, wrong_service_message

    service_name = service_numbers_to_strings(service_int)

    if service_name == "nothing":
        service_status = 0
        return service_int, service_status, wrong_service_message
    else:
        service_status = 1
        return service_int, service_status, good_service_message

def check_date(date_inp):
    date_status = 0
    date_obj = None

    try:
        date_obj = datetime.datetime.strptime(date_inp, '%d-%m-%Y')
    except:
        date_status = 0
        return date_obj, date_status, wrong_date_message
    
    if date_obj is None:
        date_status = 0
        return date_obj, date_status, wrong_date_message
    else:
        date_status = 1
        return date_obj, date_status, good_date_message



def check_time(time_inp):
    time_status = 0
    dummy_time_inp = "01-01-2000 " + time_inp
    time_obj = None

    try:
        time_obj = datetime.datetime.strptime(dummy_time_inp, '%d-%m-%Y %H:%M')
        print("Time Obj: " + str(time_obj))
    except:
        time_status = 0
        return time_obj, time_status, wrong_time_message
    
    if time_obj is None:
        time_status = 0
        return time_obj, time_status, wrong_time_message
    else:
        time_status = 1
        return time_obj, time_status, good_time_message


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

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    session['user'] = 'Anthony'
    return "Index"

@app.route('/getsession')
def getsession():
    if 'user' in session:
        return session['user']
    return "Not logged in!"

@app.route('/dropsession')
def dropsession():
    session.pop('user', None)
    return "dropped"

@app.route('/chat', methods=['POST'])
def chat():
    global STATE
    global cust_name
    global cust_first_name
    global cust_phone
    global service_int
    global date_obj
    global time_obj
    global date_time_obj
    global duration
    global emp_serial_id_dict

    json_input = request.json
    inp_msg  = json_input['message']
    print(inp_msg)

    if STATE == 0:
        out_msg = welcome_the_user()
        STATE += 1
        return out_msg 
    
    if STATE == 1:
        cust_name = inp_msg
        name_st,out_msg = check_name(cust_name)
        if name_st == 1:
            name_break = cust_name.split()
            cust_first_name = name_break[0]
            STATE += 1
            return out_msg.format(cust_first_name)
        else:
            return out_msg

    if STATE == 2:
        cust_phone = inp_msg
        phone_st,out_msg = check_phone(cust_phone)
        if phone_st == 1:
            STATE += 1
            return out_msg
        else:
            return out_msg

    if STATE == 3:
        service_int,service_st,out_msg = check_service(inp_msg)
        if service_st == 1:
            STATE += 1
            return out_msg
        else:
            return out_msg

    if STATE == 4:
        date_obj,date_st,out_msg = check_date(inp_msg)
        if date_st == 1:
            STATE += 1
            return out_msg
        else:
            return out_msg    


    if STATE == 5:
        time_obj,time_st,out_msg = check_time(inp_msg)
        if time_st == 1:
            date_time_obj = calc_date_time(date_obj,time_obj)
            relevant_employee_list = find_employees_for_service(service_int)
            avail_emp_list = check_availability(service_int, date_time_obj,relevant_employee_list,duration)
            emp_name_dict = find_employee_name()
            avail_msg = ""
            

            emp_serial = 1
            for employee in avail_emp_list:
                emp_id = employee[0]
                start_slot = employee[1]
                next_slot = employee[2]
                time_start = slot_list[start_slot]
                time_end = slot_list[next_slot]

                emp_bytearray_list = emp_name_dict[emp_id]
                emp_bytearray_firstelement = emp_bytearray_list[0]
                emp_name = emp_bytearray_firstelement.decode() ; emp_name 

                avail_msg = avail_msg + "\n" + str(emp_serial) + ") " + emp_name + " is available from " + str(time_start) + " to " + str(time_end)
                
                emp_serial_id_dict[emp_serial] = [emp_id,time_start,time_end]

                emp_serial += 1 

            avail_msg = avail_msg + "\n\nPlease choose your staff.\n\n"
              
            STATE += 1

            return avail_msg
        else:
            return out_msg
        
    if STATE == 6:

        print("EMP SER DICT")
        print(emp_serial_id_dict)
        inp_msg_int = int(inp_msg)
        result_list = emp_serial_id_dict[inp_msg_int]

        emp_id = result_list[0]
        time_start = result_list[1]
        time_end = result_list[2]
        date_format = date_time_obj.strftime("%Y-%m-%d")

        insert_into_chats_db(cust_name,cust_phone,date_format,time_start,time_end,emp_id)
         
   
    return "Cheese"




if __name__ == '__main__':
    app.run(debug=True)



