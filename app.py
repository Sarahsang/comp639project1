from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from datetime import datetime, timedelta, date
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import datetime
from dateutil.relativedelta import relativedelta

import connect
import queries

app = Flask(__name__)

dbconn = None
connection = None

#User global variable for passing logged in user information
user = None

#Date time global variables for queries
today=datetime.date.today()
today_string=today.strftime("%Y-%m-%d")
now = datetime.datetime.now() 
now_string=now.strftime("%H:%M:%S")
currentyear=today.strftime("%Y")
currentquarter=date.month
YTD_months=today.month
QTD_months=today.month%3
start_of_week = today - datetime.timedelta(days=today.weekday())
end_of_week = start_of_week + datetime.timedelta(days=6)
currentweek=[start_of_week,start_of_week + datetime.timedelta(days=1),start_of_week + datetime.timedelta(days=2),start_of_week + datetime.timedelta(days=3),start_of_week + datetime.timedelta(days=4),start_of_week + datetime.timedelta(days=5),end_of_week]
nextweek=[start_of_week+datetime.timedelta(days=7),start_of_week+datetime.timedelta(days=8),start_of_week+datetime.timedelta(days=9),start_of_week+datetime.timedelta(days=10),start_of_week+datetime.timedelta(days=11),start_of_week+datetime.timedelta(days=12),end_of_week+datetime.timedelta(days=7)]
nextnextweek=[start_of_week+datetime.timedelta(days=14),start_of_week+datetime.timedelta(days=15),start_of_week+datetime.timedelta(days=16),start_of_week+datetime.timedelta(days=17),start_of_week+datetime.timedelta(days=18),start_of_week+datetime.timedelta(days=19),end_of_week+datetime.timedelta(days=14)]

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    port=connect.dbport, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn


@app.route('/')
def home():
    return render_template("login.html")

# log in through email and password
@app.route ("/login", methods=["post", "get"])
def login():
    global user
    # get the user's login information from the form
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')

    """
    print(email)
    print(password)
    print(role)
    """

    if role=="member":
        connection=getCursor()
        connection.execute(queries.member_login(), (email, password,))
        member = connection.fetchone()
        connection.close()
        # check if email and password exist
        if member:
            #set global variable user
            user = member
            return redirect(url_for('memberHome', member=user))
        else:
            loginFail="Log in fails, try again"
            return render_template ("login.html", loginFail=loginFail )
    
    elif role=="trainer":
        connection=getCursor()
        connection.execute(queries.trainer_login(), (email, password,))
        trainer = connection.fetchone()
        connection.close()
        if trainer:
            #set global variable user
            user = trainer
            return redirect(url_for('trainerHome', trainer=user))
        else:
            loginFail="Log in fails, try again"
            return render_template ("login.html", loginFail=loginFail )
    
    elif role=="admin":
        connection=getCursor()
        connection.execute(queries.admin_login(), (email, password,))
        admin= connection.fetchone()
        connection.close()
        if admin:
            #set global variable user
            user = admin
            return redirect(url_for('adminHome', admin=user))
        else:
            loginFail="Log in fails, try again"
            return render_template ("login.html", loginFail=loginFail )
        
 #BLW adding a Join as New Member to login page       
@app.route('/join')
def join():
    return render_template('addmember.html', date=date, relativedelta=relativedelta)

#BLW adding a Pay Subscriptions

@app.route('/newMember/pay')
def newMemberpay():
    return render_template('payments.html')

@app.route ("/join/addMemberComplete", methods=["POST", "GET"])
def joinnewMemberComplete():
    role=request.form.get('member')
    first_name=request.form.get('first_name')
    last_name=request.form.get('last_name')
    email=request.form.get('email')
    password=request.form.get('password')
    gender=request.form.get('gender')
    date_of_birth=request.form.get('date_of_birth')
    phone_number=request.form.get('phone_number')
    address=request.form.get('address')
    outcomes=request.form.get('outcomes')
    weight=request.form.get('weight')
    body_fat_percentage=request.form.get('bmi')
    blood_pressure=request.form.get('bp')
    general_comments=request.form.get('comments')
    connection=getCursor()
    connection.execute(queries.add_member(), (first_name, last_name, email, password, gender, date_of_birth, phone_number, address, outcomes ))
    connection.execute("SELECT * FROM member WHERE id = LAST_INSERT_ID()")
    newMember=connection.fetchone()
    id=newMember[0]
    connection.execute(queries.add_account(), (id, id, 0, datetime.date.today(), datetime.date.today(), datetime.date.today()+relativedelta(months=+12)  ))
    current_date = datetime.date.today()
    connection.execute("INSERT INTO memberhealth (member_id,  health_id, value, date) VALUES (%s,%s,%s,%s)", (id, 1,weight,  current_date))
    connection.execute("INSERT INTO memberhealth (member_id,  health_id, value, date) VALUES (%s,%s,%s,%s)", (id, 2, body_fat_percentage ,  current_date))
    connection.execute("INSERT INTO memberhealth (member_id,  health_id, value, date) VALUES (%s,%s,%s,%s)", (id, 3, blood_pressure ,  current_date))
    connection.execute("INSERT INTO memberhealth (member_id,  health_id, value, date) VALUES (%s,%s,%s,%s)", (id, 4, general_comments ,  current_date)) 
    connection.execute(queries.newmemberpay(), (id, 200, 3, "monthlypaymentdirectdebit",datetime.date.today(),))
    connection.close()
    return render_template("newMemberConfirm.html", newMember=newMember, date=date, relativedelta=relativedelta, datetime=datetime)
    
# homepage for members
@app.route('/memberHome', methods=["GET", "POST"])
def memberHome():
    # get the member's account information
    connection = getCursor()
    member = request.args.get('member')
    connection.execute('''SELECT member_id, contract_lastdate from account where member_id=%s''', (member,))
    membership = connection.fetchone()
    connection.close()
    
    if membership:
        contract_lastdate = membership[1]
        days_left = (contract_lastdate - datetime.date.today()).days
        
        # if the membership has expired
        if days_left <= 0:
            return render_template('memberHome.html', member=user, popup="true", message="Oh no! It looks like your gym membership has expired. To avoid any interruption to your fitness routine, please renew your membership as soon as possible.")
        # if the membership will expire in 14 days or less
        elif days_left <= 14:
            return render_template('memberHome.html', member=user,  popup="true", message=f"Heads up! Your membership will expire in {days_left} days. Renew to keep your gym access.")
        # if the membership is still valid
        else:
            return render_template('memberHome.html', member=user,  popup="true", message="Welcome to the gym. Ready to sweat?")     
    # other situation
    else:
        return render_template('memberHome.html', member=user)

# homepage for trainers
@app.route('/trainerHome')
def trainerHome():
    return render_template('trainerHome.html', trainer=user)
# homepage for admin
@app.route('/adminHome')
def adminHome():
    return render_template('adminHome.html', admin=user)
  
# Display member profile for members
@app.route ("/member", methods=["POST", "GET"])
def member():
    id = request.args.get('id')
    connection = getCursor()
    connection.execute(queries.member_profile(), (id,))
    memberprofile=connection.fetchall()
    connection.execute(queries.member_subscription(), (id,))
    subscription_detail=connection.fetchall()
    member=[mb for mb in memberprofile]
    date_str=str(member[0][7])
    formatted_date = format_date(date_str)
    sub=[sub for sub in subscription_detail]
    date_time_str=str(sub[0][1])
    formatted_date_time = format_date(date_time_str)
    connection.close()
    return render_template("memberprofile.html", member=user, date_time=formatted_date_time, date=formatted_date, memberprofile=memberprofile, subscriptionDetail=subscription_detail)

