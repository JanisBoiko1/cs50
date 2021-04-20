#Title: CS50 finance code
#Author: cs50 Staff
#Date: n.d.
#Code version: 2020
#Availability: https://cs50.harvard.edu/x/2021/psets/9/finance/

import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date
from datetime import datetime
from datetime import timedelta
import datetime
import time


from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.secret_key = "jose"

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///equilibrium.db")


@app.route("/")
@login_required
def index():
    """Show ..."""
    #show date
    today = date.today()
    data_atual = today.strftime('%m/%d/%Y')
    dayw=datetime.datetime.today().weekday()


    if(dayw == 0):
        dayWeek="Monday";
    if(dayw == 1):
        dayWeek="Tuesday";
    if(dayw == 2):
        dayWeek="Wednasday";
    if(dayw == 3):
        dayWeek="Thursday";
    if(dayw == 4):
        dayWeek="Friday";
    if(dayw == 5):
        dayWeek="Saturday";
    if(dayw == 6):
        dayWeek="Sunday";

    Date={"day": data_atual,"dayWeek": dayWeek}

    #select reminders, tasks for today, tasks for this week and month

    #reminders
    Reminders=db.execute("SELECT reminder_id, reminder, datails FROM reminders WHERE id = ? INTERSECT SELECT reminder_id, reminder, datails FROM reminders WHERE doDate = ?", session["user_id"], today)

    #tasks for today
    chores=db.execute("SELECT task_id, task, datails, complete FROM tasks WHERE id = ? INTERSECT SELECT task_id, task, datails, complete FROM tasks WHERE doDate = ?", session["user_id"], today)

    #tasks for this week
    currentDay = datetime.datetime.now().day
     #add zero to month


    currentMonth = datetime.datetime.now().month
    currentYear = datetime.datetime.now().year

    #add zero to month
    if(currentMonth < 10):
        current_month = str(currentMonth)
        current_month = "0" + current_month


    #monday: tuesday, wednesday, thursday and friday tasks
    if(dayw == 0):

        #tuesday, wednesday, thursday, friday, saturday and sunday's tasks
        if((currentDay == 31) and ((currentMonth) == 1 or (currentMonth == 3) or (currentMonth) == 5 or (currentMonth == 7) or (currentMonth == 8) or (currentMonth == 10) or (currentMonth == 12))):
            t = 1
            wd = 2
            th= 3
            f = 4
            st = 5
            sd = 6

        if((currentDay == 30) and (currentMonth == 4) or (currentMonth == 6) or (currentMonth == 9) or  (currentMonth == 11)):
            t = 1
            wd = 2
            th = 3
            f = 4
            st = 5
            sd = 6

        if((currentDay == 28) and (currentMonth == 4)):
            t = 1
            wd = 2
            th = 3
            f = 4
            st = 5
            sd = 6

        else:
            t = currentDay + 1
            wd = currentDay + 2
            th = currentDay + 3
            f = currentDay + 4
            st = currentDay + 5
            sd = currentDay + 6

        w = db.execute("SELECT task_id, task, datails, doDate, complete FROM tasks WHERE id = ?", session["user_id"])


        weeks=[]
        for x in range(len(w)):
            ww = w[x]
            split = ww["doDate"].split("-")
            if len(split) >= 3:
                taksday = split[2]
                print(taksday)
                taskmonth = split[1]
                print(taskmonth)
                taskyear = split[0]
                print(taskyear)
                if int(taskyear) != int(currentYear):
                    pass
                if int(taskmonth) == int(current_month):
                    if int(taksday) == t:
                        weeks.append(ww)
                    if int(taksday) == wd:
                        weeks.append(ww)
                        print(taksday)
                    if int(taksday) == th:
                        weeks.append(ww)
                        print(taksday)
                    if int(taksday) == f:
                        weeks.append(ww)
                        print(taksday)
                    if int(taksday) == st:
                        weeks.append(ww)
                        print(taksday)
                    if int(taksday) == sd:
                        weeks.append(ww)
                        print(taksday)

    if(dayw == 1):

        #wednesday, thursday, friday, saturday and sunday's tasks
        if((currentDay == 31) and (currentMonth == 1) or (currentMonth == 3) or (currentMonth == 5) or  (currentMonth == 7) or (currentMonth == 8) or (currentMonth == 10) or (currentMonth == 12)):
            wd = 1
            th = 2
            f = 3
            st = 4
            sd = 5

        if((currentDay == 30) and (currentMonth == 4) or (currentMonth == 6) or (currentMonth == 9) or  (currentMonth == 11)):
            wd = 1
            t = 2
            f = 3
            st = 4
            sd = 5

        if((currentDay == 28) and (currentMonth == 4)):
            wd = 1
            t = 2
            f = 3

        else:
            wd = currentDay + 1
            th = currentDay + 2
            f = currentDay + 3
            st = currentDay + 4
            sd = currentDay + 5

        w= db.execute("SELECT task_id, task, datails, doDate, complete FROM tasks WHERE id = ?", session["user_id"])

        weeks=[]
        for x in range(len(w)):
            ww = w[x]
            split = ww["doDate"].split("-")
            if len(split) >= 3:
                taksday = split[2]
                print(taksday)
                taskmonth = split[1]
                print(taskmonth)
                taskyear = split[0]
                print(taskyear)
                if int(taskyear) != int(currentYear):
                    pass
                if int(taskmonth) == int(current_month):
                    if int(taksday) == wd:
                        weeks.append(ww)
                        print(taksday)
                    if int(taksday) == th:
                        weeks.append(ww)
                        print(taksday)
                    if int(taksday) == f:
                        weeks.append(ww)
                        print(taksday)
                    if int(taksday) == st:
                        weeks.append(ww)
                        print(taksday)
                    if int(taksday) == sd:
                        weeks.append(ww)
                        print(taksday)

    if(dayw == 2):

        #thursday, friday, saturday and sunday's tasks
        if((currentDay == 31) and (currentMonth == 1) or (currentMonth == 3) or (currentMonth == 5) or  (currentMonth == 7) or (currentMonth == 8) or (currentMonth == 10) or (currentMonth == 12)):
            th = 1
            f = 2
            st = 3
            sd = 4

        if((currentDay == 30) and (currentMonth == 4) or (currentMonth == 6) or (currentMonth == 9) or  (currentMonth == 11)):
            th = 1
            f = 2
            st = 3
            sd = 4

        if((currentDay == 28) and (currentMonth == 4)):
            th = 1
            f = 2
            st = 3
            sd = 4

        else:
            th = currentDay + 1
            f = currentDay + 2
            st = currentDay + 3
            sd = currentDay + 4

        w= db.execute("SELECT task_id, task, datails, doDate, complete FROM tasks WHERE id = ?", session["user_id"])

        weeks=[]
        for x in range(len(w)):
            ww = w[x]
            split = ww["doDate"].split("-")
            if len(split) >= 3:
                taksday = split[2]
                print(taksday)
                taskmonth = split[1]
                print(taskmonth)
                taskyear = split[0]
                print(taskyear)
                if int(taskyear) != int(currentYear):
                    pass
                if int(taskmonth) == int(current_month):
                    if int(taksday) == th:
                        weeks.append(ww)
                        print(taksday)
                    if int(taksday) == f:
                        weeks.append(ww)
                        print(taksday)
                    if int(taksday) == st:
                        weeks.append(ww)
                        print(taksday)
                    if int(taksday) == sd:
                        weeks.append(ww)
                        print(taksday)


    if(dayw == 3):

        #friday, saturday and sunday's tasks
        if((currentDay == 31) and (currentMonth == 1) or (currentMonth == 3) or (currentMonth == 5) or (currentMonth == 7) or (currentMonth == 8) or (currentMonth == 10) or (currentMonth == 12)):
            f = 1
            st = 2
            sd = 3

        if((currentDay == 30) and (currentMonth == 4) or (currentMonth == 6) or (currentMonth == 9) or (currentMonth == 11)):
            f = 1
            st = 2
            sd = 3

        if((currentDay == 28) and (currentMonth == 4)):
            f = 1
            st = 2
            sd = 3

        else:
            f = currentDay + 1
            st = currentDay + 2
            sd = currentDay + 3

        w= db.execute("SELECT task_id, task, datails, doDate, complete FROM tasks WHERE id = ?", session["user_id"])

        weeks=[]
        for x in range(len(w)):
            ww = w[x]
            split = ww["doDate"].split("-")
            if len(split) >= 3:
                taksday = split[2]
                print(taksday)
                taskmonth = split[1]
                print(taskmonth)
                taskyear = split[0]
                print(taskyear)
                if int(taskyear) != int(currentYear):
                    pass
                if int(taskmonth) == int(current_month):
                    if int(taksday) == f:
                        weeks.append(ww)
                        print(taksday)
                    if int(taksday) == st:
                        weeks.append(ww)
                        print(taksday)
                    if int(taksday) == sd:
                        weeks.append(ww)
                        print(taksday)


    if(dayw == 4):
        #saturday and sunday's tasks
        if((currentDay == 31) and (currentMonth == 1) or (currentMonth == 3) or (currentMonth == 5) or (currentMonth == 7) or (currentMonth == 8) or (currentMonth == 10) or (currentMonth == 12)):
            st = 1
            sd = 2

        if((currentDay == 30) and (currentMonth == 4) or (currentMonth == 6) or (currentMonth == 9) or (currentMonth == 11)):
            st = 1
            sd = 2

        if((currentDay == 28) and (currentMonth == 4)):
            st = 1
            sd = 2

        else:
            st = currentDay + 1
            sd = currentDay + 2

        w= db.execute("SELECT task_id, task, datails, doDate, complete FROM tasks WHERE id = ?", session["user_id"])

        weeks=[]
        for x in range(len(w)):
            ww = w[x]
            split = ww["doDate"].split("-")
            if len(split) >= 3:
                taksday = split[2]
                print(taksday)
                taskmonth = split[1]
                print(taskmonth)
                taskyear = split[0]
                print(taskyear)
                if int(taskyear) != int(currentYear):
                    pass
                if int(taskmonth) == int(current_month):
                    if int(taksday) == st:
                        weeks.append(ww)
                        print(taksday)
                    if int(taksday) == sd:
                        weeks.append(ww)
                        print(taksday)



    if(dayw == 5):
        #sunday's tasks
        if((currentDay == 31) and (currentMonth == 1) or (currentMonth == 3) or (currentMonth == 5) or (currentMonth == 7) or (currentMonth == 8) or (currentMonth == 10) or (currentMonth == 12)):
            sd = 1

        if((currentDay == 30) and (currentMonth == 4) or (currentMonth == 6) or (currentMonth == 9) or (currentMonth == 11)):
            sd = 1

        if((currentDay == 28) and (currentMonth == 4)):
            sd = 1

        else:
            sd = currentDay + 1

        w= db.execute("SELECT task_id, task, datails, doDate, complete FROM tasks WHERE id = ?", session["user_id"])

        weeks=[]
        for x in range(len(w)):
            ww = w[x]
            split = ww["doDate"].split("-")
            if len(split) >= 3:
                taksday = split[2]
                print(taksday)
                taskmonth = split[1]
                print(taskmonth)
                taskyear = split[0]
                print(taskyear)
                if int(taskyear) != int(currentYear):
                    pass
                if int(taskmonth) == int(current_month):
                    if int(taksday) == sd:
                        weeks.append(ww)
                        print(taksday)


    if(dayw == 6):
        Weeks = []
        weeks = []

    #tasks for this month

    if(currentMonth < 10):
        current_month = str(currentMonth)
        current_month = "0" + current_month

    months=db.execute("SELECT task_id, task, datails, doDate, complete FROM monthTasks WHERE id = ?", session["user_id"])

    Months=[]
    for y in range(len(months)):
        m = months[y]
        monthsplit = m["doDate"].split("-")
        if len(monthsplit) >= 3:
            taskmonth = monthsplit[1]
            taskyear = monthsplit[0]
            if int(taskyear) != int(currentYear):
                pass
            if int(taskmonth) == int(current_month):
                Months.append(m)


    print(weeks)

    return render_template("index.html", Reminders = Reminders, Date = Date, chores = chores, weeks=weeks, Months = Months)


