from datetime import datetime, timedelta, date
import datetime

today=datetime.date.today()
currentyear=date.year
currentquarter=date.month
YTD_months=today.month
QTD_months=today.month%3

# Fit for new design. HD13Mar23
def user_search_id():
    query = (
        f"SELECT * from member where id= 1"
    )
    #

 # Fit for new design. HD13Mar23   
def trainers():
    query = (
        f"SELECT t.first_name,t.last_name, tq.qualification_id, q.name, q.description FROM trainer t left join trainerqualification tq on t.id = tq.trainer_id left join qualification q on tq.qualification_id = q.id WHERE t.role_id = 2;"
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

 # Fit for new design. HD13Mar23   
def group_class_schedule():
    query = (
        ''' SELECT s.id, s.class_id, s.trainer_id, s.day, s.start_time, s.end_time, s.room, c.name, c.description, c.capacity, t.first_name, t.last_name, 
            COUNT(ba.id) AS Booked, CONCAT(COUNT(ba.id),"/",c.capacity) AS BOOKED_CAPACITY, cast(start_time as time) AS time
            FROM schedule AS s
            LEFT JOIN class AS c ON s.class_id=c.id
            LEFT JOIN trainer AS t ON s.trainer_id=t.id
            LEFT JOIN bookingattendance AS ba ON s.id=ba.schedule_id
            WHERE ba.cancelled=0 AND c.capacity>1
            GROUP BY s.id
            ORDER BY s.start_time
            ; '''
    )
    return query


 # Fit for new design. HD13Mar23   
def group_class_schedule_between_twodate():
    query = (
        ''' SELECT s.id, s.class_id, s.trainer_id, s.day, s.start_time, s.end_time, s.room, c.name, c.description, c.capacity, t.first_name, t.last_name, 
            COUNT(ba.id) AS Booked, CONCAT(COUNT(ba.id),"/",c.capacity) AS BOOKED_CAPACITY, cast(start_time as time) AS time
            FROM schedule AS s
            LEFT JOIN class AS c ON s.class_id=c.id
            LEFT JOIN trainer AS t ON s.trainer_id=t.id
            LEFT JOIN validbookingattendance AS ba ON s.id=ba.schedule_id
            WHERE c.capacity>1 AND s.start_time> %s AND s.start_time< %s
            GROUP BY s.id
            ORDER BY time, s.start_time
            ; '''
    )
    return query


 # Fit for new design. HD13Mar23   
def full_time_table_between_twodate():
    query = (
        ''' SELECT s.id, s.class_id, s.trainer_id, s.day, s.start_time, s.end_time, s.room, c.name, c.description, c.capacity, t.first_name, t.last_name, 
            COUNT(ba.id) AS Booked, CONCAT(COUNT(ba.id),"/",c.capacity) AS BOOKED_CAPACITY, cast(start_time as time) AS time
            FROM schedule AS s
            LEFT JOIN class AS c ON s.class_id=c.id
            LEFT JOIN trainer AS t ON s.trainer_id=t.id
            LEFT JOIN validbookingattendance AS ba ON s.id=ba.schedule_id
            WHERE c.capacity>=1 AND s.start_time> %s AND s.start_time< %s
            GROUP BY s.id
            ORDER BY time, s.start_time
            ; '''
    )
    return query


 # Fit for new design. HD13Mar23   
def member_time_table_between_twodate():
    query = (
        ''' SELECT s.id, s.class_id, s.trainer_id, s.day, s.start_time, s.end_time, s.room, c.name, c.description, c.capacity, t.first_name, t.last_name, 
            COUNT(ba.id) AS Booked, CONCAT(COUNT(ba.id),"/",c.capacity) AS BOOKED_CAPACITY, cast(start_time as time) AS time
            FROM schedule AS s
            LEFT JOIN class AS c ON s.class_id=c.id
            LEFT JOIN trainer AS t ON s.trainer_id=t.id
            LEFT JOIN validbookingattendance AS ba ON s.id=ba.schedule_id
            WHERE c.capacity>=1 AND s.start_time> %s AND s.start_time< %s AND ba.schedule_id IN (select v.schedule_id from validbookingattendance as v left join schedule as s on v.schedule_id=s.id left join class as c on c.id=s.class_id WHERE v.member_id = %s)
            GROUP BY s.id
            ORDER BY time, s.start_time
            ; '''
    )
    return query

def member_time_table_class_between_twodate():
    query = (
        ''' SELECT s.id, s.class_id, s.trainer_id, s.day, s.start_time, s.end_time, s.room, c.name, c.description, c.capacity, t.first_name, t.last_name, 
            COUNT(ba.id) AS Booked, CONCAT(COUNT(ba.id),"/",c.capacity) AS BOOKED_CAPACITY, cast(start_time as time) AS time
            FROM schedule AS s
            LEFT JOIN class AS c ON s.class_id=c.id
            LEFT JOIN trainer AS t ON s.trainer_id=t.id
            LEFT JOIN validbookingattendance AS ba ON s.id=ba.schedule_id
            WHERE c.capacity>1 AND s.start_time> %s AND s.start_time< %s AND ba.schedule_id IN (select v.schedule_id from validbookingattendance as v left join schedule as s on v.schedule_id=s.id left join class as c on c.id=s.class_id WHERE v.member_id = %s)
            GROUP BY s.id
            ORDER BY time, s.start_time
            ; '''
    )
    return query

def member_time_table_session_between_twodate():
    query = (
        ''' SELECT s.id, s.class_id, s.trainer_id, s.day, s.start_time, s.end_time, s.room, c.name, c.description, c.capacity, t.first_name, t.last_name, 
            COUNT(ba.id) AS Booked, CONCAT(COUNT(ba.id),"/",c.capacity) AS BOOKED_CAPACITY, cast(start_time as time) AS time
            FROM schedule AS s
            LEFT JOIN class AS c ON s.class_id=c.id
            LEFT JOIN trainer AS t ON s.trainer_id=t.id
            LEFT JOIN validbookingattendance AS ba ON s.id=ba.schedule_id
            WHERE c.capacity=1 AND s.start_time> %s AND s.start_time< %s AND ba.schedule_id IN (select v.schedule_id from validbookingattendance as v left join schedule as s on v.schedule_id=s.id left join class as c on c.id=s.class_id WHERE v.member_id = %s)
            GROUP BY s.id
            ORDER BY time, s.start_time
            ; '''
    )
    return query

 # Fit for new design. HD13Mar23   
def trainer_time_table_between_twodate():
    query = (
        ''' SELECT s.id, s.class_id, s.trainer_id, s.day, s.start_time, s.end_time, s.room, c.name, c.description, c.capacity, t.first_name, t.last_name, 
            COUNT(ba.id) AS Booked, CONCAT(COUNT(ba.id),"/",c.capacity) AS BOOKED_CAPACITY, cast(start_time as time) AS time
            FROM schedule AS s
            LEFT JOIN class AS c ON s.class_id=c.id
            LEFT JOIN trainer AS t ON s.trainer_id=t.id
            LEFT JOIN validbookingattendance AS ba ON s.id=ba.schedule_id
            WHERE c.capacity>=1 AND s.start_time> %s AND s.start_time< %s AND s.trainer_id = %s
            GROUP BY s.id
            ORDER BY time, s.start_time
            ; '''
    )
    return query

def trainer_time_table_class_between_twodate():
    query = (
        ''' SELECT s.id, s.class_id, s.trainer_id, s.day, s.start_time, s.end_time, s.room, c.name, c.description, c.capacity, t.first_name, t.last_name, 
            COUNT(ba.id) AS Booked, CONCAT(COUNT(ba.id),"/",c.capacity) AS BOOKED_CAPACITY, cast(start_time as time) AS time
            FROM schedule AS s
            LEFT JOIN class AS c ON s.class_id=c.id
            LEFT JOIN trainer AS t ON s.trainer_id=t.id
            LEFT JOIN validbookingattendance AS ba ON s.id=ba.schedule_id
            WHERE c.capacity>1 AND s.start_time> %s AND s.start_time< %s AND s.trainer_id = %s
            GROUP BY s.id
            ORDER BY time, s.start_time
            ; '''
    )
    return query

def trainer_time_table_session_between_twodate():
    query = (
        ''' SELECT s.id, s.class_id, s.trainer_id, s.day, s.start_time, s.end_time, s.room, c.name, c.description, c.capacity, t.first_name, t.last_name, 
            COUNT(ba.id) AS Booked, CONCAT(COUNT(ba.id),"/",c.capacity) AS BOOKED_CAPACITY, cast(start_time as time) AS time
            FROM schedule AS s
            LEFT JOIN class AS c ON s.class_id=c.id
            LEFT JOIN trainer AS t ON s.trainer_id=t.id
            LEFT JOIN validbookingattendance AS ba ON s.id=ba.schedule_id
            WHERE c.capacity=1 AND s.start_time> %s AND s.start_time< %s AND s.trainer_id = %s
            GROUP BY s.id
            ORDER BY time, s.start_time
            ; '''
    )
    return query

def trainer_session_detail():
    query = (
        ''' SELECT s.id, t.id as trainer_id, t.first_name as trainer_first_name, t.last_name as trainer_last_name, s.class_id, c.description, s.room, m.id as trainee_id, m.first_name as trainee_first_name, m.last_name as trainee_last_name, s.start_time, s.end_time, s.day
            FROM schedule s
            JOIN trainer t ON s.trainer_id = t.id
            JOIN validbookingattendance vb on s.id = vb.schedule_id
            JOIN member m on m.id = vb.member_id
            join class c on c.id = s.class_id
            where s.id = %s
            ORDER BY t.id, s.start_time
            LIMIT 1
            ; '''
    )
    return query

 # Fit for new design. HD13Mar23   
def bookscehduleforuser():
    query = (
        '''INSERT INTO bookingattendance (schedule_id, member_id) VALUES (%s, %s);'''
    )
    return query


 # Fit for new design. HD13Mar23   
def memberbookedschedule():
    query = (
        '''Select ba.schedule_id FROM bookingattendance AS ba
        WHERE ba.cancelled =0 AND ba.member_id = %s
        ;'''
    )
    return query


 # Fit for new design. HD13Mar23   
def membercancellschedule():
    query = (
        '''UPDATE bookingattendance SET cancelled = 1 WHERE schedule_id=%s AND member_id=%s ;'''
    )
    return query


 # Fit for new design. HD13Mar23   
def trainer_list():
    query = (
        '''SELECT t.id, t.first_name, t.last_name, GROUP_CONCAT(q.name SEPARATOR ", ") as Qualification, GROUP_CONCAT(q.description SEPARATOR '\n') as Qualification_Detail, t.email, t.phone_number
        FROM trainer AS t
        LEFT JOIN role AS r ON t.role_id=r.id 
        LEFT JOIN trainerqualification AS tq ON t.id=tq.trainer_id 
        LEFT JOIN qualification AS q ON tq.qualification_id=q.id 
        WHERE r.id=2
        GROUP BY t.id
        ORDER by t.last_name ASC;'''
    )
    return query

 # Fit for new design. HD13Mar23  
def trainer_profile():
    query = (
        '''SELECT t.id, t.first_name, t.last_name, GROUP_CONCAT(q.name SEPARATOR ', ') as Qualification, GROUP_CONCAT(q.description SEPARATOR '; ') as Qualification_Detail, t.email, t.phone_number
        FROM trainer AS t
        LEFT JOIN role AS r ON t.role_id=r.id 
        LEFT JOIN trainerqualification AS tq ON t.id=tq.trainer_id 
        LEFT JOIN qualification AS q ON tq.qualification_id=q.id 
        WHERE r.id=2 
        AND t.id=%s
        ;'''
    )
    return query

 # update both tables - trainer, qualification BLW 1503 
def update_trainer_detail():
    trainer_query = (
        '''UPDATE trainer SET first_name= %s, last_name=%s, email=%s, phone_number=%s WHERE id=%s
        ;'''
    )
    return trainer_query

def trainer_qualifications():
    query = (
        '''SELECT t.id trainer_id, q.id qualification_id, t.first_name, t.last_name,  q.name, q.description, t.email,  t.phone_number
    FROM trainer AS t
    LEFT JOIN trainerqualification AS tq ON t.id=tq.trainer_id 
    LEFT JOIN qualification AS q ON tq.qualification_id=q.id
    WHERE t.id=%s
        ;'''
    )
    return query

def insert_trainer_qualification():
    qualification_query = (
        '''INSERT INTO trainerqualification (trainer_id, qualification_id) VALUES (%s, %s);'''
    )
    return qualification_query

 # Fit for new design. HD13Mar23  
def member_list():
    query = (
        """SELECT m.id, r.name, m.first_name, m.last_name, m.email, m.password, m.gender, m.date_of_birth, m.phone_number, m.address, m.isactive, 
            MAX(CASE WHEN h.id=1 THEN mh.value ELSE NULL END) AS weight, 
            MAX(CASE WHEN h.id=2 THEN mh.value ELSE NULL END) AS boty_fat_percentage, 
            MAX(CASE WHEN h.id=3 THEN mh.value ELSE NULL END) AS blood_pressure, 
            MAX(CASE WHEN h.id=4 THEN mh.value ELSE NULL END) AS general_comments  
            FROM member AS m
            LEFT JOIN role AS r ON m.role_id=r.id 
            LEFT JOIN memberhealth AS mh ON m.id=mh.member_id 
            LEFT JOIN health AS h ON mh.health_id=h.id 
            WHERE r.id=3
            GROUP BY m.id;"""
    )
    return query

 # Fit for new design. HD13Mar23  
def member_profile():
    query = (
        """SELECT m.id, r.name, m.first_name, m.last_name, m.email, m.password, m.gender, m.date_of_birth, m.phone_number, m.address, m.isactive, 
            MAX(CASE WHEN h.id=1 THEN mh.value ELSE NULL END) AS weight, 
            MAX(CASE WHEN h.id=2 THEN mh.value ELSE NULL END) AS boty_fat_percentage, 
            MAX(CASE WHEN h.id=3 THEN mh.value ELSE NULL END) AS blood_pressure, 
            MAX(CASE WHEN h.id=4 THEN mh.value ELSE NULL END) AS general_comments  
            FROM member AS m
            LEFT JOIN role AS r ON m.role_id=r.id 
            LEFT JOIN memberhealth AS mh ON m.id=mh.member_id 
            LEFT JOIN health AS h ON mh.health_id=h.id 
            WHERE r.id=3 AND m.id=%s
            GROUP BY m.id;"""
    )
    return query

 # Fit for new design. HD13Mar23  
def member_subscription():
    query = (
        """SELECT member_id, contract_lastdate from account where member_id=%s;"""
    )
    return query

 # Fit for new design. HD13Mar23  
def search_member_id():
    query = (
        """SELECT m.id, r.name, m.first_name, m.last_name, m.email, m.password, m.gender, m.date_of_birth, m.phone_number, m.address, m.isactive, 
            MAX(CASE WHEN h.id=1 THEN mh.value ELSE NULL END) AS weight, 
            MAX(CASE WHEN h.id=2 THEN mh.value ELSE NULL END) AS boty_fat_percentage, 
            MAX(CASE WHEN h.id=3 THEN mh.value ELSE NULL END) AS blood_pressure, 
            MAX(CASE WHEN h.id=4 THEN mh.value ELSE NULL END) AS general_comments  
            FROM member AS m
            LEFT JOIN role AS r ON m.role_id=r.id 
            LEFT JOIN memberhealth AS mh ON m.id=mh.member_id 
            LEFT JOIN health AS h ON mh.health_id=h.id 
            WHERE r.id=3 AND m.id LIKE %s
            GROUP BY m.id;"""
    )
    return query

 # Fit for new design. HD13Mar23  
def search_member_firstname():
    query = (
        """SELECT m.id, r.name, m.first_name, m.last_name, m.email, m.password, m.gender, m.date_of_birth, m.phone_number, m.address, m.isactive, 
            MAX(CASE WHEN h.id=1 THEN mh.value ELSE NULL END) AS weight, 
            MAX(CASE WHEN h.id=2 THEN mh.value ELSE NULL END) AS boty_fat_percentage, 
            MAX(CASE WHEN h.id=3 THEN mh.value ELSE NULL END) AS blood_pressure, 
            MAX(CASE WHEN h.id=4 THEN mh.value ELSE NULL END) AS general_comments  
            FROM member AS m
            LEFT JOIN role AS r ON m.role_id=r.id 
            LEFT JOIN memberhealth AS mh ON m.id=mh.member_id 
            LEFT JOIN health AS h ON mh.health_id=h.id 
            WHERE r.id=3 AND m.first_name LIKE %s
            GROUP BY m.id;"""
    )
    return query

# Fit for new design. HD13Mar23  
def search_member_name():
    query = (
        """SELECT m.id, r.name, m.first_name, m.last_name, m.email, m.password, m.gender, m.date_of_birth, m.phone_number, m.address, m.isactive, 
            MAX(CASE WHEN h.id=1 THEN mh.value ELSE NULL END) AS weight, 
            MAX(CASE WHEN h.id=2 THEN mh.value ELSE NULL END) AS boty_fat_percentage, 
            MAX(CASE WHEN h.id=3 THEN mh.value ELSE NULL END) AS blood_pressure, 
            MAX(CASE WHEN h.id=4 THEN mh.value ELSE NULL END) AS general_comments  
            FROM member AS m
            LEFT JOIN role AS r ON m.role_id=r.id 
            LEFT JOIN memberhealth AS mh ON m.id=mh.member_id 
            LEFT JOIN health AS h ON mh.health_id=h.id 
            WHERE r.id=3 AND m.first_name LIKE %s AND m.last_name LIKE %s
            GROUP BY m.id;"""
    )
    return query

 # Fit for new design. HD13Mar23  
def member_login():
    query= ("select m.id, r.name, m.first_name, m.last_name, m.email, m.password, m.gender, m.date_of_birth, m.phone_number, m.address, m.isactive  from member as m \
            left join role as r on m.role_id=r.id \
            Where r.id=3 AND m.email = %s AND m.password = %s")
    return query

 # Fit for new design. HD13Mar23  
def trainer_login():
    query= ("select t.id, r.name, t.first_name, t.last_name, t.email, t.password, t.gender, t.date_of_birth, t.phone_number, t.address, t.isactive from trainer as t \
                            left join role as r \
                            on t.role_id=r.id \
                            Where r.id=2 AND t.email = %s AND t.password = %s")
    return query

 # Fit for new design. HD13Mar23  
def admin_login():
    query= ("select a.id, r.name, a.first_name, a.last_name, a.email, a.password, a.gender, a.date_of_birth, a.phone_number, a.address, a.isactive from admin as a \
                            left join role as r \
                            on a.role_id=r.id \
                            Where r.id=1 AND a.email = %s AND a.password = %s")
    return query

 # Fit for new design. HD13Mar23  
def add_member():
    query=("INSERT INTO  member(role_id, first_name, last_name, email, password, gender, date_of_birth, phone_number, address, notes) \
           VALUES ( 3, %s, %s,  %s,  %s,  %s,  %s,  %s,  %s, %s)")
    return query



def financialreport_session_byyearquarter():
    query = (
        '''
        SELECT ANY_VALUE(dt1.year), 'Q0' AS quarter, FORMAT(COALESCE(SUM(spt1.amount),0),'C','en-NZ') AS SessionPayment, ANY_VALUE(tt1.typename)
        FROM datetable AS dt1
        LEFT JOIN sessionpaymenttransaction AS spt1 ON dt1.date=spt1.date
        LEFT JOIN transactiontype AS tt1 ON tt1.id=spt1.paytype
        WHERE YEAR=%s
        GROUP BY dt1.year
        UNION
        SELECT ANY_VALUE(dt2.year), ANY_VALUE(dt2.quarter), FORMAT(COALESCE(SUM(spt2.amount),0),'C','en-NZ') AS SessionPayment, ANY_VALUE(tt2.typename)
        FROM datetable AS dt2
        LEFT JOIN sessionpaymenttransaction AS spt2 ON dt2.date=spt2.date
        LEFT JOIN transactiontype AS tt2 ON tt2.id=spt2.paytype
        WHERE YEAR=%s
        GROUP BY dt2.quarter
        ORDER BY quarter
        ;
        '''
    )
    return query


def financialreport_session_byyearmonth():
    query = (
        '''
        SELECT ANY_VALUE(dt.year), ANY_VALUE(dt.quarter), ANY_VALUE(dt.month), FORMAT(COALESCE(SUM(amount),0),'C','en-NZ') AS SessionPayment, MAX(typename)
        FROM datetable AS dt
        LEFT JOIN sessionpaymenttransaction AS spt ON dt.date=spt.date
        LEFT JOIN transactiontype ON transactiontype.id=spt.paytype
        WHERE YEAR=%s
        GROUP BY dt.month
        ORDER BY dt.month
        ;
        '''
    )
    return query

def financialreport_subscription_byyearquarter():
    query = (
        '''
        SELECT ANY_VALUE(dt1.year), 'Q0' AS quarter, FORMAT(COALESCE(SUM(spt1.amount),0),'C','en-NZ') AS SubscriptionPayment, ANY_VALUE(tt1.typename)
        FROM datetable AS dt1
        LEFT JOIN subscriptionpaymenttransaction AS spt1 ON dt1.date=spt1.date
        LEFT JOIN transactiontype AS tt1 ON tt1.id=spt1.paytype
        WHERE YEAR=%s
        GROUP BY dt1.year
        UNION
        SELECT ANY_VALUE(dt2.year), ANY_VALUE(dt2.quarter), FORMAT(COALESCE(SUM(spt2.amount),0),'C','en-NZ') AS SubscriptionPayment, ANY_VALUE(tt2.typename)
        FROM datetable AS dt2
        LEFT JOIN subscriptionpaymenttransaction AS spt2 ON dt2.date=spt2.date
        LEFT JOIN transactiontype AS tt2 ON tt2.id=spt2.paytype
        WHERE YEAR=%s
        GROUP BY dt2.quarter
        ORDER BY quarter
        ;
        '''
    )
    return query

def financialreport_subscription_byyearmonth():
    query = (
        '''
        SELECT ANY_VALUE(dt.year), ANY_VALUE(dt.quarter), ANY_VALUE(dt.month), FORMAT(COALESCE(SUM(amount),0),'C','en-NZ') AS SubscriptionPayment, MAX(typename)
        FROM datetable AS dt
        LEFT JOIN subscriptionpaymenttransaction AS spt ON dt.date=spt.date
        LEFT JOIN transactiontype ON transactiontype.id=spt.paytype
        WHERE YEAR=%s
        GROUP BY dt.month
        ORDER BY dt.month
        ;
        '''
    )
    return query

def financialreport_newcontract_bymonth():
    query = (
        '''
        SELECT ANY_VALUE(dt.year), ANY_VALUE(dt.quarter), ANY_VALUE(dt.month), COALESCE(COUNT(m.id),0) AS NewContract
        FROM datetable AS dt
        LEFT JOIN account as a ON dt.date=a.contract_startdate
        LEFT JOIN member as m ON m.id=a.member_id
        WHERE YEAR=%s
        GROUP BY dt.month
        ORDER BY dt.month
        ;
        '''
    )
    return query

def financialreport_newcontract_byquarter():
    query = (
        '''
        SELECT ANY_VALUE(dt1.year), 'Q0' AS quarter, COALESCE(COUNT(m1.id),0) AS NewContract
        FROM datetable AS dt1
        LEFT JOIN account as a1 ON dt1.date=a1.contract_startdate
        LEFT JOIN member as m1 ON m1.id=a1.member_id
        WHERE YEAR=%s
        GROUP BY dt1.year
        UNION
        SELECT ANY_VALUE(dt2.year), ANY_VALUE(dt2.quarter), COALESCE(COUNT(m2.id),0) AS NewContract
        FROM datetable AS dt2
        LEFT JOIN account as a2 ON dt2.date=a2.contract_startdate
        LEFT JOIN member as m2 ON m2.id=a2.member_id
        WHERE YEAR=%s
        GROUP BY dt2.quarter
        ORDER BY quarter
        ;
        '''
    )
    return query

def financialreport_expirecontract_bymonth():
    query = (
        '''
        SELECT ANY_VALUE(dt.year), ANY_VALUE(dt.quarter), ANY_VALUE(dt.month), COALESCE(COUNT(m.id),0) AS ExpiredContract
        FROM datetable AS dt
        LEFT JOIN account as a ON dt.date=a.contract_lastdate
        LEFT JOIN member as m ON m.id=a.member_id
        WHERE YEAR=%s
        GROUP BY dt.month
        ORDER BY dt.month
        ;
        '''
    )
    return query

def financialreport_expirecontract_byquarter():
    query = (
        '''
        SELECT ANY_VALUE(dt1.year), 'Q0' AS quarter, COALESCE(COUNT(m1.id),0) AS ExpiredContract
        FROM datetable AS dt1
        LEFT JOIN account as a1 ON dt1.date=a1.contract_lastdate
        LEFT JOIN member as m1 ON m1.id=a1.member_id
        WHERE YEAR=%s
        GROUP BY dt1.year
        UNION
        SELECT ANY_VALUE(dt2.year), ANY_VALUE(dt2.quarter), COALESCE(COUNT(m2.id),0) AS ExpiredContract
        FROM datetable AS dt2
        LEFT JOIN account as a2 ON dt2.date=a2.contract_lastdate
        LEFT JOIN member as m2 ON m2.id=a2.member_id
        WHERE YEAR=%s
        GROUP BY dt2.quarter
        ORDER BY quarter;
        '''
    )
    return query

def financialreport_activesubscriptioncount_byquarter():
    query = (
        '''
        SELECT ANY_VALUE(dt1.year), 'Q0' AS quarter, REPLACE(ROUND(FORMAT(COALESCE(COUNT(spt1.amount),0),'C','en-NZ')/12,0), '.0','') AS SubscriptionPayment, ANY_VALUE(tt1.typename)
        FROM datetable AS dt1
        LEFT JOIN subscriptionpaymenttransaction AS spt1 ON dt1.date=spt1.date
        LEFT JOIN transactiontype AS tt1 ON tt1.id=spt1.paytype
        WHERE YEAR=%s
        GROUP BY dt1.year
        UNION
        SELECT ANY_VALUE(dt2.year), ANY_VALUE(dt2.quarter), REPLACE(ROUND(FORMAT(COALESCE(COUNT(spt2.amount),0),'C','en-NZ')/3,0), '.0','') AS SubscriptionPayment, ANY_VALUE(tt2.typename)
        FROM datetable AS dt2
        LEFT JOIN subscriptionpaymenttransaction AS spt2 ON dt2.date=spt2.date
        LEFT JOIN transactiontype AS tt2 ON tt2.id=spt2.paytype
        WHERE YEAR=%s
        GROUP BY dt2.quarter
        ORDER BY quarter
        ;
        '''
    )
    return query

def financialreport_activesubscriptioncount_byquarter_currentyear():
    query = (
        '''
        SELECT ANY_VALUE(dt1.year), 'Q0' AS quarter, REPLACE(ROUND(FORMAT(COALESCE(COUNT(spt1.amount),0),'C','en-NZ')/%s,0), '.0','') AS SubscriptionPayment, ANY_VALUE(tt1.typename)
        FROM datetable AS dt1
        LEFT JOIN subscriptionpaymenttransaction AS spt1 ON dt1.date=spt1.date
        LEFT JOIN transactiontype AS tt1 ON tt1.id=spt1.paytype
        WHERE YEAR=%s
        GROUP BY dt1.year
        UNION
        SELECT ANY_VALUE(dt2.year), ANY_VALUE(dt2.quarter), REPLACE(ROUND(FORMAT(COALESCE(COUNT(spt2.amount),0),'C','en-NZ')/3,0), '.0','') AS SubscriptionPayment, ANY_VALUE(tt2.typename)
        FROM datetable AS dt2
        LEFT JOIN subscriptionpaymenttransaction AS spt2 ON dt2.date=spt2.date
        LEFT JOIN transactiontype AS tt2 ON tt2.id=spt2.paytype
        WHERE YEAR=%s
        GROUP BY dt2.quarter
        ORDER BY quarter
        ;
        '''
    )
    return query

def financialreport_activesubscriptioncount_bymonth():
    query = (
        '''
        SELECT ANY_VALUE(dt.year), ANY_VALUE(dt.quarter), ANY_VALUE(dt.month), COALESCE(COUNT(amount),0) AS SubscriptionPayment, MAX(typename)
        FROM datetable AS dt
        LEFT JOIN subscriptionpaymenttransaction AS spt ON dt.date=spt.date
        LEFT JOIN transactiontype ON transactiontype.id=spt.paytype
        WHERE YEAR=%s
        GROUP BY dt.month
        ORDER BY dt.month
        ;
        '''
    )
    return query

def financialreport_sessioncount_byquarter():
    query = (
        '''
        SELECT ANY_VALUE(dt1.year), 'Q0' AS quarter, FORMAT(COALESCE(COUNT(spt1.amount),0),'C','en-NZ') AS SessionPayment, ANY_VALUE(tt1.typename)
        FROM datetable AS dt1
        LEFT JOIN sessionpaymenttransaction AS spt1 ON dt1.date=spt1.date
        LEFT JOIN transactiontype AS tt1 ON tt1.id=spt1.paytype
        WHERE YEAR=%s
        GROUP BY dt1.year
        UNION
        SELECT ANY_VALUE(dt2.year), ANY_VALUE(dt2.quarter), FORMAT(COALESCE(COUNT(spt2.amount),0),'C','en-NZ') AS SessionPayment, ANY_VALUE(tt2.typename)
        FROM datetable AS dt2
        LEFT JOIN sessionpaymenttransaction AS spt2 ON dt2.date=spt2.date
        LEFT JOIN transactiontype AS tt2 ON tt2.id=spt2.paytype
        WHERE YEAR=%s
        GROUP BY dt2.quarter
        ORDER BY quarter
        ;
        '''
    )
    return query

def financialreport_sessioncount_bymonth():
    query = (
        '''
        SELECT ANY_VALUE(dt2.year), ANY_VALUE(dt2.quarter),  ANY_VALUE(dt2.month), FORMAT(COALESCE(COUNT(spt2.amount),0),'C','en-NZ') AS SessionPayment, ANY_VALUE(tt2.typename)
        FROM datetable AS dt2
        LEFT JOIN sessionpaymenttransaction AS spt2 ON dt2.date=spt2.date
        LEFT JOIN transactiontype AS tt2 ON tt2.id=spt2.paytype
        WHERE YEAR=%s
        GROUP BY dt2.month
        ORDER BY dt2.month
        ;
        '''
    )
    return query

def financialreport_total_byyearquarter():
    query = (
        '''
        SELECT ANY_VALUE(dt1.year), 'Q0' AS quarter, FORMAT(COALESCE(SUM(spt1.amount),0),'C','en-NZ') AS SessionPayment, ANY_VALUE(tt1.typename)
        FROM datetable AS dt1
        LEFT JOIN subscriptionsessionrefund AS spt1 ON dt1.date=spt1.date
        LEFT JOIN transactiontype AS tt1 ON tt1.id=spt1.paytype
        WHERE YEAR=%s
        GROUP BY dt1.year
        UNION
        SELECT ANY_VALUE(dt2.year), ANY_VALUE(dt2.quarter), FORMAT(COALESCE(SUM(spt2.amount),0),'C','en-NZ') AS SessionPayment, ANY_VALUE(tt2.typename)
        FROM datetable AS dt2
        LEFT JOIN subscriptionsessionrefund AS spt2 ON dt2.date=spt2.date
        LEFT JOIN transactiontype AS tt2 ON tt2.id=spt2.paytype
        WHERE YEAR=%s
        GROUP BY dt2.quarter
        ORDER BY quarter;
        '''
    )
    return query

def financialreport_refund_byyearquarter():
    query = (
        '''
        SELECT ANY_VALUE(dt1.year), 'Q0' AS quarter, FORMAT(COALESCE(SUM(spt1.amount),0),'C','en-NZ') AS SessionPayment, ANY_VALUE(tt1.typename)
        FROM datetable AS dt1
        LEFT JOIN refund AS spt1 ON dt1.date=spt1.date
        LEFT JOIN transactiontype AS tt1 ON tt1.id=spt1.paytype
        WHERE YEAR=%s
        GROUP BY dt1.year
        UNION
        SELECT ANY_VALUE(dt2.year), ANY_VALUE(dt2.quarter), FORMAT(COALESCE(SUM(spt2.amount),0),'C','en-NZ') AS SessionPayment, ANY_VALUE(tt2.typename)
        FROM datetable AS dt2
        LEFT JOIN refund AS spt2 ON dt2.date=spt2.date
        LEFT JOIN transactiontype AS tt2 ON tt2.id=spt2.paytype
        WHERE YEAR=%s
        GROUP BY dt2.quarter
        ORDER BY quarter;
        '''
    )
    return query

def financialreport_total_bymonth():
    query = (
        '''
        SELECT ANY_VALUE(dt.year), ANY_VALUE(dt.quarter), ANY_VALUE(dt.month), FORMAT(COALESCE(SUM(amount),0),'C','en-NZ') AS SubscriptionPayment, MAX(typename)
        FROM datetable AS dt
        LEFT JOIN subscriptionsessionrefund AS spt ON dt.date=spt.date
        LEFT JOIN transactiontype ON transactiontype.id=spt.paytype
        WHERE YEAR=%s
        GROUP BY dt.month
        ORDER BY dt.month
        '''
    )
    return query

def financialreport_refund_bymonth():
    query = (
        '''
        SELECT ANY_VALUE(dt.year), ANY_VALUE(dt.quarter), ANY_VALUE(dt.month), FORMAT(COALESCE(SUM(amount),0),'C','en-NZ') AS SubscriptionPayment, MAX(typename)
        FROM datetable AS dt
        LEFT JOIN refund AS spt ON dt.date=spt.date
        LEFT JOIN transactiontype ON transactiontype.id=spt.paytype
        WHERE YEAR=%s
        GROUP BY dt.month
        ORDER BY dt.month
        '''
    )
    return query

def classreport():
    query = (
        '''
        SELECT schedule_id, name, s.day, s.start_time, t.first_name as teacher, COUNT(member_id) AS attended
        FROM bookingattendance ba
        JOIN member as m on m.id=ba.member_id
        JOIN schedule as s on s.id=ba.schedule_id
        join class as c on c.id=s.class_id
        join trainer as t on t.id=s.trainer_id
        WHERE c.capacity > 1
        GROUP BY s.id
        ORDER BY COUNT(member_id) DESC
        ;
        '''
    )
    return query

# monthly Payment Report with timeperiod variable
def monthlyPaymentReport():
    query = ('''SELECT a.id,m.first_name AS name, m.last_name AS surname, t.amount AS payment_made, t.reference, t.created_at AS datePaid, tt.id
            FROM transaction AS t
            INNER JOIN account a ON a.id = t.account_id
            JOIN member AS m ON a.member_id = m.id
            INNER JOIN transactiontype AS tt ON tt.id= t.paytype
            WHERE t.created_at >= DATE_SUB(CURDATE(), INTERVAL %s week) AND tt.id = '3' ORDER BY t.created_at DESC;''' )        
    return query

# session Payment Report with timeperiod variable
def sessionPaymentReport():
    query = ('''SELECT a.id, m.first_name AS name, m.last_name AS surname, t.amount AS payment_made, t.reference, t.created_at AS datePaid, tt.id
            FROM transaction AS t
            INNER JOIN account a ON a.id = t.account_id
            JOIN member AS m ON a.member_id = m.id
            INNER JOIN transactiontype AS tt ON tt.id= t.paytype
            WHERE t.created_at >= DATE_SUB(CURDATE(), INTERVAL %s week) AND tt.id = '4' ORDER BY t.created_at DESC;''' )        
    return query
# refund Report with timeperiod variable
def refundSessionReport():
    query = ('''SELECT a.id, m.first_name AS name, m.last_name AS surname, t.amount AS payment_made, t.reference, t.created_at AS datePaid, tt.id
            FROM transaction AS t
            INNER JOIN account a ON a.id = t.account_id
            JOIN member AS m ON a.member_id = m.id
            INNER JOIN transactiontype AS tt ON tt.id= t.paytype
            WHERE t.created_at >= DATE_SUB(CURDATE(), INTERVAL %s week) AND tt.id = '6' ORDER BY t.created_at DESC;''' )        
    return query
# all PaymentReport with timeperiod variable
def allPaymentReport():
    query = ('''SELECT a.id, m.first_name AS name, m.last_name AS surname, t.amount AS payment_made, t.reference, t.created_at AS datePaid, tt.id
            FROM transaction AS t
            INNER JOIN account a ON a.id = t.account_id
            JOIN member AS m ON a.member_id = m.id
            INNER JOIN transactiontype AS tt ON tt.id= t.paytype
            WHERE t.created_at >= DATE_SUB(CURDATE(), INTERVAL %s week) AND ( tt.id = '6' or  tt.id = '4' or  tt.id = '3') ORDER BY t.created_at DESC;''' )        
    return query






def pay_session():
    query = (
        '''
        INSERT INTO transaction (account_id, amount, paytype, bookingAttendance_id, reference, date, time) VALUES
        (%s,%s,4,%s,'sessionpaymentweb',%s,%s);
    '''
    )
    return query

def refund_session():
    query = (
        '''
        INSERT INTO transaction (account_id, amount, paytype, bookingAttendance_id, reference, date, time) VALUES
        (%s,%s,6,%s,'sessionrefundweb',%s,%s);
    '''
    )
    return query

def check_baid():
    query = (
        '''
        select * from validbookingattendance where schedule_id = %s AND member_id = %s; 
        '''
    )
    return query

# attendance for all members with default time period of 4 weeks
def allAttendance():
    query =(
        '''SELECT m.first_name AS attendee, m.last_name AS attendee_surname, c.name AS class, s.day, ba.check_in_time AS day_time_attended,ba.cancelled
        FROM bookingattendance AS ba 
        INNER JOIN member AS m ON ba.member_id = m.id
        INNER JOIN schedule AS s ON ba.schedule_id = s.id
        INNER JOIN class AS c ON c.id = s.class_id
        WHERE ba.check_in_time >= DATE_SUB(CURDATE(), INTERVAL 4 week)
        ORDER BY ba.check_in_time DESC
;'''
    )

    return query

# attendance  by ID
def attendanceById():
    query =(
        '''SELECT m.first_name AS attendee, m.last_name AS attendee_surname, c.name AS class, s.day, ba.check_in_time, ba.cancelled
        FROM bookingattendance AS ba 
        INNER JOIN member m ON ba.member_id = m.id
        INNER JOIN schedule AS s ON ba.schedule_id = s.id
        INNER JOIN class AS c ON c.id = s.class_id
        WHERE ba.check_in_time >= DATE_SUB(CURDATE(), INTERVAL 4 week) AND m.id = %s  ORDER BY ba.check_in_time DESC;''')
    
    return query

# attendance  by name search
def attendanceByName():
    query =(
        '''SELECT m.first_name AS attendee, m.last_name AS attendee_surname, c.name AS class, s.day, ba.check_in_time, ba.cancelled
        FROM bookingattendance AS ba 
        INNER JOIN member m ON ba.member_id = m.id
        INNER JOIN schedule AS s ON ba.schedule_id = s.id
        INNER JOIN class AS c ON c.id = s.class_id
        WHERE ba.check_in_time >= DATE_SUB(CURDATE(), INTERVAL 4 week) AND (m.first_name LIKE %s or m.last_name LIKE %s)  ORDER BY ba.check_in_time DESC;''')
    
    return query

# summarise class attendance by ID
def attendanceByIdClassSummary():
    query =(
        '''SELECT SUM(times) FROM (SELECT c.name AS class, s.class_id, COUNT(ba.member_id) AS times
        FROM bookingattendance AS ba 
        INNER JOIN member m ON ba.member_id = m.id
        INNER JOIN schedule AS s ON ba.schedule_id = s.id
        INNER JOIN class AS c ON c.id = s.class_id
        WHERE ba.check_in_time >= DATE_SUB(CURDATE(), INTERVAL 4 week) AND m.id = %s AND ba.check_in_time IS NOT NULL AND (s.class_id=1 OR s.class_id=2 OR s.class_id=3)
        GROUP BY s.class_id) AS timestable;''')
    
    return query
# summarise session attendance by ID
def attendanceByIdSessionSummary():
    query =(
        '''SELECT SUM(times) FROM (SELECT c.name AS class, s.class_id, COUNT(ba.member_id) AS times
        FROM bookingattendance AS ba 
        INNER JOIN member m ON ba.member_id = m.id
        INNER JOIN schedule AS s ON ba.schedule_id = s.id
        INNER JOIN class AS c ON c.id = s.class_id
        WHERE ba.check_in_time >= DATE_SUB(CURDATE(), INTERVAL 4 week) AND m.id = %s AND ba.check_in_time IS NOT NULL AND (s.class_id=4 OR s.class_id=5)
        GROUP BY s.class_id) AS timestable;''')
    
    return query

# summarise gym access by ID
def attendanceByIdGymSummary():
    query =(
        '''SELECT SUM(times) FROM (SELECT c.name AS class, s.class_id, COUNT(ba.member_id) AS times
        FROM bookingattendance AS ba 
        INNER JOIN member m ON ba.member_id = m.id
        INNER JOIN schedule AS s ON ba.schedule_id = s.id
        INNER JOIN class AS c ON c.id = s.class_id
        WHERE ba.check_in_time >= DATE_SUB(CURDATE(), INTERVAL 4 week) AND m.id = %s AND ba.check_in_time IS NOT NULL AND (s.class_id=6)
        GROUP BY s.class_id) AS timestable;''')
    
    return query


# summarise class attendance by name
def attendanceByNameClassSummary():
    query =(
    '''SELECT SUM(times) FROM (SELECT c.name AS class, s.class_id, COUNT(ba.member_id) AS times
    FROM bookingattendance AS ba 
    INNER JOIN member m ON ba.member_id = m.id
    INNER JOIN schedule AS s ON ba.schedule_id = s.id
    INNER JOIN class AS c ON c.id = s.class_id
    WHERE ba.check_in_time >= DATE_SUB(CURDATE(), INTERVAL 4 week) AND (m.first_name LIKE %s or m.last_name LIKE %s) AND ba.check_in_time IS NOT NULL AND (s.class_id=1 OR s.class_id=2 OR s.class_id=3)
    GROUP BY s.class_id) AS timestable;''')

    return query

# summarise session attendance by name
def attendanceByNameSessionSummary():
    query =(
    '''SELECT SUM(times) FROM (SELECT c.name AS class, s.class_id, COUNT(ba.member_id) AS times
    FROM bookingattendance AS ba 
    INNER JOIN member m ON ba.member_id = m.id
    INNER JOIN schedule AS s ON ba.schedule_id = s.id
    INNER JOIN class AS c ON c.id = s.class_id
    WHERE ba.check_in_time >= DATE_SUB(CURDATE(), INTERVAL 4 week) AND (m.first_name LIKE %s or m.last_name LIKE %s) AND ba.check_in_time IS NOT NULL AND (s.class_id=4 OR s.class_id=5)
    GROUP BY s.class_id) AS timestable;''')

    return query

# summarise gym access by name
def attendanceByNameGymSummary():
    query =(
    '''SELECT SUM(times) FROM (SELECT c.name AS class, s.class_id, COUNT(ba.member_id) AS times
    FROM bookingattendance AS ba 
    INNER JOIN member m ON ba.member_id = m.id
    INNER JOIN schedule AS s ON ba.schedule_id = s.id
    INNER JOIN class AS c ON c.id = s.class_id
    WHERE ba.check_in_time >= DATE_SUB(CURDATE(), INTERVAL 4 week) AND (m.first_name LIKE %s or m.last_name LIKE %s) AND ba.check_in_time IS NOT NULL AND (s.class_id=6)
    GROUP BY s.class_id) AS timestable;''')

    return query



def member_news():
    query =(
        """ select * from newsletters where status = 1;"""
    )
    return query

def admin_news():
    query =(
        """ select * from newsletters order by newsletter_id DESC;"""
    )
    return query

def add_news():
    query=("INSERT INTO  newsletters(title, content, date, status) \
           VALUES ( %s, %s,  %s,  %s)")
    return query

 # BLW adding acccount for new member  
def add_account():
    query="INSERT INTO  account(id, member_id, balance, last_subscription_payment, contract_startdate, contract_lastdate) \
           VALUES (%s, %s,  %s,  %s,  %s,  %s)"
    return query



def newmemberpay():
    query="INSERT INTO transaction(account_id, amount, paytype, reference, created_at)\
            VALUES (%s, %s,  %s,  %s,  %s)"
    return query      