# Display member profile for admin
@app.route ("/memberprofile", methods=["POST", "GET"])
def memberprofile():
    id = request.args.get('id')
    connection = getCursor()
    connection.execute(queries.member_profile(), (id,))
    memberprofile=connection.fetchall()
    connection.execute(queries.member_subscription(), (id,))
    subscription_detail=connection.fetchall()
    member=[mb for mb in memberprofile]
    date_str=str(member[0][7])
    formatted_date = format_date(date_str)
    sub=[sub for sub in subscription_detail]
    date_time_str=str(sub[0][1])
    formatted_date_time = format_date(date_time_str)
    connection.close()
    return render_template("memberprofile.html", date_time=formatted_date_time, date=formatted_date, admin=user, memberprofile=memberprofile, subscriptionDetail=subscription_detail)

# Display member profile for trainer
@app.route ("/trainermember", methods=["POST", "GET"])
def trainermember():
    id = request.args.get('id')
    connection = getCursor()
    connection.execute(queries.member_profile(), (id,))
    memberprofile=connection.fetchall()
    connection.execute(queries.member_subscription(), (id,))
    subscription_detail=connection.fetchall()
    member=[mb for mb in memberprofile]
    date_str=str(member[0][7])
    formatted_date = format_date(date_str)
    sub=[sub for sub in subscription_detail]
    date_time_str=str(sub[0][1])
    formatted_date_time = format_date(date_time_str)
    connection.close()
    return render_template("memberprofile.html", trainer=user, date_time=formatted_date_time, date=formatted_date, memberprofile=memberprofile, subscriptionDetail=subscription_detail)


# convert date format to DD MM, YYYY
def format_date(date_str):
    from datetime import datetime
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%d %B, %Y")
    return formatted_date

# convert date and time format to DD MM, YYYY HH:MM:SS AM/PM
def format_date_time(date_time_str):
    from datetime import datetime
    date_obj = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
    formatted_date_time = date_obj.strftime("%d %B, %Y %I:%M:%S %p")
    return formatted_date_time

    
# Display member list for admin    
@app.route ("/admin/member", methods=["POST", "GET"])
def clickmember_admin():
    connection = getCursor()
    connection.execute(queries.member_list())
    memberprofile=connection.fetchall()
    connection.close()
    return render_template("memberlist.html", admin=user, memberprofile=memberprofile)

# Search a member for admin
@app.route ("/searchmember", methods=["POST", "GET"])
def searchmember():     
    if  request.method == "POST":
        searchId = request.form.get('memberid')
        Name = request.form.get('name')
        if not searchId and not Name:
            return render_template("memberlist.html", admin=user, searchFail="Please enter a member ID or a member name to search for.")           
        connection=getCursor()
        # If search by member id, data of searchId will then be passed to SQL to fetch the matched result.  
        if searchId:    
            connection.execute(queries.search_member_id(), (searchId,))
            memberprofile = connection.fetchall()
            if not memberprofile:
                return render_template("memberlist.html", admin=user, searchFail="No results found. Please try again.")
            return render_template("memberlist.html", admin=user, memberprofile = memberprofile)
        # If search by member name, check whether by full name or first name only.
        if Name:
            if " " in Name:
                Firstname, Familyname=Name.split(" ")
                connection.execute(queries.search_member_name(), (Firstname, Familyname))
                memberprofile = connection.fetchall()
                if not memberprofile:
                    return render_template("memberlist.html", admin=user, searchFail="No results found. Please try again.")
                return render_template("memberlist.html", admin=user, memberprofile = memberprofile) 
            else:
                Firstname=Name              
                connection.execute(queries.search_member_firstname(), (Firstname,))
                memberprofile = connection.fetchall()
                if not memberprofile:
                    return render_template("memberlist.html", admin=user, searchFail="No results found. Please try again.")
                return render_template("memberlist.html", admin=user, memberprofile = memberprofile) 
    return render_template("memberlist.html", admin=user)        




#View Timetable as an Admin
@app.route("/admin/timetable")
def clickclass_Admin():
    #Get list of all trainers
    connection=getCursor()
    connection.execute(queries.trainer_list())
    trainer_list=connection.fetchall()
    #timetable for current week
    connection.execute(queries.full_time_table_between_twodate(),(currentweek[0],currentweek[6]+datetime.timedelta(days=1)))
    classes_cw=connection.fetchall()
    #timetable for next week
    connection.execute(queries.full_time_table_between_twodate(),(nextweek[0],nextweek[6]+datetime.timedelta(days=1)))
    classes_nw=connection.fetchall()
    #timetable for following week
    connection.execute(queries.full_time_table_between_twodate(),(nextnextweek[0],nextnextweek[6]+datetime.timedelta(days=1)))
    classes_nnw=connection.fetchall()
    connection.close()
    #time array as reference for drawing the grid, to hide the hours that have no data at all
    timelist_cw = [(row[14]).seconds/3600 for row in classes_cw]
    timelist_nw = [(row[14]).seconds/3600 for row in classes_nw]
    timelist_nnw = [(row[14]).seconds/3600 for row in classes_nnw]
    return render_template("classlist.html", admin=user, user=user, classes=classes_cw, trainer_list=trainer_list, timelist_cw=timelist_cw, classes_nw=classes_nw, timelist_nw=timelist_nw, classes_nnw=classes_nnw, timelist_nnw=timelist_nnw, currentweek=currentweek, nextweek=nextweek, nextnextweek=nextnextweek)

#View Timetable as an Trainer
@app.route("/trainer/timetable")
def clickclass_Trainer():
    #Get list of all trainers
    connection=getCursor()
    connection.execute(queries.trainer_list())
    trainer_list=connection.fetchall()
    #timetable for current week
    connection.execute(queries.full_time_table_between_twodate(),(currentweek[0],currentweek[6]+datetime.timedelta(days=1)))
    classes_cw=connection.fetchall()
    #timetable for next week
    connection.execute(queries.full_time_table_between_twodate(),(nextweek[0],nextweek[6]+datetime.timedelta(days=1)))
    classes_nw=connection.fetchall()
    #timetable for following week
    connection.execute(queries.full_time_table_between_twodate(),(nextnextweek[0],nextnextweek[6]+datetime.timedelta(days=1)))
    classes_nnw=connection.fetchall()
    connection.close()
    #time array as reference for drawing the grid, to hide the hours that have no data at all
    timelist_cw = [(row[14]).seconds/3600 for row in classes_cw]
    timelist_nw = [(row[14]).seconds/3600 for row in classes_nw]
    timelist_nnw = [(row[14]).seconds/3600 for row in classes_nnw]
    return render_template("classlist.html", trainer=user, user=user, trainer_list=trainer_list, classes=classes_cw, timelist_cw=timelist_cw, classes_nw=classes_nw, timelist_nw=timelist_nw, classes_nnw=classes_nnw, timelist_nnw=timelist_nnw, currentweek=currentweek, nextweek=nextweek, nextnextweek=nextnextweek)

#Trainer requests to view their own timetable
@app.route("/trainer/mytimetable")
def clickmyclass_Trainer():
    #timetable for current week
    connection=getCursor()
    connection.execute(queries.trainer_time_table_between_twodate(),(currentweek[0],currentweek[6]+datetime.timedelta(days=1),int(user[0])))
    classes_cw=connection.fetchall()
    #timetable for next week
    connection.execute(queries.trainer_time_table_between_twodate(),(nextweek[0],nextweek[6]+datetime.timedelta(days=1),int(user[0])))
    classes_nw=connection.fetchall()
    #timetable for following week
    connection.execute(queries.trainer_time_table_between_twodate(),(nextnextweek[0],nextnextweek[6]+datetime.timedelta(days=1),int(user[0])))
    classes_nnw=connection.fetchall()
    connection.close()
    #time array as reference for drawing the grid, to hide the hours that have no data at all
    timelist_cw = [(row[14]).seconds/3600 for row in classes_cw]
    timelist_nw = [(row[14]).seconds/3600 for row in classes_nw]
    timelist_nnw = [(row[14]).seconds/3600 for row in classes_nnw]
    return render_template("classlist.html", trainer=user, user=user, classes=classes_cw, timelist_cw=timelist_cw, classes_nw=classes_nw, timelist_nw=timelist_nw, classes_nnw=classes_nnw, timelist_nnw=timelist_nnw, currentweek=currentweek, nextweek=nextweek, nextnextweek=nextnextweek)

