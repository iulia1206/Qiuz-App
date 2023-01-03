import tkinter as tk
from tkinter import *
import random
import sqlite3
import time
import requests
import html

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np


# function for the questions' countdown
def countDown(timer, easy_frame):
    check = 0
    for k in range(25, 0, -1):
        if k == 1:
            check = -1
        timer.configure(text=k)
        easy_frame.update()
        time.sleep(1)
        
    timer.configure(text="Time's up!")
    
    if check == -1:
        return (-1)
    else:
        return 0

# third page(login page)
def loginPage(logdata):
    # distroys the second page
    sign_up.destroy()
    global login
    login = Tk()
    login.title('Quiz Login')

    user_name = ""
    password = ""

    login_canvas = Canvas(login, width=720, height=440, bg="cyan")
    login_canvas.pack()

    login_frame = Frame(login_canvas, bg="cyan")
    login_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    # page's title
    heading = Label(login_frame, text="Quiz Login",
                    fg="dark orange", bg="cyan")
    heading.config(font=('calibri 40'))
    heading.place(relx=0.3, rely=0.1)

    # username filed
    ulabel = Label(login_frame, text="Username", fg='white', bg='dark orange')
    ulabel.place(relx=0.21, rely=0.4)
    uname = Entry(login_frame, bg='white', fg='black', textvariable=user_name)
    uname.config(width=42)
    uname.place(relx=0.31, rely=0.4)

    # password field 
    plabel = Label(login_frame, text="Password", fg='white', bg='dark orange')
    plabel.place(relx=0.215, rely=0.5)
    pas = Entry(login_frame, bg='white', fg='black',
                textvariable=password, show="*")
    pas.config(width=42)
    pas.place(relx=0.31, rely=0.5)

    # verify username and password
    def check():
        for a, b, c, d in logdata:
            if b == uname.get() and c == pas.get():
                print(logdata)
                # go to the menu page
                menu(a)
                break
        else:
            error = Label(
                login_frame, text="Wrong Username or Password!", fg='black', bg='white')
            error.place(relx=0.37, rely=0.7)

    # login button
    log = Button(login_frame, text='Login', padx=5, pady=5,
                 width=5, command=check, fg="white", bg="dark orange")
    log.configure(width=15, height=1, activebackground="cyan", relief=FLAT)
    log.place(relx=0.4, rely=0.6)

    login.mainloop()


