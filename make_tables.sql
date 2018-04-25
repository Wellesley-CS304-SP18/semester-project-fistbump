USE lluo2_db;

DROP TABLE IF EXISTS human_resources;
DROP TABLE IF EXISTS job_location;
DROP TABLE IF EXISTS job_review;
DROP TABLE IF EXISTS job_opp;
DROP TABLE IF EXISTS company;
DROP TABLE IF EXISTS reu_review;
DROP TABLE IF EXISTS reu_opp;
DROP TABLE IF EXISTS department;
DROP TABLE IF EXISTS user_id;
	
CREATE TABLE user_id (uID int AUTO_INCREMENT PRIMARY KEY,
		      uType ENUM('general', 'admin') DEFAULT 'general',
                      uName varchar(100) NOT NULL,
                      email varchar(100) NOT NULL,
                      pwd varchar(255) NOT NULL) ENGINE=InnoDB;

CREATE TABLE department (deptID int NOT NULL AUTO_INCREMENT PRIMARY KEY,
                         deptName varchar(100) NOT NULL,
                         city varchar(50) NOT NULL,
                         university varchar(50) NOT NULL) ENGINE=InnoDB;

CREATE TABLE reu_opp (reuID int NOT NULL AUTO_INCREMENT PRIMARY KEY,
                      deptID int NOT NULL,
                      link varchar(255) NOT NULL,
                      classPref ENUM('freshman', 'sophomore', 'junior', 'senior', 'underclassman', 'upperclassman', 'all') NOT NULL,
                      deadline DATE NOT NULL,
                      isUROP boolean NOT NULL,
                      poster int NOT NULL,
                      FOREIGN KEY (deptID) REFERENCES department(deptID) ON DELETE CASCADE,
                      FOREIGN KEY (poster) REFERENCES user_id(uID) ON DELETE RESTRICT) ENGINE=InnoDB;

CREATE TABLE reu_review (deptID int DEFAULT NULL,
                         reviewer int NOT NULL,
                         review varchar(1000) NOT NULL,
                         FOREIGN KEY (deptID) REFERENCES department(deptID) ON DELETE CASCADE,
                         FOREIGN KEY (reviewer) REFERENCES user_id(uID) ON DELETE CASCADE) ENGINE=InnoDB;

CREATE TABLE company (companyName varchar(100) NOT NULL PRIMARY KEY) ENGINE=InnoDB;

CREATE TABLE job_opp (jobID int NOT NULL AUTO_INCREMENT PRIMARY KEY,
                      link varchar(255) NOT NULL,
                      classPref ENUM('freshman', 'sophomore', 'junior', 'senior', 'underclassman', 'upperclassman', 'all') NOT NULL,
                      jobTitle ENUM('ENGINEERING', 'DESIGN', 'PM', 'OTHER') NOT NULL,
                      jobType ENUM('internship', 'part-time', 'full-time') NOT NULL,
		      positionName varchar(50) NOT NULL,
                      season ENUM('fall', 'spring', 'summer', 'winter', 'year-round') NOT NULL,
                      deadline DATE NOT NULL,
                      poster int NOT NULL,
		      companyName varchar(100) NOT NULL, 
                      FOREIGN KEY (poster) REFERENCES user_id(uID) ON DELETE RESTRICT,
		      FOREIGN KEY (companyName) REFERENCES company(companyName) ON DELETE RESTRICT) ENGINE=InnoDB;

CREATE TABLE job_review (jobID int,
                         jobYear int NOT NULL,
                         reviewer int NOT NULL,
                         review varchar(1000) NOT NULL,
                         FOREIGN KEY (jobID) REFERENCES job_opp(jobID) ON DELETE RESTRICT,
                         FOREIGN KEY (reviewer) REFERENCES user_id(uID) ON DELETE CASCADE) ENGINE=InnoDB;

CREATE TABLE job_location (jobID int NOT NULL,
                           city varchar(50) NOT NULL,
                           PRIMARY KEY (jobID, city),
                           FOREIGN KEY (jobID) REFERENCES job_opp(jobID)) ENGINE=InnoDB;

CREATE TABLE human_resources(uID int DEFAULT NULL,
       	     		     uName varchar(100) NOT NULL,
			     companyName int NOT NULL,
			     email varchar(100) NOT NULL,
			     personType ENUM('recruiter', 'referral') NOT NULL,
			     poster int NOT NULL,
			     FOREIGN KEY (uID) REFERENCES user_id(uID) ON DELETE SET NULL,
			     FOREIGN KEY (companyName) REFERENCES company(companyName) ON DELETE CASCADE,
			     FOREIGN KEY (poster) REFERENCES user_id(uID) ON DELETE RESTRICT) ENGINE=InnoDB; 
