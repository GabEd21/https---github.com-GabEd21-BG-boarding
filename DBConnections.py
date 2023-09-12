import mysql.connector

mydb = mysql.connector.connect(host="localhost",user="root", password="5a*YMFEP", database="bg_boarding_house")
mycursor = mydb.cursor()

def add_text(username, password,first_name, middle_name, last_name, address, email, mobile_number, school, course, year, emergencyName, emergencyNumber, emergencyRelationship):
    sql = "INSERT INTO customer (Customer_UserName, Customer_Password, Customer_FirstName, Customer_MiddleName, Customer_LastName, Customer_Address, Customer_Email, Customer_MobileNumber, School, Course, SchoolYear, Customer_EmergencyContactName, Customer_EmergencyContactNumber, Customer_EmergencyContactRelationship) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (username, password, first_name, middle_name, last_name, address, email, mobile_number, school, course, year, emergencyName, emergencyNumber, emergencyRelationship)
    mycursor.execute(sql, val)
    mydb.commit()
    return 1