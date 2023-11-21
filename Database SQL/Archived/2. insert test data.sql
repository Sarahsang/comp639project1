

-- 1. User table seed data
INSERT INTO user (id, first_name, last_name, email, password, gender, date_of_birth, phone_number, address, isactive, notes) VALUES
(1, 'Hido', 'Dai', 'hidodai@example.com', 'password123', 'Male', '1990-01-01', '1234567890', '123 St Heliers Bay Rd, St Heliers', 1, null),
(2, 'Miao', 'Sang', 'miaosang@example.com', 'password456', 'Female', '1995-01-01', '1234567890', '456 Kohimarama Rd, Mission Bay', 1, null),
(3, 'Elizabeth', 'Venz', 'elizabethvenz@example.com', 'password789', 'Female', '1985-01-01', '1234567890', '789 Antigua St, Addington', 1, null),
(4, 'Penelope', 'Sole', 'penelopesole@example.com', 'password321', 'Female', '1979-10-11', '027-3257980', '123 Main St, Lincoln', 1, null),
(5, 'Amy', 'Ferguson', 'amyferg@example.com', 'password987', 'Female', '1985-08-11', '021-3254567', '789 Third St, Lincoln', 1, null),
(6, 'John', 'Doe', 'johndoe@example.com', 'password123', 'Male', '1990-01-01', '555-1234', '123 Main St', 1, null),
(7, 'Jane', 'Doe', 'janedoe@example.com', 'password456', 'Female', '1992-02-02', '555-5678', '456 Oak St', 1, null),
(8, 'Bob', 'Smith', 'bobsmith@example.com', 'password789', 'Male', '1985-03-03', '555-2468', '789 Maple Ave', 1, null),
(9, 'Mary', 'Johnson', 'maryj@example.com', 'password123', 'Female', '1991-04-04', '555-7890', '456 Elm St', 1, null),
(10, 'Alex', 'Brown', 'alexb@example.com', 'password456', 'Male', '1993-05-05', '555-2345', '789 Oak St', 1, null),
(11, 'Linda', 'Davis', 'lindad@example.com', 'password789', 'Female', '1987-06-06', '555-6789', '123 Maple Ave', 1, null),
(12, 'Dave', 'Wilson', 'davew@example.com', 'password123', 'Male', '1992-07-07', '555-3456', '456 Elm St', 1, null),
(13, 'Emily', 'Moore', 'emilym@example.com', 'password456', 'Female', '1990-08-08', '555-7890', '789 Oak St', 1, null),
(14, 'Tom', 'Taylor', 'tomt@example.com', 'password789', 'Male', '1988-09-09', '555-2345', '123 Maple Ave', 1, null),
(15, 'Rachel', 'Clark', 'rachelc@example.com', 'password123', 'Female', '1994-10-10', '555-6789', '456 Elm St', 1, null),
(16, 'Steven', 'Lee', 'stevenl@example.com', 'password456', 'Male', '1986-11-11', '555-3456', '789 Oak St', 1, null),
(17, 'Samantha', 'Garcia', 'samanthag@example.com', 'password789', 'Female', '1995-12-12', '555-1234', '123 Main St', 1, null),
(18, 'Michael', 'Jones', 'michaelj@example.com', 'password123', 'Male', '1989-01-13', '555-5678', '456 Oak St', 1, null),
(19, 'Laura', 'Martin', 'lauram@example.com', 'password456', 'Female', '1993-02-14', '555-2468', '789 Maple Ave', 1, null),
(20, 'Brian', 'Wilson', 'brianw@example.com', 'password789', 'Male', '1985-03-15', '555-1234', '123 Main St', 1, null),
(21, 'Stephanie', 'Taylor', 'stephaniet@example.com', 'password123', 'Female', '1992-04-16', '555-5678', '456 Oak St', 1, null),
(22, 'David', 'Clark', 'davidc@example.com', 'password456', 'Male', '1986-05-17', '555-2468', '789 Maple Ave', 1, null)
;

-- 2. Role table seed data
INSERT INTO role (name, description) VALUES
('Admin_Manager', 'Manager, Receptionist and General Administration staff'),
('Trainer', 'Instructors and trainers'),
('Member', 'All subscribed users and members')
;