# second page(signing up page)
def signUpPage():
    # distroys the first page
    root.destroy()
    global sign_up
    sign_up = Tk()
    sign_up.title('Quiz App')

    fname = ""
    uname = ""
    passW = ""
    country = ""

    sup_canvas = Canvas(sign_up, width=720, height=440, bg="cyan")
    sup_canvas.pack()

    sup_frame = Frame(sup_canvas, bg="cyan")
    sup_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    # title of the page
    heading = Label(sup_frame, text="Create your account",
                    fg="dark orange", bg="cyan")
    heading.config(font=('calibri 40'))
    heading.place(relx=0.12, rely=0.1)

    # full name field
    flabel = Label(sup_frame, text="FULL NAME ", fg='white', bg='dark orange')
    flabel.place(relx=0.19, rely=0.4)
    fname = Entry(sup_frame, bg='white', fg='black', textvariable=fname)
    fname.config(width=42)
    fname.place(relx=0.31, rely=0.4)

    # username filed
    ulabel = Label(sup_frame, text="USERNAME ", fg='white', bg='dark orange')
    ulabel.place(relx=0.19, rely=0.5)
    user = Entry(sup_frame, bg='white', fg='black', textvariable=uname)
    user.config(width=42)
    user.place(relx=0.31, rely=0.5)

    # password field
    plabel = Label(sup_frame, text="PASSWORD ", fg='white', bg='dark orange')
    plabel.place(relx=0.19, rely=0.6)
    pas = Entry(sup_frame, bg='white', fg='black',
                textvariable=passW, show="*")
    pas.config(width=42)
    pas.place(relx=0.31, rely=0.6)

    # country field
    clabel = Label(sup_frame, text="  COUNTRY  ", fg='white', bg='dark orange')
    clabel.place(relx=0.19, rely=0.7)
    c = Entry(sup_frame, bg='white', fg='black', textvariable=country)
    c.config(width=42)
    c.place(relx=0.31, rely=0.7)

    def addUserToDataBase():

        fullname = fname.get()
        username = user.get()
        password = pas.get()
        country = c.get()

        # check if the fileds are completed right
        if len(fname.get()) == 0 and len(user.get()) == 0 and len(pas.get()) == 0 and len(c.get()) == 0:
            error = Label(
                text="You haven't enter any field...Please Enter all the fields", fg='black', bg='white')
            error.place(relx=0.37, rely=0.7)

        elif len(fname.get()) == 0 or len(user.get()) == 0 or len(pas.get()) == 0 or len(c.get()) == 0:
            error = Label(text="Please Enter all the fields",
                          fg='black', bg='white')
            error.place(relx=0.37, rely=0.7)

        elif len(user.get()) == 0 and len(pas.get()) == 0:
            error = Label(
                text="Username and password can't be empty", fg='black', bg='white')
            error.place(relx=0.37, rely=0.7)

        elif len(user.get()) == 0 and len(pas.get()) != 0:
            error = Label(text="Username can't be empty",
                          fg='black', bg='white')
            error.place(relx=0.37, rely=0.7)

        elif len(user.get()) != 0 and len(pas.get()) == 0:
            error = Label(text="Password can't be empty",
                          fg='black', bg='white')
            error.place(relx=0.37, rely=0.7)

        else:

            # add player to database
            conn = sqlite3.connect('quiz.db')
            create = conn.cursor()
            create.execute(
                'CREATE TABLE IF NOT EXISTS userSignUp(FULLNAME text, USERNAME text,PASSWORD text,COUNTRY text)')
            create.execute("INSERT INTO userSignUp VALUES (?,?,?,?)",
                           (fullname, username, password, country))
            conn.commit()
            create.execute('SELECT * FROM userSignUp')
            z = create.fetchall()
            print(z)
            conn.close()
            loginPage(z)


    def gotoLogin():
        conn = sqlite3.connect('quiz.db')
        create = conn.cursor()
        conn.commit()
        create.execute('SELECT * FROM userSignUp')
        z = create.fetchall()
        loginPage(z)

    # signup button adds user to database and goes to log in page
    sp = Button(sup_frame, text='SignUp', padx=5, pady=5, width=5,
                command=addUserToDataBase, bg="dark orange", fg="white")
    sp.configure(width=15, height=1, activebackground="cyan", relief=FLAT)
    sp.place(relx=0.345, rely=0.8)

    # if the player already has an account, jumps to log in page
    log = Button(sup_frame, text='Already have an Account?', padx=5,
                 pady=5, width=5, command=gotoLogin, bg="dark orange", fg="white")
    log.configure(width=18, height=1, activebackground="cyan", relief=FLAT)
    log.place(relx=0.33, rely=0.9)

    sign_up.mainloop()


