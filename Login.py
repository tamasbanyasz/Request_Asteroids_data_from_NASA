from datetime import datetime
import tkinter as tk
from tkinter import *
from tkinter import messagebox, Frame
import smtplib
import ssl
import random

users = {'Tomi': {'Password': 'QKqaCzodqQQk4Q1',
                  'Reg_date': '11-07-2022 00:00:00',
                  'Login_date': '13-07-2022 08:08:10',
                  'Logout_date': '13-07-2022 11:11:11',
                  },
         'Béla': {'Password': 'd8ra-2HYxYk4',
                  'Reg_date': '01-02-2010 15:00:22',
                  'Login_date': '31-12-2021 12:00:00',
                  'Logout_date': '01-04-2022 23:11:00'
                  },
         'Gazsi': {'Password': '22',
                   'Email': 'tamasbanyasz@gmail.com',
                   'Reg_date': '30-01-1999 10:10:11',
                   'Login_date': '13-07-2022 05:00:00',
                   'Logout_date': '13-07-2022 10:30:09'
                   }}

def send_email(users, account):
    port = 587
    smtp_server = "smtp.gmail.com"
    sender_email = "minert63@gmail.com"
    receiver_email = users[account]['Email']
    password = "fmulagkysiwvzczv"
    message = users[account]['Password']

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

def forgot_pass_or_acc(users):
    characters = 'abcdefghijklmnopqrstzxyABCDEFGHIJKLMNOPQRSTZXY0123456789*#-%&@'
    length = random.randint(8, 16)

    account = label4_e.get()
    email = label4_eme.get()

    if account in users and email == users[account]['Email']:
        users[account]['Password'] = "".join([random.choice(characters) for i in range(length)])
        send_email(users, account)
        messagebox.showinfo("Email", "Email sent.")
        label4_e.delete(0, END)
        label4_eme.delete(0, END)
        show_frame(page1)
    else:
        messagebox.showerror("Invalid", "Wrong username or password")
        label4_e.delete(0, END)
        label4_eme.delete(0, END)
    print(users)

def create_datetime_now():
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")

    return dt_string

def create_account(users):
    if users.get(label2_e.get()) == None:
        users[label2_e.get()] = {'Password': label2_p.get(), 'Reg_date': create_datetime_now(), 'Email':label2_em.get()}
        messagebox.showinfo("Register", "New account added.")
        label2_e.delete(0, END)
        label2_p.delete(0, END)
        show_frame(page1)
        print(users)

    else:
        messagebox.showerror("Invalid", "Account already exists.")


def login(users):
    if label1_e1.get() in users and label1_p2.get() == users[label1_e1.get()]['Password']:
        label1_e1.delete(0, END)
        label1_p2.delete(0, END)
        show_frame(page3)
    else:
        messagebox.showerror("Invalid", "Wrong username or password")


def show_frame(frame):
    frame.tkraise()


window = tk.Tk()
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
# window.state('zoomed')
window.geometry("800x600")
window.title("Bányász Tamás")
window.resizable(False, False)

page1 = Frame(window)
page2 = Frame(window)
page3 = Frame(window)
page4 = Frame(window)

for frame in (page1, page2, page3, page4):
    frame.grid(row=0, column=0, sticky='nsew')

show_frame(page1)

# ------------- Page 1 -------------------------------------------------------------------------------------------#

page1_label = Label(page1, text="Login and Register", fg="black", font=('Roboto', 15))
page1_label.place(x=365, y=10)

label1_u = Label(page1, text="Username : ", fg="black")
label1_e1 = Entry(page1)

label1_u.place(x=310, y=46)
label1_e1.place(x=380, y=50)

label1_p = Label(page1, text="Password : ", fg="black")
label1_p2 = Entry(page1, show="*")

label1_p.place(x=310, y=73)
label1_p2.place(x=380, y=75)

enter = tk.Button(page1, text='Login', command=lambda: login(users), font=('Roboto', 13))
enter.place(x=375, y=100)

register = tk.Button(page1, text='Register', command=lambda: show_frame(page2), font=('Roboto', 13))
register.place(x=435, y=100)

forgot_pass = tk.Button(page1, text='Forgot Password', command=lambda: show_frame(page4), font=('Roboto', 13))
forgot_pass.place(x=374, y=140)



# ------------- Page 2 -------------------------------------------------------------------------------------------#


label2_r = Label(page2, text='Register', fg='black', font=('Roboto', 15))
label2_r.place(x=400, y=10)

label2_u = Label(page2, text="Username : ", fg="black")
label2_e = Entry(page2)

label2_u.place(x=310, y=46)
label2_e.place(x=380, y=50)

label2 = Label(page2, text="Password : ", fg="black")
label2_p = Entry(page2, show="*")

label2.place(x=310, y=73)
label2_p.place(x=380, y=75)

label2_email = Label(page2, text="Email : ", fg="black")
label2_em = Entry(page2)

label2_email.place(x=310, y=97)
label2_em.place(x=380, y=100)

enter = tk.Button(page2, text='Submit', command=lambda: create_account(users), font=('Roboto', 13))
enter.place(x=415, y=140)

back = tk.Button(page2, text='Back', command=lambda: show_frame(page1), font=('Roboto', 13))
back.place(x=422, y=180)

# ------------- Page 3 -------------------------------------------------------------------------------------------#

page3_label = Label(page3, text="Welcome!", fg="black", font=('Roboto', 15))
page3_label.place(x=365, y=10)




# ------------- Page 4 -------------------------------------------------------------------------------------------#

page4_label = Label(page4, text="Forgot Password", fg="black", font=('Roboto', 15))
page4_label.place(x=365, y=10)

label4_u = Label(page4, text="Username : ", fg="black")
label4_e = Entry(page4)

label4_u.place(x=310, y=46)
label4_e.place(x=380, y=50)

label4_em = Label(page4, text="Email : ", fg="black")
label4_eme = Entry(page4)

label4_em.place(x=310, y=73)
label4_eme.place(x=380, y=75)

enter = tk.Button(page4, text='Submit', command=lambda: forgot_pass_or_acc(users), font=('Roboto', 13))
enter.place(x=410, y=120)

back = tk.Button(page4, text='Back', command=lambda: show_frame(page1), font=('Roboto', 13))
back.place(x=417, y=160)

window.mainloop()