@app.route("/reminders", methods=["GET", "POST"])
@login_required
def reminders():
    """Add and show reminders """
    if request.method == "POST":

        if not request.form.get("reminder"):
            return apology("must provide reminder", 400)


        if not request.form.get("date"):
            return apology("must provide date", 400)

        reminder = request.form.get("reminder")

        details = request.form.get("details")

        date = request.form.get("date")

        #insert reminder in db
        db.execute("INSERT INTO reminders(id, reminder, datails, doDate) VALUES(?,?,?,?)", session["user_id"], reminder, details, date)

        return redirect(url_for('reminders'))

    else:

        reminders=db.execute("SELECT reminder_id, reminder, datails, doDate FROM reminders WHERE id = ?", session["user_id"])

        Reminders=[]

        for x in range (len(reminders)):
            r = reminders[x]
            datesplit = r["doDate"].split("-")
            if len(datesplit) >= 3:
                year = datesplit[0]
                month = datesplit[1]
                day = datesplit[2]
                final_date = month + "/" + day + "/" + year
                r["doDate"] = final_date
            Reminders.append(r)

        return render_template("reminders.html", Reminders = Reminders)

#Based on:
#Title: Python Flask Beginner Tutorial - Todo App - Crash Course
#Author: Python Engineer
#Date: 2020
#Code version: none
#Availability: https://www.youtube.com/watch?v=yKHJsLUENl0

