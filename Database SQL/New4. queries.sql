
-- admins - Admin (HD)
SELECT a.id, r.name, a.first_name, a.last_name, a.email, a.password, a.gender, a.date_of_birth, a.phone_number, a.address 
FROM admin AS a
LEFT JOIN role AS r ON a.role_id=r.id WHERE r.id=1;

-- trainers - trainer (HD)
SELECT t.id, r.name, t.first_name, t.last_name, t.email, t.password, t.gender, t.date_of_birth, t.phone_number, t.address 
FROM trainer AS t
LEFT JOIN role AS r ON t.role_id=r.id WHERE r.id=2;

-- Users - Trainer Qualifications (HD)
SELECT t.id, r.name, q.name, q.description, t.first_name, t.last_name, t.email, t.password, t.gender, t.date_of_birth, t.phone_number, t.address 
FROM trainer AS t
LEFT JOIN role AS r ON t.role_id=r.id
LEFT JOIN trainerqualification AS tq ON t.id=tq.trainer_id 
LEFT JOIN qualification AS q ON tq.qualification_id=q.id 
WHERE r.id=2;

-- Users - Trainer and their Qualifications (BW)
SELECT t.id trainer_id, q.id qual_id, t.first_name, t.last_name,  q.name, q.description, t.email,  t.phone_number
FROM trainer AS t
LEFT JOIN trainerqualification AS tq ON t.id=tq.trainer_id 
LEFT JOIN qualification AS q ON tq.qualification_id=q.id;

-- Users - specific Trainer and  Qualifications (BW)
select trainer_id as tid, qualification_id as qid, name as qname  
from trainerqualification tq 
join qualification q on q.id=tq.qualification_id
where trainer_id = 3;

-- Users - Member (HD)
SELECT m.id, r.name, m.first_name, m.last_name, m.email, m.password, m.gender, m.date_of_birth, m.phone_number, m.address 
FROM member AS m
LEFT JOIN role AS r ON m.role_id=r.id WHERE r.id=3;

-- members - Member Health (HD)
SELECT m.id, r.name, m.first_name, m.last_name, m.email, m.password, m.gender, m.date_of_birth, m.phone_number, m.address, 
MAX(CASE WHEN h.id=1 THEN mh.value ELSE NULL END) AS weight, 
MAX(CASE WHEN h.id=2 THEN mh.value ELSE NULL END) AS boty_fat_percentage, 
MAX(CASE WHEN h.id=3 THEN mh.value ELSE NULL END) AS blood_pressure, 
MAX(CASE WHEN h.id=4 THEN mh.value ELSE NULL END) AS general_comments 
FROM member AS m
LEFT JOIN role AS r ON m.role_id=r.id 
LEFT JOIN memberhealth AS mh ON m.id=mh.member_id 
LEFT JOIN health AS h ON mh.health_id=h.id 
WHERE r.id=3 
GROUP BY m.id;

-- query to view class timetable (no privates) (BW)
SELECT c.name AS class, t.first_name as trainer, s.day, s.start_time, s.room
FROM class AS c
INNER JOIN schedule AS s on c.id = s.class_id
INNER JOIN trainer AS t on s.trainer_id = t.id
WHERE c.capacity > 1
;

-- query to view timetable with teacher Amy Ferguson (BW) - see both classes and private bookings (BW)
SELECT c.name AS class, t.first_name AS trainer, s.day, s.start_time, s.room
FROM class AS c
INNER JOIN schedule AS s ON c.id = s.class_id
INNER JOIN trainer AS t ON s.trainer_id = t.id
WHERE t.first_name = 'Amy'
;

-- query to view attendance by member Hido (BW)
SELECT m.first_name AS attendee, m.last_name AS attendee_surname, c.name AS class, s.day, ba.check_in_time
FROM bookingattendance AS ba 
INNER JOIN member m ON ba.member_id = m.id
INNER JOIN schedule AS s ON ba.schedule_id = s.id
INNER JOIN class AS c ON c.id = s.class_id
WHERE m.first_name = 'Miao'
;



