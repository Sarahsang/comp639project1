
# Queries for Sprint1

#User Story Index 1 
#As a Admin, I want to View group classes (Same for all users), so that Understand upcoming classes assigned to all trainers	
#Creteria 1. Push a button, then it displays all the upcoming group classes 2. Display what classes are scheduled for this week and click a button to display what's for the following week  




#Test user search. Example
def user_search():
    query = (
        f"SELECT *"
        f"FROM user"
    )
    return query

def user_search_id():
    query = (
        f"SELECT * from user where id= 1"
    )
    #
    
def trainers():
    query = (
        f"SELECT u.first_name, u.last_name, uq.qualification_id, q.name, q.description FROM user u JOIN userrole ur ON u.id=ur.user_id left join userqualification uq on u.id = uq.user_id left join qualification q on uq.qualification_id = q.id WHERE ur.role_id = 2;"
    )
    return query

    #etCursor()
    #xecute(queries.user_search())
    #tion.fetchall()
    #
    #xecute(queries.user_search_id(),(uid,))
    # connection.fetchall()
    #lose()
    #r_template('member.html', All=all, Uid_Search=uid_search)

def group_class_schedule():
    query = (
        ''' SELECT s.id, s.class_id, s.trainer_id, s.day, s.start_time, s.end_time, s.room, c.name, c.description, c.capacity, u.first_name, u.last_name, 
            COUNT(ba.id) AS Booked, CONCAT(COUNT(ba.id),"/",c.capacity) AS BOOKED_CAPACITY, cast(start_time as time) AS time
            FROM schedule AS s
            LEFT JOIN class AS c ON s.class_id=c.id
            LEFT JOIN user AS u ON s.trainer_id=u.id
            LEFT JOIN validbookingattendance AS ba ON s.id=ba.schedule_id
            WHERE c.capacity>1
            GROUP BY s.id
            ORDER BY time,s.start_time
            ; '''
    )
    return query

def group_class_schedule_between_twodate():
    query = (
        ''' SELECT s.id, s.class_id, s.trainer_id, s.day, s.start_time, s.end_time, s.room, c.name, c.description, c.capacity, u.first_name, u.last_name, 
            COUNT(ba.id) AS Booked, CONCAT(COUNT(ba.id),"/",c.capacity) AS BOOKED_CAPACITY, cast(start_time as time) AS time
            FROM schedule AS s
            LEFT JOIN class AS c ON s.class_id=c.id
            LEFT JOIN user AS u ON s.trainer_id=u.id
            LEFT JOIN validbookingattendance AS ba ON s.id=ba.schedule_id
            WHERE c.capacity>1 AND s.start_time> %s AND s.start_time< %s
            GROUP BY s.id
            ORDER BY time, s.start_time
            ; '''
    )
    return query

def full_time_table_between_twodate():
    query = (
        ''' SELECT s.id, s.class_id, s.trainer_id, s.day, s.start_time, s.end_time, s.room, c.name, c.description, c.capacity, u.first_name, u.last_name, 
            COUNT(ba.id) AS Booked, CONCAT(COUNT(ba.id),"/",c.capacity) AS BOOKED_CAPACITY, cast(start_time as time) AS time
            FROM schedule AS s
            LEFT JOIN class AS c ON s.class_id=c.id
            LEFT JOIN user AS u ON s.trainer_id=u.id
            LEFT JOIN validbookingattendance AS ba ON s.id=ba.schedule_id
            WHERE c.capacity>=1 AND s.start_time> %s AND s.start_time< %s
            GROUP BY s.id
            ORDER BY time, s.start_time
            ; '''
    )
    return query

def member_time_table_between_twodate():
    query = (
        ''' SELECT s.id, s.class_id, s.trainer_id, s.day, s.start_time, s.end_time, s.room, c.name, c.description, c.capacity, u.first_name, u.last_name, 
            COUNT(ba.id) AS Booked, CONCAT(COUNT(ba.id),"/",c.capacity) AS BOOKED_CAPACITY, cast(start_time as time) AS time
            FROM schedule AS s
            LEFT JOIN class AS c ON s.class_id=c.id
            LEFT JOIN user AS u ON s.trainer_id=u.id
            LEFT JOIN validbookingattendance AS ba ON s.id=ba.schedule_id
            WHERE c.capacity>=1 AND s.start_time> %s AND s.start_time< %s AND ba.user_id = %s
            GROUP BY s.id
            ORDER BY time, s.start_time
            ; '''
    )
    return query