@app.route('/delete2/<int:Reminder_reminder_id>')
def delete2(Reminder_reminder_id):
    reminder=db.execute("SELECT * FROM reminders WHERE id =? INTERSECT SELECT * FROM reminders WHERE reminder_id = ?", session["user_id"], Reminder_reminder_id)

    db.execute("DELETE FROM reminders WHERE id =? and reminder_id =?", session["user_id"], Reminder_reminder_id)

    return redirect(url_for('reminders'))

#Based on: Title: Build a HIIT Timer with Flask and JavaScript (Part 2)
#Author: teclado
#Date: 2020
#Aveilability: https://www.youtube.com/watch?v=9YUy26jb33g
@app.route("/timer", methods=["GET", "POST"])
@login_required
def timer():
    """ Tomato timer config """
    if request.method == "POST":

        work_min = int(request.form["work_min"])

        break_min = int(request.form["break_min"])

        sets = int(request.form["sets"])

        session["work_min"] = work_min

        session["break_min"] = break_min

        session["sets"] = sets
        session["set_counter"] = 0

        work_total = work_min*60

        break_total = break_min*60

        session["work_total"] = work_total
        session["break_total"] = break_total

        if(work_min < 10):
            workMin = "0" + str(work_min)
            session["work_min"] = workMin

        if(break_min < 10):
            breakMin = "0" + str(break_min)
            session["break_min"] = breakMin

        return redirect(url_for("work"))
    else:
        return render_template("timer.html")