-- query to view attendance by all members (BW)
SELECT m.first_name AS attendee, m.last_name AS attendee_surname, c.name AS class, ba.check_in_time AS day_time_attended
FROM bookingattendance AS ba 
INNER JOIN member AS m ON ba.member_id = m.id
INNER JOIN schedule AS s ON ba.schedule_id = s.id
INNER JOIN class AS c ON c.id = s.class_id
;

-- query to view number of attendees at each class (most popular class) (BW) 
SELECT schedule_id, name, s.day, s.start_time, t.first_name as teacher, COUNT(member_id) AS attended
FROM bookingattendance ba
JOIN member as m on m.id=ba.member_id
JOIN schedule as s on s.id=ba.schedule_id
join class as c on c.id=s.class_id
join trainer as t on t.id=s.trainer_id
WHERE c.capacity > 1
GROUP BY s.id
ORDER BY COUNT(member_id) DESC;

-- query to see all money coming into the gym (BW)
SELECT m.first_name AS name, m.last_name AS surname, t.amount AS payment_made, t.reference, t.created_at AS datePaid
FROM transaction AS t
INNER JOIN account a ON a.id = t.Account_id
JOIN member m ON a.member_id = m.id;

-- query to see private only payments (BW)
SELECT m.first_name AS name, m.last_name AS surname, t.amount AS payment_made, t.reference, t.created_at AS datePaid
FROM transaction AS t
INNER JOIN account a ON a.id = t.account_id
JOIN member AS m ON a.member_id = m.id
WHERE t.reference = 'private';


-- Upcoming Group Class by weeks
SELECT *
FROM bookingattendance AS ba
;

-- query to see all classes and sessions scheduled (MS)
SELECT trainer.first_name, trainer.last_name, class.name, schedule.day, schedule.start_time, schedule.end_time, schedule.room, role.name
FROM trainer
JOIN schedule ON trainer.id = schedule.trainer_id
JOIN class ON schedule.class_id = class.id
JOIN role ON trainer.role_id = role.id
WHERE role.name = 'trainer';

-- Schedule All (HD)
SELECT *
FROM schedule AS s
LEFT JOIN class AS c ON s.class_id=c.id
LEFT JOIN trainer AS t ON s.trainer_id=t.id
ORDER BY s.start_time
;

-- Class Schedule Only Personal Training Session(HD)
SELECT *
FROM schedule AS s
LEFT JOIN class AS c ON s.class_id=c.id
LEFT JOIN trainer AS t ON s.trainer_id=t.id
WHERE c.capacity=1
ORDER BY s.start_time
;

-- Class Schedule Only Group Class (HD)
SELECT *
FROM schedule AS s
LEFT JOIN class AS c ON s.class_id=c.id
LEFT JOIN trainer AS t ON s.trainer_id=t.id
WHERE c.capacity>1
ORDER BY s.start_time
;

-- GROUP Class Schedule with BOOKING TO CAPACITY (HD)
SELECT s.id, s.class_id, s.trainer_id, s.day, s.start_time, s.end_time, s.room, c.name, c.description, c.capacity, t.first_name, t.last_name, 
COUNT(ba.id) AS Booked, CONCAT(COUNT(ba.id),"/",c.capacity) AS BOOKED_CAPACITY
FROM schedule AS s
LEFT JOIN class AS c ON s.class_id=c.id
LEFT JOIN trainer AS t ON s.trainer_id=t.id
LEFT JOIN bookingattendance AS ba ON s.id=ba.schedule_id
WHERE ba.cancelled=0 AND c.capacity>1
GROUP BY s.id
ORDER BY s.start_time
;

-- query to see all trainers and their qualification (MS)
SELECT t.first_name, t.last_name, tq.qualification_id, q.name, q.description FROM trainer t
left join trainerqualification tq on t.id = tq.trainer_id
left join qualification q on tq.qualification_id = q.id
WHERE t.role_id = 2;

-- query to see class at a particular time (MS)
SELECT schedule.id, class.name, schedule.room, schedule.start_time, schedule.end_time,
                trainer.first_name, trainer.last_name
                FROM schedule
                LEFT JOIN bookingattendance ON bookingattendance.schedule_id = schedule.id
                LEFT JOIN class ON class.id = schedule.class_id
                LEFT JOIN trainer ON trainer.id = schedule.trainer_id
                WHERE schedule.start_time BETWEEN '2023-03-13 09:00:00' AND '2023-03-13 10:00:00'
                ORDER BY schedule.start_time;