def trainer_time_table_between_twodate():
    query = (
        ''' SELECT s.id, s.class_id, s.trainer_id, s.day, s.start_time, s.end_time, s.room, c.name, c.description, c.capacity, u.first_name, u.last_name, 
            COUNT(ba.id) AS Booked, CONCAT(COUNT(ba.id),"/",c.capacity) AS BOOKED_CAPACITY, cast(start_time as time) AS time
            FROM schedule AS s
            LEFT JOIN class AS c ON s.class_id=c.id
            LEFT JOIN user AS u ON s.trainer_id=u.id
            LEFT JOIN validbookingattendance AS ba ON s.id=ba.schedule_id
            WHERE c.capacity>=1 AND s.start_time> %s AND s.start_time< %s AND s.trainer_id = %s
            GROUP BY s.id
            ORDER BY time, s.start_time
            ; '''
    )
    return query

def bookscehduleforuser():
    query = (
        '''INSERT INTO bookingattendance (schedule_id, user_id) VALUES (%s, %s);'''
    )
    return query

def memberbookedschedule():
    query = (
        '''Select ba.schedule_id FROM bookingattendance AS ba
        WHERE ba.cancelled =0 AND ba.user_id = %s
        ;'''
    )
    return query

def membercancellschedule():
    query = (
        '''UPDATE bookingattendance SET cancelled = 1 WHERE schedule_id=%s AND user_id=%s ;'''
    )
    return query

def trainer_list():
    query = (
        '''SELECT u.id, u.first_name, u.last_name, GROUP_CONCAT(q.name SEPARATOR ", ") as Qualification, GROUP_CONCAT(q.description SEPARATOR '\n') as Qualification_Detail, u.email, u.phone_number
        FROM user AS u 
        LEFT JOIN userrole AS ur ON u.id=ur.user_id 
        LEFT JOIN role AS r ON ur.role_id=r.id 
        LEFT JOIN userqualification AS uq ON u.id=uq.user_id 
        LEFT JOIN qualification AS q ON uq.qualification_id=q.id 
        WHERE r.id=2
        GROUP BY u.id
        ORDER by u.last_name ASC;'''
    )
    return query

def trainer_profile():
    query = (
        '''SELECT u.id, u.first_name, u.last_name, GROUP_CONCAT(q.name SEPARATOR ', ') as Qualification, GROUP_CONCAT(q.description SEPARATOR '; ') as Qualification_Detail, u.email, u.phone_number
        FROM user AS u 
        LEFT JOIN userrole AS ur ON u.id=ur.user_id 
        LEFT JOIN role AS r ON ur.role_id=r.id 
        LEFT JOIN userqualification AS uq ON u.id=uq.user_id 
        LEFT JOIN qualification AS q ON uq.qualification_id=q.id 
        WHERE r.id=2 
        AND u.id = %s
        ;'''
    )
    return query

def member_list():
    query = (
        """SELECT u.id, r.name, u.first_name, u.last_name, u.email, u.password, u.gender, u.date_of_birth, u.phone_number, u.address, u.isactive, 
            MAX(CASE WHEN h.id=1 THEN uh.value ELSE NULL END) AS weight, 
            MAX(CASE WHEN h.id=2 THEN uh.value ELSE NULL END) AS boty_fat_percentage, 
            MAX(CASE WHEN h.id=3 THEN uh.value ELSE NULL END) AS blood_pressure, 
            MAX(CASE WHEN h.id=4 THEN uh.value ELSE NULL END) AS general_comments  
            FROM user AS u 
            LEFT JOIN userrole AS ur ON u.id=ur.user_id 
            LEFT JOIN role AS r ON ur.role_id=r.id 
            LEFT JOIN userhealth AS uh ON u.id=uh.user_id 
            LEFT JOIN health AS h ON uh.health_id=h.id 
            WHERE r.id=3
            GROUP BY u.id;"""
    )
    return query

def member_profile():
    query = (
        """select  u.id, r.name, u.first_name, u.last_name, u.email, u.password, u.gender, u.date_of_birth, u.phone_number, u.address, u.isactive,
            MAX(CASE WHEN h.id=1 THEN uh.value ELSE NULL END) AS weight, 
            MAX(CASE WHEN h.id=2 THEN uh.value ELSE NULL END) AS boty_fat_percentage, 
            MAX(CASE WHEN h.id=3 THEN uh.value ELSE NULL END) AS blood_pressure, 
            MAX(CASE WHEN h.id=4 THEN uh.value ELSE NULL END) AS general_comments  
            FROM user AS u 
            LEFT JOIN userrole AS ur ON u.id=ur.user_id 
            LEFT JOIN role AS r ON ur.role_id=r.id 
            LEFT JOIN userhealth AS uh ON u.id=uh.user_id 
            LEFT JOIN health AS h ON uh.health_id=h.id 
            WHERE r.id=3 AND u.id=%s
            GROUP BY u.id;"""
    )
    return query

