import tkinter as tk
from tkinter import *
# from PIL import ImageTk
from PIL import ImageTk, Image
from tkinter import messagebox
import mysql.connector as sql
import random
from tkinter.messagebox import askyesno
from datetime import datetime as dtime

### send attachment####
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import pandas as pd



class Login:
    def __init__(self,root):
            self.root = root
            self.root.title("User Login ")
            self.root.geometry("1199x600+100+50")
            self.root.resizable(False,False)
            self.bg =ImageTk.PhotoImage(file='C:/Users/Divya sohani/Desktop/pyprojects/banking login system/Images/loginbg.jpg')
            self.bg_image = Label(self.root,image=self.bg).place(x = 0,y=0,relwidth=1,relheight=1)

            try:
                self.con = sql.connect(host = 'localhost',user = 'root',password = 'mysql@123',database = 'userdata')

            except:
                messagebox.showerror('Error',"Database Connectivity Issue Try Again")
            else:
                pass   
                # print('connection stablished')

#################### OTP function #######################################
    def send_email(self,user_email_id,otp):
        # print(otp)
        user_email = user_email_id               ########### jis email pr bhejna hai otp 

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("sohnid3@gmail.com", "ucvzcpaewaeiujzr")         ######## is email se bhejna hai or ye passkey hai mere email ki 
        s.sendmail('BANK PASSWORD',user_email,str(otp))               

#################### main page #######################################
    def first_page(self):
            def forword_to_login_page():
                first_page_fm.destroy()
                root.update()
                self.login_window()

            def forword_to_forget_password():
                 first_page_fm.destroy()
                 root.update()
                 self.forget_password()

            def forword_to_registration_page():
                 first_page_fm.destroy()
                 root.update()
                 self.registration_page()
                 
            first_page_fm = Frame(self.root,bg='light blue')
            first_page_fm.place(x=85,y=150,height=418,width=500)
            heading_lbl = Label(first_page_fm,text='Welcome To HDFC Bank',font=('Impact',35,'bold'),bg='light blue',fg='#00154f').place(x = 12,y=30)

            registration_btn = Button(first_page_fm,text='Register Here',bg='#00154f',fg='light blue',font=('Goudy old style',20,'bold'),bd=0,activeforeground='light blue',activebackground='#00154f',cursor='hand2',command=forword_to_registration_page)
            registration_btn.place(x = 200,y = 130,width = 260)

            login_btn = Button(first_page_fm,text='Login Here',bg='#00154f',fg='light blue',font=('Goudy old style',20,'bold'),bd=0,activeforeground='light blue',activebackground='#00154f',cursor='hand2',command=forword_to_login_page)
            login_btn.place(x = 200,y = 210,width = 260)

            forget_btn = Button(first_page_fm,text='Forget Password',bg='#00154f',fg='light blue',font=('Goudy old style',20,'bold'),bd=0,activeforeground='light blue',activebackground='#00154f',cursor='hand2',command=forword_to_forget_password)
            forget_btn.place(x = 200,y = 290,width = 260)

#####################  registration page ##########################
    def registration_page(self):
        def backword_to_main_page():
            registration_page_fm.destroy()
            root.update()
            self.first_page()
        def forword_to_login_page():
            registration_page_fm.destroy()
            root.update()
            self.login_window()     

        def register_c():
            entry_username = self.reg_user
            entry_email = self.reg_email
            entry_mobile_no = self.reg_Mobile_no
