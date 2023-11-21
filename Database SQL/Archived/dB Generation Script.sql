drop database gym_management;
create database gym_management;
use gym_management;
CREATE TABLE User (
  id INT NOT NULL AUTO_INCREMENT,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  gender ENUM('Male', 'Female', 'Other') NOT NULL,
  date_of_birth DATE NOT NULL,
  phone_number VARCHAR(20) NOT NULL,
  address VARCHAR(255) NOT NULL,
  isactive boolean default(TRUE),
  notes VARCHAR(255) NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);
CREATE TABLE Role (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  description VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);

CREATE TABLE UserRole (
  user_id INT NOT NULL,
  role_id INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES User(id),
  FOREIGN KEY (role_id) REFERENCES Role(id),
  PRIMARY KEY (user_id, role_id)
);
CREATE TABLE Qualification (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  description VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);

CREATE TABLE UserQualification (
  user_id INT NOT NULL,
  qualification_id INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES User(id),
  FOREIGN KEY (qualification_id) REFERENCES Qualification(id),
  PRIMARY KEY (user_id, qualification_id)
);
CREATE TABLE Class (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  description VARCHAR(255) NOT NULL,
  capacity INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);

CREATE TABLE schedule (
	id INT NOT NULL AUTO_INCREMENT, 
    class_id INT NOT NULL,
    trainer_id INT NULL,
    day VARCHAR(55) NOT NULL,
    start_time TIME NULL,
    end_time TIME NULL,
    room VARCHAR(50) NOT NULL,
    FOREIGN KEY (class_id) REFERENCES Class(id),
	FOREIGN KEY (trainer_id) REFERENCES User(id),
	PRIMARY KEY (id)
);

CREATE TABLE BookingAttendance (
  id INT NOT NULL AUTO_INCREMENT,
  schedule_id INT NOT NULL,
  user_id INT NOT NULL,
  check_in_time DATETIME NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (schedule_id) REFERENCES schedule(id),
  FOREIGN KEY (user_id) REFERENCES User(id),
  PRIMARY KEY (id)
);

CREATE TABLE account (
  id INT NOT NULL AUTO_INCREMENT,
  user_id INT NOT NULL,
  balance INT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES User(id),
  PRIMARY KEY (id)
);

CREATE TABLE transaction (
  id INT NOT NULL AUTO_INCREMENT,
  account_id INT NOT NULL,
  amount INT NOT NULL,
  BookingAttendance_id INT NULL,
  reference NVARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (account_id) REFERENCES account(id),
  FOREIGN KEY (BookingAttendance_id) REFERENCES BookingAttendance(id),
  PRIMARY KEY (id)
);

-- User table seed data
INSERT INTO User (id, first_name, last_name, email, password, gender, date_of_birth, phone_number, address, isactive, notes) VALUES
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

-- Role table seed data
INSERT INTO role (name, description) VALUES
('Admin_Manager', 'Manager, Receptionist and General Administration staff'),
('Trainer', 'Instructors and trainers'),
('Member', 'All subscribed users and members');

-- userrole table seed data
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
(22, 3)
;

-- Qualification table seed data
INSERT INTO Qualification (name, description) VALUES
('Certified Personal Trainer', 'Qualified to create and implement individualized exercise programs for clients.'),
('Group Fitness Instructor', 'Qualified to lead group exercise classes in a variety of formats.'),
('Gym Manager', 'Qualified in management.'),
('Les Mills Instructor', 'Qualified to teach Les Mills classes.'),
('YMCA certified group Instructor', 'YMCA qualified to lead group exercise classes.'),
('NetFit Coach', 'Qualified as a NetFitNZ Personal Trainer');

-- UserQualification table seed data
INSERT INTO UserQualification (user_id, qualification_id) VALUES
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

-- Class table seed data
INSERT INTO Class (name, description, capacity) VALUES
('Yoga', 'Yoga is the perfect class for stretching and strengthening your entire body.', 30),
('RPM', 'RPM is a 60-minute group indoor cycling workout where you control the intensity', 30),
('BODYATTACK', 'BODYATTACK is a 60-minute high-energy fitness class with moves that cater for total beginners to total addicts.', 30), -- classes are max 30 people
('Private Session with Penelope', 'Private session  with Penny Sole is the perfect way to get maximum benefit for not only your body but your mind as well.', 1),
('Private Session with Amy', 'Private session  with Amy Ferguson is the best way to get maximum benefit out of your workout.', 1), -- privates are max 1 person
('Gym Session', 'A gym session is where you do you - either do the workout you planned with your trainer, or your own choice of workout.', -1) -- general gym attendance has no limit
;