@app.route("/work", methods=["GET"])
@login_required
def work():
    """ Pomodoro """

    if session["set_counter"] == session["sets"]:
        return redirect(url_for("completed"))
    session["set_counter"] += 1
    return render_template("work.html", work_total = session["work_total"], work_min = session["work_min"])

@app.route("/break", methods=["GET"])
@login_required
def break_time():
    """ Break """
    return render_template("break.html", break_total = session["break_total"], break_min = session["break_min"])

@app.route("/complete")
@login_required
def completed():
    """ Work done """
    return render_template("completed.html", sets=session["sets"])

#Based on:
#Title: CS50 finance code
#Author: cs50 Staff
#Date: n.d.
#Code version: 2020
#Availability: https://cs50.harvard.edu/x/2021/psets/9/finance/
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

#Based on:
#Title: CS50 finance code
#Author: cs50 Staff
#Date: n.d.
#Code version: 2020
#Availability: https://cs50.harvard.edu/x/2021/psets/9/finance/
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/tasks")
@login_required
def show():
    """ Show tasks """
    #show what day is it
    data_atual = date.today().strftime('%m/%d/%Y')
    dayw=datetime.datetime.today().weekday()

    if(dayw == 0):
        dayWeek="Monday";
    if(dayw == 1):
        dayWeek="Tuesday";
    if(dayw == 2):
        dayWeek="Wednasday";
    if(dayw == 3):
        dayWeek="Thursday";
    if(dayw == 4):
        dayWeek="Friday";
    if(dayw == 5):
        dayWeek="Saturday";
    else:
        dayWeek="Sunday";

    Date={"day": data_atual,"dayWeek": dayWeek}

    #show tasks list
    data=db.execute("SELECT task_id, task, datails, doDate, complete FROM tasks WHERE id = ?", session["user_id"])
    chores=[]

    for x in range (len(data)):
        Tasks = data[x]
        datesplit = Tasks["doDate"].split("-")
        if len(datesplit) >= 3:
            year = datesplit[0]
            month = datesplit[1]
            day = datesplit[2]
            do_date = month + "/" + day + "/" + year
            Tasks["doDate"] = do_date
        chores.append(Tasks)


    return render_template("tasks.html", chores=chores, Date=Date)