########################sql of register page #########################################
       

            if entry_email.get()==''or entry_username.get()=='' or entry_mobile_no.get()=='' :
                messagebox.showerror("Error",'All Fields Are Required')
            else :
                if " " in entry_username.get():
                    messagebox.showerror("Error",'Space is not allowed in user name')
                else:
                    mycursor = self.con.cursor()
                    query = 'select * from data where username = %s'
                    mycursor.execute(query,[entry_username.get()])
                    row = mycursor.fetchall()
                    if len(row)>0:
                        messagebox.showerror("Error",'User Name Already ')
                        self.clear(entry_email,entry_username,entry_mobile_no)
                        # forword_to_login_page()
                    else:
                        try:
                            a1 = random.randint(0,9)
                            a2 = random.randint(0,9)
                            ac = list('abcdefghijklmnopqrstuvxyz')
                            a3 = random.choice(ac)
                            AC = list('ABCDEFGHJKLMNOPQRSTUVXYZ')
                            a4 = random.choice(AC)
                            sc = list('!@#$%^&*_')
                            a5 = random.choice(sc)
                            a6 = random.choice(ac)
                            a7 = random.choice(AC)
                            a8 = random.randint(0,9)
                            otp = [a1,a2,a3,a4,a5,a6,a7,a8]
                            random.shuffle(otp)
                            otp = "".join(map(str, otp))

                            mycursor = self.con.cursor()
                            
                            query = f'insert into data (username,password,mobile,email) values("{entry_username.get()}","{otp}","{entry_mobile_no.get()}","{entry_email.get()}")'
                            mycursor.execute(query)
                            # print('Entry done in data')
                            query = f"create table {entry_username.get()}(date DATE NOT NULL, deposite INT NULL, withdraw INT NULL , balance INT NOT NULL)"
                            # print(query)
                            
                            mycursor = self.con.cursor()
                            mycursor.execute(query)

                            self.con.commit()
                            date  = dtime.now().strftime("%Y-%m-%d")
                            
                            query = f'insert into {entry_username.get()} (date , deposite, withdraw,balance) values(%s,%s,%s,%s)'
                            # print(query)
                            mycursor.execute(query,(date,0,0,0))
                            self.con.commit()

                            # print('transaction table created')
                        except Exception as e:
                            messagebox.showerror('Error', 'Something Wrong')
                            self.clear(entry_email,entry_username,entry_mobile_no)
                        else:
                            
                            self.send_email(entry_email.get(),otp)
                            messagebox.showinfo('Successfull', 'Password sent on Email')
                            
                            self.clear(entry_email,entry_username,entry_mobile_no)         
                            forword_to_login_page()
#######designing of register page ###############33
        registration_page_fm = Frame(self.root,bg='light blue')
        registration_page_fm.place(x=85,y=150,height=418,width=500)
        
        title = Label(registration_page_fm,text="Register Yourself Here",font=("Impact",35,'bold'),bg='light blue',fg='#00154f').place(x = 15,y=50)
        
        lbl_reg_user = Label(registration_page_fm,text=' Enter Username ',font=('Goudy old style',15,'bold'),fg='#363636',bg='light blue').place(x = 70,y=140)
        self.reg_user = Entry(registration_page_fm,font=('times new roman',15),bg='#CCCCCC')
        self.reg_user.place(x=70,y=170,width=350,height=35)

        lbl_reg_email = Label(registration_page_fm,text='Enter Email',font=('Goudy old style',15,'bold'),fg='#363636',bg='light blue').place(x = 70,y=215)
        self.reg_email = Entry(registration_page_fm,font=('times new roman',15),bg='#CCCCCC')
        self.reg_email.place(x=70,y=247,width=350,height=35)

        lbl_reg_Mobile_no = Label(registration_page_fm,text='Enter Mobile Number',font=('Goudy old style',15,'bold'),fg='#363636',bg='light blue').place(x = 70,y=290)
        self.reg_Mobile_no = Entry(registration_page_fm,font=('times new roman',15),bg='#CCCCCC')
        self.reg_Mobile_no.place(x=70,y=322,width=350,height=35)

        register_btn = Button(root,text='Register',bg='#00154f',fg='light blue',font=('Goudy old style',20,'bold'),bd=0,activeforeground='light blue',activebackground='#00154f',cursor='hand2',command=register_c)
        register_btn.place(x = 250,y = 530,width = 180,height=40)
        
        back_btn = Button(registration_page_fm,text='←\nBack',bg='light blue',fg='#00154f',font=('bold',15),bd=0,activeforeground='#00154f',activebackground='light blue',cursor='hand2',command=backword_to_main_page)
        back_btn.place(x = 5 ,y = 0)