-- 3. UserRole table seed data
INSERT INTO userrole (user_id, role_id) VALUES
(1, 3), -- Hido is a member
(2, 3), -- Miao is a member
(3, 1), -- Elizabeth is a manager
(1, 2), -- Hido is also a trainer
(4, 2), -- Penelope is a trainer
(5, 2), -- Amy is a trainer
(6, 3), -- the rest are members only
(7, 3),
(8, 3),
(9, 3),
(10, 3),
(11, 3),
(12, 3),
(13, 3),
(14, 3),
(15, 3),
(16, 3),
(17, 3),
(18, 3),
(19, 3),
(20, 3),
(21, 3),
(22, 3);


-- 4. Account table seed data
INSERT INTO account (user_id, balance, last_subscription_payment, contract_startdate, contract_lastdate) VALUES
(1, 100, '2023-02-28 10:00:00', '2022-03-31', '2023-03-31'),
(2, 0, '2023-02-28 10:00:00', '2022-04-30', '2023-04-30'), -- Miao is at zero balance so needs to topup/reminder email
(3, 0,null, null, null),
(4, 0,null, null, null), -- Penelope is a trainer so we dont need to bother her
(5, 0,null, null, null), -- Amy is a trainer so not worried about her balance either
(6, -120, '2023-02-28 10:00:00', '2022-08-28', '2023-08-28'), -- John Doe is in negative balance so needs to topup/reminder email
(7, 100, '2023-02-28 10:00:00', '2022-09-27', '2023-09-27'),
(8, 0, '2023-02-28 10:00:00', '2022-10-27', '2023-10-27'),
(9, 60, '2023-02-28 10:00:00', '2022-11-26', '2023-11-26'),
(10, 0, '2023-02-28 10:00:00', '2022-12-26', '2023-12-26'),
(11, 200, '2023-02-28 10:00:00', '2023-01-25', '2024-01-25'),
(12, 132, '2023-02-28 10:00:00', '2023-02-24', '2024-02-24'),
(13, 152, '2023-02-28 10:00:00', '2023-03-26', '2024-03-25'),
(14, 172, '2023-02-28 10:00:00', '2023-04-25', '2024-04-24'),
(15, 192, '2023-02-28 10:00:00', '2023-05-25', '2024-05-24'),
(16, 212, '2023-02-28 10:00:00', '2023-06-24', '2024-06-23'),
(17, 232, '2023-02-28 10:00:00', '2023-07-24', '2024-07-23'),
(18, 252, '2023-02-28 10:00:00', '2023-08-23', '2024-08-22'),
(19, 272, '2023-02-28 10:00:00', '2023-09-22', '2024-09-21'),
(20, 292, '2023-02-28 10:00:00', '2023-10-22', '2024-10-21'),
(21, 312, '2023-02-28 10:00:00', '2023-11-21', '2024-11-20'),
(22, 332, '2023-02-28 10:00:00', '2023-12-21', '2024-12-20')
;


-- 5. Health table seed data
INSERT INTO health (name, description) VALUES
('Weight', 'The weight of the user in kilograms'),
('Body Fat Percentage', 'The percentage of body fat in the user''s body'),
('Blood Pressure', 'The systolic and diastolic blood pressure values of the user'),
('General Comments', 'Allergies eg asthma, coeliac')
;

-- 6. UserHealth table seed data
INSERT INTO userhealth (user_id, health_id, value, date) VALUES
(1, 1, '75.5', '2023-02-15'),
(1, 2, '22.0', '2023-02-15'),
(1, 3, '120/80', '2023-02-15'),
(1, 4, 'no allergies', '2023-02-15'),
(2, 1, '68.2', '2023-02-15'),
(2, 2, '18.5', '2023-02-15'),
(2, 3, '130/85', '2023-02-15'),
(2, 4, 'asthmatic', '2023-02-15'),
(3, 1, '90.0', '2023-02-15'),
(3, 2, '25.0', '2023-02-15'),
(3, 3, '120/75', '2023-02-15'),
(3, 4, 'coeliac', '2023-02-15')
;

