import mysql.connector
import datetime
import time
from dateutil import relativedelta
from flask import Flask, session, jsonify, request 
import os
import traceback
import json

STATE = "WELCOME_ASK_NAME" 
cust_name = ""
is_nickname = ""
cust_nickname = ""
cust_birthday = ""
is_time_for_more = ""
cust_phone = ""
cust_color = ""
cust_type_of_salon = ""
is_reservation_now = ""
cust_date_obj = ""
cust_service_id = ""
cust_avail_msg = ""
cust_avail_display_options = []
cust_avail_option_list = []
cust_responses = {}
return_list_of_dicts = [] 

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
all_okay_message = """
All Okay.

"""

welcome_ask_name_message = """
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

old_is_nickname_message = """
とっても可愛いお名前ですね。
ニックネームはありますか？

1) はい
2) いいえ

Very lovely name, do you have a nickname? 

1) Yes
2) No

"""

is_nickname_message = """
とっても可愛いお名前ですね。
ニックネームはありますか？

Very lovely name, do you have a nickname? 

"""

new_is_nickname_options = """
1) はい / Yes
2) いいえ / No
"""

is_confirm_message = """
確認しますか？

Would You like to confirm?

"""

wrong_is_nickname_message = """
Please type a valid response which I can understand.
Press 1 for Yes or 2 for No.

"""

wrong_is_reservation_now_message = """
Please type a valid response which I can understand.
Press 1 for Yes or 2 for No.

"""

wrong_is_time_for_more_message = """
Please type a valid response which I can understand.
Press 1 for Yes or 2 for No.

"""

wrong_cust_type_of_salon_message = """
Please type a valid response which I can understand.

"""
wrong_cust_service_message = """
Please type a valid response which I can understand.

"""
wrong_cust_avail_options_message = """
Please type a valid response which I can understand.

"""



ask_nickname_message = """
ニックネームは何ですか？

What is your nickname?

"""

ask_birthday_message = """
いいですね。ありがとうございました（　　　　ちゃん/さん）。
今後も仲良くしてください。

お誕生日を教えていただけますか（….ちゃん/さん）？

Great, thank you (nickname chan/san), we are going to be best friends.


May I know your birthday (nickname chan/san)?

"""

old_is_time_for_more_message = """
そうなんですね。
もう少し質問に答えていただける時間はありますか？

1) はい、今から大丈夫です。
2) 今は難しいです。

oh, cool,
do you have time for more questions or we can talk later?

1) I can chat now  
2) let’s talk later 

"""

is_time_for_more_message = """
そうなんですね。
もう少し質問に答えていただける時間はありますか？

oh, cool,
do you have time for more questions or we can talk later?

"""

ask_phone_message = """
ありがとうございます。
電話番号を教えてください。

Oh, I’m so happy we can talk now 
What is your phone number?

"""

ask_color_message = """
ありがとうございます。
（….ちゃん/さん）、何色がお好きですか？

Thank you very much, 
(nickname chan/san), what is your favorite color?

"""

old_ask_type_of_salon_message = """
いい色ですよね。この色は・・・

どんな美容サロンが好きですか？

1) 早く仕上げてくれる。
2) 安い。
3) 静かなサロン。
4) 接客がとてもいいサロン。
5) 高級感のあるサロン。
6) スタッフの質が高いサロン。
7) 清潔感のあるサロン。
8) 落ち着いたサロン。


Oh nice color, this color represent ………

What type of beauty salons do you like?

1) Fast salon, 
2) Cheap price, 
3) Quite salon, 
4) Salon where I can have a good conversation and get good treatment, 
5) Expensive salon,
6) High quality salon staff 
7) Salon with cleanliness
8) Calm Salon

"""

ask_type_of_salon_message = """
いい色ですよね。この色は・・・

どんな美容サロンが好きですか？

Oh nice color, this color represent ………

What type of beauty salons do you like?
"""

is_reservation_now_message = """
わかりました。
お客様の期待に答えられるように、努めてまいります。

次回予約をお取りしましょうか？

I understand, I will always try to find you best options and best services for you, 

Would you like to make a reservation at your salon for next time? Or later?