-- SELECT for creating view for trainer to view personal sessions for each member (MS)
SELECT t.id as trainer_id, t.first_name as trainer_first_name, t.last_name as trainer_last_name, s.class_id, s.room, m.id as trainee_id, m.first_name as trainee_first_name, m.last_name as trainee_last_name, s.start_time, s.end_time, s.day
FROM schedule s
JOIN trainer t ON s.trainer_id = t.id
JOIN validbookingattendance vb on s.id = vb.schedule_id
JOIN member m on m.id = vb.member_id
ORDER BY t.id, s.start_time;


-- create view for trainer to view personal sessions for each member (MS)
CREATE VIEW bookings_by_trainer AS
SELECT t.id as trainer_id, t.first_name as trainer_first_name, t.last_name as trainer_last_name, s.class_id, s.room, m.id as trainee_id, m.first_name as trainee_first_name, m.last_name as trainee_last_name, s.start_time, s.end_time, s.day
FROM schedule s
JOIN trainer t ON s.trainer_id = t.id
JOIN validbookingattendance vb on s.id = vb.schedule_id
JOIN member m on m.id = vb.user_id
ORDER BY t.id, s.start_time;

-- 
SELECT * from member where id= 1;

--
SELECT t.first_name,t.last_name, tq.qualification_id, q.name, q.description FROM trainer t left join trainerqualification tq on t.id = tq.trainer_id left join qualification q on tq.qualification_id = q.id WHERE t.role_id = 2;

--
SELECT t.id, t.first_name, t.last_name, GROUP_CONCAT(q.name SEPARATOR ", ") as Qualification, GROUP_CONCAT(q.description SEPARATOR '\n') as Qualification_Detail, t.email, t.phone_number
        FROM trainer AS t
        LEFT JOIN role AS r ON t.role_id=r.id 
        LEFT JOIN trainerqualification AS tq ON t.id=tq.trainer_id 
        LEFT JOIN qualification AS q ON tq.qualification_id=q.id 
        WHERE r.id=2
        GROUP BY t.id
        ORDER by t.last_name ASC;

--
SELECT t.id, t.first_name, t.last_name, GROUP_CONCAT(q.name SEPARATOR ', ') as Qualification, GROUP_CONCAT(q.description SEPARATOR '; ') as Qualification_Detail, t.email, t.phone_number
        FROM trainer AS t
        LEFT JOIN role AS r ON t.role_id=r.id 
        LEFT JOIN trainerqualification AS tq ON t.id=tq.trainer_id 
        LEFT JOIN qualification AS q ON tq.qualification_id=q.id 
        WHERE r.id=2 
        AND t.id = 2;

--
SELECT m.id, r.name, m.first_name, m.last_name, m.email, m.password, m.gender, m.date_of_birth, m.phone_number, m.address, m.isactive, 
            MAX(CASE WHEN h.id=1 THEN mh.value ELSE NULL END) AS weight, 
            MAX(CASE WHEN h.id=2 THEN mh.value ELSE NULL END) AS boty_fat_percentage, 
            MAX(CASE WHEN h.id=3 THEN mh.value ELSE NULL END) AS blood_pressure, 
            MAX(CASE WHEN h.id=4 THEN mh.value ELSE NULL END) AS general_comments  
            FROM member AS m
            LEFT JOIN role AS r ON m.role_id=r.id 
            LEFT JOIN memberhealth AS mh ON m.id=mh.member_id 
            LEFT JOIN health AS h ON mh.health_id=h.id 
            WHERE r.id=3
            GROUP BY m.id;
            
