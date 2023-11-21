create database gym_management;
use gym_management;

-- 1. User table
CREATE TABLE user (
  id INT NOT NULL AUTO_INCREMENT,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  email VARCHAR(255) NOT NULL,
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

-- 2. Role table
CREATE TABLE role (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  description VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);

-- 3. UserRole table
CREATE TABLE userrole (
  user_id INT NOT NULL,
  role_id INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (role_id) REFERENCES role(id),
  PRIMARY KEY (user_id, role_id)
);

-- 4. Account table
CREATE TABLE account (
  id INT NOT NULL AUTO_INCREMENT,
  user_id INT NOT NULL,
  balance INT NULL,
  last_subscription_payment DATETIME,
  contract_startdate DATE,
  contract_lastdate DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES user(id),
  PRIMARY KEY (id)
);

-- 5. Health table
CREATE TABLE health (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  PRIMARY KEY (id)
);

-- 6. UserHealth table
CREATE TABLE userhealth (
  id INT NOT NULL AUTO_INCREMENT,
  user_id INT NOT NULL,
  health_id INT NOT NULL,
  value NVARCHAR(255) NOT NULL,
  date DATE NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (health_id) REFERENCES health(id)
);

-- 7. Qualification table
CREATE TABLE qualification (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  description VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);

-- 8. UserQualification table
CREATE TABLE userqualification (
  user_id INT NOT NULL,
  qualification_id INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (qualification_id) REFERENCES qualification(id),
  PRIMARY KEY (user_id, qualification_id)
);

-- 9. Class table
CREATE TABLE class (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  description VARCHAR(255) NOT NULL,
  capacity INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);

-- 10. Schedule table
CREATE TABLE schedule (
	id INT NOT NULL AUTO_INCREMENT, 
    class_id INT NOT NULL,
    trainer_id INT NULL,
    day VARCHAR(55) NOT NULL,
    start_time DATETIME NULL,
    end_time DATETIME NULL,
    room VARCHAR(50) NOT NULL,
    FOREIGN KEY (class_id) REFERENCES class(id),
	FOREIGN KEY (trainer_id) REFERENCES user(id),
	PRIMARY KEY (id)
);

-- 11. BookingAttendance table
CREATE TABLE bookingattendance (
  id INT NOT NULL AUTO_INCREMENT,
  schedule_id INT NOT NULL,
  user_id INT NOT NULL,
  check_in_time DATETIME NULL,
  cancelled BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (schedule_id) REFERENCES schedule(id),
  FOREIGN KEY (user_id) REFERENCES user(id),
  PRIMARY KEY (id)
);

-- 12. Transaction table
CREATE TABLE transaction (
  id INT NOT NULL AUTO_INCREMENT,
  account_id INT NOT NULL,
  amount INT NOT NULL,
  BookingAttendance_id INT NULL,
  reference NVARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (account_id) REFERENCES account(id),
  FOREIGN KEY (BookingAttendance_id) REFERENCES bookingattendance(id),
  PRIMARY KEY (id)
);

-- 13. weeklyTimetable table
CREATE TABLE weeklytimetable (
id INT NOT NULL,
tableday VARCHAR(55) NULL,
tabletime TIME NULL
);

-- 14. Create view validbookingattendance
CREATE VIEW validbookingattendance AS
SELECT *
FROM bookingattendance
WHERE cancelled=0;

-- 15. Create view Trainer
CREATE VIEW trainer AS
SELECT u.id, r.name, u.first_name, u.last_name, u.email, u.gender, u.date_of_birth, u.phone_number, u.address 
FROM user AS u 
LEFT JOIN userrole AS ur ON u.id=ur.user_id 
LEFT JOIN role AS r ON ur.role_id=r.id WHERE r.id=2;

-- 16. Create view Member
CREATE VIEW member AS
SELECT u.id, r.name, u.first_name, u.last_name, u.email, u.gender, u.date_of_birth, u.phone_number, u.address 
FROM user AS u 
LEFT JOIN userrole AS ur ON u.id=ur.user_id 
LEFT JOIN role AS r ON ur.role_id=r.id WHERE r.id=3;