#Member requests to view a specific trainer's timetable
@app.route("/member/timetable/trainer", methods=["POST", "GET"])
def memberclicksearch_TrainerClass():
    #message for member search on timetable
    message = ""
    #message for booking or cancelling feedback
    bookingmessage = ""
    if request.form.get('trainersearch') != None:
        trainersearch = request.form.get('trainersearch').split(",")
        tid=trainersearch[0]
        #print(trainersearch)
        message = "Viewing Trainer " + trainersearch[1] +" " +trainersearch[2] +"'s Class and Session"
        #Check member booked scheudle
        connection=getCursor()
        connection.execute(queries.memberbookedschedule(),(int(user[0]),))
        bookedschedule=connection.fetchall()
        #Get list of all trainers
        connection.execute(queries.trainer_list())
        trainer_list=connection.fetchall()
        #timetable for current week
        connection.execute(queries.trainer_time_table_between_twodate(),(currentweek[0],currentweek[6]+datetime.timedelta(days=1),tid))
        classes_cw=connection.fetchall()
        #timetable for next week
        connection.execute(queries.trainer_time_table_between_twodate(),(nextweek[0],nextweek[6]+datetime.timedelta(days=1),tid))
        classes_nw=connection.fetchall()
        #timetable for following week
        connection.execute(queries.trainer_time_table_between_twodate(),(nextnextweek[0],nextnextweek[6]+datetime.timedelta(days=1),tid))
        classes_nnw=connection.fetchall()
        connection.close()
        #time array as reference for drawing the grid, to hide the hours that have no data at all
        timelist_cw = [(row[14]).seconds/3600 for row in classes_cw]
        timelist_nw = [(row[14]).seconds/3600 for row in classes_nw]
        timelist_nnw = [(row[14]).seconds/3600 for row in classes_nnw]
    else:
        connection=getCursor()
        connection.execute(queries.memberbookedschedule(),(int(user[0]),))
        bookedschedule=connection.fetchall()
        #Get list of all trainers
        connection.execute(queries.trainer_list())
        trainer_list=connection.fetchall()
        
        if request.args.get('action')=='1':
            uid = request.args.get('uid')
            sid = request.args.get('sid')
            SID = (int(sid),)
            print(SID)
            if str(uid) == str(user[0]): #If TRUE, book the schedule
                if SID not in bookedschedule:
                    connection=getCursor()
                    connection.execute(queries.bookscehduleforuser(),(int(sid),int(uid)))
                    print("Book Schedule " + str(sid) + " For User " + str(user[0]))
                    bookingmessage = "Successfully booked."
                if request.args.get('pay')=='1':
                    bookingid=connection.lastrowid
                    connection=getCursor()
                    connection.execute(queries.pay_session(),(int(uid), 60, bookingid, today_string, now_string))
                    bookingmessage = bookingmessage + " Paid."
        elif request.args.get('action')=='0':
            uid = request.args.get('uid')
            sid = request.args.get('sid')
            if str(uid) == str(user[0]): #If TRUE, cancell the schedule
                    if request.args.get('refund')=='1':
                        connection=getCursor()
                        connection.execute(queries.check_baid(),(int(sid),int(uid)))
                        baid=connection.fetchone()
                        print(baid[0])
                    connection=getCursor()
                    connection.execute(queries.membercancellschedule(),(int(sid),int(uid)))
                    bookingmessage = "Booking cancelled."
                    print("Schedule" + str(sid) + " Cancelled For User " + str(user[0]))
                    if request.args.get('refund')=='1':
                        connection=getCursor()
                        connection.execute(queries.refund_session(),(int(uid), -60, baid[0], today_string, now_string))
                        bookingmessage = bookingmessage + " Refund processed."
        connection=getCursor()
        #timetable for current week
        connection.execute(queries.full_time_table_between_twodate(),(currentweek[0],currentweek[6]+datetime.timedelta(days=1)))
        classes_cw=connection.fetchall()
        #timetable for next week
        connection.execute(queries.full_time_table_between_twodate(),(nextweek[0],nextweek[6]+datetime.timedelta(days=1)))
        classes_nw=connection.fetchall()
        #timetable for following week
        connection.execute(queries.full_time_table_between_twodate(),(nextnextweek[0],nextnextweek[6]+datetime.timedelta(days=1)))
        classes_nnw=connection.fetchall()
        connection=getCursor()
        connection.execute(queries.memberbookedschedule(),(int(user[0]),))
        bookedschedule=connection.fetchall()
        connection.close()
        #time array as reference for drawing the grid, to hide the hours that have no data at all
        timelist_cw = [(row[14]).seconds/3600 for row in classes_cw]
        timelist_nw = [(row[14]).seconds/3600 for row in classes_nw]
        timelist_nnw = [(row[14]).seconds/3600 for row in classes_nnw]
    return render_template("classlist.html", member=user, user=user, trainer_list=trainer_list, message=message, bookingmessage=bookingmessage, classes=classes_cw, timelist_cw=timelist_cw, classes_nw=classes_nw, timelist_nw=timelist_nw, classes_nnw=classes_nnw, timelist_nnw=timelist_nnw, bookedschedule=bookedschedule, currentweek=currentweek, nextweek=nextweek, nextnextweek=nextnextweek)

@app.route("/trainer/mytimetable/view", methods=["POST"])
def trainerclickview_ClassOrSession():

    viewoption = request.form.get('viewoption')
    if viewoption=="class":
        message = "Viewing Class Only"
        connection=getCursor()
        #timetable for current week
        connection.execute(queries.trainer_time_table_class_between_twodate(),(currentweek[0],currentweek[6]+datetime.timedelta(days=1),int(user[0])))
        classes_cw=connection.fetchall()
        #timetable for next week
        connection.execute(queries.trainer_time_table_class_between_twodate(),(nextweek[0],nextweek[6]+datetime.timedelta(days=1),int(user[0])))
        classes_nw=connection.fetchall()
        #timetable for following week
        connection.execute(queries.trainer_time_table_class_between_twodate(),(nextnextweek[0],nextnextweek[6]+datetime.timedelta(days=1),int(user[0])))
        classes_nnw=connection.fetchall()
        connection.close()
    if viewoption=="session":
        message = "Viewing Session Only"
        connection=getCursor()
        #timetable for current week
        connection.execute(queries.trainer_time_table_session_between_twodate(),(currentweek[0],currentweek[6]+datetime.timedelta(days=1),int(user[0])))
        classes_cw=connection.fetchall()
        #timetable for next week
        connection.execute(queries.trainer_time_table_session_between_twodate(),(nextweek[0],nextweek[6]+datetime.timedelta(days=1),int(user[0])))
        classes_nw=connection.fetchall()
        #timetable for following week
        connection.execute(queries.trainer_time_table_session_between_twodate(),(nextnextweek[0],nextnextweek[6]+datetime.timedelta(days=1),int(user[0])))
        classes_nnw=connection.fetchall()
        connection.close()
    elif viewoption=="all":
        message = "Viewing Session and Class"
        connection=getCursor()
        #timetable for current week
        connection.execute(queries.trainer_time_table_between_twodate(),(currentweek[0],currentweek[6]+datetime.timedelta(days=1),int(user[0])))
        classes_cw=connection.fetchall()
        #timetable for next week
        connection.execute(queries.trainer_time_table_between_twodate(),(nextweek[0],nextweek[6]+datetime.timedelta(days=1),int(user[0])))
        classes_nw=connection.fetchall()
        #timetable for following week
        connection.execute(queries.trainer_time_table_between_twodate(),(nextnextweek[0],nextnextweek[6]+datetime.timedelta(days=1),int(user[0])))
        classes_nnw=connection.fetchall()
        connection.close()
    #time array as reference for drawing the grid, to hide the hours that have no data at all
    timelist_cw = [(row[14]).seconds/3600 for row in classes_cw]
    timelist_nw = [(row[14]).seconds/3600 for row in classes_nw]
    timelist_nnw = [(row[14]).seconds/3600 for row in classes_nnw]
    return render_template("classlist.html", message=message, trainer=user, user=user, classes=classes_cw, timelist_cw=timelist_cw, classes_nw=classes_nw, timelist_nw=timelist_nw, classes_nnw=classes_nnw, timelist_nnw=timelist_nnw, currentweek=currentweek, nextweek=nextweek, nextnextweek=nextnextweek)


