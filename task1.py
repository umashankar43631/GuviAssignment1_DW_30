import re
import os
import json
import mysql.connector

# loading the cursor from localhost
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)
mycursor = db.cursor(buffered=True)

mycursor.execute("CREATE DATABASE IF NOT EXISTS USERDB")

mycursor.execute("USE USERDB")

mycursor.execute("CREATE TABLE IF NOT EXISTS user(email VARCHAR(20) PRIMARY KEY, password VARCHAR(15))")

def isEmailValidOne(email):
    email_regex = r'^[^!1-9#@%!&][a-zA-Z][a-zA-Z1-9]+@[^\.][A-Za-z0-9]+\.[a-zA-Z]{2,4}\b'
    if (re.fullmatch(email_regex, email)):
        return True

def isPassValidOne(password):
    if (re.search(r'[a-z]', password) and 
            re.search(r'[A-Z]', password) and 
            re.search(r'[0-9]', password) and 
            re.search(r'[!@#$%\^&\*()-\+\\\:\",\.~]', password) and 
            len(password) > 5 and 
            len(password)<16 ): 
        return True


def UserForm():
    option = int(input("Choose the option by giving specific number \n \
    1. Login  \n \
    2. Registration \n\
    3. Forgot Password \n "))

    # Checking Valid options and proceeding Further
    if(option == 1 or option ==2 or option ==3):
        email = input("Enter your Mail Id to validate: ")
        email = email.lower()
        # Checking Email Valid or not
        isEmailValid = isEmailValidOne(email)

        if(option == 1 or option ==2):
            password = input("Enter the Password: ")
            # Checking Password Valid or not
            isPassValid = isPassValidOne(password)

        # We are checking only Email valid first because that is same for all the options
        if(isEmailValid):
            if(option == 3):
                sqlSt = "SELECT password from user where email = %s"
                val = (email,)
                mycursor.execute(sqlSt, val)
                x = mycursor.fetchall()
                
                if(x == None):
                    return "Go For Registration"
                else:
                    x = x[0][0]
                    return f"your Password is: {x}"
        
            elif((option ==1 or option ==2 ) and isPassValid):
                if(option == 2):
                    sqlSt = "INSERT INTO user(email, password) VALUES (%s, %s)"
                    val = (email, password)
                    mycursor.execute(sqlSt, val)
                    return "You are registerd Successfully"

                else:
                    # User selected option 1 (To Login)
                    sqlSt ="SELECT email from user where email=%s"
                    val = (email,)
                    x = mycursor.execute(sqlSt, val)
                    x = mycursor.fetchall()
                    if(x == None):
                        return "Go For Registration"
                    else:
                        return "Logged In Successfully"

            else:
                return "Password not Valid"
        else:
            return "Email not valid"

    # User Selected other than 1, 2 or 3
    else:
        return "Invalid Option"



print(UserForm())