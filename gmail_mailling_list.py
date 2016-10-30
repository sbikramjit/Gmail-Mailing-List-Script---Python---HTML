'''Required files: 'MailAdresses.txt' containing a list of mail addresses
                   'Message.txt' containing your mail written in html'''

import os
import smtplib
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


global key

key = '123456789' # create new & store somewhere safe

def read_doc(file) :

    file = open(file,'r')
    data = []
    i = 0
    for line in file :

        data.append(line.rstrip()) 
        i += 1
        
    file.close()
    return data

def write_doc(file, data) :

    file = open(file,'w')
    for line in data :
        file.write(line + "\n")
        
    file.close()
    return 

def encode(string): # uses global key
    enc = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(string[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def decode(string) : # uses global key
    dec = []
    enc = base64.urlsafe_b64decode(string).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

def read_html() : # reads the message file

    file = open("Message.txt",'r')
    message = file.read().rstrip()    
    file.close()
    return message

    
def send_mail(data) :

    # Personal Data needed for log in
    gmail_user = decode(data[0])  
    gmail_password = decode(data[1])


    
    FROM = gmail_user
    TO = read_doc("MailAdresses.txt")
    SUBJECT = "Your Subject"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT


    # Write content of mail using html 
    html = read_html()
    mail_cont= MIMEText(html, 'html')
    msg.attach(mail_cont)

    # Sending process
    server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server_ssl.ehlo()
    server_ssl.login(gmail_user, gmail_password)

    for adress in TO :
        server_ssl.sendmail(FROM, adress, msg.as_string())
        print('Email to ' + adress + ' sent!')
        
    server_ssl.close()


def init() : # checks whether neccesary files "MailAdresses.txt" , "UserData.txt" exist and reads the user data into : data variable

    if not os.path.isfile("MailAdresses.txt") :
        print("Unable to locate 'MailAdresses.txt'. \nPlease make sure it's available and stored in the directory.\n")
        exit(1)

    if not os.path.isfile("Message.txt") :
        print("Unable to locate 'Message.txt'. \nPlease make sure it's available and stored in the directory.\n")
        exit(1)
        
    if os.path.isfile("UserData.txt") :
        data = read_doc("UserData.txt")
        return data
    
    else :
        user_name = input("Please enter your mailadress [username@gmail.com] : \n")
        pw = input("Please enter your password : \n")
        data = [encode(user_name), encode(pw)]
        write_doc("UserData.txt", data)
        return data
        
data = init()
send_mail(data)