@app.route("/admin/timetable/trainer", methods=["POST"])
def adminclicksearch_TrainerClass():

    trainersearch = request.form.get('trainersearch').split(",")
    tid=trainersearch[0]
    print(trainersearch)
    message = "Viewing Trainer " + trainersearch[1] +" " +trainersearch[2] +"'s Class and Session"

    #Get list of all trainers
    connection=getCursor()
    connection.execute(queries.trainer_list())
    trainer_list=connection.fetchall()
    ##timetable for current week
    connection.execute(queries.trainer_time_table_between_twodate(),(currentweek[0],currentweek[6]+datetime.timedelta(days=1),tid))
    classes_cw=connection.fetchall()
    #timetable for next week
    connection.execute(queries.trainer_time_table_between_twodate(),(nextweek[0],nextweek[6]+datetime.timedelta(days=1),tid))
    classes_nw=connection.fetchall()
    #timetable for following week
    connection.execute(queries.trainer_time_table_between_twodate(),(nextnextweek[0],nextnextweek[6]+datetime.timedelta(days=1),tid))
    classes_nnw=connection.fetchall()
    connection.close()
    #time array as reference for drawing the grid, to hide the hours that have no data at all
    timelist_cw = [(row[14]).seconds/3600 for row in classes_cw]
    timelist_nw = [(row[14]).seconds/3600 for row in classes_nw]
    timelist_nnw = [(row[14]).seconds/3600 for row in classes_nnw]
    return render_template("classlist.html", admin=user, user=user, trainer_list=trainer_list, message=message, classes=classes_cw, timelist_cw=timelist_cw, classes_nw=classes_nw, timelist_nw=timelist_nw, classes_nnw=classes_nnw, timelist_nnw=timelist_nnw, currentweek=currentweek, nextweek=nextweek, nextnextweek=nextnextweek)

@app.route("/trainer/timetable/trainer", methods=["POST"])
def trainerclicksearch_TrainerClass():

    trainersearch = request.form.get('trainersearch').split(",")
    tid=trainersearch[0]
    print(trainersearch)
    message = "Viewing Trainer " + trainersearch[1] +" " +trainersearch[2] +"'s Class and Session"

    #Get list of all trainers
    connection=getCursor()
    connection.execute(queries.trainer_list())
    trainer_list=connection.fetchall()
    #timetable for current week
    connection.execute(queries.trainer_time_table_between_twodate(),(currentweek[0],currentweek[6]+datetime.timedelta(days=1),tid))
    classes_cw=connection.fetchall()
    #timetable for next week
    connection.execute(queries.trainer_time_table_between_twodate(),(nextweek[0],nextweek[6]+datetime.timedelta(days=1),tid))
    classes_nw=connection.fetchall()
    #timetable for following week
    connection.execute(queries.trainer_time_table_between_twodate(),(nextnextweek[0],nextnextweek[6]+datetime.timedelta(days=1),tid))
    classes_nnw=connection.fetchall()
    connection.close()
    #time array as reference for drawing the grid, to hide the hours that have no data at all
    timelist_cw = [(row[14]).seconds/3600 for row in classes_cw]
    timelist_nw = [(row[14]).seconds/3600 for row in classes_nw]
    timelist_nnw = [(row[14]).seconds/3600 for row in classes_nnw]
    return render_template("classlist.html", trainer=user, user=user, trainer_list=trainer_list, message=message, classes=classes_cw, timelist_cw=timelist_cw, classes_nw=classes_nw, timelist_nw=timelist_nw, classes_nnw=classes_nnw, timelist_nnw=timelist_nnw, currentweek=currentweek, nextweek=nextweek, nextnextweek=nextnextweek)


@app.route("/member/timetable",  methods=["GET"])
def clickclass_Member():
    bookingmessage = ""
    #Check member booked scheudle
    connection=getCursor()
    connection.execute(queries.memberbookedschedule(),(int(user[0]),))
    bookedschedule=connection.fetchall()
    #Get list of all trainers
    connection.execute(queries.trainer_list())
    trainer_list=connection.fetchall()
    #
    if request.args.get('action')=='1':
        uid = request.args.get('uid')
        sid = request.args.get('sid')
        SID = (int(sid),)
        print(SID)
        if str(uid) == str(user[0]): #If TRUE, book the schedule
            if SID not in bookedschedule:
                connection=getCursor()
                connection.execute(queries.bookscehduleforuser(),(int(sid),int(uid)))
                print("Book Schedule " + str(sid) + " For User " + str(user[0]))
                bookingmessage = "Successfully booked."
        if request.args.get('pay')=='1':
            bookingid=connection.lastrowid
            connection=getCursor()
            connection.execute(queries.pay_session(),(int(uid), 60, bookingid, today_string, now_string))
            bookingmessage = bookingmessage + " Paid."
    elif request.args.get('action')=='0':
        uid = request.args.get('uid')
        sid = request.args.get('sid')
        if str(uid) == str(user[0]): #If TRUE, cancell the schedule
                if request.args.get('refund')=='1':
                    connection=getCursor()
                    connection.execute(queries.check_baid(),(int(sid),int(uid)))
                    baid=connection.fetchone()
                    print(baid[0])
                connection=getCursor()
                connection.execute(queries.membercancellschedule(),(int(sid),int(uid)))
                bookingmessage = "Booking cancelled."
                print("Schedule" + str(sid) + " Cancelled For User " + str(user[0]))
                if request.args.get('refund')=='1':
                    connection=getCursor()
                    connection.execute(queries.refund_session(),(int(uid), -60, baid[0], today_string, now_string))
                    bookingmessage = bookingmessage + " Refund processed."

   # elif (request.args.get('action')=='0' and request.args.get('refund')=='1'):
    connection=getCursor()
    #timetable for current week
    connection.execute(queries.full_time_table_between_twodate(),(currentweek[0],currentweek[6]+datetime.timedelta(days=1)))
    classes_cw=connection.fetchall()
    #timetable for next week
    connection.execute(queries.full_time_table_between_twodate(),(nextweek[0],nextweek[6]+datetime.timedelta(days=1)))
    classes_nw=connection.fetchall()
    #timetable for following week
    connection.execute(queries.full_time_table_between_twodate(),(nextnextweek[0],nextnextweek[6]+datetime.timedelta(days=1)))
    classes_nnw=connection.fetchall()
    connection=getCursor()
    connection.execute(queries.memberbookedschedule(),(int(user[0]),))
    bookedschedule=connection.fetchall()
    connection.close()
    #time array as reference for drawing the grid, to hide the hours that have no data at all
    timelist_cw = [(row[14]).seconds/3600 for row in classes_cw]
    timelist_nw = [(row[14]).seconds/3600 for row in classes_nw]
    timelist_nnw = [(row[14]).seconds/3600 for row in classes_nnw]
    return render_template("classlist.html", member=user, user=user, bookingmessage=bookingmessage, trainer_list=trainer_list, classes=classes_cw, timelist_cw=timelist_cw, classes_nw=classes_nw, timelist_nw=timelist_nw, classes_nnw=classes_nnw, timelist_nnw=timelist_nnw, bookedschedule=bookedschedule, currentweek=currentweek, nextweek=nextweek, nextnextweek=nextnextweek)