--
SELECT m.id, r.name, m.first_name, m.last_name, m.email, m.password, m.gender, m.date_of_birth, m.phone_number, m.address, m.isactive, 
            MAX(CASE WHEN h.id=1 THEN mh.value ELSE NULL END) AS weight, 
            MAX(CASE WHEN h.id=2 THEN mh.value ELSE NULL END) AS boty_fat_percentage, 
            MAX(CASE WHEN h.id=3 THEN mh.value ELSE NULL END) AS blood_pressure, 
            MAX(CASE WHEN h.id=4 THEN mh.value ELSE NULL END) AS general_comments  
            FROM member AS m
            LEFT JOIN role AS r ON m.role_id=r.id 
            LEFT JOIN memberhealth AS mh ON m.id=mh.member_id 
            LEFT JOIN health AS h ON mh.health_id=h.id 
            WHERE r.id=3 AND m.id=2
            GROUP BY m.id;
--
SELECT m.id, m.first_name, m.last_name, a.balance, t.reference, DATE_ADD(a.last_subscription_payment, INTERVAL 30 DAY) AS duedate
            FROM member AS m
            LEFT JOIN account AS a ON m.id=a.member_id
            LEFT JOIN transaction AS t ON a.id=t.account_id
            where m.id=2;

--
SELECT m.id, r.name, m.first_name, m.last_name, m.email, m.password, m.gender, m.date_of_birth, m.phone_number, m.address, m.isactive, 
            MAX(CASE WHEN h.id=1 THEN mh.value ELSE NULL END) AS weight, 
            MAX(CASE WHEN h.id=2 THEN mh.value ELSE NULL END) AS boty_fat_percentage, 
            MAX(CASE WHEN h.id=3 THEN mh.value ELSE NULL END) AS blood_pressure, 
            MAX(CASE WHEN h.id=4 THEN mh.value ELSE NULL END) AS general_comments  
            FROM member AS m
            LEFT JOIN role AS r ON m.role_id=r.id 
            LEFT JOIN memberhealth AS mh ON m.id=mh.member_id 
            LEFT JOIN health AS h ON mh.health_id=h.id 
            WHERE r.id=3 AND m.id LIKE 5
            GROUP BY m.id;
            
--
select m.id, r.name, m.first_name, m.last_name, m.email, m.password, m.gender, m.date_of_birth, m.phone_number, m.address  from member as m 
            left join role as r on m.role_id=r.id 
            Where r.id=3 AND m.email = %s AND m.password = %s;
            
--
SELECT trainer.id AS trainer_id, trainer.first_name, trainer.last_name, schedule.day, schedule.start_time, schedule.end_time, schedule.room, class.name AS class_name 
        FROM trainer JOIN schedule ON schedule.trainer_id = trainer.id JOIN class ON schedule.class_id = class.id 
            WHERE schedule.start_time IS NOT NULL ORDER BY schedule.start_time, schedule.day;
            
--
SELECT schedule.id, schedule.day, schedule.start_time, schedule.end_time, schedule.room 
                FROM schedule 
                WHERE schedule.start_time IS NULL 
                ORDER BY schedule.day, schedule.start_time;



SELECT t.id as trainer_id, t.first_name as trainer_first_name, t.last_name as trainer_last_name, s.class_id, s.room, m.id as trainee_id, m.first_name as trainee_first_name, m.last_name as trainee_last_name, s.start_time, s.end_time, s.day
FROM schedule s
JOIN trainer t ON s.trainer_id = t.id
JOIN validbookingattendance vb on s.id = vb.schedule_id
JOIN member m on m.id = vb.member_id
ORDER BY t.id, s.start_time;



SELECT t.id as trainer_id, t.first_name as trainer_first_name, t.last_name as trainer_last_name, s.class_id, c.description, s.room, m.id as trainee_id, m.first_name as trainee_first_name, m.last_name as trainee_last_name, s.start_time, s.end_time, s.day
FROM schedule s
JOIN trainer t ON s.trainer_id = t.id
JOIN validbookingattendance vb on s.id = vb.schedule_id
JOIN member m on m.id = vb.member_id
join class c on c.id = s.class_id
where c.id = 4 or c.id = 5
ORDER BY t.id, s.start_time;

-- Test Finance Table
SELECT *
FROM datetable AS dt
LEFT JOIN transaction AS t ON dt.date=t.date
LEFT JOIN transactiontype ON transactiontype.id=t.paytype
;