@app.route("/add", methods=["POST"])
@login_required
def addtasks():
    """Add tasks"""
    #Render apology if task input is blank
    if not request.form.get("newtask"):
        return apology("must provide Task", 400)

    #save new task in tasks table
    task = request.form.get("newtask")

    details = request.form.get("details")

    doDate = request.form.get("doDate")

    if not request.form.get("doDate"):
        return apology("must provide do date", 400)

    lengthType = request.form.get("lengthType")

    #if the duration of the task is bigger than one day, it must be saved in another database and show to the users in other ways
    lengthNumber=request.form.get("lengthNumber")

    if not request.form.get("lengthNumber"):
        return apology("must provide expected duration", 400)

    if not request.form.get("lengthType"):
        return apology("must provide expected duration", 400)

    #saving the duration of as a number of hours
    temp=0

    if (lengthType == "Hours"):
        temp=1

    if (lengthType == "Days"):
        temp=24

    if (lengthType == "Weeks"):
        temp=168

    totalLength = temp * int(lengthNumber)

    #insert task in DB
    db.execute("INSERT INTO tasks(id, task, datails, length, doDate, complete) VALUES(?,?,?,?,?,?)", session["user_id"], task, details, totalLength, doDate, 0)

    #if task takes more than 7 days
    if (totalLength > 168):

        m=db.execute("INSERT INTO monthTasks(id, task, datails, length, doDate, complete) VALUES(?,?,?,?,?,?)", session["user_id"], task, details, totalLength, doDate, 0)

    return redirect(url_for('show'))

