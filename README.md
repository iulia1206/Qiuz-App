# App Description #
A quiz app created with GUI in python using tkinter. The app opens the starting frame prompting you to start the quiz. After pressing the button, you are taken on a login page. You can choose to create an account or login with an existing one. The sign up page requires you to fill all fields.

After starting the Quiz, you have to choose your test's difficulty level. The 5 questions are randomly generated from TriviaDB's API, so they are most likely to be different at every run.

After choosing the difficulty, you have 25 seconds to answer the questions. If the time is up and you do not click submit, your answer will not be registered.

After taking the quiz you have a diagram pie that represents your results. You can choose to re-attempt the quiz (with different questions) or, if you want a different one, you have to sign out, sign in and choose your difficulty.

# Implementation #

The main features of this app are : 
* TkInter GUI
* SQLite login page
* TriviaDB API
* timer on questions

We began by creating the FrontEnd, the start page, sign up page and login page using TkInter's Documentation. In quiz.db are stored the accounts and the application connects to this database using SQLite syntax (functions addUserToDataBase and gotoLogin).

Then, we created the menu prompting you to choose the difficulty and start the actual quiz based on that. Every difficulty has its special functions getting the questions from TriviaDB's API. Based on the button pressed we start each function. Using the requests module, we get the questions from https://opentdb.com/api_config.php. Then, start the quiz, display the questions, get the answers and display the countdown on the TkInter frame. 

After each question is displayed and we get the responses, we build a diagram pie using matplotlib and display it. We have also implemented the Re-attempt and Sign Out buttons by destroying the current frame and calling back the functions from the beginning.

# How to Run #
In order to start the application make sure that both quiz.py and quiz-icon.png are in the same file. Otherwise, it is going to trigger a TkInter Exception. Run the following command in bash:

```bash
$ python quiz.py
```
# Documentation #
* https://docs.python.org/3/library/tk.html
* https://compucademy.net/user-login-with-python-and-sqlite/
* https://www.udemy.com/course/100-days-of-code/
* https://www.w3schools.com/python/matplotlib_pie_charts.asp
* https://datatofish.com/matplotlib-charts-tkinter-gui/
* https://www.geeksforgeeks.org/how-to-embed-matplotlib-charts-in-tkinter-gui/

# Project Contribution #
 * Iulia-Andreea Constantinescu - TriviaDB fetch, easy, medium and difficult functions, start page
 * Cicoare Ana-Maria - SQLite login, login page, timer, diagram pie and the showmark function (the last page)

 # Difficulties #
 By being total beginners, we had no idea how to use the TkInter GUI, labels, frames, grid and everything. So, we had quite a hard time learning those in order to succeed (since this project was heavily based on that). Then, we had the idea of implementing a pie chart for the correct answer ratio and we did not really have any idea on how to start doing that (we did not know of matplotlib before). But overall, the most difficult part was the implementation of the GUI and putting everything on the frame/label (not forgetting the .pack()). 