####################### login window  ##################################################
    def login_window(self):
        # image = Image.open(r'C:\Users\Divya sohani\Desktop\pyprojects\banking login system\Images\add_student_img.png')
        # openeye  =ImageTk.PhotoImage(image)

        Frame_login = Frame(self.root,bg='light blue')
        # Frame_login = Frame(self.root)
        Frame_login.place(x=85,y=150,height=418,width=500)

        def backword_to_main_page():
            Frame_login.destroy()
            root.update()
            self.registration_page()

        back_login_btn = Button(Frame_login,text='←\nBack',bg='light blue',fg='#00154f',font=('bold',15),bd=0,activeforeground='#00154f',activebackground='light blue',cursor='hand2',command=backword_to_main_page)
        back_login_btn.place(x = 5 ,y = 0)

        title = Label(Frame_login,text="Login Here",font=("Impact",35,'bold'),bg='light blue',fg='#00154f').place(x = 90,y=30)
        desc = Label(Frame_login,text='Accountant Employee Login Area',font=('Goudy old style',15,'bold'),fg='#00154f',bg='light blue').place(x = 70,y=100)

        lbl_user = Label(Frame_login,text='Username ',font=('Goudy old style',15,'bold'),fg='#363636',bg='light blue').place(x = 70,y=140)
        self.txt_user = Entry(Frame_login,font=('times new roman',15),bg='#CCCCCC')
        self.txt_user.place(x=70,y=170,width=350,height=35)

        lbl_pass = Label(Frame_login,text='Password',font=('Goudy old style',15,'bold'),fg='#363636',bg='light blue').place(x = 70,y=215)
        self.txt_pass = Entry(Frame_login,font=('times new roman',15),bg='#CCCCCC')
        self.txt_pass.place(x=70,y=247,width=350,height=35)

        ############ OPEN EYE ##############

        # print('Image',openeye)
        # label = tk.Label(Frame_login, image=openeye)
        # label.pack()
        # eyeButton = Button(Frame_login,image=openeye,bd=0,bg='white',activebackground='white',cursor='hand2')
        # eyeButton.place(x = 390,y=251)
        
        lbl_Mobile = Label(Frame_login,text='Mobile Number',font=('Goudy old style',15,'bold'),fg='#363636',bg='light blue').place(x = 70,y=290)
        self.Mobile = Entry(Frame_login,font=('times new roman',15),bg='#CCCCCC')
        self.Mobile.place(x=70,y=322,width=350,height=35)
            
        forget_btn = Button(Frame_login,text='Forget Password ?',bg='light blue',fg='#00154f',bd=0,font=('Goudy old style',15,'bold'),activeforeground='#00154f',activebackground='lightblue',cursor='hand2',command=self.forget_password).place(x=260,y=358)

        Login_btn = Button(root,text='Login',bg='#00154f',fg='light blue',font=('Goudy old style',20,'bold'),activeforeground='#00154f',activebackground='lightblue',cursor='hand2',command=self.sqllogin).place(x=150,y=530,width=180,height=40)

######################  forget password ##############################################
    def forget_password(self):   
     Forget_pass_fm = Frame(root,bg='light blue')
     Forget_pass_fm.place(x=85,y=150,height=418,width=500)

     def backword_to_main_page():
        Forget_pass_fm.destroy()
        root.update()
        self.login_window()