-- Finance Table, non topup transactions
SELECT dt.year, dt.quarter, dt.month, amount, typename
FROM datetable AS dt
LEFT JOIN transaction AS t ON dt.date=t.date
LEFT JOIN transactiontype ON transactiontype.id=t.paytype
WHERE paytype <> 1
;

-- Finance Table, subscription transactions sums up, Group by Quarter
SELECT ANY_VALUE(dt.year), ANY_VALUE(dt.quarter), FORMAT(COALESCE(SUM(amount),0),'C','en-NZ') AS SubscriptionPayment, ANY_VALUE(typename)
FROM datetable AS dt
LEFT JOIN subscriptionpaymenttransaction AS spt ON dt.date=spt.date
LEFT JOIN transactiontype ON transactiontype.id=spt.paytype
WHERE YEAR=2022
GROUP BY dt.quarter
ORDER BY dt.quarter
;

-- Finance Table, subscription transactions sums up, Group by Year
SELECT ANY_VALUE(dt.year), ANY_VALUE(dt.quarter), FORMAT(COALESCE(SUM(amount),0),'C','en-NZ') AS SubscriptionPayment, ANY_VALUE(typename)
FROM datetable AS dt
LEFT JOIN subscriptionpaymenttransaction AS spt ON dt.date=spt.date
LEFT JOIN transactiontype ON transactiontype.id=spt.paytype
WHERE YEAR=2022
GROUP BY dt.year
;

-- Finance Table, subscription transactions sums up, first result in year union with quarter resultes
SELECT ANY_VALUE(dt1.year), 'Q0' AS quarter, FORMAT(COALESCE(SUM(spt1.amount),0),'C','en-NZ') AS SubscriptionPayment, ANY_VALUE(tt1.typename)
FROM datetable AS dt1
LEFT JOIN subscriptionpaymenttransaction AS spt1 ON dt1.date=spt1.date
LEFT JOIN transactiontype AS tt1 ON tt1.id=spt1.paytype
WHERE YEAR=2022
GROUP BY dt1.year
UNION
SELECT ANY_VALUE(dt2.year), ANY_VALUE(dt2.quarter), FORMAT(COALESCE(SUM(spt2.amount),0),'C','en-NZ') AS SubscriptionPayment, ANY_VALUE(tt2.typename)
FROM datetable AS dt2
LEFT JOIN subscriptionpaymenttransaction AS spt2 ON dt2.date=spt2.date
LEFT JOIN transactiontype AS tt2 ON tt2.id=spt2.paytype
WHERE YEAR=2022
GROUP BY dt2.quarter
ORDER BY quarter
;



-- Finance Table, subscription transactions sums up, Group by Month
SELECT ANY_VALUE(dt.year), ANY_VALUE(dt.quarter), ANY_VALUE(dt.month), FORMAT(COALESCE(SUM(amount),0),'C','en-NZ') AS SubscriptionPayment, MAX(typename)
FROM datetable AS dt
LEFT JOIN subscriptionpaymenttransaction AS spt ON dt.date=spt.date
LEFT JOIN transactiontype ON transactiontype.id=spt.paytype
WHERE YEAR=2022
GROUP BY dt.month
ORDER BY dt.month
;

-- Finance Table, session transactions sums up, Group by Quarter
SELECT ANY_VALUE(dt.year), ANY_VALUE(dt.quarter), FORMAT(COALESCE(SUM(amount),0),'C','en-NZ') AS SessionPayment, MAX(typename)
FROM datetable AS dt
LEFT JOIN sessionpaymenttransaction AS spt ON dt.date=spt.date
LEFT JOIN transactiontype ON transactiontype.id=spt.paytype
WHERE YEAR=2022
GROUP BY dt.quarter
ORDER BY dt.quarter
;