-- 7. Qualification table seed data
INSERT INTO qualification (name, description) VALUES
('Certified Personal Trainer', 'Qualified to create and implement individualized exercise programs for clients'),
('Group Fitness Instructor', 'Qualified to lead group exercise classes in a variety of formats'),
('Gym Manager', 'Qualified in management'),
('Les Mills Instructor', 'Qualified to teach Les Mills classes'),
('YMCA certified group Instructor', 'YMCA qualified to lead group exercise classes'),
('NetFit Coach', 'Qualified as a NetFitNZ Personal Trainer');

-- 8. UserQualification table seed data
INSERT INTO userqualification (user_id, qualification_id) VALUES
(1, 4), -- Hido has a Les Mills qualification
(4, 1), -- Penelope has 4 different quals
(4, 2),
(4, 4),
(4, 5),
(3, 3), -- Elizabeth has a management degree
(5, 1), -- Amy has 4 qualifications
(5, 2),
(5, 4),
(5, 5)
;

-- 9. Class table seed data
INSERT INTO class (name, description, capacity) VALUES
('Yoga', 'Yoga is the perfect class for stretching and strengthening your entire body.', 30),
('RPM', 'RPM is a 60-minute group indoor cycling workout where you control the intensity', 30),
('BODYATTACK', 'BODYATTACK is a 60-minute high-energy fitness class with moves that cater for total beginners to total addicts.', 30), -- classes are max 30 people
('Private Session with Penelope', 'Private session  with Penny Sole is the perfect way to get maximum benefit for not only your body but your mind as well.', 1),
('Private Session with Amy', 'Private session  with Amy Ferguson is the best way to get maximum benefit out of your workout.', 1), -- privates are max 1 person
('Gym Session', 'A gym session is where you do you - either do the workout you planned with your trainer, or your own choice of workout.', -1) -- general gym attendance has no limit
;