########################### sql of forget password ############### 
     def forget_pass():
        # messagebox.showinfo('done','Submit successfull')
        user = entry_username
        # print(entry_username.get())
        # txt_pass = self.txt_pass
        mobile = entry_mobile_no
        email= entry_email
        
        if entry_email.get() ==''or entry_username.get()=='' or mobile.get()=='' :
            messagebox.showerror("Error",'All Fields Are Required')
        else:
            mycursor = self.con.cursor()
        
            query = 'select * from data where username = %s'
            mycursor.execute(query,[user.get()])
            
            row = mycursor.fetchone()
            # print(row)
            if row != None:
                if len(row) != 0:
                    a,b,c,d = row
                    # print(a,b,c,d)
                    # print(user.get(),mobile.get(),entry_email.get()) #,self.txt_pass.get() 
                    # if b ==  self.txt_pass.get():
                    
                    
                    if c== mobile.get():
                        # messagebox.showinfo('Done','Login Successfull')

                        if d == entry_email.get():
                            self.send_email(otp =b,user_email_id=d)
                            messagebox.showinfo('Done','Password Sent On Email')

                        else:
                            messagebox.showerror('Wrong Email','Enter Correct Email')
                        
                    else:
                        messagebox.showerror('Wrong Mobile number','Enter Correct Mobile Number')
                            
            else:
                messagebox.showerror('Wrong User Name','Enter Correct Username')
            
        self.clear(entry_email,entry_username,mobile)
################## designing of forget password ############### 
     back_forget_btn = Button(Forget_pass_fm,text='←\nBack',bg='light blue',fg='#00154f',font=('bold',15),bd=0,activeforeground='#00154f',activebackground='light blue',cursor='hand2',command=backword_to_main_page)
     back_forget_btn.place(x = 5 ,y = 0)


     title = Label(Forget_pass_fm,text="FORGET PASSWORD",font=("Impact",35,'bold'),bg='light blue',fg='#00154f').place(x = 70,y=30)
  
 
     lbl_username = Label (Forget_pass_fm , text='Enter Username',font=('Goudy old style',15,'bold'),fg='#363636',bg='light blue').place(x = 70,y=140)
     entry_username = Entry(Forget_pass_fm,font=('times new roman',15),bg='#CCCCCC')
     entry_username.place(x=70,y=170,width=350,height=35)
                    
     lbl_mobile_no = Label(Forget_pass_fm,text='Enter Mobile Number',font=('Goudy old style',15,'bold'),fg='#363636',bg='light blue').place(x = 70,y=215)
     entry_mobile_no = Entry(Forget_pass_fm, font=('times new roman',15),bg='#CCCCCC')
     entry_mobile_no.place(x=70,y=247,width=350,height=35)

     lbl_email = Label(Forget_pass_fm,text='Enter Email',font=('Goudy old style',15,'bold'),fg='#363636',bg='light blue').place(x =70,y=290)
     entry_email = Entry(Forget_pass_fm,font=('times new roman',15),bg='#CCCCCC')
     entry_email.place(x=70,y= 322, width=350,height=35)

     Submit = Button(root,text='Submit',bg='#00154f',fg='light blue',font=('Goudy old style',20,'bold'),activeforeground='#00154f',activebackground='lightblue',cursor='hand2',command = forget_pass).place(x=150,y=530,width=180,height=40) 
 
     
