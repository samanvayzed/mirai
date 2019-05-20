import mysql.connector
import datetime
import time
from dateutil import relativedelta


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="12345678",
  database="test"
)
mycursor = mydb.cursor()

def check_nail_availability(date):

    available = 0

    #date = ('2019-05-18', )
    #score1 =  (40, )

    date_time_str = str(date)
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
    date_format = date_time_obj.strftime("%Y-%m-%d")

    date_tuple = (date_format, )
    sql = "SELECT score FROM busy WHERE date = %s"
    mycursor.execute(sql,date_tuple)
    myresult_list = mycursor.fetchall()
    myresult_tuple = myresult_list[0] 
    myresult = myresult_tuple[0]
    print(date_format)
    print(myresult)

    if myresult < 50:
        print("available")
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
        sql = "SELECT score FROM busy WHERE date = %s"
        mycursor.execute(sql,new_date_tuple)
        new_myresult_list = mycursor.fetchall()
        #print(new_myresult_list)
        new_myresult_tuple = new_myresult_list[0]
        #print(new_myresult_tuple)
        new_myresult = new_myresult_tuple[0]
        print(new_date_format)
        print(new_myresult)
        if new_myresult < least:
            least = new_myresult
            least_day = new_date_format

    print("Availability:" + str(available))
    print("Least Day:" + least_day)
                    
    return available,least_day



check_nail_availability('2019-05-15')