# fourth page(the page where you choose the difficulty level of the quiz)
def menu(player_name):
    # distroys the previous page
    login.destroy()
    global menu
    menu = Tk()
    menu.title('Quiz Menu')

    menu_canvas = Canvas(menu, width=720, height=440, bg="cyan")
    menu_canvas.pack()

    menu_frame = Frame(menu_canvas, bg="cyan")
    menu_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    # page's title 
    wel = Label(menu_canvas, text=' W E L C O M E  T O  T H E  Q U I Z ',
                fg="white", bg="dark orange")
    wel.config(font=('Broadway 22'))
    wel.place(relx=0.15, rely=0.02)

    player_name = 'Hello, ' + player_name + \
        "! Please select your quiz' difficulty level:"
    level34 = Label(menu_frame, text=player_name,
                    font="calibri 18", bg="dark orange", fg="white")
    level34.place(relx=0.10, rely=0.15)

    var = IntVar()

    # button to select difficulty level "easy"
    easyR = Radiobutton(menu_frame, text='EASY', bg="dark orange", fg="white",
                        font="calibri 11", value=1, variable=var, activebackground="cyan")
    easyR.place(relx=0.1, rely=0.35)

    # button to select difficulty level "medium"
    mediumR = Radiobutton(menu_frame, text='MEDIUM', bg="dark orange", fg="white",
                          font="calibri 11", value=2, variable=var, activebackground="cyan")
    mediumR.place(relx=0.1, rely=0.45)

    # button to select difficulty level "hard"
    hardR = Radiobutton(menu_frame, text='HARD', bg="dark orange", fg="white",
                        font="calibri 11", value=3, variable=var, activebackground="cyan")
    hardR.place(relx=0.1, rely=0.55)

    def navigate():

        x = var.get()
        print(x)
        if x == 1:
            menu.destroy()
            easy()
        elif x == 2:
            menu.destroy()
            medium()

        elif x == 3:
            menu.destroy()
            difficult()
        else:
            pass

    # go to quiz button
    letsgo = Button(menu_frame, text="Let's Go", bg="dark orange",
                    fg="white", font="calibri 20", command=navigate)
    letsgo.place(relx=0.4, rely=0.8)
    menu.mainloop()


