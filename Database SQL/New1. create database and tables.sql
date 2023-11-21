create database gym_management;
use gym_management;


-- 1. Role table
CREATE TABLE role (
  id TINYINT NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  description VARCHAR(100) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);

-- 2. Member table
CREATE TABLE member (
  id INT NOT NULL AUTO_INCREMENT,
  role_id TINYINT,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  email VARCHAR(50) NOT NULL,
  password VARCHAR(50) NOT NULL,
  gender ENUM('Male', 'Female', 'Other') NOT NULL,
  date_of_birth DATE NOT NULL,
  phone_number VARCHAR(20) NOT NULL,
  address VARCHAR(255) NOT NULL,
  isactive boolean default TRUE,
  notes VARCHAR(255) NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (role_id) REFERENCES role(id),
  PRIMARY KEY (id)
);

-- 3. Trainer table
CREATE TABLE trainer (
  id INT NOT NULL AUTO_INCREMENT,
  role_id TINYINT,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  email VARCHAR(50) NOT NULL,
  password VARCHAR(50) NOT NULL,
  gender ENUM('Male', 'Female', 'Other') NOT NULL,
  date_of_birth DATE NOT NULL,
  phone_number VARCHAR(20) NOT NULL,
  address VARCHAR(255) NOT NULL,
  isactive boolean default TRUE,
  notes VARCHAR(255) NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (role_id) REFERENCES role(id),
  PRIMARY KEY (id)
);

-- 4. Admin table
CREATE TABLE admin (
  id INT NOT NULL AUTO_INCREMENT,
  role_id TINYINT,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  email VARCHAR(50) NOT NULL,
  password VARCHAR(50) NOT NULL,
  gender ENUM('Male', 'Female', 'Other') NOT NULL,
  date_of_birth DATE NOT NULL,
  phone_number VARCHAR(20) NOT NULL,
  address VARCHAR(255) NOT NULL,
  isactive boolean default TRUE,
  notes VARCHAR(255) NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (role_id) REFERENCES role(id),
  PRIMARY KEY (id)
);

-- 5. Account table
CREATE TABLE account (
  id INT NOT NULL AUTO_INCREMENT,
  member_id INT NOT NULL,
  balance INT NULL,
  last_subscription_payment DATETIME,
  contract_startdate DATE,
  contract_lastdate DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (member_id) REFERENCES member(id),
  PRIMARY KEY (id)
);

-- 6. Health table
CREATE TABLE health (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  description VARCHAR(100),
  PRIMARY KEY (id)
);

-- 7. MemberHealth table
CREATE TABLE memberhealth (
  id INT NOT NULL AUTO_INCREMENT,
  member_id INT NOT NULL,
  health_id INT NOT NULL,
  value NVARCHAR(50) NOT NULL,
  date DATE NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (member_id) REFERENCES member(id),
  FOREIGN KEY (health_id) REFERENCES health(id)
);

-- 8. Qualification table
CREATE TABLE qualification (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  description VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);

-- 9. TrainerQualification table
CREATE TABLE trainerqualification (
  trainer_id INT NOT NULL,
  qualification_id INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (trainer_id) REFERENCES trainer(id),
  FOREIGN KEY (qualification_id) REFERENCES qualification(id),
  PRIMARY KEY (trainer_id, qualification_id)
);

-- 10. Class table
CREATE TABLE class (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  description VARCHAR(255) NOT NULL,
  capacity INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);

-- 11. Schedule table
CREATE TABLE schedule (
	id INT NOT NULL AUTO_INCREMENT, 
    class_id INT NOT NULL,
    trainer_id INT NULL,
    day VARCHAR(55) NOT NULL,
    start_time DATETIME NULL,
    end_time DATETIME NULL,
    room VARCHAR(50) NOT NULL,
    FOREIGN KEY (class_id) REFERENCES class(id),
	FOREIGN KEY (trainer_id) REFERENCES trainer(id),
	PRIMARY KEY (id)
);

-- 12. BookingAttendance table
CREATE TABLE bookingattendance (
  id INT NOT NULL AUTO_INCREMENT,
  schedule_id INT NOT NULL,
  member_id INT NOT NULL,
  check_in_time DATETIME NULL,
  cancelled BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (schedule_id) REFERENCES schedule(id),
  FOREIGN KEY (member_id) REFERENCES member(id),
  PRIMARY KEY (id)
);

-- 14. Transaction type

CREATE TABLE transactiontype (
	id INT NOT NULL AUTO_INCREMENT,
    typename CHAR(20),
    PRIMARY KEY (id, typename)
);

-- 13. Transaction table
CREATE TABLE transaction (
  id INT NOT NULL AUTO_INCREMENT,
  account_id INT NOT NULL,
  amount INT NOT NULL,
  paytype INT NOT NULL,
  bookingAttendance_id INT NULL,
  reference NVARCHAR(255) NOT NULL,
  date DATE,
  time TIME,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (account_id) REFERENCES account(id),
  FOREIGN KEY (bookingAttendance_id) REFERENCES bookingattendance(id),
  FOREIGN KEY (paytype) REFERENCES transactiontype(id),
  PRIMARY KEY (id)
);

-- 14. datetable table
CREATE TABLE datetable (
id INT NOT NULL,
year YEAR,
quarter CHAR(2),
month TINYINT,
date DATE,
PRIMARY KEY (id)
);

-- 15. Create view validbookingattendance
CREATE VIEW validbookingattendance AS
SELECT *
FROM bookingattendance
WHERE cancelled=0;

-- 16. Create view subscription payment transaction
CREATE VIEW subscriptionpaymenttransaction AS
SELECT *
FROM transaction
WHERE paytype=3
;

-- 17. Create view session payment transaction
CREATE VIEW sessionpaymenttransaction AS
SELECT *
FROM transaction
WHERE paytype=4
;

-- 18. Create view refund transaction
CREATE VIEW refund AS
SELECT *
FROM transaction
WHERE paytype>=5
;

-- 19. Create view session payment transaction
CREATE VIEW subscriptionsessionrefund AS
SELECT *
FROM transaction
WHERE paytype>=3
;

-- 20. Create News Letter table
CREATE TABLE newsletters (
  newsletter_id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(50),
  content TEXT,
  date DATE,
  status boolean,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);