######################  RESET WINDOW ##############################################
    def change_passowrd(self):
        Frame_reset = Frame(self.root,bg='light blue')
        Frame_reset.place(x=85,y=150,height=418,width=500)

        def backword_to_transaction():
            Frame_reset.destroy()
            root.update()
            self.Transaction_window()

        back_login_btn = Button(Frame_reset,text='←\nBack',bg='light blue',fg='#00154f',font=('bold',15),bd=0,activeforeground='#00154f',activebackground='light blue',cursor='hand2',command=backword_to_transaction)
        back_login_btn.place(x = 5 ,y = 0)

        title = Label(Frame_reset,text="Reset Password",font=("Impact",35,'bold'),bg='light blue',fg='#00154f').place(x = 90,y=30)

        old_p = Label(Frame_reset,text=' Enter Old Password ',font=('Goudy old style',15,'bold'),fg='#363636',bg='light blue').place(x = 63,y=115)
        self.old_p_entry = Entry(Frame_reset,font=('times new roman',15),bg='#CCCCCC')
        self.old_p_entry.place(x=70,y=152,width=350,height=35)

        new_p = Label(Frame_reset,text='Enter New Password',font=('Goudy old style',15,'bold'),fg='#363636',bg='light blue').place(x = 70,y=200)
        self.new_p_entry = Entry(Frame_reset,font=('times new roman',15),bg='#CCCCCC')
        self.new_p_entry.place(x=70,y=237,width=350,height=35)

        confirm_p = Label(Frame_reset,text='Confirm Password',font=('Goudy old style',15,'bold'),fg='#363636',bg='light blue').place(x = 70,y=285)
        self.confirm_p_entry = Entry(Frame_reset,font=('times new roman',15),bg='#CCCCCC')
        self.confirm_p_entry.place(x=70,y=322,width=350,height=35)


        submit_btn = Button(Frame_reset,text='Submit',bg='#00154f',fg='light blue',font=('Goudy old style',20,'bold'),activeforeground='#00154f',activebackground='lightblue',cursor='hand2',command = self.reset_password).place(x=150,y=370,width=180,height=40)

######################  Transaction window  ##############################################
    def Transaction_window(self):

        Frame_Transaction = Frame(self.root,bg='light blue')
        Frame_Transaction.place(x=85,y=150,height=418,width=500)

        # def backword_to_login():
        #     Frame_Transaction.destroy()
        #     root.update()
        #     self.login_window()

        def confirm():
            ans = askyesno(title='LOGOUT',message='Do You Want To Logout ?')
            if ans:
                root.destroy()
        

        root.protocol('WM_DELETE_WINDOW',confirm)


        heading_lbl_T = Label(Frame_Transaction,text='Transaction',font=('Impact',35,'bold'),bg='light blue',fg='#00154f').place(x = 110,y=10)

        # back_Transaction_btn = Button(Frame_Transaction,text='←\nBack',bg='light blue',fg='#00154f',font=('bold',15),bd=0,activeforeground='#00154f',activebackground='light blue',cursor='hand2',command=backword_to_login)
        # back_Transaction_btn.place(x = 5 ,y = 0)

        lbl_current_balance = Label(Frame_Transaction,text='Current Balance - ',font=('Goudy old style',15,'bold'),fg='#363636',bg='light blue').place(x = 70,y=85)
        self.current_balance = Entry(Frame_Transaction,font=('times new roman',15),bg='#CCCCCC')
        # acc_bal = self.show_balance(self.txt_user.get())
        # acc_bal = str(acc_bal)
        
        self.current_balance.insert(END,self.show_balance(self.txt_user.get()))
        self.current_balance.place(x=70,y=120,width=350,height=35)


        lbl_amount = Label(Frame_Transaction,text='Amount - ',font=('Goudy old style',15,'bold'),fg='#363636',bg='light blue').place(x = 70,y=158)
        self.amount= Entry(Frame_Transaction,font=('times new roman',15),bg='#CCCCCC')
        self.amount.place(x=70,y=193,width=350,height=35)

        deposite_btn = Button(Frame_Transaction,text='Deposite',bg='#00154f',fg='light blue',font=('Goudy old style',20,'bold'),bd=0,activeforeground='light blue',activebackground='#00154f',cursor='hand2',command=self.deposit)
        deposite_btn.place(x = 300,y = 249,width = 165)

        Statement_btn = Button(Frame_Transaction,text='Statement',bg='#00154f',fg='light blue',font=('Goudy old style',20,'bold'),bd=0,activeforeground='light blue',activebackground='#00154f',cursor='hand2',command=self.send_statement)
        Statement_btn.place(x = 300,y = 310,width = 165)

        Withdraw_btn = Button(Frame_Transaction,text='Withdraw',bg='#00154f',fg='light blue',font=('Goudy old style',20,'bold'),bd=0,activeforeground='light blue',activebackground='#00154f',cursor='hand2',command=self.withdraw)
        Withdraw_btn.place(x = 70,y = 249,width = 200)

        Reset_btn = Button(Frame_Transaction,text='Reset Password',bg='#00154f',fg='light blue',font=('Goudy old style',20,'bold'),bd=0,activeforeground='light blue',activebackground='#00154f',cursor='hand2',command=self.change_passowrd)
        Reset_btn.place(x = 70,y = 310,width = 200)

        Exit_btn = Button(Frame_Transaction,text='** LOG OUT **',bg='light blue',fg='#00154f',font=('Goudy old style',20,'bold'),bd=0,activeforeground='#00154f',activebackground='light blue',cursor='hand2',command=confirm)
        Exit_btn.place(x = 250,y = 370,width = 260)                

