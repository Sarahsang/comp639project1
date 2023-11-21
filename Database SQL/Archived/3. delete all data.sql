-- Disable Safemode
SET SQL_SAFE_UPDATES = 0;

-- 12. Transaction table
DELETE from transaction;

-- 11. BookingAttendance table
DELETE from bookingattendance;

-- 10. Schedule table
DELETE from schedule;

-- 9. Class table
DELETE from class;

-- 8. UserQualification table
DELETE from userqualification;

-- 7. Qualification table
DELETE from qualification;

-- 6. UserHealth table
DELETE from userhealth;

-- 5. Health table
DELETE from health;

-- 4. Account table
DELETE from account;

-- 3. UserRole table
DELETE from userrole;

-- 2. Role table
DELETE from role;

-- 1. User table
DELETE from user;

-- Enable Safemode
SET SQL_SAFE_UPDATES = 1;