@app.route("/member/mytimetable/",  methods=["GET"])
def clickmyclass_Member():

    bookingmessage = ""

     #Check member booked scheudle
    connection=getCursor()
    connection.execute(queries.memberbookedschedule(),(int(user[0]),))
    bookedschedule=connection.fetchall()
    #Get list of all trainers
    connection.execute(queries.trainer_list())
    trainer_list=connection.fetchall()
    #
    if request.args.get('action')=='1':
        uid = request.args.get('uid')
        sid = request.args.get('sid')
        SID = (int(sid),)
        print(SID)
        if str(uid) == str(user[0]): #If TRUE, book the schedule
            if SID not in bookedschedule:
                connection=getCursor()
                connection.execute(queries.bookscehduleforuser(),(int(sid),int(uid)))
                print("Book Schedule " + str(sid) + " For User " + str(user[0]))
                bookingmessage = "Successfully booked."
        if request.args.get('pay')=='1':
            bookingid=connection.lastrowid
            connection=getCursor()
            connection.execute(queries.pay_session(),(int(uid), 60, bookingid, today_string, now_string))
            bookingmessage = bookingmessage + " Paid."
    elif request.args.get('action')=='0':
        uid = request.args.get('uid')
        sid = request.args.get('sid')
        if str(uid) == str(user[0]): #If TRUE, cancell the schedule
                if request.args.get('refund')=='1':
                    connection=getCursor()
                    connection.execute(queries.check_baid(),(int(sid),int(uid)))
                    baid=connection.fetchone()
                    print(baid[0])
                connection=getCursor()
                connection.execute(queries.membercancellschedule(),(int(sid),int(uid)))
                bookingmessage = "Booking cancelled."
                print("Schedule" + str(sid) + " Cancelled For User " + str(user[0]))
                if request.args.get('refund')=='1':
                    connection=getCursor()
                    connection.execute(queries.refund_session(),(int(uid), -60, baid[0], today_string, now_string))
                    bookingmessage = bookingmessage + " Refund processed."

   # elif (request.args.get('action')=='0' and request.args.get('refund')=='1'):
    connection=getCursor()
    #timetable for current week
    connection.execute(queries.member_time_table_between_twodate(),(currentweek[0],currentweek[6]+datetime.timedelta(days=1),int(user[0])))
    classes_cw=connection.fetchall()
    #timetable for next week
    connection.execute(queries.member_time_table_between_twodate(),(nextweek[0],nextweek[6]+datetime.timedelta(days=1),int(user[0])))
    classes_nw=connection.fetchall()
    #timetable for following week
    connection.execute(queries.member_time_table_between_twodate(),(nextnextweek[0],nextnextweek[6]+datetime.timedelta(days=1),int(user[0])))
    classes_nnw=connection.fetchall()
    connection=getCursor()
    connection.execute(queries.memberbookedschedule(),(int(user[0]),))
    bookedschedule=connection.fetchall()
    connection.close()
    #time array as reference for drawing the grid, to hide the hours that have no data at all
    timelist_cw = [(row[14]).seconds/3600 for row in classes_cw]
    timelist_nw = [(row[14]).seconds/3600 for row in classes_nw]
    timelist_nnw = [(row[14]).seconds/3600 for row in classes_nnw]
    return render_template("classlist.html", member=user, user=user, bookingmessage=bookingmessage, trainer_list=trainer_list, classes=classes_cw, timelist_cw=timelist_cw, classes_nw=classes_nw, timelist_nw=timelist_nw, classes_nnw=classes_nnw, timelist_nnw=timelist_nnw, bookedschedule=bookedschedule, currentweek=currentweek, nextweek=nextweek, nextnextweek=nextnextweek)

@app.route("/member/mytimetable/view",  methods=["GET", "POST"])
def memberclickview_ClassOrSession():

    message = ""
    bookingmessage = ""

    connection=getCursor()
    connection.execute(queries.memberbookedschedule(),(int(user[0]),))
    bookedschedule=connection.fetchall()
    #timetable for current week
    connection.execute(queries.member_time_table_between_twodate(),(currentweek[0],currentweek[6]+datetime.timedelta(days=1),int(user[0])))
    classes_cw=connection.fetchall()
    #timetable for next week
    connection.execute(queries.member_time_table_between_twodate(),(nextweek[0],nextweek[6]+datetime.timedelta(days=1),int(user[0])))
    classes_nw=connection.fetchall()
    #timetable for following week
    connection.execute(queries.member_time_table_between_twodate(),(nextnextweek[0],nextnextweek[6]+datetime.timedelta(days=1),int(user[0])))
    classes_nnw=connection.fetchall()

    if request.args.get('action')=='1':
        uid = request.args.get('uid')
        sid = request.args.get('sid')
        SID = (int(sid),)
        print(SID)
        if str(uid) == str(user[0]): #If TRUE, book the schedule
            if SID not in bookedschedule:
                connection=getCursor()
                connection.execute(queries.bookscehduleforuser(),(int(sid),int(uid)))
                print("Book Schedule " + str(sid) + " For User " + str(user[0]))
                bookingmessage = "Successfully booked."
        if request.args.get('pay')=='1':
            bookingid=connection.lastrowid
            connection=getCursor()
            connection.execute(queries.pay_session(),(int(uid), 60, bookingid, today_string, now_string))
            bookingmessage = bookingmessage + " Paid."
    elif request.args.get('action')=='0':
        uid = request.args.get('uid')
        sid = request.args.get('sid')
        if str(uid) == str(user[0]): #If TRUE, cancell the schedule
                if request.args.get('refund')=='1':
                    connection=getCursor()
                    connection.execute(queries.check_baid(),(int(sid),int(uid)))
                    baid=connection.fetchone()
                    print(baid[0])
                connection=getCursor()
                connection.execute(queries.membercancellschedule(),(int(sid),int(uid)))
                bookingmessage = "Booking cancelled."
                print("Schedule" + str(sid) + " Cancelled For User " + str(user[0]))
                if request.args.get('refund')=='1':
                    connection=getCursor()
                    connection.execute(queries.refund_session(),(int(uid), -60, baid[0], today_string, now_string))
                    bookingmessage = bookingmessage + " Refund processed."
    viewoption = request.form.get('viewoption')
    if viewoption=="class":
        message = "Viewing Class Only"
        connection=getCursor()
        #timetable for current week
        connection.execute(queries.member_time_table_class_between_twodate(),(currentweek[0],currentweek[6]+datetime.timedelta(days=1),int(user[0])))
        classes_cw=connection.fetchall()
        #timetable for next week
        connection.execute(queries.member_time_table_class_between_twodate(),(nextweek[0],nextweek[6]+datetime.timedelta(days=1),int(user[0])))
        classes_nw=connection.fetchall()
        #timetable for following week
        connection.execute(queries.member_time_table_class_between_twodate(),(nextnextweek[0],nextnextweek[6]+datetime.timedelta(days=1),int(user[0])))
        classes_nnw=connection.fetchall()
    if viewoption=="session":
        message = "Viewing Session Only"
        connection=getCursor()
        #timetable for current week
        connection.execute(queries.member_time_table_session_between_twodate(),(currentweek[0],currentweek[6]+datetime.timedelta(days=1),int(user[0])))
        classes_cw=connection.fetchall()
        #timetable for next week
        connection.execute(queries.member_time_table_session_between_twodate(),(nextweek[0],nextweek[6]+datetime.timedelta(days=1),int(user[0])))
        classes_nw=connection.fetchall()
        #timetable for following week
        connection.execute(queries.member_time_table_session_between_twodate(),(nextnextweek[0],nextnextweek[6]+datetime.timedelta(days=1),int(user[0])))
        classes_nnw=connection.fetchall()
    elif viewoption=="all":
        message = "Viewing Session and Class"
        connection=getCursor()
        #timetable for current week
        connection.execute(queries.member_time_table_between_twodate(),(currentweek[0],currentweek[6]+datetime.timedelta(days=1),int(user[0])))
        classes_cw=connection.fetchall()
        #timetable for next week
        connection.execute(queries.member_time_table_between_twodate(),(nextweek[0],nextweek[6]+datetime.timedelta(days=1),int(user[0])))
        classes_nw=connection.fetchall()
        #timetable for following week
        connection.execute(queries.member_time_table_between_twodate(),(nextnextweek[0],nextnextweek[6]+datetime.timedelta(days=1),int(user[0])))
        classes_nnw=connection.fetchall()

    connection=getCursor()
    connection.execute(queries.memberbookedschedule(),(int(user[0]),))
    bookedschedule=connection.fetchall()
    connection.close()

    #time array as reference for drawing the grid, to hide the hours that have no data at all  
    timelist_cw = [(row[14]).seconds/3600 for row in classes_cw]
    timelist_nw = [(row[14]).seconds/3600 for row in classes_nw]
    timelist_nnw = [(row[14]).seconds/3600 for row in classes_nnw]
    return render_template("classlist.html", message=message, bookingmessage=bookingmessage, member=user, user=user, classes=classes_cw, timelist_cw=timelist_cw, classes_nw=classes_nw, timelist_nw=timelist_nw, classes_nnw=classes_nnw, timelist_nnw=timelist_nnw, bookedschedule=bookedschedule, currentweek=currentweek, nextweek=nextweek, nextnextweek=nextnextweek)