###################### sql connectivity for login window    
    def sqllogin(self):
        txt_user = self.txt_user
        txt_pass = self.txt_pass
        mobile = self.Mobile
        if txt_pass.get()==''or txt_user.get()=='' or mobile.get()=='' :
            messagebox.showerror("Error",'All Fields Are Required')

        mycursor = self.con.cursor()
        query = 'select * from data where username = %s'
        mycursor.execute(query,[txt_user.get()])
        row = mycursor.fetchone()
        # print(row)
        if row!= None:
            if len(row) != 0:
                # a,b,c,d = row
                # print(a,b,c,d)
                # print(txt_user.get(),txt_pass.get(),mobile.get())       
                if row[1] ==  txt_pass.get():
                            
                    if row[2]== mobile.get():
                        messagebox.showinfo('Done','Login Successfull')
                        global user_a, pwd_b, mob_c, email_d
                        user_a, pwd_b, mob_c, email_d = row
                        self.Transaction_window()
                        return user_a, pwd_b, mob_c, email_d
                                       
                                
                    else:
                        messagebox.showerror('Wrong Mobile number','Enter Correct Mobile Number')
                else:                      
                    messagebox.showerror('Wrong Password','Enter Correct Password')
                                
            else:
                messagebox.showerror('Wrong User Name','Enter Correct Username')
        else:
            messagebox.showerror('Error','Unregistered user Please Register Yourself First')
            return None        

        
        # messagebox.showinfo('Success','Registraiton Successful')
        self.clear(txt_user,txt_pass,mobile)
           
###################### sql of reset window #################
    def reset_password(self):
        # print(user_a, pwd_b, mob_c, email_d)
        old_p = self.old_p_entry
        new_p = self.new_p_entry
        confirm_p = self.confirm_p_entry
        # print(old_p.get(),new_p.get(),confirm_p.get())

        if old_p.get()==''or new_p.get()=='' or confirm_p.get()=='' :
            messagebox.showerror("Error",'All Fields Are Required')
        else:
            cur = self.con.cursor()
            # print('Cur created')
            if old_p.get() == pwd_b:
                # print('Old Password matched')
                if new_p.get()==confirm_p.get():
                    query = f'update data set password ="{confirm_p.get()}" where username = "{user_a}"'
                    # print(query)
                    cur.execute(query)
                    self.con.commit()
                    messagebox.showinfo('Done','Password Changed')
                    self.clear(old_p,new_p,confirm_p)
                    self.login_window()
                else:
                    messagebox.showwarning('Error','New Password Not Matched With Old Password')
            else:
                messagebox.showwarning('Error','Enter Correct Old Password')
# def clear(self):
    def clear(self,a1,b1,c1):
            a1.delete(0,END)
            b1.delete(0,END)
            c1.delete(0,END)  