-- 10. Schedule seed data
INSERT INTO schedule (class_id, trainer_id, day, start_time, end_time, room) VALUES
(1, 4, 'Monday', '2023-03-13 09:00:00', '2023-03-13 10:00:00', 'Studio 1'),
(3, 5, 'Tuesday', '2023-03-14 12:00:00', '2023-03-14 13:00:00', 'Studio 2'),
(4, 4, 'Wednesday', '2023-03-15 06:00:00', '2023-03-15 07:00:00', 'Main Gym'), -- Hido has a private with Penelope at this time - see bookingattendance for details
(2, 4, 'Thursday', '2023-03-16 12:00:00', '2023-03-16 13:00:00', 'Cycle Studio'),
(5, 5, 'Friday', '2023-03-17 07:00:00', '2023-03-17 08:00:00', 'Main Gym'), -- Miao is booked with Amy at this time 
(6, null, 'Any day gym', null, null, 'Main Gym'), -- this is the schedule (id 7) that will log for anyone who just scans into the main gym
(1, 4, 'Tuesday', '2023-03-14 09:00:00', '2023-03-14 10:00:00', 'Studio 1'),
(1, 4, 'Wednesday', '2023-03-15 09:00:00', '2023-03-15 10:00:00', 'Studio 1'),
(1, 4, 'Thursday', '2023-03-16 09:00:00', '2023-03-16 10:00:00', 'Studio 1'),
(1, 4, 'Friday', '2023-03-17 09:00:00', '2023-03-17 10:00:00', 'Studio 1'),
(3, 5, 'Monday', '2023-03-13 12:00:00', '2023-03-13 13:00:00', 'Studio 2'),
(3, 5, 'Wednesday', '2023-03-15 12:00:00', '2023-03-15 13:00:00', 'Studio 2'),
(3, 5, 'Thursday', '2023-03-16 12:00:00', '2023-03-16 13:00:00', 'Studio 2'),
(3, 5, 'Friday', '2023-03-17 12:00:00', '2023-03-17 13:00:00', 'Studio 2'),
(1, 4, 'Monday', '2023-03-20 09:00:00', '2023-03-20 10:00:00', 'Studio 1'),
(1, 4, 'Tuesday', '2023-03-21 09:00:00', '2023-03-21 10:00:00', 'Studio 1'),
(1, 4, 'Wednesday', '2023-03-22 09:00:00', '2023-03-22 10:00:00', 'Studio 1'),
(1, 1, 'Thursday', '2023-03-23 09:00:00', '2023-03-23 10:00:00', 'Studio 1'),
(1, 4, 'Friday', '2023-03-24 09:00:00', '2023-03-24 10:00:00', 'Studio 1'),
(3, 5, 'Monday', '2023-03-20 12:00:00', '2023-03-20 13:00:00', 'Studio 2'),
(3, 5, 'Tuesday', '2023-03-21 12:00:00', '2023-03-21 13:00:00', 'Studio 2'),
(3, 1, 'Wednesday', '2023-03-22 12:00:00', '2023-03-22 13:00:00', 'Studio 2'),
(3, 5, 'Thursday', '2023-03-23 12:00:00', '2023-03-23 13:00:00', 'Studio 2'),
(3, 5, 'Friday', '2023-03-24 12:00:00', '2023-03-24 13:00:00', 'Studio 2'),
(4, 4, 'Wednesday', '2023-03-22 06:00:00', '2023-03-22 07:00:00', 'Main Gym'), -- Hido has a private with Penelope at this time - see bookingattendance for details
(2, 4, 'Thursday', '2023-03-23 12:00:00', '2023-03-23 13:00:00', 'Cycle Studio'),
(5, 5, 'Friday', '2023-03-24 07:00:00', '2023-03-24 08:00:00', 'Main Gym'), -- Miao is booked with Amy at this time 
(1, 4, 'Tuesday', '2023-03-07 09:00:00', '2023-03-07 10:00:00', 'Studio 1'),
(1, 4, 'Wednesday', '2023-03-08 09:00:00', '2023-03-08 10:00:00', 'Studio 1'),
(1, 4, 'Thursday', '2023-03-09 09:00:00', '2023-03-09 10:00:00', 'Studio 1'),
(1, 4, 'Friday', '2023-03-10 09:00:00', '2023-03-10 10:00:00', 'Studio 1'),
(3, 5, 'Monday', '2023-03-06 12:00:00', '2023-03-06 13:00:00', 'Studio 2'),
(3, 5, 'Wednesday', '2023-03-08 12:00:00', '2023-03-08 13:00:00', 'Studio 2'),
(3, 5, 'Thursday', '2023-03-09 12:00:00', '2023-03-09 13:00:00', 'Studio 2'),
(3, 5, 'Friday', '2023-03-10 12:00:00', '2023-03-10 13:00:00', 'Studio 2'),
(1, 4, 'Monday', '2023-03-27 09:00:00', '2023-03-27 10:00:00', 'Studio 1'),
(1, 4, 'Tuesday', '2023-03-28 09:00:00', '2023-03-28 10:00:00', 'Studio 1'),
(1, 4, 'Wednesday', '2023-03-29 09:00:00', '2023-03-29 10:00:00', 'Studio 1'),
(1, 4, 'Thursday', '2023-03-30 09:00:00', '2023-03-30 10:00:00', 'Studio 1'),
(1, 4, 'Friday', '2023-03-31 09:00:00', '2023-03-31 10:00:00', 'Studio 1'),
(3, 5, 'Monday', '2023-03-27 12:00:00', '2023-03-27 13:00:00', 'Studio 2'),
(3, 5, 'Tuesday', '2023-03-28 12:00:00', '2023-03-28 13:00:00', 'Studio 2'),
(3, 5, 'Wednesday', '2023-03-29 12:00:00', '2023-03-29 13:00:00', 'Studio 2'),
(3, 5, 'Thursday', '2023-03-30 12:00:00', '2023-03-30 13:00:00', 'Studio 2'),
(3, 5, 'Friday', '2023-03-31 12:00:00', '2023-03-31 13:00:00', 'Studio 2'),
(4, 4, 'Wednesday', '2023-03-29 06:00:00', '2023-03-29 07:00:00', 'Main Gym'), -- Hido has a private with Penelope at this time - see bookingattendance for details
(2, 4, 'Thursday', '2023-03-30 12:00:00', '2023-03-30 13:00:00', 'Cycle Studio'),
(5, 5, 'Friday', '2023-03-31 07:00:00', '2023-03-31 08:00:00', 'Main Gym'), -- Miao is booked with Amy at this time 
(4,4,'Monday','2023-03-13 11:00:00','2023-03-13 12:00:00','Main Gym'),
(5,5,'Monday','2023-03-13 14:00:00','2023-03-13 15:00:00','Main Gym'),
(4,4,'Tuesday','2023-03-14 07:00:00','2023-03-14 08:00:00','Main Gym'),
(5,5,'Tuesday','2023-03-14 15:00:00','2023-03-14 16:00:00','Main Gym'),
(5,5,'Wednesday','2023-03-15 07:00:00','2023-03-15 08:00:00','Main Gym'),
(4,4,'Wednesday','2023-03-15 14:00:00','2023-03-15 15:00:00','Main Gym'),
(5,5,'Thursday','2023-03-16 06:00:00','2023-03-16 07:00:00','Main Gym'),
(4,4,'Thursday','2023-03-16 07:00:00','2023-03-16 08:00:00','Main Gym'),
(5,5,'Thursday','2023-03-16 14:00:00','2023-03-16 15:00:00','Main Gym'),
(4,4,'Friday','2023-03-17 06:00:00','2023-03-17 07:00:00','Main Gym'),
(5,5,'Friday','2023-03-17 10:00:00','2023-03-17 11:00:00','Main Gym'),
(4,4,'Friday','2023-03-17 15:00:00','2023-03-17 16:00:00','Main Gym'),
(4,4,'Monday','2023-03-20 11:00:00','2023-03-20 12:00:00','Main Gym'),
(5,5,'Monday','2023-03-20 14:00:00','2023-03-20 15:00:00','Main Gym'),
(4,4,'Tuesday','2023-03-21 07:00:00','2023-03-21 08:00:00','Main Gym'),
(5,5,'Tuesday','2023-03-21 15:00:00','2023-03-21 16:00:00','Main Gym'),
(5,5,'Wednesday','2023-03-22 07:00:00','2023-03-22 08:00:00','Main Gym'),
(4,4,'Wednesday','2023-03-22 14:00:00','2023-03-22 15:00:00','Main Gym'),
(5,5,'Thursday','2023-03-23 06:00:00','2023-03-23 07:00:00','Main Gym'),
(4,4,'Thursday','2023-03-23 07:00:00','2023-03-23 08:00:00','Main Gym'),
(5,5,'Thursday','2023-03-23 14:00:00','2023-03-23 15:00:00','Main Gym'),
(4,4,'Friday','2023-03-24 06:00:00','2023-03-24 07:00:00','Main Gym'),
(5,5,'Friday','2023-03-24 10:00:00','2023-03-24 11:00:00','Main Gym'),
(4,4,'Friday','2023-03-24 15:00:00','2023-03-24 16:00:00','Main Gym'),
(4,4,'Monday','2023-03-27 11:00:00','2023-03-27 12:00:00','Main Gym'),
(5,5,'Monday','2023-03-27 14:00:00','2023-03-27 15:00:00','Main Gym'),
(4,4,'Tuesday','2023-03-28 07:00:00','2023-03-28 08:00:00','Main Gym'),
(5,5,'Tuesday','2023-03-28 15:00:00','2023-03-28 16:00:00','Main Gym'),
(5,5,'Wednesday','2023-03-29 07:00:00','2023-03-29 08:00:00','Main Gym'),
(4,4,'Wednesday','2023-03-29 14:00:00','2023-03-29 15:00:00','Main Gym'),
(5,5,'Thursday','2023-03-30 06:00:00','2023-03-30 07:00:00','Main Gym'),
(4,4,'Thursday','2023-03-30 07:00:00','2023-03-30 08:00:00','Main Gym'),
(5,5,'Thursday','2023-03-30 14:00:00','2023-03-30 15:00:00','Main Gym'),
(4,4,'Friday','2023-03-31 06:00:00','2023-03-31 07:00:00','Main Gym'),
(5,5,'Friday','2023-03-31 10:00:00','2023-03-31 11:00:00','Main Gym'),
(4,4,'Friday','2023-03-31 15:00:00','2023-03-31 16:00:00','Main Gym')