def easy():

    global e
    e = Tk()
    e.title('Quiz - Easy Level')

    easy_canvas = Canvas(e, width=720, height=440, bg="dark orange")
    easy_canvas.pack()

    easy_frame = Frame(easy_canvas, bg="cyan")
    easy_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    # Trivia DB parameters to fetch the questions
    parameters = {
        "amount": 5, 
        "difficulty": "easy",
        "type": "multiple"
    }

    response = requests.get("https://opentdb.com/api.php", params=parameters)
    response.raise_for_status()
    data = response.json()

    global score
    score = 0

    # list with the questions and answers
    easyQ = [
        [
            html.unescape(data["results"][0]["question"]),
            html.unescape(data["results"][0]["correct_answer"]),
            html.unescape(data["results"][0]["incorrect_answers"][0]),
            html.unescape(data["results"][0]["incorrect_answers"][1]),
            html.unescape(data["results"][0]["incorrect_answers"][2]),
        ],
        [
            html.unescape(data["results"][1]["question"]),
            html.unescape(data["results"][1]["correct_answer"]),
            html.unescape(data["results"][1]["incorrect_answers"][0]),
            html.unescape(data["results"][1]["incorrect_answers"][1]),
            html.unescape(data["results"][1]["incorrect_answers"][2]),
        ],
        [
            html.unescape(data["results"][2]["question"]),
            html.unescape(data["results"][2]["correct_answer"]),
            html.unescape(data["results"][2]["incorrect_answers"][0]),
            html.unescape(data["results"][2]["incorrect_answers"][1]),
            html.unescape(data["results"][2]["incorrect_answers"][2]),
        ],
        [
            html.unescape(data["results"][3]["question"]),
            html.unescape(data["results"][3]["correct_answer"]),
            html.unescape(data["results"][3]["incorrect_answers"][0]),
            html.unescape(data["results"][3]["incorrect_answers"][1]),
            html.unescape(data["results"][3]["incorrect_answers"][2]),
        ],
        [
            html.unescape(data["results"][4]["question"]),
            html.unescape(data["results"][4]["correct_answer"]),
            html.unescape(data["results"][4]["incorrect_answers"][0]),
            html.unescape(data["results"][4]["incorrect_answers"][1]),
            html.unescape(data["results"][4]["incorrect_answers"][2]),
        ]
    ]

    # the correct answers to the questions 
    answer = [
        html.unescape(data["results"][0]["correct_answer"]),
        html.unescape(data["results"][1]["correct_answer"]),
        html.unescape(data["results"][2]["correct_answer"]),
        html.unescape(data["results"][3]["correct_answer"]),
        html.unescape(data["results"][4]["correct_answer"])
    ]

    # choose random the question
    li = ['', 0, 1, 2, 3, 4]
    x = random.choice(li[1:])

    # shuffle the answers 
    for i in range(4):
        easyQ[i].pop(0)
        random.shuffle(easyQ[i])
        easyQ[i].insert(0,html.unescape(data["results"][i]["question"]))

    ques = Label(easy_frame, text=easyQ[x][0],
                 font="calibri 12", bg="dark orange")
    ques.place(relx=0.5, rely=0.2, anchor=CENTER)

    var = StringVar()

    # possible answers
    a = Radiobutton(easy_frame, text=easyQ[x][1], font="calibri 10",
                    value=easyQ[x][1], variable=var, bg="dark orange")
    a.place(relx=0.5, rely=0.42, anchor=CENTER)

    b = Radiobutton(easy_frame, text=easyQ[x][2], font="calibri 10",
                    value=easyQ[x][2], variable=var, bg="dark orange")
    b.place(relx=0.5, rely=0.52, anchor=CENTER)

    c = Radiobutton(easy_frame, text=easyQ[x][3], font="calibri 10",
                    value=easyQ[x][3], variable=var, bg="dark orange")
    c.place(relx=0.5, rely=0.62, anchor=CENTER)

    d = Radiobutton(easy_frame, text=easyQ[x][4], font="calibri 10",
                    value=easyQ[x][4], variable=var, bg="dark orange")
    d.place(relx=0.5, rely=0.72, anchor=CENTER)

    li.remove(x)

    timer = Label(e)
    timer.place(relx=0.8, rely=0.82, anchor=CENTER)

    def display():

        if len(li) == 1:
            e.destroy()
            showMark(score)
        if len(li) == 2:
            nextQuestion.configure(text='End', command=calc)

        if li:
            x = random.choice(li[1:])
            ques.configure(text=easyQ[x][0])

            a.configure(text=easyQ[x][1], value=easyQ[x][1])

            b.configure(text=easyQ[x][2], value=easyQ[x][2])

            c.configure(text=easyQ[x][3], value=easyQ[x][3])

            d.configure(text=easyQ[x][4], value=easyQ[x][4])

            li.remove(x)
            y = countDown(timer, easy_frame)
            if y == -1:
                display()

    def calc():
        global score
        if (var.get() in answer):
            score += 1
        display()

    # button for submitting the answers
    submit = Button(easy_frame, command=calc, text="Submit",
                    fg="black", bg="dark orange", font="calibri 15")
    submit.place(relx=0.5, rely=0.9, anchor=CENTER)

    # button for the next question
    nextQuestion = Button(easy_frame, command=display,
                          text="Next", fg="black", bg="dark orange")
    nextQuestion.place(relx=0.87, rely=0.82, anchor=CENTER)

    y = countDown(timer, easy_frame)
    if y == -1:
        display()
    e.mainloop()