def member_subscription():
    query = (
        """SELECT u.id, u.first_name, u.last_name, a.balance, t.reference, DATE_ADD(a.last_subscription_payment, INTERVAL 30 DAY) AS duedate
            FROM user AS u 
            LEFT JOIN account AS a ON u.id=a.user_id
            LEFT JOIN transaction AS t ON a.id=t.account_id
            where u.id=%s;"""
    )
    return query

def search_member_id():
    query = (
        """SELECT u.id, r.name, u.first_name, u.last_name, u.email, u.password, u.gender, u.date_of_birth, u.phone_number, u.address, u.isactive, 
            MAX(CASE WHEN h.id=1 THEN uh.value ELSE NULL END) AS weight, 
            MAX(CASE WHEN h.id=2 THEN uh.value ELSE NULL END) AS boty_fat_percentage, 
            MAX(CASE WHEN h.id=3 THEN uh.value ELSE NULL END) AS blood_pressure, 
            MAX(CASE WHEN h.id=4 THEN uh.value ELSE NULL END) AS general_comments  
            FROM user AS u 
            LEFT JOIN userrole AS ur ON u.id=ur.user_id 
            LEFT JOIN role AS r ON ur.role_id=r.id 
            LEFT JOIN userhealth AS uh ON u.id=uh.user_id 
            LEFT JOIN health AS h ON uh.health_id=h.id 
            WHERE r.id=3 AND u.id LIKE %s
            GROUP BY u.id;"""
    )
    return query


def search_member_name():
    query = (
        """SELECT u.id, r.name, u.first_name, u.last_name, u.email, u.password, u.gender, u.date_of_birth, u.phone_number, u.address, u.isactive,  
            MAX(CASE WHEN h.id=1 THEN uh.value ELSE NULL END) AS weight, 
            MAX(CASE WHEN h.id=2 THEN uh.value ELSE NULL END) AS boty_fat_percentage, 
            MAX(CASE WHEN h.id=3 THEN uh.value ELSE NULL END) AS blood_pressure, 
            MAX(CASE WHEN h.id=4 THEN uh.value ELSE NULL END) AS general_comments  
            FROM user AS u 
            LEFT JOIN userrole AS ur ON u.id=ur.user_id 
            LEFT JOIN role AS r ON ur.role_id=r.id 
            LEFT JOIN userhealth AS uh ON u.id=uh.user_id 
            LEFT JOIN health AS h ON uh.health_id=h.id 
            WHERE r.id=3 AND u.first_name LIKE %s 
            GROUP BY u.id;"""
    )
    return query


def member_login():
    query= ("select u.id, r.name, u.first_name, u.last_name, u.email, u.password, u.gender, u.date_of_birth, u.phone_number, u.address  from user as u \
            left join userrole ur on u.id=ur.user_id left join role as r on ur.role_id=r.id \
            Where r.id=3 AND u.email = %s AND u.password = %s")
    return query

def trainer_login():
    query= ("select u.id, r.name, u.first_name, u.last_name, u.email, u.password, u.gender, u.date_of_birth, u.phone_number, u.address from user as u \
                            left join userrole ur \
                            on u.id=ur.user_id \
                            left join role as r \
                            on ur.role_id=r.id \
                            Where r.id=2 AND u.email = %s AND u.password = %s")
    return query

def admin_login():
    query= ("select u.id, r.name, u.first_name, u.last_name, u.email, u.password, u.gender, u.date_of_birth, u.phone_number, u.address from user as u \
                            left join userrole ur \
                            on u.id=ur.user_id \
                            left join role as r \
                            on ur.role_id=r.id \
                            Where r.id=1 AND u.email = %s AND u.password = %s")
    return query

def add_member():
    query=("INSERT INTO  User(first_name, last_name, email, password, gender, date_of_birth, phone_number, address) \
           VALUES ( %s, %s,  %s,  %s,  %s,  %s,  %s,  %s)")
    return query




def changestatus_member():
    query = (
        """SELECT u.id, r.name, u.first_name, u.last_name, u.email, u.password, u.gender, u.date_of_birth, u.phone_number, u.address, u.isactive
           FROM user AS u LEFT JOIN userrole AS ur ON u.id=ur.user_id LEFT JOIN role AS r ON ur.role_id=r.id 
           WHERE r.id= %s;"""
    )
    return query