-- Finance Table, session transactions sums up, first result in year union with quarter resultes
SELECT ANY_VALUE(dt1.year), 'Q0' AS quarter, FORMAT(COALESCE(SUM(spt1.amount),0),'C','en-NZ') AS SessionPayment, ANY_VALUE(tt1.typename)
FROM datetable AS dt1
LEFT JOIN sessionpaymenttransaction AS spt1 ON dt1.date=spt1.date
LEFT JOIN transactiontype AS tt1 ON tt1.id=spt1.paytype
WHERE YEAR=2022
GROUP BY dt1.year
UNION
SELECT ANY_VALUE(dt2.year), ANY_VALUE(dt2.quarter), FORMAT(COALESCE(SUM(spt2.amount),0),'C','en-NZ') AS SessionPayment, ANY_VALUE(tt2.typename)
FROM datetable AS dt2
LEFT JOIN sessionpaymenttransaction AS spt2 ON dt2.date=spt2.date
LEFT JOIN transactiontype AS tt2 ON tt2.id=spt2.paytype
WHERE YEAR=2022
GROUP BY dt2.quarter
ORDER BY quarter
;

-- Finance Table, session transactions sums up, Group by Month
SELECT ANY_VALUE(dt.year), ANY_VALUE(dt.quarter), ANY_VALUE(dt.month), FORMAT(COALESCE(SUM(amount),0),'C','en-NZ') AS SessionPayment, MAX(typename)
FROM datetable AS dt
LEFT JOIN sessionpaymenttransaction AS spt ON dt.date=spt.date
LEFT JOIN transactiontype ON transactiontype.id=spt.paytype
WHERE YEAR=2022
GROUP BY dt.month
ORDER BY dt.month
;


-- New Member Each Month --
SELECT ANY_VALUE(dt.year), ANY_VALUE(dt.quarter), ANY_VALUE(dt.month), COALESCE(COUNT(m.id),0) AS NewContract
FROM datetable AS dt
LEFT JOIN account as a ON dt.date=a.contract_startdate
LEFT JOIN member as m ON m.id=a.member_id
WHERE YEAR=2022
GROUP BY dt.month
ORDER BY dt.month;


-- New Member Each Quarter --
SELECT ANY_VALUE(dt.year), ANY_VALUE(dt.quarter), COALESCE(COUNT(m.id),0) AS NewContract
FROM datetable AS dt
LEFT JOIN account as a ON dt.date=a.contract_startdate
LEFT JOIN member as m ON m.id=a.member_id
WHERE YEAR=2022
GROUP BY dt.quarter
ORDER BY dt.quarter;

-- New Member Each Year -- first result in year union with quarter resultes
SELECT ANY_VALUE(dt1.year), 'Q0' AS quarter, COALESCE(COUNT(m1.id),0) AS NewContract
FROM datetable AS dt1
LEFT JOIN account as a1 ON dt1.date=a1.contract_startdate
LEFT JOIN member as m1 ON m1.id=a1.member_id
WHERE YEAR=2022
GROUP BY dt1.year
UNION
SELECT ANY_VALUE(dt2.year), ANY_VALUE(dt2.quarter), COALESCE(COUNT(m2.id),0) AS NewContract
FROM datetable AS dt2
LEFT JOIN account as a2 ON dt2.date=a2.contract_startdate
LEFT JOIN member as m2 ON m2.id=a2.member_id
WHERE YEAR=2022
GROUP BY dt2.quarter
ORDER BY quarter;

-- Expired Member Each Month --
SELECT ANY_VALUE(dt.year), ANY_VALUE(dt.quarter), ANY_VALUE(dt.month), COALESCE(COUNT(m.id),0) AS ExpiredContract
FROM datetable AS dt
LEFT JOIN account as a ON dt.date=a.contract_lastdate
LEFT JOIN member as m ON m.id=a.member_id
WHERE YEAR=2022
GROUP BY dt.month
ORDER BY dt.month;

-- Expired Member Each Quarter --
SELECT ANY_VALUE(dt.year), ANY_VALUE(dt.quarter), COALESCE(COUNT(m.id),0) AS ExpiredContract
FROM datetable AS dt
LEFT JOIN account as a ON dt.date=a.contract_lastdate
LEFT JOIN member as m ON m.id=a.member_id
WHERE YEAR=2022
GROUP BY dt.quarter
ORDER BY dt.quarter;

