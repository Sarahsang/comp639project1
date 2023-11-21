
-- Display all users data with roles (HD)
SELECT u.id, r.name, u.first_name, u.last_name, u.email, u.password, u.gender, u.date_of_birth, u.phone_number, u.address
FROM user AS u 
LEFT JOIN userrole AS ur ON u.id=ur.user_id 
LEFT JOIN role AS r ON ur.role_id=r.id;

-- Users - Admin (HD)
SELECT u.id, r.name, u.first_name, u.last_name, u.email, u.password, u.gender, u.date_of_birth, u.phone_number, u.address 
FROM user AS u 
LEFT JOIN userrole AS ur ON u.id=ur.user_id 
LEFT JOIN role AS r ON ur.role_id=r.id WHERE r.id=1;

-- Users - Trainer (HD)
SELECT u.id, r.name, u.first_name, u.last_name, u.email, u.password, u.gender, u.date_of_birth, u.phone_number, u.address 
FROM user AS u 
LEFT JOIN userrole AS ur ON u.id=ur.user_id 
LEFT JOIN role AS r ON ur.role_id=r.id WHERE r.id=2;

-- Users - Trainer Qualifications (HD)
SELECT u.id, r.name, q.name, q.description, u.first_name, u.last_name, u.email, u.password, u.gender, u.date_of_birth, u.phone_number, u.address 
FROM user AS u 
LEFT JOIN userrole AS ur ON u.id=ur.user_id 
LEFT JOIN role AS r ON ur.role_id=r.id 
LEFT JOIN userqualification AS uq ON u.id=uq.user_id 
LEFT JOIN qualification AS q ON uq.qualification_id=q.id 
WHERE r.id=2;

-- Users - Member (HD)
SELECT u.id, r.name, u.first_name, u.last_name, u.email, u.password, u.gender, u.date_of_birth, u.phone_number, u.address 
FROM user AS u 
LEFT JOIN userrole AS ur ON u.id=ur.user_id 
LEFT JOIN role AS r ON ur.role_id=r.id WHERE r.id=3;

-- Users - Member Health (HD)
SELECT u.id, r.name, u.first_name, u.last_name, u.email, u.password, u.gender, u.date_of_birth, u.phone_number, u.address, 
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
GROUP BY u.id;

-- query to view class timetable (no privates) (BW)
SELECT c.name AS class, u.first_name as trainer, s.day, s.start_time, s.room
FROM class AS c
INNER JOIN schedule AS s on c.id = s.class_id
INNER JOIN user AS u on s.trainer_id = u.id
WHERE c.capacity > 1
;

-- query to view timetable with teacher Amy Ferguson (BW) - see both classes and private bookings (BW)
SELECT c.name AS class, u.first_name AS trainer, s.day, s.start_time, s.room
FROM class AS c
INNER JOIN schedule AS s ON c.id = s.class_id
INNER JOIN user AS u ON s.trainer_id = u.id
WHERE u.first_name = 'Amy'
;

-- query to view attendance by member Hido (BW)
SELECT u.first_name AS attendee, u.last_name AS attendee_surname, c.name AS class, s.day, ba.check_in_time
FROM bookingattendance AS ba 
INNER JOIN user u ON ba.user_id = u.id
INNER JOIN schedule AS s ON ba.schedule_id = s.id
INNER JOIN class AS c ON c.id = s.class_id
WHERE u.first_name = 'Hido'
;

-- query to view attendance by all members (BW)
SELECT u.first_name AS attendee, u.last_name AS attendee_surname, c.name AS class, ba.check_in_time AS day_time_attended
FROM bookingattendance AS ba 
INNER JOIN user AS u ON ba.user_id = u.id
INNER JOIN schedule AS s ON ba.schedule_id = s.id
INNER JOIN class AS c ON c.id = s.class_id
;

-- query to view number of attendees at each class (most popular class) (BW) (Need troubleshoot)
SELECT c.name AS class, s.day, ba.check_in_time, COUNT(user_id) AS attended
FROM bookingattendance AS ba 
INNER JOIN user AS u ON ba.user_id = u.id
INNER JOIN schedule AS s ON ba.schedule_id = s.id
INNER JOIN class AS c ON c.id = s.class_id
WHERE c.capacity > 1
GROUP BY s.id
-- ORDER BY attended
;

-- query to see all money coming into the gym (BW)
SELECT u.first_name AS name, u.last_name AS surname, t.amount AS payment_made, t.reference, t.created_at AS datePaid
FROM transaction AS t
INNER JOIN account a ON a.id = t.Account_id
JOIN user u ON a.user_id = u.id;