@app.route('/trainer/viewdetail/<int:class_id>', methods=['GET'])
def view_detail(class_id):
    class_id = request.args.get('class_id')
    connection = getCursor()
    connection.execute(queries.trainer_session_detail(), (class_id,))
    sessions = connection.fetchall()

    connection.close()
    return render_template("viewdetail.html", sessions=sessions, trainer=user, user=user, currentweek=currentweek, nextweek=nextweek, nextnextweek=nextnextweek)




#Belinda adding trainer view details (BLW)
# Route for admin to view the list of trainers
@app.route("/admin/trainerlist")
def clicktrainer_admin():
    # Get a database cursor
    connection=getCursor()
    # Execute the query to fetch the list of trainers
    connection.execute(queries.trainer_list())
    # Fetch all the trainers from the result
    trainers=connection.fetchall()
    # Close the database connection
    connection.close()
    # Render the trainer list template with the admin user and the list of trainers
    return render_template("trainerlist.html", admin=user, trainers=trainers)
# Route for member to view the list of trainers
@app.route("/member/trainerlist")
def clicktrainer_member():
    connection=getCursor()
    connection.execute(queries.trainer_list())
    trainers=connection.fetchall()
    connection.close()
    return render_template("trainerlist.html", member=user, trainers=trainers)

# Route to view trainer profile as member (BLW)
@app.route ("/member/trainer_profile", methods=["POST", "GET"])
def clicktrainerprofile_member():
    id = request.args.get('id')
    connection=getCursor()
    connection.execute(queries.trainer_profile(), (id,))
    trainerprofile=connection.fetchone()
    print (trainerprofile)
    connection.close()
    return render_template("trainerprofile.html", member=user, trainerprofile=trainerprofile)

# Route to view trainer profile as admin (BLW)
@app.route ("/admin/trainer_profile", methods=["POST", "GET"])
def clicktrainerprofile_admin():
    id = request.args.get('id')
    connection=getCursor()
    connection.execute(queries.trainer_profile(), (id,))
    trainerprofile=connection.fetchone()
    print (trainerprofile)
    connection.close()
    return render_template("trainerprofile.html", admin=user, trainerprofile=trainerprofile)

# Route to view own trainer profile as trainer (BLW)
@app.route ("/trainer/trainer_profile", methods=["POST", "GET"])
def clicktrainerprofile_trainer():
    id = request.args.get('id')
    connection=getCursor()
    connection.execute(queries.trainer_profile(), (id,))
    trainerprofile=connection.fetchone()
    print (trainerprofile)
    connection.close()
    return render_template("trainerprofile.html", trainer=user, trainerprofile=trainerprofile)

# edit trainer profile as trainer (BLW) 
@app.route ("/trainer/edit_trainerprofile", methods=["POST", "GET"])
def trainer_edit_trainerprofile():
    if request.method == 'POST':
        trainerid=request.form.get('id')
        first_name=request.form.get('first_name')
        last_name=request.form.get('last_name')
        qualification_ids=request.form.getlist('qualification_id')
        email=request.form.get('email')
        phone_number=request.form.get('phone_number')
        connection=getCursor()
        td_parameters = (first_name, last_name, email, phone_number, trainerid)
        connection.execute(queries.update_trainer_detail(), td_parameters)
        trainerprofile=connection.fetchall()
        connection.execute('DELETE FROM trainerqualification WHERE trainer_id = %s', (trainerid,))
        for qualification_id in qualification_ids:
            connection.execute('INSERT INTO trainerqualification (trainer_id, qualification_id) VALUES (%s, %s)', (trainerid, qualification_id))
        trainerqual=connection.fetchall()
        connection.execute(queries.trainer_profile(), (trainerid,))
        trainerprofile=connection.fetchone()
        print (trainerprofile)
        connection.close()
        return render_template("trainerprofile.html", trainer=user, trainerprofile=trainerprofile, trainerqual=trainerqual)       
    id = request.args.get('id')
    connection=getCursor()
    connection.execute(queries.trainer_profile(), (id,))
    trainerprofile=connection.fetchone()
    print (trainerprofile)
    connection.execute('''select * from qualification''')
    qualifications = connection.fetchall()

    # Get the selected qualifications for the trainer
    connection.execute('''select qualification_id 
                            from trainerqualification
                            join qualification on qualification.id=trainerqualification.qualification_id
                            where trainer_id = %s''', (id,))
    selected_qualifications = [row[0] for row in connection.fetchall()]
    connection.close()

    # Render the edited trainer profile template with the trainer profile, qualifications, and selected qualifications
    return render_template("trainer_edit_trainerprofile.html", trainerprofile=trainerprofile, qualifications=qualifications, selected_qualifications=selected_qualifications)

# book a trainer for a private session as a member (BLW)
@app.route ("/member/book_trainer")
def booktrainer_member():
    return render_template("classlist.html")
#add a new member
@app.route ("/admin/addMember", methods=["POST", "GET"])
def addMember():
    return render_template("addMember.html", admin=user, date=date, relativedelta=relativedelta)
#get user input and update database to add a new member
@app.route ("/admin/addMemberComplete", methods=["POST", "GET"])
def addMemberComplete():
    role=request.form.get('member')
    first_name=request.form.get('first_name')
    last_name=request.form.get('last_name')
    email=request.form.get('email')
    password=request.form.get('password')
    gender=request.form.get('gender')
    date_of_birth=request.form.get('date_of_birth')
    phone_number=request.form.get('phone_number')
    address=request.form.get('address')
    outcomes=request.form.get('outcomes')
    weight=request.form.get('weight')
    body_fat_percentage=request.form.get('bmi')
    blood_pressure=request.form.get('bp')
    general_comments=request.form.get('comments')
    connection=getCursor()
    connection.execute(queries.add_member(), (first_name, last_name, email, password, gender, date_of_birth, phone_number, address, outcomes ))
    connection.execute("SELECT * FROM member WHERE id = LAST_INSERT_ID()")
    newMember=connection.fetchone()
    id=newMember[0]
    connection.execute(queries.add_account(), (id, id, 0, datetime.date.today(), datetime.date.today(), datetime.date.today()+relativedelta(months=+12)  ))
    current_date = datetime.date.today()
    connection.execute("INSERT INTO memberhealth (member_id,  health_id, value, date) VALUES (%s,%s,%s,%s)", (id, 1,weight,  current_date))
    connection.execute("INSERT INTO memberhealth (member_id,  health_id, value, date) VALUES (%s,%s,%s,%s)", (id, 2, body_fat_percentage ,  current_date))
    connection.execute("INSERT INTO memberhealth (member_id,  health_id, value, date) VALUES (%s,%s,%s,%s)", (id, 3, blood_pressure ,  current_date))
    connection.execute("INSERT INTO memberhealth (member_id,  health_id, value, date) VALUES (%s,%s,%s,%s)", (id, 4, general_comments ,  current_date)) 
    connection.execute(queries.newmemberpay(), (id, 200, 3, "monthlypaymentdirectdebit",datetime.date.today(),))
    connection.close()
    return render_template("newMemberConfirm.html", admin=user, newMember=newMember, date=date, relativedelta=relativedelta, current_date=current_date)
    
       
