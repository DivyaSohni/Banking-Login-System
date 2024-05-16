### send attachment####
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import pandas as pd

import mysql.connector as sql

def file_create(tbl_name):
    try:
        con = sql.connect(host = 'localhost',user = 'root',password = '*****',database = 'userdata')

    except Exception as e:
        print(f'{e}')
    else:   
        print('connection stablished')

        statement = {'Date': [],'Deposit':[],'Withdraw':[],'Balance':[] }

        cur = con.cursor()
        
        query = f'select * from {tbl_name}'
        cur.execute(query)
        data = cur.fetchall()
        # print(data)
        for i in data:
            # print(i)
            # print(i[1], i[2],i[3])
            d = str(i[0]).split("-")
            dt = "-".join((d[2],d[1],d[0]))
            statement['Date'].append(dt)
            statement['Deposit'].append(i[1])
            statement['Withdraw'].append(i[2])
            statement['Balance'].append(i[3])
        # print(statement)
        df = pd.DataFrame(statement)
        df.to_excel('statement.xlsx',index = False)
        # print(df)
        




def send_email_attachment(user_email_id, fn_name):

        # print(otp)
        sender_email = "*"
        sender_password = "*"
        reciver_email = user_email_id 
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = reciver_email
        msg['Subject'] = 'Statement From Python Bank'
        body = 'Please find the atteched bank Statement'
        msg.attach(MIMEText(body,'plain'))

        fn = fn_name
        with open (fn, 'rb') as f:
            attachment = MIMEApplication(f.read(),_subtype ='xlsx')
            attachment.add_header('content-Disposition','attachement',filename = fn)
            msg.attach(attachment) 

                   

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("*", "*")         
        s.send_message(msg)

        os.remove(fn) # to delete after send the email



file_create('manthan')
send_email_attachment("*", 'statement.xlsx')