;

-- 11. BookingAttendance table seed data
INSERT INTO bookingattendance (schedule_id, user_id) VALUES
(1, 1),
(1, 2),
(1, 3),
(2, 1),
(2, 2),
(3, 1), -- this is Penelopes private with Hido
(5, 2), -- this is Amys private with Miao
(6, 3), -- the following are the attendees to Hidos RPM class on Saturday 
(6, 2),
(6, 4),
(6, 5),
(7, 6), -- open gym attendance by John Doe who is in negative balance
(4, 2), -- Miao goes to the RPM class 
(4, 3) -- Elizabeth goes to the RPM class 
;

-- 12. Transaction table seed data
INSERT INTO transaction (account_id, amount, BookingAttendance_id, reference) VALUES
(1, 200, null, 'topup'), -- Hido manually put money in to his account so he could book some private sessions later
(2, 200, null, 'monthlyAP'), -- Miao's automatice payment came through - not for class
(1, 60, 6, 'private'), -- Hido having a private session with Penelope and paying $60 for it
(2, 60, 7, 'private') -- Miao having a private session with Amy and paying $60 for it
;

-- 13. weeklytimetable table seed data
INSERT INTO weeklytimetable (id, tableday, tabletime) VALUES
(1,'Monday','06:00:00'),
(2,'Tuesday','06:00:00'),
(3,'Wednesday','06:00:00'),
(4,'Thursday','06:00:00'),
(5,'Friday','06:00:00'),
(6,'Monday','07:00:00'),
(7,'Tuesday','07:00:00'),
(8,'Wednesday','07:00:00'),
(9,'Thursday','07:00:00'),
(10,'Friday','07:00:00'),
(11,'Monday','08:00:00'),
(12,'Tuesday','08:00:00'),
(13,'Wednesday','08:00:00'),
(14,'Thursday','08:00:00'),
(15,'Friday','08:00:00'),
(16,'Monday','09:00:00'),
(17,'Tuesday','09:00:00'),
(18,'Wednesday','09:00:00'),
(19,'Thursday','09:00:00'),
(20,'Friday','09:00:00'),
(21,'Monday','10:00:00'),
(22,'Tuesday','10:00:00'),
(23,'Wednesday','10:00:00'),
(24,'Thursday','10:00:00'),
(25,'Friday','10:00:00'),
(26,'Monday','11:00:00'),
(27,'Tuesday','11:00:00'),
(28,'Wednesday','11:00:00'),
(29,'Thursday','11:00:00'),
(30,'Friday','11:00:00'),
(31,'Monday','12:00:00'),
(32,'Tuesday','12:00:00'),
(33,'Wednesday','12:00:00'),
(34,'Thursday','12:00:00'),
(35,'Friday','12:00:00'),
(36,'Monday','13:00:00'),
(37,'Tuesday','13:00:00'),
(38,'Wednesday','13:00:00'),
(39,'Thursday','13:00:00'),
(40,'Friday','13:00:00'),
(41,'Monday','14:00:00'),
(42,'Tuesday','14:00:00'),
(43,'Wednesday','14:00:00'),
(44,'Thursday','14:00:00'),
(45,'Friday','14:00:00'),
(46,'Monday','15:00:00'),
(47,'Tuesday','15:00:00'),
(48,'Wednesday','15:00:00'),
(49,'Thursday','15:00:00'),
(50,'Friday','15:00:00'),
(51,'Monday','16:00:00'),
(52,'Tuesday','16:00:00'),
(53,'Wednesday','16:00:00'),
(54,'Thursday','16:00:00'),
(55,'Friday','16:00:00'),
(56,'Monday','17:00:00'),
(57,'Tuesday','17:00:00'),
(58,'Wednesday','17:00:00'),
(59,'Thursday','17:00:00'),
(60,'Friday','17:00:00'),
(61,'Monday','18:00:00'),
(62,'Tuesday','18:00:00'),
(63,'Wednesday','18:00:00'),
(64,'Thursday','18:00:00'),
(65,'Friday','18:00:00')
;

-- 14. add cancel records
INSERT INTO transaction (account_id, amount, paytype, BookingAttendance_id, reference, date, time) VALUES
(30, 60, 6,  null, "sessionrefund", "2023-3-14", "10:00:00"),
(15, 60, 6,  null, "sessionrefund", "2023-3-15", "12:00:00"),
(32, 60, 6,  null, "sessionrefund", "2023-3-16", "08:00:00"),
(7, 60, 6,  null, "sessionrefund", "2023-3-18", "12:00:00"),
(3, 60, 6,  null, "sessionrefund", "2023-3-18", "10:00:00"),
(14, 60, 6,  null, "sessionrefund", "2023-3-18", "09:00:00")
;