-- query to see private only payments (BW)
SELECT u.first_name AS name, u.last_name AS surname, t.amount AS payment_made, t.reference, t.created_at AS datePaid
FROM transaction AS t
INNER JOIN account a ON a.id = t.account_id
JOIN user AS u ON a.user_id = u.id
WHERE t.reference = 'private';


-- Upcoming Group Class by weeks
SELECT *
FROM bookingattendance AS ba
;

-- query to see all classes and sessions scheduled (MS)
SELECT user.first_name, user.last_name, class.name, schedule.day, schedule.start_time, schedule.end_time, schedule.room, role.name
FROM user
JOIN schedule ON user.id = schedule.trainer_id
JOIN class ON schedule.class_id = class.id
JOIN userrole ON user.id = userrole.user_id
JOIN role ON userrole.role_id = role.id
WHERE role.name = 'trainer';

-- Schedule All (HD)
SELECT *
FROM schedule AS s
LEFT JOIN class AS c ON s.class_id=c.id
LEFT JOIN user AS u ON s.trainer_id=u.id
ORDER BY s.start_time
;

-- Class Schedule Only Personal Training Session(HD)
SELECT *
FROM schedule AS s
LEFT JOIN class AS c ON s.class_id=c.id
LEFT JOIN user AS u ON s.trainer_id=u.id
WHERE c.capacity=1
ORDER BY s.start_time
;

-- Class Schedule Only Group Class (HD)
SELECT *
FROM schedule AS s
LEFT JOIN class AS c ON s.class_id=c.id
LEFT JOIN user AS u ON s.trainer_id=u.id
WHERE c.capacity>1
ORDER BY s.start_time
;

-- GROUP Class Schedule with BOOKING TO CAPACITY (HD)
SELECT s.id, s.class_id, s.trainer_id, s.day, s.start_time, s.end_time, s.room, c.name, c.description, c.capacity, u.first_name, u.last_name, 
COUNT(ba.id) AS Booked, CONCAT(COUNT(ba.id),"/",c.capacity) AS BOOKED_CAPACITY
FROM schedule AS s
LEFT JOIN class AS c ON s.class_id=c.id
LEFT JOIN user AS u ON s.trainer_id=u.id
LEFT JOIN bookingattendance AS ba ON s.id=ba.schedule_id
WHERE ba.cancelled=0 AND c.capacity>1
GROUP BY s.id
ORDER BY s.start_time
;

-- query to see all trainers and their qualification (MS)
SELECT u.first_name, u.last_name, uq.qualification_id, q.name, q.description FROM user u 
JOIN userrole ur ON u.id=ur.user_id
left join userqualification uq on u.id = uq.user_id
left join qualification q on uq.qualification_id = q.id
WHERE ur.role_id = 2;

-- query to see class at a particular time (MS)
SELECT schedule.id, class.name, schedule.room, schedule.start_time, schedule.end_time,
                user.first_name, user.last_name
                FROM schedule
                LEFT JOIN bookingattendance ON bookingattendance.schedule_id = schedule.id
                LEFT JOIN class ON class.id = schedule.class_id
                LEFT JOIN user ON user.id = schedule.trainer_id
                WHERE schedule.start_time BETWEEN '2023-03-13 09:00:00' AND '2023-03-13 10:00:00'
                ORDER BY schedule.start_time;


-- create view for trainer to view personal sessions for each member (MS)
CREATE VIEW bookings_by_trainer AS
SELECT t.id as trainer_id, t.first_name as trainer_first_name, t.last_name as trainer_last_name, s.class_id, s.room, m.id as trainee_id, m.first_name as trainee_first_name, m.last_name as trainee_last_name, s.start_time, s.end_time, s.day
FROM schedule s
JOIN trainer t ON s.trainer_id = t.id
JOIN validbookingattendance vb on s.id = vb.schedule_id
JOIN member m on m.id = vb.user_id
ORDER BY t.id, s.start_time;


-- create view for trainer to view personal sessions for each member (MS)
CREATE VIEW bookings_by_trainer AS
SELECT t.id as trainer_id, t.first_name as trainer_first_name, t.last_name as trainer_last_name, s.class_id, s.room, m.id as trainee_id, m.first_name as trainee_first_name, m.last_name as trainee_last_name, s.start_time, s.end_time, s.day
FROM schedule s
JOIN trainer t ON s.trainer_id = t.id
JOIN validbookingattendance vb on s.id = vb.schedule_id
JOIN member m on m.id = vb.user_id
ORDER BY t.id, s.start_time;