-- Timetable schedule seed data
INSERT INTO schedule (class_id, trainer_id, day, start_time, end_time, room) VALUES
(1, 4, 'Monday', '09:00:00', '10:00:00', 'Studio 1'),
(3, 5, 'Tuesday', '12:00:00', '13:00:00', 'Studio 2'),
(4, 4, 'Wednesday', '06:00:00', '07:00:00', 'Main Gym'), -- Hido has a private with Penelope at this time - see bookingattendance for details
(2, 4, 'Thursday', '12:00:00', '01:00:00', 'Cycle Studio'),
(5, 5, 'Friday', '07:00:00', '08:00:00', 'Main Gym'), -- Miao is booked with Amy at this time 
(2, 1, 'Saturday', '06:00:00', '07:00:00', 'Cycle Studio'), -- Hido is teaching this spin class 
(6, null, 'Any day gym', null, null, 'Main Gym') -- this is the schedule (id 7) that will log for anyone who just scans into the main gym 
;

-- BookingAttendance table seed data
INSERT INTO BookingAttendance (schedule_id, user_id, check_in_time) VALUES
(1, 1, '2023-03-01 09:00:00'),
(1, 2, '2023-03-02 09:00:00'),
(1, 3, '2023-03-04 09:00:00'),
(2, 1, '2023-03-06 12:00:00'),
(2, 2, '2023-03-06 12:00:00'),
(3, 1, '2023-03-01 06:00:00'), -- this is Penelopes private with Hido
(5, 2, '2023-03-03 07:00:00'), -- this is Amys private with Miao
(6, 3, '2023-03-04 06:00:00'), -- the following are the attendees to Hidos RPM class on Saturday 
(6, 2, '2023-03-04 06:00:00'),
(6, 4, '2023-03-04 06:00:00'),
(6, 5, '2023-03-04 06:00:00'),
(7, 6, '2023-03-05 10:00:00'), -- open gym attendance by John Doe who is in negative balance
(4, 2, '2023-03-02 12:00:00'), -- Miao goes to the RPM class 
(4, 3, '2023-03-02 12:00:00'); -- Elizabeth goes to the RPM class 

-- Health table definition
CREATE TABLE Health (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  PRIMARY KEY (id)
);

-- UserHealth table definition
CREATE TABLE UserHealth (
  id INT NOT NULL AUTO_INCREMENT,
  user_id INT NOT NULL,
  health_id INT NOT NULL,
  value NVARCHAR(255) NOT NULL,
  date DATE NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id) REFERENCES User(id),
  FOREIGN KEY (health_id) REFERENCES Health(id)
);

-- Health table seed data
INSERT INTO Health (name, description) VALUES
('Weight', 'The weight of the user in kilograms'),
('Body Fat Percentage', 'The percentage of body fat in the user''s body'),
('Blood Pressure', 'The systolic and diastolic blood pressure values of the user'),
('General Comments', 'Allergies eg asthma, coeliac');

-- UserHealth table seed data
INSERT INTO UserHealth (user_id, health_id, value, date) VALUES
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
(3, 4, 'coeliac', '2023-02-15');

-- account table seed data
INSERT INTO account (user_id, balance) VALUES
(1, 100),
(2, 0), -- Miao is at zero balance so needs to topup/reminder email
(3, 60),
(4, 0), -- Penelope is a trainer so we dont need to bother her
(5, 200), -- Amy is a trainer so not worried about her balance either
(6, -120) -- John Doe is in negative balance so needs to topup/reminder email
;

-- transaction table seed data
INSERT INTO transaction (account_id, amount, BookingAttendance_id, reference) VALUES
(1, 200, null, 'topup'), -- Hido manually put money in to his account so he could book some private sessions later
(2, 200, null, 'monthlyAP'), -- Miao's automatice payment came through - not for class
(1, 60, 6, 'private'), -- Hido having a private session with Penelope and paying $60 for it
(2, 60, 7, 'private') -- Miao having a private session with Amy and paying $60 for it
;
