import mysql.connector
import datetime
import time
from dateutil import relativedelta


mydb = mysql.connector.connect(
                               host="34.85.64.241",
                               user="jts",
                               passwd="Jts5678?",
                               database="jtsboard_jts"
                               )

mycursor = mydb.cursor()

local_connection = mysql.connector.connect(
                               host="localhost",
                               user="root",
                               passwd="12345678",
                               database="test"
                               )

local_cursor = local_connection.cursor()

def insert_into_chats_db(name,email,date,start_time,end_time,emp_id):
    #sql = "insert into chats values(default,'samanvay', 's@s.com','2015-01-01 00:00:00', '17:00:00', '19:00:00',49)"
    #sql = "select * from chats"
    sql = "insert into chats values(default,%s,%s,%s,%s,%s,%s)"
    insert_tuple = (name,email,date,start_time,end_time,emp_id)
    local_cursor.execute(sql,insert_tuple)
    local_connection.commit()
  
  
   
i_name = "samanvay"
i_email = "s@s.com" 
i_date = "2015-01-01 00:00:00"
i_start_time = "13:00:00"
i_end_time = "15:00:00"
i_emp_id = 49

insert_into_chats_db(i_name,i_email,i_date,i_start_time,i_end_time,i_emp_id)   



slot_list = ["00:00:00","00:30:00","01:00:00","01:30:00","02:00:00","02:30:00","03:00:00","03:30:00",
             "04:00:00","04:30:00","05:00:00","05:30:00","06:00:00","06:30:00","07:00:00","07:30:00",
             "08:00:00","08:30:00","09:00:00","09:30:00","10:00:00","10:30:00","11:00:00","11:30:00",
             "12:00:00","12:30:00","13:00:00","13:30:00","14:00:00","14:30:00","15:00:00","15:30:00",
             "16:00:00","16:30:00","17:00:00","17:30:00","18:00:00","18:30:00","19:00:00","19:30:00",
             "20:00:00","20:30:00","21:00:00","21:30:00","22:00:00","22:30:00","23:00:00","23:30:00"]

def find_emp_name():
    sql = "select id,name from employees where user_id = 102 and is_technician = 1 order by service_id "
    mycursor.execute(sql)
    
    myresult_list = mycursor.fetchall()
    #print(myresult_list)
    emp_name_dict = dict()
    
    for emp_tuple in myresult_list:
            emp_name_dict[emp_tuple[0]] = [emp_tuple[1]]

    return emp_name_dict

def enter_details_into_db():
    sql = "insert into chat values(name, phone, date, start_time, end_time, service_id, staff_id)"
    local_cursor.execute(sql)


"""
my_dict= find_emp_name()

x = my_dict[49]
print(x)
y = x[0]
print(y)
s1 = y.decode() ; s1
print(type(s1))

#print(str(my_dict[49]))
"""

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

    service_dict[4] = [49]
    service_dict[5] = [74,49,43]
    service_dict[6] = [74,49,43]

    return service_dict[service_id]


def check_availability(service_int, date_time_obj,employee_list,time_duration):
    
    result_list = list() 
    date_format = date_time_obj.strftime("%Y-%m-%d")
    time_format = date_time_obj.strftime("%H:%M:%S")
    for employee in employee_list:
        print("Employee ID: " + str(employee))
        
        employee_schedule = []
        for i in range(48):
            employee_schedule.append(0)

        sql = "select service_id, employee_ids, start_date, start_time, end_time from reservations where user_id = 102 and reservation_type='1' and start_date = %s and employee_ids = %s"
        

        tuple = (date_format,employee)
        mycursor.execute(sql,tuple)

        appointments = mycursor.fetchall()
        
        for appointment in appointments:
            print("--- appointment ---")
            service_id = appointment[0]
            employee_id = appointment[1]
            date = appointment[2]
            start_time = appointment[3]
            end_time = appointment[4]
            #print("Service ID: " + str(service_id))
            # print("Employee ID " + str(employee_id))
            #print("Date: " + str(date))
            print("Start Time: " + str(start_time))
            #print("End Time: " + str(end_time))
            start_hour = start_time.seconds//3600
            start_minute = (start_time.seconds//60) % 60
            #print("Start Hour:" + str(start_hour))
            #print("Start Minute:" + str(start_minute))
            
            start_slot_number = start_hour * 2
            if start_minute >= 30 and start_minute <= 59:
                start_slot_number += 1
            
            #print("Start slot number:" + str(start_slot_number))

                

            print("End Time: " + str(end_time))
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
        
        #print("Employee " + str(employee) + " is available from " + str(slot_list[avail_start_slot]) + " to " + str(slot_list[avail_next_slot]))
        row_list = [employee,avail_start_slot,avail_next_slot]
        #print(row_list)
        result_list.append(row_list)
            
        print("")
        print("")
    #print("HI")
    #print("result List:")
    #print(result_list) 
    return result_list           


service_int = 3
date_time_str = "2019-03-16 17:00:00"
date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
relevant_employee_list = [49,55,74]
duration = 2

#x = check_availability(service_int, date_time_obj,relevant_employee_list,duration)
#print("HELLO")
#print(x)


"""
print(find_employees_for_service(1))
print(find_employees_for_service(2))
print(find_employees_for_service(3))
print(find_employees_for_service(4))
print(find_employees_for_service(5))
print(find_employees_for_service(6))
                        

myresult_first_tuple = myresult_list[0]

service_id = myresult_first_tuple[0]
employee_id = myresult_first_tuple[1]
date = myresult_first_tuple[2]
start_time = myresult_first_tuple[3]
end_time = myresult_first_tuple[4]

"""