"""

ask_date_message = """
かしこまりました。
ご予約のお日にちはいつがよろしいですか？

Oh, great, when you like to visit?

"""

ask_service_message = """"
メニューはお決まりですか？
What you like to do?

"""


empty_name_message = """
I am pretty sure you have a wonderful name.

Please tell me. I won't tell anyone.

"""

empty_nickname_message = """
Hmm.. I guess you forgot to type your nickname.

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
empty_color_message = """
I guess you forgot to enter your favourite color.

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


def check_new_availability(date_time_obj,employee_list,time_duration):

    result_dict = {}
    date_format = date_time_obj.strftime("%Y-%m-%d")
    time_format = date_time_obj.strftime("%H:%M:%S")
    for employee in employee_list:

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
            start_hour = start_time.seconds//3600
            start_minute = (start_time.seconds//60) % 60

            start_slot_number = start_hour * 2
            if start_minute >= 30 and start_minute <= 59:
                start_slot_number += 1
            
            end_hour = end_time.seconds//3600
            end_minute = (end_time.seconds//60) % 60

            end_slot_number = end_hour * 2

            if end_minute == 0:
                end_slot_number -= 1
            if end_minute > 30 and end_minute <= 59:
                end_slot_number += 1

            for i in range(start_slot_number,end_slot_number+1):
                employee_schedule[i] = 1

        num_of_slots_needed = time_duration * 2
        
        
        free_slots = []
        slot_i = 20 # Starting at 10:00 AM

        for i in range(3):
            #print("Iteration " + str(i) + " Started")
            zero_count = 0

            if i != 0 :     ## Increase slot number 
                slot_i += 1 ## from previous iteration

            while slot_i <= 44: # Ending search at 10:00 PM
                #print("Inside While Loop")
                #print("slot = " + str(slot_i))

                if employee_schedule[slot_i] == 1:
                    zero_count = 0
                else:
                    zero_count += 1

                if zero_count == num_of_slots_needed:
                    break
                slot_i += 1
        
            avail_end_slot = slot_i
            avail_start_slot = avail_end_slot - num_of_slots_needed + 1

            free_slots.append(avail_start_slot)
        result_dict[employee] = free_slots 


    return result_dict


def convert_avail_dict_to_display_options(avail_dict,emp_name_dict):
    avail_msg = "かしこまりました。次のお日にちで空きがあります。\n"
    avail_msg = avail_msg + "Okay, we have availability at the following times:\n"
    option_list = []
    
    display_options = []

    emp_serial = 1
    for emp_id in avail_dict:
        list_of_avail_slots = avail_dict[emp_id]
        for slot in list_of_avail_slots:
            time_start = slot_list[slot] 
        
            emp_bytearray_list = emp_name_dict[emp_id]
            emp_bytearray_firstelement = emp_bytearray_list[0]
            emp_name = emp_bytearray_firstelement.decode() ; emp_name 

            #avail_msg = avail_msg + "\n" + str(emp_serial) + ") " + emp_name + " is available at " + str(time_start)

            option_str = str(emp_serial) + ") " + emp_name + " is available at " + str(time_start)
            option_list.append(option_str) 
            option = [emp_serial,emp_id,slot]
            display_options.append(option)
        
            emp_serial += 1 
    
    #avail_msg = avail_msg + "\n" + str(emp_serial) + ") " + "None of the above times suit me.\n\n" 
    
    none_option_str = str(emp_serial) + ") " + "None of the above times suit me."
    option_list.append(none_option_str)

    none_option = [emp_serial,"none","none"]
    display_options.append(none_option)

    return avail_msg,display_options,option_list      

 
    



def type_of_salon_menu_int_to_name(argument):
    switcher = {
        1: "早く仕上げてくれる",
        2: "安い",
        3: "静かなサロン",
        4: "接客がとてもいいサロン",
        5: "高級感のあるサロン",
        6: "スタッフの質が高いサロン",
        7: "清潔感のあるサロン",
        8: "落ち着いたサロン"

    }

    return switcher.get(argument, "nothing")

def service_menu_int_to_id(argument):
    switcher = {
        1: 1,
        2: 3,
        3: 2
    }

    return switcher.get(argument, "nothing")







def service_numbers_to_strings(argument):
    switcher = {
        1: "nails",
        2: "beauty_treatment",
        3: "eye_lashes",
        4: "body",
        5: "hair_removal",
        6: "facial"
    }
    return switcher.get(argument, "nothing")



def welcome_the_user():
    return welcome_message

def welcome_ask_name():
    return welcome_ask_name_message

def is_nickname():
    is_nickname_options = ["1) はい / Yes", "2) いいえ / No"] 
    return is_nickname_message,is_nickname_options

def ask_nickname():
    return ask_nickname_message 

def ask_birthday():
    return ask_birthday_message

def is_time_for_more():
    is_time_for_more_options = ["1) はい、今から大丈夫です。/ I can chat now", "2) 今は難しいです。/ let’s talk later"]
    return is_time_for_more_message,is_time_for_more_options

def ask_phone():
    return ask_phone_message     

def ask_color():
    return ask_color_message

def ask_type_of_salon():
    ask_type_of_salon_options = ["1) 早く仕上げてくれる。/ Fast salon","2) 安い。/ Cheap price",
    "3) 静かなサロン。/ Quite salon","4) 接客がとてもいいサロン。/ Salon where I can have a good conversation and get good treatment",
    "5) 高級感のあるサロン。/ Expensive salon","6) スタッフの質が高いサロン。/ High quality salon staff","7) 清潔感のあるサロン。/ Salon with cleanliness",
    "落ち着いたサロン。/ Calm salon"]
    return ask_type_of_salon_message, ask_type_of_salon_options

def is_reservation_now():
    is_reservation_now_options = ["1) 予約を取る。/ Make a reservation","2) 後で予約を取る。/ Later"]

    return is_reservation_now_message,is_reservation_now_options

def ask_date():
    return ask_date_message

def ask_service():
    ask_service_options = ["1) ネイル / Nail","2) アイラッシュ / Eyelash","3) エステ / Aesthetic"]
    return ask_service_message, ask_service_options

def show_avail_options():
    return cust_avail_msg

def is_confirm():
    is_confirm_options = ["1) はい / Yes", "2) いいえ / No"]
    return is_confirm_message,is_confirm_options


     
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


def check_is_nickname(is_nickname_menu_int):
    
    is_nickname_status = 0

    try:
        is_nickname_menu_int = int(is_nickname_menu_int)
    except:
        is_nickname_status = 0
        is_nickname_response = None
        out_msg = wrong_is_nickname_message
        return is_nickname_status, is_nickname_response, out_msg

    
    if is_nickname_menu_int != 1 and is_nickname_menu_int != 2:
        is_nickname_status = 0
        is_nickname_response = None
        out_msg = wrong_is_nickname_message

    if is_nickname_menu_int == 1:
        is_nickname_status = 1
        is_nickname_response = "yes"
        out_msg = all_okay_message
      
    if is_nickname_menu_int == 2:
        is_nickname_status = 1 
        is_nickname_response = "no"
        out_msg = all_okay_message
    
    return is_nickname_status, is_nickname_response, out_msg 



def check_is_reservation_now(is_reservation_now_menu_int):
    
    is_reservation_now_status = 0

    try:
        is_reservation_now_menu_int = int(is_reservation_now_menu_int)
    except:
        is_reservation_now_status = 0
        is_reservation_now_response = None
        out_msg = wrong_is_reservation_now_message
        return is_reservation_now_status, is_reservation_now_response, out_msg

    
    if is_reservation_now_menu_int != 1 and is_reservation_now_menu_int != 2:
        is_reservation_now_status = 0
        is_reservation_now_response = None
        out_msg = wrong_is_reservation_now_message

    if is_reservation_now_menu_int == 1:
        is_reservation_now_status = 1
        is_reservation_now_response = "yes"
        out_msg = all_okay_message
      
    if is_reservation_now_menu_int == 2:
        is_reservation_now_status = 1 
        is_reservation_now_response = "no"
        out_msg = all_okay_message
    
    return is_reservation_now_status, is_reservation_now_response, out_msg 

       
def check_nickname(nickname):
    nickname_status = 0 
    if not nickname:
        nickname_status = 0 
        return nickname_status, empty_nickname_message
    else:
        nickname_status = 1
        return nickname_status, all_okay_message 


def check_is_time_for_more(is_time_for_more_menu_int):
    
    is_time_for_more_status = 0

    try:
        is_time_for_more_menu_int = int(is_time_for_more_menu_int)
    except:
        is_time_for_more_status = 0
        is_time_for_more_response = None
        out_msg = wrong_is_time_for_more_message
        return is_time_for_more_status, is_time_for_more_response, out_msg

    
    if is_time_for_more_menu_int != 1 and is_time_for_more_menu_int != 2:
        is_time_for_more_status = 0
        is_time_for_more_response = None
        out_msg = wrong_is_time_for_more_message

    if is_time_for_more_menu_int == 1:
        is_time_for_more_status = 1
        is_time_for_more_response = "yes"
        out_msg = all_okay_message
      
    if is_time_for_more_menu_int == 2:
        is_time_for_more_status = 1 
        is_time_for_more_response = "no"
        out_msg = all_okay_message
    
    return is_time_for_more_status, is_time_for_more_response, out_msg 


def check_cust_type_of_salon(cust_type_of_salon_menu_int):
    
    cust_type_of_salon_status = 0

    try:
        cust_type_of_salon_menu_int = int(cust_type_of_salon_menu_int)
    except:
        cust_type_of_salon_status = 0
        cust_type_of_salon_response = None
        out_msg = wrong_cust_type_of_salon_message
        return cust_type_of_salon_status, cust_type_of_salon_response, out_msg

    salon_type_name = type_of_salon_menu_int_to_name(cust_type_of_salon_menu_int)

    
    if salon_type_name == "nothing":
        cust_type_of_salon_status = 0
        cust_type_of_salon_response = None
        out_msg = wrong_cust_type_of_salon_message

    else:
        cust_type_of_salon_status = 1
        cust_type_of_salon_response = salon_type_name 
        out_msg = all_okay_message
   
    return cust_type_of_salon_status, cust_type_of_salon_response, out_msg 

def check_service(cust_service_menu_int):
    cust_service_status = 0
    try:
        cust_service_menu_int = int(cust_service_menu_int)
    except:
        cust_service_status = 0
        cust_service_response = None
        out_msg = wrong_cust_service_message
        return cust_service_status, cust_service_response, out_msg

    service_id = service_menu_int_to_id(cust_service_menu_int)

    
    if service_id == "nothing":
        cust_service_status = 0
        cust_service_response = None
        out_msg = wrong_cust_service_message

    else:
        cust_service_status = 1
        cust_service_response = service_id 
        out_msg = all_okay_message
   
    return cust_service_status, cust_service_response, out_msg 


def check_avail_options(cust_avail_options_menu_int, avail_display_options):
    cust_avail_options_status = 0
    try: 
        cust_avail_options_menu_int = int(cust_avail_options_menu_int)
    except:
        cust_avail_options_status = 0
        cust_avail_options_response = None 
        out_msg = wrong_cust_avail_options_message
        return cust_avail_options_status, cust_avail_options_response, out_msg

    #avail_options_id = avail_options_menu_int_to_id(cust_avail_options_menu_int)
    found = 0
    selected_option = [0,0,0]
    print("HELLO")
    for option in avail_display_options:
        print(option)
        print(option[0])
        if cust_avail_options_menu_int == option[0]:
            found = 1
            selected_option = option
     
    if found == 0:
        cust_avail_options_status = 0
        cust_avail_options_response = None 
        out_msg = wrong_cust_avail_options_message

    elif found == 1:
        cust_avail_options_status = 1
        cust_avail_options_response = selected_option 
        out_msg = all_okay_message
   
    return cust_avail_options_status, selected_option, out_msg 



def check_phone(phone):
    phone_status = 0 
    if not phone:
        phone_status = 0 
        return phone_status, empty_phone_message
    else:
        phone_status = 1
        return phone_status, all_okay_message 

def check_color(color):
    color_status = 0 
    if not color:
        color_status = 0 
        return color_status, empty_color_message
    else:
        color_status = 1
        return color_status, all_okay_message 


"""
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
"""

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
        return date_obj, date_status, all_okay_message



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


def old_ask_date():
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
    return "Index\n"

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
    global is_nickname
    global cust_nickname
    global cust_first_name
    global cust_birthday
    global is_time_for_more
    global cust_phone
    global cust_color
    global cust_type_of_salon 
    global is_reservation_now 
    global cust_date_obj 
    global cust_service_id
    global cust_avail_msg
    global cust_avail_display_options
    global cust_avail_option_list
    global cust_responses
    global return_list_of_dicts

    global service_int
    global date_obj
    global time_obj
    global date_time_obj
    global duration
    global emp_serial_id_dict

    json_input = request.json
    inp_msg  = json_input['message']
    print(inp_msg)

    if STATE == "WELCOME_ASK_NAME":
        out_msg = welcome_ask_name()
        STATE = "NAME_ASKED"
        out_dict = {"type" : "input", "question": out_msg, "answer": 0} 
        return_list_of_dicts.append(out_dict)
        #out_json = json.dumps(out_dict,ensure_ascii= False)
        out_json = json.dumps(return_list_of_dicts,ensure_ascii= False)
        return out_json
       
        
    if STATE == "NAME_ASKED":
        cust_name = inp_msg 
        name_st,out_msg = check_name(cust_name)
        if name_st == 1:
            cust_responses["name"] = cust_name
            return_list_of_dicts[-1]["answer"] = cust_name
            return_list_of_dicts[-1]["type"] = "text"
            STATE = "IS_NICKNAME" 
        else:
            return out_msg


    if STATE == "IS_NICKNAME":
        out_msg,option_list = is_nickname()
        STATE = "IS_NICKNAME_ASKED" 
        out_dict = {"type" : "option", "question": out_msg, "option_list": option_list, "answer": 0} 
        return_list_of_dicts.append(out_dict)
        out_json = json.dumps(return_list_of_dicts,ensure_ascii= False)
        return out_json
       

    if STATE == "IS_NICKNAME_ASKED":
        is_nickname_menu_int = inp_msg

        is_nickname_status,is_nickname_response,out_msg = check_is_nickname(is_nickname_menu_int)
                       
        if is_nickname_status == 1:
            cust_responses["is_nickname"] = is_nickname_response
            return_list_of_dicts[-1]["answer"] = is_nickname_response
            return_list_of_dicts[-1]["type"] = "text"
            if is_nickname_response == "yes":
                STATE = "ASK_NICKNAME"
            elif is_nickname_response == "no":
                STATE = "ASK_BIRTHDAY"
        else:
            return out_msg


    if STATE == "ASK_NICKNAME":
        out_msg = ask_nickname()
        STATE = "NICKNAME_ASKED"
        out_dict = {"type" : "input", "question": out_msg, "answer": 0} 
        return_list_of_dicts.append(out_dict)
        out_json = json.dumps(return_list_of_dicts,ensure_ascii= False)
        return out_json

    if STATE == "NICKNAME_ASKED":
        cust_nickname = inp_msg 
        nickname_status,out_msg = check_name(cust_nickname)
        if nickname_status == 1:
            cust_responses["nickname"] = cust_nickname
            return_list_of_dicts[-1]["answer"] = cust_nickname
            return_list_of_dicts[-1]["type"] = "text" 
            STATE = "ASK_BIRTHDAY" 
        else:
            return out_msg



    if STATE == "ASK_BIRTHDAY":
        out_msg = ask_birthday()
        STATE = "BIRTHDAY_ASKED"
        out_dict = {"type" : "input", "question": out_msg, "answer": 0} 
        return_list_of_dicts.append(out_dict)
        out_json = json.dumps(return_list_of_dicts,ensure_ascii= False)
        return out_json

    if STATE == "BIRTHDAY_ASKED":
        cust_birthday = inp_msg
        birthday_obj,birthday_status,out_msg = check_date(cust_birthday)
        birthday_str = str(birthday_obj)
        if birthday_status == 1:
            cust_responses["birthday"] = birthday_str
            return_list_of_dicts[-1]["answer"] = birthday_str
            return_list_of_dicts[-1]["type"] = "text"
            STATE = "IS_TIME_FOR_MORE"
        else:
            return out_msg


        
    if STATE == "IS_TIME_FOR_MORE":
        out_msg,option_list = is_time_for_more()
        STATE = "IS_TIME_FOR_MORE_ASKED"
        out_dict = {"type" : "option", "question": out_msg, "option_list": option_list, "answer": 0} 
        return_list_of_dicts.append(out_dict)
        out_json = json.dumps(return_list_of_dicts,ensure_ascii= False)
        return out_json


    if STATE == "IS_TIME_FOR_MORE_ASKED":
        is_time_for_more_menu_int = inp_msg

        is_time_for_more_status,is_time_for_more_response,out_msg = check_is_time_for_more(is_time_for_more_menu_int)
                       
        if is_time_for_more_status == 1:
            cust_responses["is_time_for_more"] = is_time_for_more_response
            return_list_of_dicts[-1]["answer"] = is_time_for_more_response
            return_list_of_dicts[-1]["type"] = "text"
            if is_time_for_more_response == "yes":
                STATE = "ASK_PHONE"
            elif is_time_for_more_response == "no":
                STATE = "IS_RESERVATION_NOW"
        else:
            return out_msg


    if STATE == "ASK_PHONE":
        out_msg = ask_phone()
        STATE = "PHONE_ASKED"
        out_dict = {"type" : "input", "question": out_msg, "answer": 0}
        return_list_of_dicts.append(out_dict) 
        out_json = json.dumps(return_list_of_dicts,ensure_ascii= False)
        return out_json

    if STATE == "PHONE_ASKED":
        cust_phone = inp_msg
        phone_status,out_msg = check_phone(cust_phone)
        if phone_status == 1:
            cust_responses["phone"] = cust_phone
            return_list_of_dicts[-1]["answer"] = cust_phone
            return_list_of_dicts[-1]["type"] = "text"
            STATE = "ASK_COLOR"
        else:
            return out_msg




    if STATE == "ASK_COLOR":
        out_msg = ask_color()
        STATE = "COLOR_ASKED"
        out_dict = {"type" : "input", "question": out_msg, "answer": 0}
        return_list_of_dicts.append(out_dict) 
        out_json = json.dumps(return_list_of_dicts,ensure_ascii= False)
        return out_json

    if STATE == "COLOR_ASKED":
        cust_color = inp_msg

        color_status,out_msg = check_color(cust_color)
        if color_status == 1:
            cust_responses["color"] = cust_color
            return_list_of_dicts[-1]["answer"] = cust_color
            return_list_of_dicts[-1]["type"] = "text"
            STATE = "ASK_TYPE_OF_SALON"
        else:
            return out_msg


    if STATE == "ASK_TYPE_OF_SALON": 
        out_msg,option_list = ask_type_of_salon()
        STATE = "TYPE_OF_SALON_ASKED"
        out_dict = {"type" : "option", "question": out_msg, "option_list": option_list, "answer": 0}
        return_list_of_dicts.append(out_dict) 
        out_json = json.dumps(return_list_of_dicts,ensure_ascii= False)
        return out_json

    if STATE == "TYPE_OF_SALON_ASKED":
        cust_type_of_salon_menu_int = inp_msg

        STATE = "IS_RESERVATION_NOW"

        cust_type_of_salon_status,cust_type_of_salon,out_msg = check_cust_type_of_salon(cust_type_of_salon_menu_int)
                       
        if cust_type_of_salon_status == 1:
            cust_responses["type_of_salon"] = cust_type_of_salon    
            return_list_of_dicts[-1]["answer"] = cust_type_of_salon
            return_list_of_dicts[-1]["type"] = "text" 

            STATE = "IS_RESERVATION_NOW"
        else:
            return out_msg



    if STATE == "IS_RESERVATION_NOW":
        out_msg,option_list = is_reservation_now()
        STATE = "IS_RESERVATION_NOW_ASKED"
        out_dict = {"type" : "option", "question": out_msg, "option_list": option_list, "answer": 0}
        return_list_of_dicts.append(out_dict) 
        out_json = json.dumps(return_list_of_dicts,ensure_ascii= False)
        return out_json


    if STATE == "IS_RESERVATION_NOW_ASKED":
        is_reservation_now_menu_int = inp_msg

        is_reservation_now_status,is_reservation_now_response,out_msg = check_is_reservation_now(is_reservation_now_menu_int)
                       
        if is_reservation_now_status == 1:
            cust_responses["is_reservation_now"] = is_reservation_now_response
            return_list_of_dicts[-1]["answer"] = is_reservation_now_response 
            return_list_of_dicts[-1]["type"] = "text" 
            if is_reservation_now_response == "yes":
                STATE = "ASK_DATE"
            elif is_reservation_now_response == "no":
                STATE = "GOOD_BYE"
        else:
            return out_msg


    if STATE == "ASK_DATE":
        out_msg = ask_date()
        STATE = "DATE_ASKED"
        out_dict = {"type" : "input", "question": out_msg, "answer": 0}
        return_list_of_dicts.append(out_dict) 
        out_json = json.dumps(return_list_of_dicts,ensure_ascii= False)
        return out_json

    if STATE == "DATE_ASKED":
        cust_date = inp_msg
        cust_date_obj,cust_date_status,out_msg = check_date(cust_date)
        cust_date_str = str(cust_date_obj)
        if cust_date_status == 1:
            cust_responses["date"] = cust_date_str
            return_list_of_dicts[-1]["answer"] = cust_date_str
            return_list_of_dicts[-1]["type"] = "text"
            STATE = "ASK_SERVICE"
        else:
            return out_msg


    if STATE == "ASK_SERVICE":
        out_msg,option_list = ask_service()
        STATE = "SERVICE_ASKED"
        out_dict = {"type" : "option", "question": out_msg, "option_list": option_list,"answer": 0} 
        return_list_of_dicts.append(out_dict)
        out_json = json.dumps(return_list_of_dicts,ensure_ascii= False)
        return out_json

    if STATE == "SERVICE_ASKED":

        cust_service_menu_int = inp_msg
        cust_service_status, cust_service_id, out_msg = check_service(cust_service_menu_int)
       
        if cust_service_status == 1:
            cust_responses["service"] = cust_service_id 
            return_list_of_dicts[-1]["answer"] = cust_service_id
            return_list_of_dicts[-1]["type"] = "text"
            relevant_employee_list = find_employees_for_service(cust_service_id)
            avail_emp_dict = check_new_availability(cust_date_obj,relevant_employee_list,duration)
            emp_name_dict = find_employee_name()
            cust_avail_msg, cust_avail_display_options ,cust_avail_option_list = convert_avail_dict_to_display_options(avail_emp_dict,emp_name_dict)
            
            # Cust Avail Display Options is in "short" format
            # Cust Avail Option List is in "full" format

            STATE = "SHOW_AVAIL_OPTIONS"
        else:
            return out_msg 

    if STATE == "SHOW_AVAIL_OPTIONS":
        out_msg = show_avail_options()
        STATE = "AVAIL_OPTIONS_SHOWN"
        out_dict = {"type" : "option", "question": out_msg, "option_list": cust_avail_option_list,"answer": 0}
        return_list_of_dicts.append(out_dict) 
        out_json = json.dumps(return_list_of_dicts,ensure_ascii= False)
        return out_json

    if STATE == "AVAIL_OPTIONS_SHOWN":
        cust_avail_options_menu_int = inp_msg
        cust_avail_options_status, cust_selected_option, out_msg = check_avail_options(cust_avail_options_menu_int,cust_avail_display_options)
        
        if cust_avail_options_status == 1:
            cust_responses["avail_options"] = cust_selected_option 
            return_list_of_dicts[-1]["answer"] = cust_selected_option 
            return_list_of_dicts[-1]["type"] = "text"

            STATE = "IS_CONFIRM"
        else:
            return out_msg 

    if STATE == "IS_CONFIRM":
        out_msg, option_list = is_confirm()
        STATE = "IS_CONFIRM_ASKED"
        out_dict = {"type" : "option", "question": out_msg, "option_list": option_list,"answer": 0}
        return_list_of_dicts.append(out_dict)
        out_json = json.dumps(return_list_of_dicts,ensure_ascii= False)
        return out_json



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