def medium():

    global m
    m = Tk()
    m.title('Quiz - Medium Level')

    med_canvas = Canvas(m, width=720, height=440, bg="dark orange")
    med_canvas.pack()

    med_frame = Frame(med_canvas, bg="cyan")
    med_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    # Trivia DB parameters to fetch the questions
    parameters = {
        "amount": 5, 
        "difficulty": "medium",
        "type": "multiple"
    }

    response = requests.get("https://opentdb.com/api.php", params=parameters)
    response.raise_for_status()
    data = response.json()

    global score
    score = 0

    # list with the questions and answers
    mediumQ = [
        [
            html.unescape(data["results"][0]["question"]),
            html.unescape(data["results"][0]["correct_answer"]),
            html.unescape(data["results"][0]["incorrect_answers"][0]),
            html.unescape(data["results"][0]["incorrect_answers"][1]),
            html.unescape(data["results"][0]["incorrect_answers"][2]),
        ],
        [
            html.unescape(data["results"][1]["question"]),
            html.unescape(data["results"][1]["correct_answer"]),
            html.unescape(data["results"][1]["incorrect_answers"][0]),
            html.unescape(data["results"][1]["incorrect_answers"][1]),
            html.unescape(data["results"][1]["incorrect_answers"][2]),
        ],
        [
            html.unescape(data["results"][2]["question"]),
            html.unescape(data["results"][2]["correct_answer"]),
            html.unescape(data["results"][2]["incorrect_answers"][0]),
            html.unescape(data["results"][2]["incorrect_answers"][1]),
            html.unescape(data["results"][2]["incorrect_answers"][2]),
        ],
        [
            html.unescape(data["results"][3]["question"]),
            html.unescape(data["results"][3]["correct_answer"]),
            html.unescape(data["results"][3]["incorrect_answers"][0]),
            html.unescape(data["results"][3]["incorrect_answers"][1]),
            html.unescape(data["results"][3]["incorrect_answers"][2]),
        ],
        [
            html.unescape(data["results"][4]["question"]),
            html.unescape(data["results"][4]["correct_answer"]),
            html.unescape(data["results"][4]["incorrect_answers"][0]),
            html.unescape(data["results"][4]["incorrect_answers"][1]),
            html.unescape(data["results"][4]["incorrect_answers"][2]),
        ]
    ]

    # the correct answers to the questions 
    answer = [
        html.unescape(data["results"][0]["correct_answer"]),
        html.unescape(data["results"][1]["correct_answer"]),
        html.unescape(data["results"][2]["correct_answer"]),
        html.unescape(data["results"][3]["correct_answer"]),
        html.unescape(data["results"][4]["correct_answer"])
    ]

    # choose random the question
    li = ['', 0, 1, 2, 3, 4]
    x = random.choice(li[1:])

    # shuffle the answers 
    for i in range(4):
        mediumQ[i].pop(0)
        random.shuffle(mediumQ[i])
        mediumQ[i].insert(0,html.unescape(data["results"][i]["question"]))

    ques = Label(med_frame, text=mediumQ[x][0],
                 font="calibri 12", bg="dark orange")
    ques.place(relx=0.5, rely=0.2, anchor=CENTER)

    var = StringVar()

    # possible answers
    a = Radiobutton(med_frame, text=mediumQ[x][1], font="calibri 10",
                    value=mediumQ[x][1], variable=var, bg="dark orange")
    a.place(relx=0.5, rely=0.42, anchor=CENTER)

    b = Radiobutton(med_frame, text=mediumQ[x][2], font="calibri 10",
                    value=mediumQ[x][2], variable=var, bg="dark orange")
    b.place(relx=0.5, rely=0.52, anchor=CENTER)

    c = Radiobutton(med_frame, text=mediumQ[x][3], font="calibri 10",
                    value=mediumQ[x][3], variable=var, bg="dark orange")
    c.place(relx=0.5, rely=0.62, anchor=CENTER)

    d = Radiobutton(med_frame, text=mediumQ[x][4], font="calibri 10",
                    value=mediumQ[x][4], variable=var, bg="dark orange")
    d.place(relx=0.5, rely=0.72, anchor=CENTER)

    li.remove(x)

    timer = Label(m)
    timer.place(relx=0.8, rely=0.82, anchor=CENTER)

    def display():

        if len(li) == 1:
            m.destroy()
            showMark(score)
        if len(li) == 2:
            nextQuestion.configure(text='End', command=calc)

        if li:
            x = random.choice(li[1:])
            ques.configure(text=mediumQ[x][0])

            a.configure(text=mediumQ[x][1], value=mediumQ[x][1])

            b.configure(text=mediumQ[x][2], value=mediumQ[x][2])

            c.configure(text=mediumQ[x][3], value=mediumQ[x][3])

            d.configure(text=mediumQ[x][4], value=mediumQ[x][4])

            li.remove(x)
            y = countDown(timer, med_frame)
            if y == -1:
                display()

    def calc():
        global score
        if (var.get() in answer):
            score += 1
        display()

    # button for submitting the answers
    submit = Button(med_frame, command=calc, text="Submit",
                    fg="black", bg="dark orange", font="calibri 15")
    submit.place(relx=0.5, rely=0.9, anchor=CENTER)

    # button for the next question
    nextQuestion = Button(med_frame, command=display,
                          text="Next", fg="black", bg="dark orange")
    nextQuestion.place(relx=0.87, rely=0.82, anchor=CENTER)

    y = countDown(timer, med_frame)
    if y == -1:
        display()
    m.mainloop()