#Based on:
#Title: Python Flask Beginner Tutorial - Todo App - Crash Course
#Author: Python Engineer
#Date: 2020
#Code version: none
#Availability: https://www.youtube.com/watch?v=yKHJsLUENl0
@app.route('/update/<int:chore_task_id>')
def update(chore_task_id):
    task=db.execute("SELECT * FROM tasks WHERE id =? INTERSECT SELECT * FROM tasks WHERE task_id = ?", session["user_id"], chore_task_id)
    db.execute("UPDATE tasks SET complete =? WHERE id =? and task_id =?", 1, session["user_id"], chore_task_id  )

    return redirect(url_for('show'))

@app.route('/delete/<int:chore_task_id>')
def delete(chore_task_id):
    task=db.execute("SELECT * FROM tasks WHERE id =? INTERSECT SELECT * FROM tasks WHERE task_id = ?", session["user_id"], chore_task_id)

    db.execute("DELETE FROM tasks WHERE id =? and task_id =?", session["user_id"], chore_task_id)

    return redirect(url_for('show'))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # Render an apology if the user’s input is blank
        if not request.form.get("username"):
            return apology("Must provide username", 400)

        #or the username already exists.
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if (len(rows) != 0):
            return apology("Username taken, please choose a new one", 400)

        #Render apology it no password
        if not request.form.get("password"):
            return apology("Must provide password", 400)

        #Render apology if no confirmation
        if not request.form.get("confirmation"):
            return apology("Must provide password confirmation", 400)

        else:
            #username
            username = request.form.get("username")

            #password
            password = request.form.get("password")

            #Hash the user’s password with generate_password_hash
            password_hash = generate_password_hash(password)
            confirmation = request.form.get("confirmation")

            #Render an apology if either input is blank or the passwords do not match.
            if password != confirmation:
                return apology("Password and password confirmation do not match.", 400)

        #INSERT the new user into users, storing a hash of the user’s password, not the password itself.
        userId = db.execute("INSERT INTO users(username, hash) VALUES(?,?)", username, password_hash)

        if userId is None:
            return apology("Registration error", 403)

        session["user_id"] = userId

        return redirect("/login")

    else:
        return render_template("register.html")


#Based on:
#Title: Using FullCalendar.js in Flask - Python Backend #1
#Author: Gordon Chan
#Date: 2020
#Code version: none
#Availability:https://www.youtube.com/watch?v=VXW2A4Q81Ok -->
@app.route("/calendar", methods=["GET"])
@login_required
def calendar():
    """Show plans for on a calendar"""

    rows = db.execute("SELECT task, doDate, complete FROM tasks WHERE id = ?", session["user_id"])

    reminders=db.execute("SELECT reminder, doDate FROM reminders WHERE id = ?", session["user_id"])

    events = []
    for x in range (len(rows)):
        data=rows[x]
        if data["complete"] == 0:
            events.append(data)

    for y in range (len(reminders)):
        r=reminders[y]
        t=r["reminder"]
        r["task"]=t
        events.append(r)

    return render_template("calendar.html", events = events)


@app.route("/selfcare", methods=["GET"])
@login_required
def selfcare():
    """Show selfcare activitys"""
    activities = db.execute("SELECT * FROM selfcare WHERE id = ?", session["user_id"])
    return render_template("selfcare.html", activities = activities)


@app.route("/scadd", methods=["POST"])
@login_required
def scadd():
    """Add activity"""
    if not request.form.get("activity"):
        return apology("must provide activity", 400)

    #save new activity in selfcare table
    activity = request.form.get("activity")

    details = request.form.get("details")

    #insert activity into DB
    db.execute("INSERT INTO selfcare(id, activity, details, complete) VALUES(?,?,?,?)", session["user_id"], activity, details, 0)

    return redirect(url_for('selfcare'))

