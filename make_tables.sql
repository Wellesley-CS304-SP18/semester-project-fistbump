USE fistbump_db;

DROP TABLE IF EXISTS prof_pic;
DROP TABLE IF EXISTS job_location;
DROP TABLE IF EXISTS job_review;
DROP TABLE IF EXISTS job_opp;
DROP TABLE IF EXISTS company;
DROP TABLE IF EXISTS city;
DROP TABLE IF EXISTS user_id;

CREATE TABLE user_id (bnum varchar(12) NOT NULL PRIMARY KEY,
		      firstname varchar(50) NOT NULL,
		      username varchar(20) NOT NULL,
		      numLogins int DEFAULT 1,
		      uType ENUM('general', 'admin') NOT NULL) ENGINE=InnoDB;

CREATE TABLE prof_pic (bnum varchar(12) NOT NULL PRIMARY KEY,
       	               pic blob,
		       FOREIGN KEY (bnum) REFERENCES user_id(bnum) ON DELETE CASCADE) ENGINE=InnoDB;

CREATE TABLE city (city varchar(50) NOT NULL PRIMARY KEY) ENGINE=InnoDB;

CREATE TABLE company (companyName varchar(100) NOT NULL PRIMARY KEY) ENGINE=InnoDB;

CREATE TABLE job_opp (jobID int NOT NULL AUTO_INCREMENT PRIMARY KEY,
                      link varchar(255) NOT NULL,
                      classPref ENUM('freshman', 'sophomore', 'junior', 'senior', 'underclassman', 'upperclassman', 'all') DEFAULT 'all',
                      jobTitle ENUM('engineering', 'design', 'pm', 'other') DEFAULT 'other',
                      jobType ENUM('internship', 'part-time', 'full-time') DEFAULT 'internship',
		      positionName varchar(50) NOT NULL,
                      season ENUM('fall', 'spring', 'summer', 'winter', 'year-round') DEFAULT 'summer',
                      deadline DATE NOT NULL,
                      poster varchar(12) NOT NULL,
		      companyName varchar(100) NOT NULL,
                      FOREIGN KEY (poster) REFERENCES user_id(bnum) ON DELETE RESTRICT,
		      FOREIGN KEY (companyName) REFERENCES company(companyName) ON DELETE CASCADE) ENGINE=InnoDB;

CREATE TABLE job_review (jobID int NOT NULL,
                         jobYear int NOT NULL,
                         reviewer varchar(12) NOT NULL,
                         review varchar(1000) NOT NULL,
			 PRIMARY KEY (jobID, reviewer),
                         FOREIGN KEY (reviewer) REFERENCES user_id(bnum) ON DELETE CASCADE) ENGINE=InnoDB;

CREATE TABLE job_location (jobID int NOT NULL,
                           city varchar(50) NOT NULL,
                           PRIMARY KEY (jobID, city),
                           FOREIGN KEY (jobID) REFERENCES job_opp(jobID) ON DELETE CASCADE,
			   FOREIGN KEY (city) REFERENCES city(city) ON DELETE RESTRICT) ENGINE=InnoDB;

CREATE TABLE favorites (bnum varchar(12) NOT NULL,
                 	jobID int NOT NULL,
			PRIMARY KEY (bnum, jobID)) ENGINE=InnoDB;

