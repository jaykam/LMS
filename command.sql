#user table
CREATE TABLE users(
	username char(30) not null,
	rollno integer(10) primary key not null,
	password varchar (80) not null,
	book_issued integer(10),
	book_time1 char(30),
	book_time2 char(30),
	book_time3 char(30),
	fine integer(10),
	reserve_id varchar(10)
	);

#admin table
CREATE TABLE admin(
	username char(30) not null,
	password varchar(80) not null
	);

#student_login table
CREATE TABLE student_login(
	username char(30) not null,
	rollno integer(30) primary key not null,
	password varchar(80) not null,
	fine integer(10),
	reserve_id varchar(10)
	);

#books table
CREATE TABLE books(
	book_name char(30) not null,
	book_id varchar(30) not null,
	availability integer(5) not null
	);

#record table
CREATE TABLE record(
	username char(30) not null,
	rollno integer(10) primary key not null,
	password varchar(80) not null,
	book_name1 char(30),
	book_name2 char(30),
	book_name3 char(30),
	fine integer(10),
	reserve_id varchar(10)
	);















