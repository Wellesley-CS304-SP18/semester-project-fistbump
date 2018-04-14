USE lluo2_db;

CREATE TABLE user_id (uID int NOT NULL AUTO_INCREMENT PRIMARY KEY,
                      uName varchar(100) NOT NULL,
                      email varchar(100) NOT NULL,
                      pwd varchar(255) NOT NULL) ENGINE=InnoDB;

CREATE TABLE human_resources(uID int DEFAULT NULL,
       	     		     uName varchar(100) NOT NULL,
			     cID int NOT NULL,
			     email varchar(100) NOT NULL,
			     personType ENUM('recruiter', 'referral') NOT NULL,
			     FOREIGN KEY (uID) REFERENCES user_id(uID) ON DELETE SET NULL,
			     FOREIGN KEY (cID) REFERENCES company(cID) ON DELETE CASCADE) ENGINE=InnoDB; 

CREATE TABLE job_opp (jobID int NOT NULL AUTO_INCREMENT PRIMARY KEY, 
       	     	      cID int NOT NULL, 
		      link varchar(255) NOT NULL, 
		      classPref ENUM('freshman', 'sophomore', 'junior', 'senior', 'underclassman', 'upperclassman', 'all') NOT NULL, 
		      jobTitle ENUM('ENGINEERING', 'DESIGN', 'PM', 'OTHER') NOT NULL, 
		      jobType ENUM('internship', 'part-time', 'full-time') NOT NULL,
		      season ENUM('fall', 'spring', 'summer', 'winter', 'year-round') NOT NULL, 
		      deadline DATE NOT NULL
		      FOREIGN KEY (cID) REFERENCES company(cID) ON DELETE CASCADE) ENGINE=InnoDB;

CREATE TABLE job_location (jobID int NOT NULL,
       	     		   city varchar(50) NOT NULL, 
			   PRIMARY KEY (jobID, city),
       	     		   FOREIGN KEY (jobID) REFERENCES job_opp(jobID)) ENGINE=InnoDB; 

CREATE TABLE company (cID int NOT NULL AUTO_INCREMENT PRIMARY KEY,
                      companyName varchar(100) NOT NULL) ENGINE=InnoDB;

CREATE TABLE job_review (jobID int DEFAULT NULL,
       	     		 jobYear YEAR NOT NULL,
			 reviewer int NOT NULL,
			 review varchar(1000) NOT NULL,
			 PRIMARY KEY(jobID, reviewer),
       	     	  	 FOREIGN KEY (jobID) REFERENCES job_opps(jobID) ON DELETE SET NULL,
			 FOREIGN KEY (reviewer) REFERENCES user_id(uID) ON DELETE CASCADE) ENGINE=InnoDB;

CREATE TABLE reu_opp (reuID int NOT NULL AUTO_INCREMENT PRIMARY KEY,
       	     	      deptID int NOT NULL,
		      link varchar(255) NOT NULL,
		      classPref ENUM('freshman', 'sophomore', 'junior', 'senior', 'underclassman', 'upperclassman', 'all') NOT NULL,
		      deadline DATE NOT NULL,
		      isUROP boolean NOT NULL,		      
		      FOREIGN KEY (deptID) REFERENCES department(deptID) ON DELETE CASCADE) ENGINE=InnoDB;  

CREATE TABLE department (deptID int NOT NULL AUTO_INCREMENT PRIMARY KEY,
       	     	 	 deptName varchar(100) NOT NULL,
			 city varchar(50) NOT NULL,
			 university varchar(50) NOT NULL) ENGINE=InnoDB;

CREATE TABLE reu_review (deptID int DEFAULT NULL,
       	     		 reviewer int NOT NULL,
			 review varchar(1000) NOT NULL,	  
      			 FOREIGN KEY (deptID) REFERENCES department(deptID) ON DELETE CASCADE,
			 FOREIGN KEY (reviewer) REFERENCES user_id(uID) ON DELETE CASCADE) ENGINE=InnoDB;