#admin to activate and deactivate members
@app.route ("/admin/changestatus", methods=["POST", "GET"])
def changestatus():
    isactive=request.form.get('isactive')
    id=request.form.get('id')
    connection=getCursor()
    connection.execute("UPDATE member SET isactive= %s WHERE id=%s;", (isactive, id))
    connection.close()
    return redirect(url_for('clickmember_admin'))

#get user input and update member profile for admin.
@app.route ("/admin/edit_memberprofile", methods=["POST", "GET"])
def admin_edit_memberprofile():
    if request.method == "POST":
        memberid=request.form.get('id')
        first_name=request.form.get('first_name')
        last_name=request.form.get('last_name')
        email=request.form.get('email')
        password=request.form.get('password')
        gender=request.form.get('gender')
        date_of_birth=request.form.get('date_of_birth')
        phone_number=request.form.get('phone_number')
        address=request.form.get('address')
        weight=request.form.get('weight')
        body_fat_percentage=request.form.get('bmi')
        blood_pressure=request.form.get('bp')
        general_comments=request.form.get('comments')
        connection=getCursor()        
        sql="UPDATE member SET first_name= %s, last_name=%s, email=%s, password=%s, gender=%s, date_of_birth=%s, phone_number=%s, address=%s WHERE id=%s;"
        parameters = (first_name, last_name, email, password, gender, date_of_birth, phone_number, address, memberid)
        connection.execute(sql, parameters)
        connection.execute("UPDATE memberhealth SET value=%s where health_id=%s and member_id=%s", (weight, 1, memberid))
        connection.execute("UPDATE memberhealth SET value=%s where health_id=%s and member_id=%s", (body_fat_percentage, 2, memberid))
        connection.execute("UPDATE memberhealth SET value=%s where health_id=%s and member_id=%s", (blood_pressure, 3, memberid))
        connection.execute("UPDATE memberhealth SET value=%s where health_id=%s and member_id=%s", (general_comments, 4, memberid)) 
        # Display member profile after update.
        id = memberid
        connection.execute(queries.member_profile(), (id,))
        memberprofile=connection.fetchall()
        connection.execute(queries.member_subscription(), (id,))
        subscription_detail=connection.fetchall()
        member=[mb for mb in memberprofile]
        date_str=str(member[0][7])
        formatted_date = format_date(date_str)
        sub=[sub for sub in subscription_detail]
        date_time_str=str(sub[0][1])
        formatted_date_time = format_date(date_time_str)
        connection.close()
        return render_template("memberprofile.html", admin=user, date=formatted_date, date_time=formatted_date_time, memberprofile=memberprofile, subscriptionDetail=subscription_detail)
    # Display member profile before update.
    id = request.args.get('id')
    connection = getCursor()
    connection.execute(queries.member_profile(), (id,))
    memberprofile=connection.fetchall()
    connection.execute(queries.member_subscription(), (id,))
    subscription_detail=connection.fetchall()
    member=[mb for mb in memberprofile]
    date_str=str(member[0][7])
    formatted_date = format_date(date_str)
    sub=[sub for sub in subscription_detail]
    date_time_str=str(sub[0][1])
    formatted_date_time = format_date(date_time_str)
    connection.close()
    return render_template("edit_memberprofile.html", admin=user, date_time=formatted_date_time, date=formatted_date, memberprofile=memberprofile, Date=date, relativedelta=relativedelta)


#get user input and update member profile for member.
@app.route ("/member/edit_memberprofile", methods=["POST", "GET"])
def member_edit_memberprofile():
    if request.method == "POST":
        memberid=request.form.get('id')
        first_name=request.form.get('first_name')
        last_name=request.form.get('last_name')
        email=request.form.get('email')
        password=request.form.get('password')
        gender=request.form.get('gender')
        date_of_birth=request.form.get('date_of_birth')
        phone_number=request.form.get('phone_number')
        address=request.form.get('address')
        weight=request.form.get('weight')
        body_fat_percentage=request.form.get('bmi')
        blood_pressure=request.form.get('bp')
        general_comments=request.form.get('comments')
        connection=getCursor()        
        sql="UPDATE member SET first_name= %s, last_name=%s, email=%s, password=%s, gender=%s, date_of_birth=%s, phone_number=%s, address=%s WHERE id=%s;"
        parameters = (first_name, last_name, email, password, gender, date_of_birth, phone_number, address, memberid)
        connection.execute(sql, parameters)
        connection.execute("UPDATE memberhealth SET value=%s where health_id=%s and member_id=%s", (weight, 1, memberid))
        connection.execute("UPDATE memberhealth SET value=%s where health_id=%s and member_id=%s", (body_fat_percentage, 2, memberid))
        connection.execute("UPDATE memberhealth SET value=%s where health_id=%s and member_id=%s", (blood_pressure, 3, memberid))
        connection.execute("UPDATE memberhealth SET value=%s where health_id=%s and member_id=%s", (general_comments, 4, memberid)) 
        # Display member profile after update.
        id = memberid
        connection.execute(queries.member_profile(), (id,))
        memberprofile=connection.fetchall()
        connection.execute(queries.member_subscription(), (id,))
        subscription_detail=connection.fetchall()
        member=[mb for mb in memberprofile]
        date_str=str(member[0][7])
        formatted_date = format_date(date_str)
        sub=[sub for sub in subscription_detail]
        date_time_str=str(sub[0][1])
        formatted_date_time = format_date(date_time_str)
        connection.close()
        return render_template("memberprofile.html", member=user, date_time=formatted_date_time, date=formatted_date, memberprofile=memberprofile, subscriptionDetail=subscription_detail)
    # Display member profile before update.
    id = request.args.get('id')
    connection = getCursor()
    connection.execute(queries.member_profile(), (id,))
    memberprofile=connection.fetchall()
    connection.execute(queries.member_subscription(), (id,))
    subscription_detail=connection.fetchall()
    member=[mb for mb in memberprofile]
    date_str=str(member[0][7])
    formatted_date = format_date(date_str)
    sub=[sub for sub in subscription_detail]
    date_time_str=str(sub[0][1])
    formatted_date_time = format_date(date_time_str)
    connection.close()
    return render_template("edit_memberprofile.html", date=formatted_date, date_time=formatted_date_time, member=user, memberprofile=memberprofile, Date=date, relativedelta=relativedelta)

# Belinda added reports page for financial, newsletter, class popularity, member attendance, and payments reports
@app.route("/admin/reports")
def reports():
    return render_template("reports.html", admin=user)
# Route to display the most popular classes report page
@app.route("/admin/reports/classreport")
def classreport():
    connection=getCursor()
    connection.execute(queries.classreport())
    classreport=connection.fetchall()
    print (classreport)
    connection.close()
    return render_template("classreport.html", admin=user, classreport=classreport)