###################### withdraw sql ####################
    def withdraw(self):
    #    print(user_a)
    #    print(self.amount.get())
       mycursor = self.con.cursor()
       date  = dtime.now().strftime("%Y-%m-%d")
                    
       query = f'insert into {user_a} (date , deposite,withdraw,balance) values(%s,%s,%s,%s)'
    #    print(query)
       balance = self.show_balance(user_a)
    #    print(balance)
       if self.amount.get() != '':
            try:
                amount = float(self.amount.get())
            except:
                messagebox.showwarning('Error','Enter Numeric Value Only')
                
            else:
                    

                if balance>= amount:
                    balance  = balance-amount
                    mycursor.execute(query,(date,0,amount,balance))
                    self.con.commit()
                    messagebox.showinfo('Done','Transaction successfull')
                    self.current_balance.delete(0,END)
                    self.amount.delete(0,END)
                    self.current_balance.insert(END,self.show_balance(user_a))
                
                else:
                    messagebox.showwarning('Error','Insufficient Balance')
                    self.current_balance.delete(0,END)
                    self.amount.delete(0,END)
                    self.current_balance.insert(END,self.show_balance(user_a))
        
       else:
           messagebox.showwarning('Error','Enter Amount First')
              


########### deposite sql ##########
    def deposit(self):
    #    print(user_a)
    #    print(self.amount.get())
       mycursor = self.con.cursor()
       date  = dtime.now().strftime("%Y-%m-%d")
                    
       query = f'insert into {user_a} (date , deposite,withdraw,balance) values(%s,%s,%s,%s)'
    #    print(query)
       balance = self.show_balance(user_a)
    #    print(balance)
       if self.amount.get() != '':
            try:
                amount = float(self.amount.get())
            except:
                messagebox.showwarning('Error','Enter Numeric Value Only')
                self.current_balance.delete(0,END)
                self.amount.delete(0,END)
                self.current_balance.insert(END,self.show_balance(user_a))
                
            else:
                    
                    balance  = balance+amount
                    # print(balance)
                    mycursor.execute(query,(date,amount,0,balance))
                    self.con.commit()
                    messagebox.showinfo('Done','Transaction successfull')
                    self.current_balance.delete(0,END)
                    self.amount.delete(0,END)
                    self.current_balance.insert(END,self.show_balance(user_a))
            
       else:
           messagebox.showwarning('Error','Enter Amount First')
       
############# statement sql #############
    def send_statement(self):
        tbl_name = user_a
        statement = {'Date': [],'Deposit':[],'Withdraw':[],'Balance':[] }

        cur = self.con.cursor()
        
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
        print('File Created ---------')
        sender_email = "sohnid3@gmail.com"
        sender_password = "ucvzcpaewaeiujzr"
        reciver_email = email_d ########### jis email pr bhejna hai otp
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = reciver_email
        msg['Subject'] = 'Statement From Python Bank'
        body = 'Please find the atteched bank Statement'
        msg.attach(MIMEText(body,'plain'))

        fn = 'statement.xlsx'
        with open (fn, 'rb') as f:
            attachment = MIMEApplication(f.read(),_subtype ='xlsx')
            attachment.add_header('content-Disposition','attachement',filename = fn)
            msg.attach(attachment) 

                   

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("sohnid3@gmail.com", "ucvzcpaewaeiujzr")         ######## is email se bhejna hai or ye passkey hai mere email ki 
        s.send_message(msg)

        os.remove(fn) # to delete after send the email
        return messagebox.showinfo('Done',f'Statement Send To Your Mail {email_d}')


    def show_balance(self, user_name):
        # print(user_name)
        mycursor = self.con.cursor()
        query = f'select * from {user_name}'
        mycursor.execute(query)
        row = mycursor.fetchall()

        # print('Balance',row[-1][-1])
        self.con.commit()
        return round((float(row[-1][-1])),2)
         


if __name__ == "__main__":
    root = Tk()
    obj = Login(root)
    # obj.Transaction_window()
    obj.first_page()
    root.mainloop()