def difficult():

    global h
    h = Tk()
    h.title('Quiz - Hard Level')

    hard_canvas = Canvas(h, width=720, height=440, bg="dark orange")
    hard_canvas.pack()

    hard_frame = Frame(hard_canvas, bg="cyan")
    hard_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    # Trivia DB parameters to fetch the questions
    parameters = {
        "amount": 5, 
        "difficulty": "hard",
        "type": "multiple"
    }

    response = requests.get("https://opentdb.com/api.php", params=parameters)
    response.raise_for_status()
    data = response.json()


    global score
    score = 0

    hardQ = [
        [
            html.unescape(data["results"][0]["question"]),
            html.unescape(data["results"][0]["correct_answer"]),
            html.unescape(data["results"][0]["incorrect_answers"][0]),
            html.unescape(data["results"][0]["incorrect_answers"][1]),
            html.unescape(data["results"][0]["incorrect_answers"][2]),
        ],
        [
            html.unescape(data["results"][1]["question"]),
            html.unescape(data["results"][1]["correct_answer"]),
            html.unescape(data["results"][1]["incorrect_answers"][0]),
            html.unescape(data["results"][1]["incorrect_answers"][1]),
            html.unescape(data["results"][1]["incorrect_answers"][2]),
        ],
        [
            html.unescape(data["results"][2]["question"]),
            html.unescape(data["results"][2]["correct_answer"]),
            html.unescape(data["results"][2]["incorrect_answers"][0]),
            html.unescape(data["results"][2]["incorrect_answers"][1]),
            html.unescape(data["results"][2]["incorrect_answers"][2]),
        ],
        [
            html.unescape(data["results"][3]["question"]),
            html.unescape(data["results"][3]["correct_answer"]),
            html.unescape(data["results"][3]["incorrect_answers"][0]),
            html.unescape(data["results"][3]["incorrect_answers"][1]),
            html.unescape(data["results"][3]["incorrect_answers"][2]),
        ],
        [
            html.unescape(data["results"][4]["question"]),
            html.unescape(data["results"][4]["correct_answer"]),
            html.unescape(data["results"][4]["incorrect_answers"][0]),
            html.unescape(data["results"][4]["incorrect_answers"][1]),
            html.unescape(data["results"][4]["incorrect_answers"][2]),
        ]
    ]

    # the correct answers to the questions 
    answer = [
        html.unescape(data["results"][0]["correct_answer"]),
        html.unescape(data["results"][1]["correct_answer"]),
        html.unescape(data["results"][2]["correct_answer"]),
        html.unescape(data["results"][3]["correct_answer"]),
        html.unescape(data["results"][4]["correct_answer"])
    ]

    # choose random the question
    li = ['', 0, 1, 2, 3, 4]
    x = random.choice(li[1:])

    # shuffle the answers 
    for i in range(4):
        hardQ[i].pop(0)
        random.shuffle(hardQ[i])
        hardQ[i].insert(0,html.unescape(data["results"][i]["question"]))

    ques = Label(hard_frame, text=hardQ[x][0],
                 font="calibri 12", bg="dark orange")
    ques.place(relx=0.5, rely=0.2, anchor=CENTER)

    var = StringVar()

    # possible answers
    a = Radiobutton(hard_frame, text=hardQ[x][1], font="calibri 10",
                    value=hardQ[x][1], variable=var, bg="dark orange")
    a.place(relx=0.5, rely=0.42, anchor=CENTER)

    b = Radiobutton(hard_frame, text=hardQ[x][2], font="calibri 10",
                    value=hardQ[x][2], variable=var, bg="dark orange")
    b.place(relx=0.5, rely=0.52, anchor=CENTER)

    c = Radiobutton(hard_frame, text=hardQ[x][3], font="calibri 10",
                    value=hardQ[x][3], variable=var, bg="dark orange")
    c.place(relx=0.5, rely=0.62, anchor=CENTER)

    d = Radiobutton(hard_frame, text=hardQ[x][4], font="calibri 10",
                    value=hardQ[x][4], variable=var, bg="dark orange")
    d.place(relx=0.5, rely=0.72, anchor=CENTER)

    li.remove(x)

    timer = Label(h)
    timer.place(relx=0.8, rely=0.82, anchor=CENTER)

    def display():

        if len(li) == 1:
            h.destroy()
            showMark(score)
        if len(li) == 2:
            nextQuestion.configure(text='End', command=calc)

        if li:
            x = random.choice(li[1:])
            ques.configure(text=hardQ[x][0])

            a.configure(text=hardQ[x][1], value=hardQ[x][1])

            b.configure(text=hardQ[x][2], value=hardQ[x][2])

            c.configure(text=hardQ[x][3], value=hardQ[x][3])

            d.configure(text=hardQ[x][4], value=hardQ[x][4])

            li.remove(x)
            y = countDown(timer, hard_frame)
            if y == -1:
                display()

    def calc():
        global score
        # count=count+1
        if (var.get() in answer):
            score += 1
        display()

    # button for submitting the answers
    submit = Button(hard_frame, command=calc, text="Submit",
                    fg="black", bg="dark orange", font="calibri 15")
    submit.place(relx=0.5, rely=0.9, anchor=CENTER)

    # button for the next question
    nextQuestion = Button(hard_frame, command=display,
                          text="Next", fg="black", bg="dark orange")
    nextQuestion.place(relx=0.87, rely=0.82, anchor=CENTER)

    y = countDown(timer, hard_frame)
    if y == -1:
        display()
    h.mainloop()


