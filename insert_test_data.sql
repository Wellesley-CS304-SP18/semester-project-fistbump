USE lluo2_db;

INSERT INTO user_id (uType, uName, email, pwd) VALUES ('admin', 'Havannah Tran', 'htran@wellesley.edu', 'password123');
INSERT INTO user_id (uType, uName, email, pwd) VALUES ('admin', 'Marissa Shen', 'mshen4n@wellesley.edu', 'password456');
INSERT INTO user_id (uType, uName, email, pwd) VALUES ('admin', 'Lauren Luo', 'lluo2@wellesley.edu', 'password789');

INSERT INTO department (deptName, city, university) VALUES ('CS', 'Wellesley', 'Wellesley College');
INSERT INTO department (deptName, city, university) VALUES ('Math', 'Northampton', 'Smith College');
INSERT INTO department (deptName, city, university) VALUES ('Physics', 'Providence', 'Brown University');

INSERT INTO reu_opp(deptID, link, classPref, deadline, isUROP, poster) VALUES (1, 'cs.wellesley.edu', 'sophomore', '2018-04-18', true, 1);
INSERT INTO reu_opp(deptID, link, classPref, deadline, isUROP, poster) VALUES (2, 'math.smith.edu', 'upperclassman', '2018-04-18', false, 2);
INSERT INTO reu_opp(deptID, link, classPref, deadline, isUROP, poster) VALUES (3, 'physics.brown.edu', 'underclassman', '2018-04-18', false, 1);

INSERT INTO reu_review(deptID, reviewer, review) VALUES (2, 1, 'WOW SMITH IS AWESOME');
INSERT INTO reu_review(deptID, reviewer, review) VALUES (1, 3, 'Yeah this place is kinda sketchy');
INSERT INTO reu_review(deptID, reviewer, review) VALUES	(3, 3, 'I would love to go back!'); 

INSERT INTO company(companyName) VALUES ('Google');
INSERT INTO company(companyName) VALUES ('Adobe');
INSERT INTO company(companyName) VALUES ('Dropbox');

INSERT into human_resources (uID, uName, cID, email, personType, poster) VALUES (1, 'Havannah', 1, 'htran@wellesley.edu', 'referral', 1 );
INSERT into human_resources (uID, uName, cID, email, personType, poster) VALUES (2, 'Marissa', 1, 'mshen4@wellesley.edu', 'referral', 2 );
INSERT into human_resources (uID, uName, cID, email, personType, poster) VALUES (3, 'Lauren', 1, 'lluo2@wellesley.edu', 'referral', 3 );

INSERT into job_opp(cID, link, classPref, jobTitle, jobType, season, deadline, poster) VALUES (1, 'google.com', 'freshman', 'ENGINEERING', 'internship', 'summer', '2019-01-01', 1);
INSERT into job_opp(cID, link, classPref, jobTitle, jobType, season, deadline, poster) VALUES (2, 'google.com', 'freshman', 'ENGINEERING', 'internship', 'summer', '2019-01-01', 2);
INSERT into job_opp(cID, link, classPref, jobTitle, jobType, season, deadline, poster) VALUES (3, 'google.com', 'freshman', 'ENGINEERING', 'internship', 'summer', '2019-01-01', 3);

INSERT into job_location(jobID, city) VALUES (1, 'Boston, MA');
INSERT into job_location(jobID, city) VALUES (1, 'San Francisco, CA');
INSERT into job_location(jobID, city) VALUES (1, 'Seattle, WA');

INSERT into job_review(jobID, jobYear, reviewer, review) VALUES (1, 2018, 1, 'This place is great!');
INSERT into job_review(jobID, jobYear, reviewer, review) VALUES (1, 2018, 2, 'This place is OK...');
INSERT into job_review(jobID, jobYear, reviewer, review) VALUES (1, 2018, 3, 'This place is bad.');