-- Expired Member Each Year -- first result in year union with quarter resultes
SELECT ANY_VALUE(dt1.year), 'Q0' AS quarter, COALESCE(COUNT(m1.id),0) AS ExpiredContract
FROM datetable AS dt1
LEFT JOIN account as a1 ON dt1.date=a1.contract_lastdate
LEFT JOIN member as m1 ON m1.id=a1.member_id
WHERE YEAR=2022
GROUP BY dt1.year
UNION
SELECT ANY_VALUE(dt2.year), ANY_VALUE(dt2.quarter), COALESCE(COUNT(m2.id),0) AS ExpiredContract
FROM datetable AS dt2
LEFT JOIN account as a2 ON dt2.date=a2.contract_lastdate
LEFT JOIN member as m2 ON m2.id=a2.member_id
WHERE YEAR=2022
GROUP BY dt2.quarter
ORDER BY quarter;

-- Finance Table, subscription transactions count, Group by Quarter
SELECT ANY_VALUE(dt.year), ANY_VALUE(dt.quarter), COALESCE(COUNT(amount),0) AS SubscriptionPayment, ANY_VALUE(typename)
FROM datetable AS dt
LEFT JOIN subscriptionpaymenttransaction AS spt ON dt.date=spt.date
LEFT JOIN transactiontype ON transactiontype.id=spt.paytype
WHERE YEAR=2022
GROUP BY dt.quarter
ORDER BY dt.quarter
;

-- Finance Table, subscription transactions count, Group by Month
SELECT ANY_VALUE(dt.year), ANY_VALUE(dt.quarter), ANY_VALUE(dt.month), COALESCE(COUNT(amount),0) AS SubscriptionPayment, MAX(typename)
FROM datetable AS dt
LEFT JOIN subscriptionpaymenttransaction AS spt ON dt.date=spt.date
LEFT JOIN transactiontype ON transactiontype.id=spt.paytype
WHERE YEAR=2022
GROUP BY dt.month
ORDER BY dt.month
;

-- Finance Table, subscription transactions COUNT, first result in year union with quarter resultes
SELECT ANY_VALUE(dt1.year), 'Q0' AS quarter, FORMAT(COALESCE(COUNT(spt1.amount),0),'C','en-NZ') AS SubscriptionPayment, ANY_VALUE(tt1.typename)
FROM datetable AS dt1
LEFT JOIN subscriptionpaymenttransaction AS spt1 ON dt1.date=spt1.date
LEFT JOIN transactiontype AS tt1 ON tt1.id=spt1.paytype
WHERE YEAR=2022
GROUP BY dt1.year
UNION
SELECT ANY_VALUE(dt2.year), ANY_VALUE(dt2.quarter), FORMAT(COALESCE(COUNT(spt2.amount),0),'C','en-NZ') AS SubscriptionPayment, ANY_VALUE(tt2.typename)
FROM datetable AS dt2
LEFT JOIN subscriptionpaymenttransaction AS spt2 ON dt2.date=spt2.date
LEFT JOIN transactiontype AS tt2 ON tt2.id=spt2.paytype
WHERE YEAR=2022
GROUP BY dt2.quarter
ORDER BY quarter
;

-- Finance Table, session transactions Count, first result in year union with quarter resultes
SELECT ANY_VALUE(dt1.year), 'Q0' AS quarter, FORMAT(COALESCE(COUNT(spt1.amount),0),'C','en-NZ') AS SessionPayment, ANY_VALUE(tt1.typename)
FROM datetable AS dt1
LEFT JOIN sessionpaymenttransaction AS spt1 ON dt1.date=spt1.date
LEFT JOIN transactiontype AS tt1 ON tt1.id=spt1.paytype
WHERE YEAR=2022
GROUP BY dt1.year
UNION
SELECT ANY_VALUE(dt2.year), ANY_VALUE(dt2.quarter), FORMAT(COALESCE(COUNT(spt2.amount),0),'C','en-NZ') AS SessionPayment, ANY_VALUE(tt2.typename)
FROM datetable AS dt2
LEFT JOIN sessionpaymenttransaction AS spt2 ON dt2.date=spt2.date
LEFT JOIN transactiontype AS tt2 ON tt2.id=spt2.paytype
WHERE YEAR=2022
GROUP BY dt2.quarter
ORDER BY quarter
;