# last page(shows the results)
def showMark(mark):
    sh = Tk()
    sh.title('Your Marks')

    # shows your score
    st = "Your score is "+str(mark)+"/5"
    mlabel = Label(sh, text=st, fg="black", bg="white")
    mlabel.pack()

    # if you press the "signup page" button, the last page will be erased
    def callsignUpPage():
        sh.destroy()
        start()

    def myeasy():
        sh.destroy()
        easy()

    # button for re-attempting the quiz 
    b24 = Button(sh, text="Re-attempt", command=myeasy, bg="black", fg="white")
    b24.pack()

    # creates the percentage figure
    fig = Figure(figsize=(5, 4), dpi=100)
    labels = 'Marks Obtained', 'Total Marks'
    sizes = [int(mark), 5-int(mark)]
    explode = (0.1, 0)
    fig.add_subplot(111).pie(sizes, explode=explode, labels=labels,
                             autopct='%1.1f%%', shadow=True, startangle=0)

    canvas = FigureCanvasTkAgg(fig, master=sh) 
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    # finish the quiz
    b23 = Button(text="Sign Out", command=callsignUpPage,
                 fg="white", bg="black")
    b23.pack()

    sh.mainloop()


# first page(starting page)
def start():
    global root
    root = Tk()
    root.title('Quiz App')
    canvas = Canvas(root, width=720, height=440, bg='cyan')
    canvas.grid(column=0, row=1)
    img = PhotoImage(file="quiz-icon.png")
    canvas.create_image(360, 220, image=img, anchor=CENTER)

    button = Button(root, text='Start', command=signUpPage,
                    bg="dark orange", fg="cyan")
    button.configure(width=102, height=2,
                     activebackground="cyan", relief=RAISED)
    button.grid(column=0, row=2)

    root.mainloop()


if __name__ == '__main__':
    start()