# Hido added financial reporting
@app.route("/admin/reports/financial", methods=["GET", "POST"])
def clickfinancialreport_Admin():

    year = request.args.get('fyear')
    print(year)

    connection = getCursor()

    connection.execute(queries.financialreport_session_byyearquarter(),(year,year))
    report_sessiondollar_quarter=connection.fetchall()
    connection.execute(queries.financialreport_session_byyearmonth(),(year,))
    report_sessiondollar_month=connection.fetchall()

    connection.execute(queries.financialreport_subscription_byyearquarter(),(year,year))
    report_subscriptiondollar_quarter=connection.fetchall()
    connection.execute(queries.financialreport_subscription_byyearmonth(),(year,))
    report_subscriptiondollar_month=connection.fetchall()

    connection.execute(queries.financialreport_activesubscriptioncount_byquarter(),(year,year))
    report_subscriptioncount_quarter=connection.fetchall()
    connection.execute(queries.financialreport_activesubscriptioncount_byquarter_currentyear(),(YTD_months,year,year))
    report_subscriptioncount_quarter_currentyear=connection.fetchall()
    connection.execute(queries.financialreport_activesubscriptioncount_bymonth(),(year,))
    report_subscriptioncount_month=connection.fetchall()

    connection.execute(queries.financialreport_expirecontract_byquarter(),(year,year))
    report_expirecontract_quarter=connection.fetchall()
    connection.execute(queries.financialreport_expirecontract_bymonth(),(year,))
    report_expirecontract_month=connection.fetchall()

    connection.execute(queries.financialreport_newcontract_byquarter(),(year,year))
    report_newcontract_quarter=connection.fetchall()
    connection.execute(queries.financialreport_newcontract_bymonth(),(year,))
    report_newcontract_month=connection.fetchall()

    connection.execute(queries.financialreport_refund_byyearquarter(),(year,year))
    report_refund_quarter=connection.fetchall()
    connection.execute(queries.financialreport_refund_bymonth(),(year,))
    report_refund_month=connection.fetchall()

    connection.execute(queries.financialreport_total_byyearquarter(),(year,year))
    report_total_quarter=connection.fetchall()
    connection.execute(queries.financialreport_total_bymonth(),(year,))
    report_total_month=connection.fetchall()

    connection.close()
    return render_template("financialreport.html", currentyear=str(currentyear), year=str(year), admin=user, report_sessiondollar_quarter=report_sessiondollar_quarter, report_sessiondollar_month=report_sessiondollar_month, report_subscriptiondollar_quarter=report_subscriptiondollar_quarter, report_subscriptiondollar_month=report_subscriptiondollar_month, report_subscriptioncount_quarter=report_subscriptioncount_quarter, report_subscriptioncount_quarter_currentyear=report_subscriptioncount_quarter_currentyear, report_subscriptioncount_month=report_subscriptioncount_month, report_expirecontract_quarter=report_expirecontract_quarter, report_expirecontract_month=report_expirecontract_month, report_newcontract_quarter=report_newcontract_quarter, report_newcontract_month=report_newcontract_month, report_refund_quarter=report_refund_quarter, report_total_quarter=report_total_quarter, report_refund_month=report_refund_month, report_total_month=report_total_month)

# admin to view payment reports
@app.route("/admin/reports/payments", methods=["GET", "POST"])
def paymentsreport():
    connection = getCursor()
    connection.execute(queries.allPaymentReport(), (4,))
    allPaymentReport=connection.fetchall() 
    # timeperiod filter (two weeks, a month or two months)
    timePeriod=request.args.get('timePeriod')
    all=request.args.get('all') 
    monthlyPayment=request.args.get('monthlyPayment')
    sessionPayment=request.args.get('sessionPayment')
    refundSession=request.args.get('refundSession')
    # view all payment for the chosen time period
    if all:
        connection = getCursor()
        connection.execute(queries.allPaymentReport(), (timePeriod,))
        allPaymentReport=connection.fetchall()
        return render_template("payments.html", admin=user, allPaymentReport=allPaymentReport )
    # view subscription payment for the chosen time period
    elif monthlyPayment:
        connection = getCursor()
        connection.execute(queries.monthlyPaymentReport(), (timePeriod,))
        monthlyPayment=connection.fetchall()
        return render_template("payments.html", admin=user, monthlyPayment=monthlyPayment )
    # view session payment for the chosen time period
    elif sessionPayment:
        connection = getCursor()
        connection.execute(queries.sessionPaymentReport(), (timePeriod, ))
        sessionPayment=connection.fetchall()
        return render_template("payments.html", admin=user, sessionPayment=sessionPayment)
    # view refund for the chosen time period
    elif refundSession:
        connection = getCursor()
        connection.execute(queries.refundSessionReport(), (timePeriod,))
        refundSession=connection.fetchall()
        return render_template("payments.html", admin=user, refundSession=refundSession)   
    return render_template("payments.html", admin=user, allPaymentReport=allPaymentReport)

#attendance payment for each member, users are able to search by id or name
@app.route("/admin/reports/attendance", methods=["GET", "POST"])
def attendancereport():
    searchId = request.form.get('memberid')
    Name = request.form.get('name')
    connection=getCursor()
    connection.execute(queries.allAttendance())
    allAttendance=connection.fetchall()
         
    # view member attendance by ID
    if searchId:
        connection=getCursor()
        connection.execute(queries.attendanceById(), (searchId,))
        attendanceById=connection.fetchall()
        connection.execute(queries.attendanceByIdClassSummary(), (searchId,))
        attendanceByIdClassSummary=connection.fetchone()
        connection.execute(queries.attendanceByIdSessionSummary(), (searchId,))
        attendanceByIdSessionSummary=connection.fetchone()
        connection.execute(queries.attendanceByIdGymSummary(), (searchId,))
        attendanceByIdGymSummary=connection.fetchone()
        return render_template("attendance.html", admin=user, attendanceById=attendanceById, attendanceByIdGymSummary=attendanceByIdGymSummary, attendanceByIdSessionSummary=attendanceByIdSessionSummary, attendanceByIdClassSummary=attendanceByIdClassSummary)
    # view member attendance by name
    if Name:
        searchName = "%" + Name + "%"
        connection=getCursor()
        connection.execute(queries.attendanceByName(), (searchName, searchName,))
        attendanceByName=connection.fetchall()
        connection.execute(queries.attendanceByNameClassSummary(), (searchName, searchName,))
        attendanceByNameClassSummary=connection.fetchone()
        connection.execute(queries.attendanceByNameSessionSummary(), (searchName, searchName,))
        attendanceByNameSessionSummary=connection.fetchone()
        connection.execute(queries.attendanceByNameGymSummary(), (searchName, searchName,))
        attendanceByNameGymSummary=connection.fetchone()

        return render_template("attendance.html", admin=user, attendanceByName=attendanceByName,attendanceByNameGymSummary=attendanceByNameGymSummary, attendanceByNameSessionSummary=attendanceByNameSessionSummary, attendanceByNameClassSummary=attendanceByNameClassSummary)
     # display default attendance report     
    return render_template("attendance.html", admin=user, allAttendance=allAttendance) 

# Display latest news for member
@app.route ("/member/news")
def clickmember_news():
    connection = getCursor()
    connection.execute(queries.member_news())
    membernews=connection.fetchone()
    connection.close()
    return render_template("member_news.html", member=user, membernews=membernews)   


# get the user input and update newsletter report for admin.
@app.route("/admin/reports/newsletter", methods=["GET", "POST"])
def newsletterreport():
    if request.method == "POST":
        title=request.form.get('title')
        content=request.form.get('content')
        connection = getCursor()
        connection.execute("UPDATE newsletters SET status=0")
        connection.execute(queries.add_news(), (title, content, today, 1))
        connection.execute(queries.admin_news())
        newsletter=connection.fetchall()
        connection.close()
        return render_template("newsletter.html", admin=user, newsletter=newsletter, addcomplete="Newsletter added, please check on newsletter reports")
    # Display newsletter report for admin
    connection = getCursor()
    connection.execute(queries.admin_news())
    newsletter=connection.fetchall()
    connection.close()
    return render_template("newsletter.html", admin=user, newsletter=newsletter)




# Code to enable debug mode
if __name__ == '__main__':
    app.run(debug=True)