#Based on:
#Title: Python Flask Beginner Tutorial - Todo App - Crash Course
#Author: Python Engineer
#Date: 2020
#Code version: none
#Availability: https://www.youtube.com/watch?v=yKHJsLUENl0
@app.route('/updatesc/<int:activity_activity_id>')
def updatesc(activity_activity_id):
    """Complete activity"""

    activity=db.execute("SELECT * FROM selfcare WHERE id =? INTERSECT SELECT * FROM selfcare WHERE activity_id = ?", session["user_id"], activity_activity_id)
    db.execute("UPDATE selfcare SET complete =? WHERE id =? and activity_id =?", 1, session["user_id"], activity_activity_id)
    print(activity)

    return redirect(url_for('selfcare'))

@app.route('/deletesc/<int:activity_activity_id>')
def deletesc(activity_activity_id):
    """Delete activity"""

    activity=db.execute("SELECT * FROM selfcare WHERE id =? INTERSECT SELECT * FROM selfcare WHERE activity_id = ?", session["user_id"], activity_activity_id)

    db.execute("DELETE FROM selfcare WHERE id =? and activity_id =?", session["user_id"], activity_activity_id)

    return redirect(url_for('selfcare'))

#Based on: Title: Build a HIIT Timer with Flask and JavaScript (Part 2)
#Author: teclado
#Date: 2020
#Aveilability: https://www.youtube.com/watch?v=9YUy26jb33g
@app.route("/meditation", methods=["GET", "POST"])
@login_required
def meditation():
    """Set meditation timer"""
    if request.method == "POST":

        duration = int(request.form["duration"])

        interval = int(request.form["interval"])

        durationSec = duration*60

        intervalSec = interval*60

        session["duration"] = duration
        session["interval"] = interval

        if (duration < 10):
            Duration = "0" + str(duration)
            session ["duration"] = Duration

        if (interval < 10):
            Interval = "0" + str(interval)
            session ["interval"] = Interval

        session["durationSec"] = durationSec
        session["intervalSec"] = intervalSec

        return redirect(url_for("meditationDuration"))
    else:
        return render_template("meditation.html")

@app.route("/meditationDuration", methods=["GET"])
@login_required
def meditationDuration():
    """Meditation ongoing"""
    return render_template("meditationDuration.html", duration = session["duration"], durationSec = session["durationSec"])

@app.route("/meditationInterval", methods=["GET"])
@login_required
def meditationInterval():
    """Interval"""
    return render_template("meditationInterval.html", interval = session["interval"],  intervalSec = session["intervalSec"])

@app.route("/meditationComplete")
@login_required
def meditationComplete():
    """Meditation done"""
    return render_template("meditationComplete.html")

@app.route("/journal", methods=["POST"])
@login_required
def journal():
    """Write entrys on a journal and query old entrys"""
    if not request.form.get("journal"):
        return apology("must provide entry", 400)

    # store entry in a variable
    text = request.form.get("journal")

    #add text to journal table
    data_atual = date.today()
    db.execute("INSERT INTO journal(id, entry, date) VALUES(?,?,?)", session["user_id"], text, data_atual)

    return redirect(url_for('journaling'))

@app.route("/journaling", methods=["GET"])
@login_required
def journaling():
    return render_template("journaling.html")

@app.route("/query", methods=["POST", "GET"])
@login_required
def query():
    """Show old entrys"""

    if request.method == "POST":
        date = request.form.get("date")

        if not request.form.get("date"):
            return apology("must provide date", 400)


        entrys = db.execute("SELECT * FROM journal WHERE id=? INTERSECT SELECT * FROM journal WHERE date = ?", session["user_id"], date)

        return render_template("oldentrys.html",  entrys = entrys)

    else:
        return render_template("oldentrys.html")

@app.route("/scores", methods=["GET"])
@login_required
def scores():

    scores_g=db.execute("SELECT * FROM score WHERE id=?", session["user_id"])

    return render_template("scores.html", scores = scores_g)

#Based on:
#Title: CS50 finance code
#Author: cs50 Staff
#Date: n.d.
#Code version: 2020
#Availability: https://cs50.harvard.edu/x/2021/psets/9/finance/
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
