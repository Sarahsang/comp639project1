-- query to view class timetable (no privates) (BW)
select c.name as class, u.first_name as trainer, s.day, s.start_time, s.room
FROM class c
INNER JOIN schedule s on c.id = s.class_id
INNER JOIN user u on s.trainer_id = u.id
WHERE c.capacity > 1
;

-- query to view timetable with teacher Amy Ferguson (BW) - see both classes and private bookings
select c.name as class, u.first_name as trainer, s.day, s.start_time, s.room
FROM class c
INNER JOIN schedule s on c.id = s.class_id
INNER JOIN user u on s.trainer_id = u.id
WHERE u.first_name = 'Amy'
;

-- query to view attendance by member Hido (BW)
select u.first_name as attendee, u.last_name as attendee_surname, c.name as class, s.day, ba.check_in_time
FROM BookingAttendance ba 
INNER JOIN user u on ba.user_id = u.id
INNER JOIN schedule s on ba.schedule_id = s.id
INNER JOIN class c on c.id = s.class_id
WHERE u.first_name = 'Hido'
;

-- query to view attendance by all members (BW)
select u.first_name as attendee, u.last_name as attendee_surname, c.name as class, ba.check_in_time as day_time_attended
FROM BookingAttendance ba 
INNER JOIN user u on ba.user_id = u.id
INNER JOIN schedule s on ba.schedule_id = s.id
INNER JOIN class c on c.id = s.class_id
;

-- query to view number of attendees at each class (most popular class) (BW)
select c.name as class, s.day, ba.check_in_time, count(user_id) as attended
FROM BookingAttendance ba 
INNER JOIN user u on ba.user_id = u.id
INNER JOIN schedule s on ba.schedule_id = s.id
INNER JOIN class c on c.id = s.class_id
where c.capacity > 1
group by s.id
order by count(user_id)
;

-- query to see all money coming into the gym (BW)
select u.first_name as name, u.last_name as surname, t.amount as payment_made, t.reference, t.created_at as datePaid
from transaction t
inner join account a on a.id = t.account_id
join user u on a.user_id = u.id;

-- query to see private only payments (BW)
select u.first_name as name, u.last_name as surname, t.amount as payment_made, t.reference, t.created_at as datePaid
from transaction t
inner join account a on a.id = t.account_id
join user u on a.user_id = u.id
where t.reference = 'private';


-- Users - Member Health (HD)
select u.id, r.name, u.first_name, u.last_name, u.email, u.password, u.gender, u.date_of_birth, u.phone_number, u.address, max(case when h.id=1 then uh.value else null end) as weight, 
max(case when h.id=2 then uh.value else null end) as body_fat_percentage, max(case when h.id=3 then uh.value else null end) as blood_pressure, 
max(case when h.id=4 then uh.value else null end) as general_comments from user as u 
left join userrole on u.id=userrole.user_id 
left join role as r on userrole.role_id=r.id 
left join userhealth as uh on u.id=uh.user_id 
left join health as h on uh.health_id=h.id 
Where r.id=3 
group by u.id;

-- All users - Select All (HD)
select u.id, r.name, u.first_name, u.last_name, u.email, u.password, u.gender, u.date_of_birth, u.phone_number, u.address, u.isactive 
from user as u 
left join userrole ur 
on u.id=ur.user_id 
left join role as r 
on ur.role_id=r.id;

-- Users - Select Members (HD)
select u.id, r.name, u.first_name, u.last_name, u.email, u.password, u.gender, u.date_of_birth, u.phone_number, u.address 
from user as u 
left join userrole ur
on u.id=ur.user_id 
left join role as r 
on ur.role_id=r.id 
Where r.id=3;

-- Users - Select Admin/Managers (HD)
select u.id, r.name, u.first_name, u.last_name, u.email, u.password, u.gender, u.date_of_birth, u.phone_number, u.address 
from user as u 
left join userrole ur 
on u.id=ur.user_id 
left join role as r 
on ur.role_id=r.id 
Where r.id=1;

-- Users - Select Trainers (HD)
select u.id, r.name, u.first_name, u.last_name, u.email, u.password, u.gender, u.date_of_birth, u.phone_number, u.address 
from user as u 
left join userrole ur 
on u.id=ur.user_id 
left join role as r on ur.role_id=r.id 
Where r.id=2;

-- Users - Select Trainer Qualifications (HD)
select u.id, r.name, q.name, q.description, u.first_name, u.last_name, u.email, u.password, u.gender, u.date_of_birth, u.phone_number, u.address 
from user as u 
left join userrole ur on u.id=ur.user_id 
left join role as r on ur.role_id=r.id 
left join userqualification as uq on u.id=uq.user_id 
left join qualification as q on uq.qualification_id=q.id 
Where r.id=2;


