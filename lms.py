#for databse
import MySQLdb 

#for access current time
from datetime import datetime  
from datetime import timedelta

#for password saving in #form
from werkzeug import generate_password_hash, check_password_hash 

#database connenctivity
conn = MySQLdb.connect('localhost', 'root', 'jaykm', 'lms')
cur=conn.cursor()


class Admin:
	def __init__(self, username, password):
		self.username = username
		self.password = password
		
		hashed_password = generate_password_hash(self.password)
		try:
			val = "insert into admin values(\'" + str(self.username)+"\',\'" + str(hashed_password)+"\')"
			cur.execute(val)
			conn.commit()
		except:
			print "Enter Correct Details !"
		
class Book:
	def __init__(self, book_name, book_id, availability):
		self.book_name = book_name
		self.book_id = book_id
		self.availability = 1
		val1 = "insert into books values(\'" + str(self.book_name)+"\',\'" + str(self.book_id)+"\',\'" + str(self.availability)+"\')"
		cur.execute(val1)
		conn.commit()
		

class User:
	def __init__(self, username, rollno, password, book_issued, book_time1, book_time2, book_time3, fine, reserve_id, book_name1, book_name2, book_name3):
		self.username = username
		self.rollno = rollno
		self.password = password
		hashed_password = generate_password_hash(self.password)
		self.book_issued = 0
		self.book_time1 = "null"
		self.book_time2 = "null"
		self.book_time3 = "null"
		self.book_name1 = "null"
		self.book_name2 = "null"
		self.book_name3 = "null"
		self.fine = 0
		self.reserve_id = "null"
		val = "insert into users values(\'" + str(self.username)+"\', \'" + str(self.rollno)+"\',\'" + str(hashed_password)+"\', \'" + str(self.book_issued)+"\', \'" + str(self.book_time1)+"\', \'" + str(self.book_time2)+"\', \'" + str(self.book_time3)+"\', \'" + str(self.fine)+"\', \'" + str(self.reserve_id)+"\')"
		cur.execute(val)
		conn.commit()
		val = "insert into student_login values(\'" + str(self.username)+"\', \'" + str(self.rollno)+"\', \'" + str(hashed_password)+"\', \'" + str(self.fine)+"\', \'" + str(self.reserve_id)+"\')"
		cur.execute(val)
		conn.commit()
		val = "insert into record values(\'" + str(self.username)+"\', \'" + str(self.rollno)+"\', \'" + str(hashed_password)+"\', \'" + str(self.book_name1)+"\',  \'" + str(self.book_name2)+"\',  \'" + str(self.book_name3)+"\', \'" + str(self.fine)+"\', \'" + str(self.reserve_id)+"\')"
		cur.execute(val)
		conn.commit()

def store():
	print " "
	admin_username = raw_input("Enter admin username:-")
	admin_password = raw_input("Enter admin password:-")
	val = "select * from admin where username =  \'" + str(admin_username)+"\'"
	cur.execute(val)
	rows = cur.fetchone()
	if rows == None:
		print " "
		print "Admin does not exit"
	else:
		password = rows[1]
		if not check_password_hash(password, admin_password):
			print " "
			print "Admin password is incorrect!"
		else:
			print " "
			student_rollno = raw_input("Enter the student rollno:-")
			
			val = "select * from student_login where rollno = \'" + str(student_rollno)+"\'"
			cur.execute(val)
			rows = cur.fetchone()
			if rows == None:
				print " "
				print "This rollno does not exit!, Please enter again!"
			else:
				print " "
				book_issue = raw_input("want to issue a book (y/n): ")
				if book_issue == "y" or book_issue == "Y":
					val = "select * from users where rollno = \'" + str(student_rollno)+"\'"
					cur.execute(val)
					student = cur.fetchone()
					fine = student[7]
					if fine == 0:
						book_issued = student[3]
						if book_issued == 3:
							print " "
							print "You cant issue more books-"
						elif book_issued == 2:
							print " "
							book_no = raw_input("How many books you want to issue:-")
							if book_no >= 2:
								print " "
								print "You cant issue "
							else:
								if book_no == 0:
									print " "
									print "Enter the valid no. "
								else:
									book_id = raw_input("Enter the book id which you want to issue-")
									val = "select * from books where book_id =  \'" + str(book_id)+"\'"
									cur.execute(val)
									rows = cur.fetchone()
									if rows == None:
										print " "
										print "This book is not available in  library!"
									else:
										available = rows[2]
										if available == 0:
											print " "
											print "This book is issued to someone so you cant issue"
										else:
											book3 = rows[0]
											val = "update record set book_name3 = \'" + str(book3)+"\' where rollno = \'" + str(student_rollno)+"\'"
											cur.execute(val)
											conn.commit()

											n = 0
											val = "update books set availability = \'" + str(n)+"\' where book_id = \'" + str(book_id)+"\'"

											
											temp1 = student[3]
											temp1+=1
											val = "update users set book_issued = \'" + str(temp1)+"\' where rollno = \'" + str(student_rollno)+"\")"
											cur.execute(val)
											conn.commit()
											
											T = datetime.now()
											li = [T.day, T.month, T.year]
											val = "update users set book_time3 = \'" + str(li)+"\' where rollno = \'" + str(student_rollno)+"\'"
											cur.execute(val)
											conn.commit()
											print " "
											print "				 Book issued!"

						elif book_issued == 1:
							print " "
							book_no = raw_input("How many books you want to issue:-")
							if book_no > 2:
								print " "
								print "you cant issue"
							elif book_no == 2:
								book_id1, book_id2 = map(int, raw_input("Enter the books id:-").split())
								val = "select * from books where book_id = \'" + str(book_id1)+"\'"
								cur.execute(val)
								rows = cur.fetchone()
								if rows == None:
									print " "
									print "First book is not available in library"
								else:
									available = rows[2]
									if available == 0:
										print " "
										print "first book is issued to someone so you cant issue"
									else:
										book1 = rows[1]
										val = "update record set book_name2 = \'" + str(book1)+"\' where rollno = \'" + str(student_rollno)+"\'"
										cur.execute(val)
										conn.commit()

										n = 0
										val = "update books set availability = \'" + str(n)+"\' where book_id = \'" + str(book_id1)+"\'"
										
										temp1 = student[3]
										temp1+=1
										val = "update users set book_issued = \'" + str(temp1)+"\' where rollno = \'" + str(student_rollno)+"\")"
										cur.execute(val)
										conn.commit()
										
										T = datetime.now()
										li = [T.day, T.month, T.year]
										val = "update users set book_time2 = \'" + str(li)+"\' where rollno = \'" + str(student_rollno)+"\'"
										cur.execute(val)
										conn.commit()
										
										


								val = "select * from books where book_id = \'" + str(book_id2)+"\'"
								cur.execute(val)
								rows = cur.fetchone()
								if rows == None:
									print " "
									print "Second book is not available in library"
								else:
									available = rows[2]
									if available == 0:
										print " "
										print "Second book is issued to someone so you cant issue "
									else:
										book_name = rows[0]
										val = "update record set book_name3 = \'" + str(book_name)+"\' where rollno = \'" + str(student_rollno)+"\'"
										cur.execute(val)
										conn.commit()

										n = 0
										val = "update books set availability = \'" + str(n)+"\' where book_id = \'" + str(book_id2)+"\'"
										
										temp1 = student[3]
										temp1+=1
										val = "update users set book_issued = \'" + str(temp1)+"\' where rollno = \'" + str(student_rollno)+"\")"
										cur.execute(val)
										conn.commit()
										
										T = datetime.now()
										li = [T.day, T.month, T.year]
										val = "update users set book_time3 = \'" + str(li)+"\' where rollno = \'" + str(student_rollno)+"\'"
										cur.execute(val)
										conn.commit()
										print " "
										print "			   Book issued"
										
						else:
							print " "
							book_no = raw_input("How many books you want to issue:-")
							if book_no > 3:
								print " "
								print "You cant issue more than 3 books"
							elif book_no == 3:
								book_id1, book_id2, book_id3 = map(int, raw_input("Enter the books id's ").split())
								val = "select * from books where book_id = \'" + str(book_id1)+"\'"
								cur.execute(val)
								rows = cur.fetchone()
								if rows == None:
									print " "
									print "First book is not available in library"
								else:
									available = rows[2]
									if available == 0:
										print "First book is issued to someone so you cant issue"
									else:
										book_name = rows[0]
										val = "update record set book_name1 = \'" + str(book_name)+"\' where rollno = \'" + str(student_rollno)+"\'"
										cur.execute(val)
										conn.commit()

										n = 0
										val = "update books set availability = \'" + str(n)+"\' where book_id = \'" + str(book_id1)+"\'"
										
										temp1 = student[3]
										temp1+=1
										val = "update users set book_issued = \'" + str(temp1)+"\' where rollno = \'" + str(student_rollno)+"\")"
										cur.execute(val)
										conn.commit()
										
										T = datetime.now()
										li = [T.day, T.month, T.year]
										val = "update users set book_time1 = \'" + str(li)+"\' where rollno = \'" + str(student_rollno)+"\'"
										cur.execute(val)
										conn.commit()
										

								val = "select * from books where book_id = \'" + str(book_id2)+"\'"
								cur.execute(val)
								rows = cur.fetchone()
								if rows == None:
									print " "
									print "Second book is not available in library"
								else:
									available = rows[2]
									if available == 0:
										print " "
										print "Second book is issued to someone so you cant issue"
									else:
										book_no = rows[0]
										val = "update record set book_name2 = \'" + str(book_name)+"\' where rollno = \'" + str(student_rollno)+"\'"
										cur.execute(val)
										conn.commit()

										n = 0
										val = "update books set availability = \'" + str(n)+"\' where book_id = \'" + str(book_id2)+"\'"
										
										temp1 = student[3]
										temp1+=1
										val = "update users set book_issued = \'" + str(temp1)+"\' where rollno = \'" + str(student_rollno)+"\")"
										cur.execute(val)
										conn.commit()
										
										T = datetime.now()
										li = [T.day, T.month, T.year]
										val = "update users set book_time2 = \'" + str(li)+"\' where rollno = \'" + str(student_rollno)+"\'"
										cur.execute(val)
										conn.commit()
										

								val = "select * from books where book_id = \'" + str(book_id3)+"\'"
								cur.execute(val)
								rows = cur.fetchone()
								if rows == None:
									print " "
									print "Third book is not available in library"
								else:
									available = rows[2]
									if available == 0:
										print "Third book is issued to someone so you cant issue"
									else:
										book_name = rows[0]
										val = "update record set book_name3 = \'" + str(book_name)+"\' where rollno = \'" + str(student_rollno)+"\'"
										cur.execute(val)
										conn.commit()

										n = 0
										val = "update books set availability = \'" + str(n)+"\' where book_id = \'" + str(book_id3)+"\'"
										
										temp1 = student[3]
										temp1+=1
										val = "update users set book_issued = \'" + str(temp1)+"\' where rollno = \'" + str(student_rollno)+"\")"
										cur.execute(val)
										conn.commit()
										
										T = datetime.now()
										li = [T.day, T.month, T.year]
										val = "update users set book_time3 = \'" + str(li)+"\' where rollno = \'" + str(student_rollno)+"\'"
										cur.execute(val)
										conn.commit()
							
							elif book_no == 2:
								book_id1, book_id2 = map(int, raw_input("Enter the books id's:- ").split())
								val = "select * from books where book_id = \'" + str(book_id1)+"\'"
								cur.execute(val)
								rows = cur.fetchone()
								if rows == None:
									print " "
									print "First book is not available in library"
								else:
									available = rows[2]
									if available == 0:
										print "First book is issued to someone so you cant issue"
									else:
										book_name = rows[0]
										val = "update record set book_name1 = \'" + str(book_name)+"\' where rollno = \'" + str(student_rollno)+"\'"
										cur.execute(val)
										conn.commit()

										n = 0
										val = "update books set availability = \'" + str(n)+"\' where book_id = \'" + str(book_id1)+"\'"
										
										temp1 = student[3]
										temp1+=1
										val = "update users set book_issued = \'" + str(temp1)+"\' where rollno = \'" + str(student_rollno)+"\")"
										cur.execute(val)
										conn.commit()
										
										T = datetime.now()
										li = [T.day, T.month, T.year]
										val = "update users set book_time1 = \'" + str(li)+"\' where rollno = \'" + str(student_rollno)+"\'"
										cur.execute(val)
										conn.commit()
										

								val = "select * from books where book_id = \'" + str(book_id2)+"\'"
								cur.execute(val)
								rows = cur.fetchone()
								if rows == None:
									print " "
									print "Second book is not available in library"
								else:
									available = rows[2]
									if available == 0:
										print " "
										print "Second book is issued to someone so you cant issue"
									else:
										book_no = rows[0]
										val = "update record set book_name2 = \'" + str(book_name)+"\' where rollno = \'" + str(student_rollno)+"\'"
										cur.execute(val)
										conn.commit()

										n = 0
										val = "update books set availability = \'" + str(n)+"\' where book_id = \'" + str(book_id2)+"\'"
										
										temp1 = student[3]
										temp1+=1
										val = "update users set book_issued = \'" + str(temp1)+"\' where rollno = \'" + str(student_rollno)+"\")"
										cur.execute(val)
										conn.commit()
										
										T = datetime.now()
										li = [T.day, T.month, T.year]
										val = "update users set book_time2 = \'" + str(li)+"\' where rollno = \'" + str(student_rollno)+"\'"
										cur.execute(val)
										conn.commit()

							elif book_no == 1:
									book_id = raw_input("Enter the book id which you want to issue-")
									val = "select * from books where book_id =  \'" + str(book_id)+"\'"
									cur.execute(val)
									rows = cur.fetchone()
									if rows == None:
										print "This book is not available in  library"
									else:
										available = rows[2]
										if available == 0:
											print " "
											print "This book is issued to someone so you cant issue"
										else:
											book3 = rows[0]
											val = "update record set book_name3 = \'" + str(book3)+"\' where rollno = \'" + str(student_rollno)+"\'"
											cur.execute(val)
											conn.commit()

											n = 0
											val = "update books set availability = \'" + str(n)+"\' where book_id = \'" + str(book_id)+"\'"

											
											temp1 = student[3]
											temp1 += 1
											val = "update users set book_issued = \'" + str(temp1)+"\' where rollno = \'" + str(student_rollno)+"\")"
											cur.execute(val)
											conn.commit()
											
											T = datetime.now()
											li = [T.day, T.month, T.year]
											val = "update users set book_time3 = \'" + str(li)+"\' where rollno = \'" + str(student_rollno)+"\'"
											cur.execute(val)
											conn.commit()
											print " "
											print "				 Book issued!"
							else:
								print " "
								print "Enter valid no.!"

					else:
						print " "
						print "		You cant issue books due to fine so First pay the fine"
						
				
				else:
					print " "
					print "Ok fine!"
				
				



def fine():
	admin_rollno = raw_input("Enter admin username-")
	admin_password = raw_input("Enter admin password-")
	val = "select * from admin where username =  \'" + str(admin_rollno)+"\'"
	cur.execute(val)
	rows = cur.fetchone()
	if rows == None:
		print "Admin does not exit"
	else:
		rows2 = rows[1]
		if not check_password_hash(rows2, admin_password):
			print "Password is incorrect"
		else:
			student_rollno = raw_input("Enter student rollno-")
			val = "select * from users where rollno = \'" +str(student_rollno)+"\'"
			cur.execute(val)
			rows = cur.fetchone()
			if rows == None:
				print "Enter the valid rollno"
			else:
				val1 = rows[4]
				if val1 == 3:
					x = int(raw_input("No. of books you want to return-"))

					if x > 3:
						print "Enter valid no."
					elif x == 3:
						t1 = int(raw_input("Enter the extra due time for book1-"))
						t2 = int(raw_input("Enter the extra due time for book2-"))
						t3 = int(raw_input("Enter the extra due time for book3-"))
						bk1, bk2, bk3 = map(int, raw_input("Enter the books name you want to return-"))
						val = "select * from record where rollno = \'" + str(student_rollno)+"\'"
						cur.execute(val)
						rows = cur.fetchone()
						book1 = rows[3]
						book2 = rows[4]
						book3 = rows[5]
						ct = 0
						if bk1 != book1 and bk1 != book2 and bk1 !=book3:
							ct += 1
							print "First book name incorrect"
						elif bk2 != book1 and bk2 != book2 and bk2 !=book3:
							ct += 1
							print "Second book name incorrect "
						elif bk3 != book1 and bk3 != book2 and bk3 !=book3:
							ct += 1
							print "Third book name incorrect "
						if ct == 0:
							y = val1 - x
							val = "update users set book_issued = \'" + str(y)+"\' where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							conn.commit()
							n = "null"
							nn = 1

							val = "select * from record where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							rows1 = cur.fetchone()
							nn = 1
							
							val = "update books set availability = \'" + str(nn)+"\' where book_name =  \'" + str(bk1)+"\'"
							cur.execute(val)
							conn.commit()
							val = "update books set availability = \'" + str(nn)+"\' where book_name =  \'" + str(bk2)+"\'"
							cur.execute(val)
							conn.commit()
							val = "update books set availability = \'" + str(nn)+"\' where book_name =  \'" + str(bk3)+"\'"
							cur.execute(val)
							conn.commit()
							
							
							n = "null"
							val = "update record set book_name1 = \'" + str(n)+"\' where  rollno= \'" + str(student_rollno)+"\'"
							cur.execute(val)
							conn.commit()
							val = "update record set book_name2 = \'" + str(n)+"\' where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							conn.commit()
							val = "update record set book_name3 = \'" + str(n)+"\' where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							conn.commit()

							T = t1+t2+t3
							total = T*10
							val = "update users set fine = \'" + str(total)+"\' where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							conn.commit()
							val = "update student_login set fine = \'" + str(total)+"\' where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							conn.commit()
							val = "update record set fine = \'" + str(total)+"\' where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							conn.commit()
							

							val = "update users set book_time1 = \'" + str(n)+"\' where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							conn.commit()
							val = "update users set book_time2 = \'" + str(n)+"\' where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							conn.commit()
							val = "update users set book_time3 = \'" + str(n)+"\' where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							conn.commit()

							print "Your fine is"
							print total
						else:
							print "Please Enter the correct books name"


					elif x == 2:
						t1 = int(raw_input("Enter the issued time for book1-"))
						t2 = int(raw_input("Enter the issued time for book2-"))
						bk1, bk2 = map(int, raw_input("Enter the books name you want to return-"))
						val = "select * from record where rollno = \'" + str(student_rollno)+"\'"
						cur.execute(val)
						rows = cur.fetchone()
						book1 = rows[3]
						book2 = rows[4]
						book3 = rows[5]
						ct = 0
						if bk1 !=book1 and bk1 !=book2 and bk1 !=book3:
							ct = 1
							print "First book name incorrect "
						elif bk2 !=book1 and bk2 !=book2 and bk2 !=book3:
							ct = 1
							print "Second book name incorrect "

						if ct == 0:
							y = val1 - x
							val = "update users set book_issued = \'" + str(y)+"\' where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							conn.commit()
							n = "null"
							nn = 1

							val = "update books set availability = \'" + str(nn)+"\' where book_name =  \'" + str(bk1)+"\'"
							cur.execute(val)
							conn.commit()
							val = "update books set availability = \'" + str(nn)+"\' where book_name =  \'" + str(bk2)+"\'"
							cur.execute(val)
							conn.commit()

							val = "select * from record where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							rowss = cur.fetchone()
							rowss1 = rowss[3]
							rowss2 = rowss[4]
							rowss3 = rowss[5]
							if rowss1  == bk1 or rowss1 == bk2:
								val = "update record set book_name1 = \'" + str(n)+"\' where  rollno= \'" + str(student_rollno)+"\'"
								cur.execute(val)
								conn.commit()
								val = "update users set book_time1 = \'" + str(n)+"\' where rollno = \'" + str(student_rollno)+"\'"
								cur.execute(val)
								conn.commit()

							elif rowss2  == bk1 or rowss2 == bk2:
								val = "update record set book_name2 = \'" + str(n)+"\' where  rollno= \'" + str(student_rollno)+"\'"
								cur.execute(val)
								conn.commit()
								val = "update users set book_time2 = \'" + str(n)+"\' where rollno = \'" + str(student_rollno)+"\'"
								cur.execute(val)
								conn.commit()
							else:
								val = "update record set book_name3 = \'" + str(n)+"\' where  rollno= \'" + str(student_rollno)+"\'"
								cur.execute(val)
								conn.commit()
								val = "update users set book_time3 = \'" + str(n)+"\' where rollno = \'" + str(student_rollno)+"\'"
								cur.execute(val)
								conn.commit()

							T = t1+t2
							total = T*10
							val = "update users set fine = \'" + str(total)+"\' where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							conn.commit()
							val = "update student_login set fine = \'" + str(total)+"\' where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							conn.commit()
							val = "update record set fine = \'" + str(total)+"\' where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							conn.commit()
							
							print "Your fine is"
							print total
						else:
							print "Please Enter the correct books name"
							
					elif x == 1:
						t1 = int(raw_input("Enter the extra due time for book1-"))
						bk = raw_input("Enter the book name which you want to return-")
						val = "select * from record where rollno = \'" + str(student_rollno)+"\'"
						cur.execute(val)
						rows = cur.fetchone()
						book1 = rows[3]
						book2 = rows[4]
						book3 = rows[5]
						ct = 0
						if bk !=book1 and bk !=book2 and bk !=book3:
							ct = 1
							print "This book name incorrect "
						if ct == 0:
							y = val1 - x
							val = "update users set book_issued = \'" + str(y)+"\' where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							conn.commit()
							n = "null"
							nn = 1

							val = "select * from record where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							rowss = cur.fetchone()
							
							rowss1 = rowss[3]
							rowss2 = rowss[4]
							rowss3 = rowss[5]
							if bk == rowss1:
								val = "update record set book_name1 = \'" + str(n)+"\' where  rollno= \'" + str(student_rollno)+"\'"
								cur.execute(val)
								conn.commit()
								val = "update users set book_time1 = \'" + str(n)+"\' where rollno = \'" + str(student_rollno)+"\'"
								cur.execute(val)
								conn.commit()
							elif bk == rowss2:
								val = "update record set book_name2 = \'" + str(n)+"\' where  rollno= \'" + str(student_rollno)+"\'"
								cur.execute(val)
								conn.commit()
								val = "update users set book_time2 = \'" + str(n)+"\' where rollno = \'" + str(student_rollno)+"\'"
								cur.execute(val)
								conn.commit()
							else:
								val = "update record set book_name3 = \'" + str(n)+"\' where  rollno= \'" + str(student_rollno)+"\'"
								cur.execute(val)
								conn.commit()
								val = "update users set book_time3 = \'" + str(n)+"\' where rollno = \'" + str(student_rollno)+"\'"
								cur.execute(val)
								conn.commit()
						


							T = t1
							total = T*10
							val = "update users set fine = \'" + str(total)+"\' where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							conn.commit()
							val = "update student_login set fine = \'" + str(total)+"\' where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							conn.commit()
							val = "update record set fine = \'" + str(total)+"\' where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							conn.commit()

							print "Your fine is"
							print total
						
						else:
							print "Please Enter the correct book name"
							


					else:
						print "Enter the valid no."


				elif val1 == 2:
					x = int(raw_input("No. of books you want to return-"))

					if x > 2:
						print "Enter valid no."
					elif x == 2:
						t1 = int(raw_input("Enter the extra due time for book1-"))
						t2 = int(raw_input("Enter the extra due time for book2-"))
						bk1, bk2 = map(int, raw_input("Enter the books name you want to return-"))
						val = "select * from record where rollno = \'" + str(student_rollno)+"\'"
						cur.execute(val)
						rows = cur.fetchone()
						book1 = rows[3]
						book2 = rows[4]
						book3 = rows[5]
						ct = 0
						if bk1 !=book1 and bk1 !=book2 and bk1 !=book3:
							ct = 1
							print "First book name is incorrect "
						elif bk2 !=book1 and bk2 !=book2 and bk2 !=book3:
							ct = 1
							print "Second book name is incorrect "
						if ct == 0:
							y = val1 - x
							val = "update users set book_issued = \'" + str(y)+"\' where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							conn.commit()
							n = "null"
							nn = 1

							val = "select * from record where rollno = \'" + strs(student_rollno)+"\'"
							cur.execute(val)
							rows1 = cur.fetchone()
							

							val = "update books set availability = \'" + str(nn)+"\' where book_name =  \'" + str(bk1)+"\'"
							cur.execute(val)
							conn.commit()
							val = "update books set availability = \'" + str(nn)+"\' where book_name =  \'" + str(bk2)+"\'"
							cur.execute(val)
							conn.commit()
								
							val = "select * from record where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							rowss = cur.fetchone()
							rowss1 = rowss[3]
							rowss2 = rowss[4]
							rowss3 = rowss[5]
							if rowss1  == bk1 or rowss1 == bk2:
								val = "update record set book_name1 = \'" + str(n)+"\' where  rollno= \'" + str(student_rollno)+"\'"
								cur.execute(val)
								conn.commit()
								val = "update users set book_time1 = \'" + str(n)+"\' where rollno = \'" + str(student_rollno)+"\'"
								cur.execute(val)
								conn.commit()

							elif rowss2  == bk1 or rowss2 == bk2:
								val = "update record set book_name2 = \'" + str(n)+"\' where  rollno= \'" + str(student_rollno)+"\'"
								cur.execute(val)
								conn.commit()
								val = "update users set book_time2 = \'" + str(n)+"\' where rollno = \'" + str(student_rollno)+"\'"
								cur.execute(val)
								conn.commit()
							else:
								val = "update record set book_name3 = \'" + str(n)+"\' where  rollno= \'" + str(student_rollno)+"\'"
								cur.execute(val)
								conn.commit()
								val = "update users set book_time3 = \'" + str(n)+"\' where rollno = \'" + str(student_rollno)+"\'"
								cur.execute(val)
								conn.commit()	
								
							

							T = t1+t2
							total = T*10
							val = "update users set fine = \'" + str(total)+"\' where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							conn.commit()
							val = "update student_login set fine = \'" + str(total)+"\' where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							conn.commit()
							val = "update record set fine = \'" + str(total)+"\' where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							conn.commit()

							print "Your fine is"
							print total
							
						else:
							print "Please Enter the correct books name"
							
							
					elif x == 1:
						t1 = int(raw_input("Enter the extra due time for book1-"))
						bk = raw_input("Enter the book id which you want to return-")
						val = "select * from record where rollno = \'" + str(student_rollno)+"\'"
						cur.execute(val)
						rows = cur.fetchone()
						book1 = rows[3]
						book2 = rows[4]
						book3 = rows[5]
						ct = 0
						if bk !=book1 and bk !=book2 and bk !=book3:
							ct = 1
							print "This book name is incorrect "
						if ct == 0:
							y = val1 - x
							val = "update users set book_issued = \'" + str(y)+"\' where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							conn.commit()
							n = "null"
							nn = 1

							val = "select * from record where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							rowss = cur.fetchone()
							
							rowss1 = rowss[3]
							rowss2 = rowss[4]
							rowss3 = rowss[5]
							if bk == rowss1:
								val = "update record set book_name1 = \'" + str(n)+"\' where  rollno= \'" + str(student_rollno)+"\'"
								cur.execute(val)
								conn.commit()
								val = "update users set book_time1 = \'" + str(n)+"\' where rollno = \'" + str(student_rollno)+"\'"
								cur.execute(val)
								conn.commit()
							elif bk == rowss2:
								val = "update record set book_name2 = \'" + str(n)+"\' where  rollno= \'" + str(student_rollno)+"\'"
								cur.execute(val)
								conn.commit()
								val = "update users set book_time2 = \'" + str(n)+"\' where rollno = \'" + str(student_rollno)+"\'"
								cur.execute(val)
								conn.commit()
							else:
								val = "update record set book_name3 = \'" + str(n)+"\' where  rollno= \'" + str(student_rollno)+"\'"
								cur.execute(val)
								conn.commit()
								val = "update users set book_time3 = \'" + str(n)+"\' where rollno = \'" + str(student_rollno)+"\'"
								cur.execute(val)
								conn.commit()
						


							T = t1
							total = T*10
							val = "update users set fine = \'" + str(total)+"\' where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							conn.commit()
							val = "update student_login set fine = \'" + str(total)+"\' where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							conn.commit()
							val = "update record set fine = \'" + str(total)+"\' where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							conn.commit()
							print "Your fine is"
							print total
						
						else:
							print "Please Enter the correct book name"
							
					else:
						print "Enter valid no."

				elif val1 == 1:
					x = int(raw_input("No. of books you want to return-"))

					if x > 1:
						print "Enter valid no."
					elif x == 1:
						t1 = int(raw_input("Enter the extra due time for book1-"))
						bk = raw_input("Enter the book id which you want to return-")
						val = "select * from record where rollno = \'" + str(student_rollno)+"\'"
						cur.execute(val)
						rows = cur.fetchone()
						book1 = rows[3]
						book2 = rows[4]
						book3 = rows[5]
						ct = 0
						if bk !=book1 and bk !=book2 and bk !=book3:
							ct = 1
							print "This book name is incorrect "
						if ct == 0:
							y = val1 - x
							val = "update users set book_issued = \'" + str(y)+"\' where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							conn.commit()
							n = "null"
							nn = 1

							val = "select * from record where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							rowss = cur.fetchone()
							
							rowss1 = rowss[3]
							rowss2 = rowss[4]
							rowss3 = rowss[5]
							if bk == rowss1:
								val = "update record set book_name1 = \'" + str(n)+"\' where  rollno= \'" + str(student_rollno)+"\'"
								cur.execute(val)
								conn.commit()
								val = "update users set book_time1 = \'" + str(n)+"\' where rollno = \'" + str(student_rollno)+"\'"
								cur.execute(val)
								conn.commit()
							elif bk == rowss2:
								val = "update record set book_name2 = \'" + str(n)+"\' where  rollno= \'" + str(student_rollno)+"\'"
								cur.execute(val)
								conn.commit()
								val = "update users set book_time2 = \'" + str(n)+"\' where rollno = \'" + str(student_rollno)+"\'"
								cur.execute(val)
								conn.commit()
							else:
								val = "update record set book_name3 = \'" + str(n)+"\' where  rollno= \'" + str(student_rollno)+"\'"
								cur.execute(val)
								conn.commit()
								val = "update users set book_time3 = \'" + str(n)+"\' where rollno = \'" + str(student_rollno)+"\'"
								cur.execute(val)
								conn.commit()
						

							T = t1
							total = T*10
							val = "update users set fine = \'" + str(total)+"\' where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							conn.commit()
							val = "update student_login set fine = \'" + str(total)+"\' where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							conn.commit()
							val = "update record set fine = \'" + str(total)+"\' where rollno = \'" + str(student_rollno)+"\'"
							cur.execute(val)
							conn.commit()

							print "Your fine is"
							print fine
						
						else:
							print "Please Enter the correct book name"
						
						
					else:
						print "Enter valid no."
				elif val1 == 0:
					print "You have no more books"

				else:
					print "Error"



							
def another_admin():
	val = "select * from admin"
	cur.execute(val)
	rows = cur.fetchall()
	if rows == ():
		admin_username = raw_input("Enter New admin username:-")
		admin_password = raw_input("Enter New admin password:-")
	
		adm = Admin(admin_username, admin_password)
	else:
		admin_username = raw_input("Enter existing admin username:-")
		admin_password = raw_input("Enter existing admin password:-")
		val = "select * from admin where username = \'" + str(admin_username)+"\'"
		cur.execute(val)
		rows = cur.fetchone()
		if rows == None:
			print "Admin does not exit"
		else:
			password = rows[1]
			if check_password_hash(password, admin_password):
				print " "
				print "Admin succefully logged in..!"
				print " "
				another_admin = raw_input("You want add a another admin (y/n): ")
				if another_admin == "y" or another_admin == "Y":
					another_admin_username = raw_input("Enter another username-")
					another_admin_password = raw_input("Enter another password-")
					rows = []
					try:
						val = "select * from admin where username = \'" + str(another_admin_username)+"\'"
						cur.execute(val)
						rows = cur.fetchone()
					except:
						print "Enter Correct Details"
					if rows == None:
						adm = Admin(another_admin_username, another_admin_password)
						print " "
						print "succefully added another admin"
					elif rows == []:
						pass
					else:
						print "Admin username already exit"
				else:
					print "You cant be admin!"
			else:
				print "Admin password incorrect"
					
		
		
		
						
		
			
					
					
		



				
							
		



	
	
		
		
				



def admin():
	admin_username = raw_input("Enter admin username:-")
	admin_password = raw_input("Enter admin password:-")
	val = "select * from admin where username =  \'" + str(admin_username)+"\'"
	cur.execute(val)
	rows = cur.fetchone()
	if rows == None:
		print " "
		print "Admin does not exit"
	else:
		password = rows[1]
		if check_password_hash(password, admin_password):
			print " "
			print "Succefully logged in"
			print " "
			print "Add books in library"
			add_book()
		else:
			print " "
			print "Admin Password incorrect!"

		



def add_book():
	print " "
	book_name = raw_input("Enter book name-")
	book_id = raw_input("Enter book id:-")
	book_availability = 1
	val = "select * from books where book_id = \'" + str(book_id)+"\'"
	cur.execute(val)
	rows = cur.fetchone()
	if rows == None:
		book = Book(book_name, book_id, book_availability)
		print "				Book Added!"
	else:
		print " "
		print "            This book id already exit"
	

			
	






def add_user():
	print " "
	admin_username = raw_input("Enter admin username:-")
	admin_password = raw_input("Enter admin password:-")
	val = "select * from admin where username =  \'" + str(admin_username)+"\'"
	cur.execute(val)
	rows = cur.fetchone()
	if rows == None:
		print " "
		print "Admin does not exit"
	else:
		password = rows[1]
		if check_password_hash(password, admin_password):
			print " "
			print "Succefully logged in!"
			print " "
			print "Add students!! "
			user_username = raw_input("Enter student username:-")
			user_rollno = raw_input("Enter student rollno:-")
			user_password = "fuckoff"
			book_issued = 0
			user_book_time1 = "null" 
			user_book_time2 = "null"
			user_book_time3 = "null"
			user_book_name1 = "null"
			user_book_name2 = "null"
			user_book_name3 = "null"
			user_fine = 0 
			user_reserve_id = "null"
			val = "select * from users where rollno = \'" + str(user_rollno)+"\'"
			cur.execute(val)
			rows = cur.fetchone()
			if rows == None:
				user = User(user_username, user_rollno, user_password, book_issued, user_book_time1, user_book_time2, user_book_time3, user_fine, user_reserve_id, user_book_name1, user_book_name2, user_book_name3)    
				print "				Student added"
			else:
				print " "
				print "Rollno already exit!"

		else:
			print " "
			print "Admin Password incorrect!"

def del_student():
	print " "
	admin_username = raw_input("Enter admin username:-")
	admin_password = raw_input("Enter admin password:-")
	val = "select * from admin where username =  \'" + str(admin_username)+"\'"
	cur.execute(val)
	rows = cur.fetchone()
	if rows == None:
		print " "
		print "Admin does not exit"
	else:
		password = rows[1]
		if check_password_hash(password, admin_password):
			print " "
			print "Succefully logged in!"
			print " "
			delete_student = raw_input("You want to delete a student (y/n): ")
			
			if delete_student == "Y" or delete_student == "y":
				print " "
				students_list = "select * from users"
				cur.execute(students_list)
				students_roll_list = cur.fetchall()
				print ""
				print " 				Registered Students!"
				print " "
				for i in students_roll_list:
					print i[1]

				print " "	
				roll_no = raw_input("Enter roll no.:-")
				val = "select * from users where rollno = \'" + str(roll_no)+"\'"
				cur.execute(val)
				
				student = cur.fetchone()
				
				if student == None:
					print " "
					print "Student Does not Exit!"
				else:
					book_issued  = student[3]
					fine = student[7]

					print " "
					if book_issued != 0:
						print "He have library books So you cant delete!"
					elif fine != 0:
						print "First take fine from this student!"
						print "So you cant delete"
					else:
						val1 = "delete from users where rollno = \'" + str(roll_no)+"\'"
						val2 = "delete from student_login where rollno = \'" + str(roll_no)+"\'"
						val3 = "delete from record where rollno = \'" + str(roll_no)+"\'"
						cur.execute(val1)
						cur.execute(val2)
						cur.execute(val3)
						conn.commit()


						print " "
						print "Succefully Delete!"
			else:
				
				print " "
				print "				Ok Fine!"
		else:
			print " "
			print "incorrect Password"
					
				

					
						
						
						
						
						
		











def student__login():
	print " "
	student_rollno = raw_input("Enter the student rollno:-")
	student_password = raw_input("Enter the student password:-")
	val = "select * from student_login where rollno = \'" + str(student_rollno)+"\'"
	cur.execute(val)
	rows = cur.fetchone()
	if rows == None:
		print " "
		print "This rollno does not exit!, Please enter again"
	else:
		password = rows[2]
		if check_password_hash(password, student_password):
			fine = rows[3]
			print " "
			print "Your fine is.........!!"
			print fine
			reserve_book = rows[4]
			book_issue = raw_input("You want to reserve a book (y/n): ")
			if book_issue == "Y" or book_issue == "y":
				vall = "select * from books"
				cur.execute(vall)
				books = cur.fetchall()
				if books == ():
					print " "
					print "			No books in library!"
				else:
					print " "
					print " "
					print "			Books id's Are!"
					for i in books:
						print i[1]
				reserve_book = rows[4]
				if reserve_book == "null":
					print " "
					book__id = raw_input("Enter the book_id:-")
					val = "select * from books where book_id = \'" + str(book__id)+"\'"
					cur.execute(val)
					rows = cur.fetchone()
				
					if rows == None:
						print " "
						print "Book id does not match!"
					else:
						val = "update users set reserve_id = \'" + str(book_id)+"\' where rollno = \'" + str(student_rollno)+"\'"
						cur.execute(val)
						conn.commit()
						val1 = "update student_login set reserve_id = \'" + str(book_id)+"\' where rollno = \'" + str(student_rollno)+"\'"
						cur.execute(val1)
						conn.commit()
						val3 = "update record set reserve_id = \'" + str(book_id)+"\' where rollno = \'" + str(student_rollno)+"\'"
						cur.execute(val3)
						conn.commit()
					
				else:
					print " ", 
					print " !Already reserved book"
					print " ", 
					print "your reserve book is ",
					print reserve_book
			else:
				print " ",
				print "your reserve book is ",
				print reserve_book

			print " "
			print " "
			del_reserve = raw_input("You want to delete reserve book (y/n): ")
			if del_reserve == "Y" or del_reserve == "y":
				val = "select * from student_login where rollno =  \'" + str(student_rollno)+"\'"
				cur.execute(val)
				rows = cur.fetchone()
				reserve_book = rows[4]
				if reserve_book == "null":
					print "You have no reserve book so you cant delete anything"
				else:
					del_reserve_id = raw_input("Enter reserve book id which you want to delete-")
					val = "select * from student_login where reserve_id = \'" + str(del_reserve_id)+"\'"
					cur.execute(val)
					rows = cur.fetchone()
					if rows == None:
						print " "
						print "This book is not reserved by you, Please enter correct id "
					else:
						del_book = "null"
						val = "update users set reserve_id =  \'" + str(del_book)+"\' where rollno = \'" + str(student_rollno)+"\'"
						cur.execute(val)
						conn.commit()
						val = "update student_login set reserve_id =  \'" + str(del_book)+"\' where rollno = \'" + str(student_rollno)+"\'"
						cur.execute(val)
						conn.commit()
						val = "update record set reserve_id =  \'" + str(del_book)+"\' where rollno = \'" + str(student_rollno)+"\'"
						cur.execute(val)
						conn.commit()
						print " "
						print "				Delete Succefully!"

						
			else:
				val = "select * from student_login where rollno = \'" + str(student_rollno)+"\'"
				cur.execute(val)
				rows = cur.fetchone()
				reserve_book = rows[4]
				print "Ok fine!"
				print "Your reserve book is",
				print reserve_book
		
			print " "
			change_password = raw_input("You want change your password (y/n): ")
			if change_password == "Y" or change_password == "y":
				changed__password = raw_input("Enter your password:-")
				changed_password = generate_password_hash(changed__password)
				val1 = "update student_login set password = \'" + str(changed_password)+"\' where rollno = \'" + str(student_rollno)+"\'"
				cur.execute(val1)
				conn.commit()
				val2 = "update users set password = \'" + str(changed_password)+"\' where rollno = \'" + str(student_rollno)+"\'"
				cur.execute(val2)
				conn.commit()
				val3 = "update record set password = \'" + str(changed_password)+"\' where rollno = \'" + str(student_rollno)+"\'"
				cur.execute(val3)
				conn.commit()
				
				print changed_password
				print " "
				print " 		Password Succefully Changed!"
			else:
				print "Ok Fine!"

		else:
			print " "
			print "Please enter correct password"
		
		
		
		
		
				

				
				
			


				
				
				
				
				
				








				
				
				
				

			
			



def show_record():
	admin_username = raw_input("Enter admin username:-")
	admin_password = raw_input("Enter admin password:-")
	val = "select * from admin where username =  \'" + str(admin_username)+"\'"
	cur.execute(val)
	rows = cur.fetchone()
	if rows == None:
		print "Admin does not exit"
	else:
		password = rows[1]
		if check_password_hash(password, admin_password):
			print "Succefully logged in!"
			val = "select * from users"
			cur.execute(val)
			students_list = cur.fetchall()
			print " "
			print "		Registered Student list Are!"
			for i in students_list:

				
				
				print i[1]
			print " "
			user_rollno = raw_input("Enter the rollno whose you want to check the recod!-")
			val = "select * from users where rollno =  \'" + str(user_rollno)+"\'"
			cur.execute(val)
			rows = cur.fetchone()
			

			if rows == None:
				print "Roll no. does not exit"
			else:
				print ".......Your record is.......!!"
				

				print "  username  rollno  book_name1  book_name2  book_name3  fine  reserve_id "
				val = "select * from users"
				cur.execute(val)
				rowss = cur.fetchall()
				
				print rows
		else:
			print "Admin Password incorrect"
		

					


def show_fine():
	student_rollno = raw_input("Enter the student rollno-")
	student_password = raw_input("Enter the student password-")
	val = "select * from student_login where rollno = \'" + str(student_rollno)+"\'"
	cur.execute(val)
	rows = cur.fetchone()
	if rows == None:
		print "This rollno does not exit!, Please enter again"
	else:
		x1 = rows[2]
		if check_password_hash(x1, student_password):
			val = "select * from record where rollno =  \'" + str(student_rollno)+"\'"
			cur.execute(val)
			rows = cur.fetchone()
			rows1 = rows[7]
			print "Your fine is"
			print rows1

					

def del_book():
	admin_username = raw_input("Enter admin username:-")
	admin_password = raw_input("Enter admin password:-")
	val = "select * from admin where username =  \'" + str(admin_username)+"\'"
	cur.execute(val)
	rows = cur.fetchone()
	if rows == None:
		print " "
		print "Admin does not exit"
	else:
		rows2 = rows[1]
		if check_password_hash(rows2, admin_password):
			vall = "select * from books"
			cur.execute(vall)
			books = cur.fetchall()
			if books == ():
				print " "
				print "			No books in library!"
			else:
				print " "
				print " "
				print "			Books id's Are!"
				for i in books:
					print i[1]
			book__id = raw_input("Enter the book id which you want to delete-")
			val = "select * from books where book_id = \'" + str(book__id)+"\'"
			cur.execute(val)
			rows = cur.fetchone()
			if rows == None:
				print " "
				print "This book is not available in library"
			else:
				rowss = rows[2]
				if rowss == 0:
					print "This book is issued to someone so you cant delete this book"
				else:
					val = "delete from books where book_id = \'" + str(book__id)+"\'"
					cur.execute(val)
					conn.commit()
					print " "
					print "          Succefully Delete!"
		else:
			print " "
			print "Incorrect Password"			

def show_books():
	print " "
	val = "select * from books"
	cur.execute(val)
	books = cur.fetchall()
	print "-----------------------------------------------"
	print "			Library Books Are!"
	print "-----------------------------------------------"
	print "Book Name     Book Id     Availability"
	for i in books:
		for j in range(len(i)):
			if j == 2:
				if i[j] == "1":
					print "YES   ",
				else:
					print "NO   "
			else:
				print str(i[j]) + "           " ,
		print ""



		
def show_users():
	admin_username = raw_input("Enter admin username:-")
	admin_password = raw_input("Enter admin password:-")
	val = "select * from admin where username =  \'" + str(admin_username)+"\'"
	cur.execute(val)
	rows = cur.fetchone()
	if rows == None:
		print "Admin does not exit"
	else:
		password = rows[1]
		if check_password_hash(password, admin_password):
			print "Succefully logged in"
			val = "select * from users "
			cur.execute(val)
			rows = cur.fetchall()
			if rows == None:
				print "...........No students...........!! "
			else:
				print " "
				print "      Registered Student Are!"

				for i in rows:
					print i[0]     ,      i[1]

					
		else:
			print ""
			print "Incorrect Password!"	


		






#user = User(username="snhdfhg",pashjfgy)
if __name__=='__main__':
	#for display database
	
	print " "
	print " "
	print "		     !!Welcome to Library Management System!!"

	while 1:
		print "--------------------------------------------------------------------------------"
		print "                  <<<<<<<------------Main menu------------>>>>>>>>"
		print "--------------------------------------------------------------------------------"
		print "1- Add a admin"
		print "2- Add books details"
		print "3- Add a user"
		print "4- Delete student"
		print "5- Student login"
		print "6- Check user record"
		
		print "7- Issue a book"
		print "8- Return book"
		print "9- Check your fine"
		print "10- Delete book"
		print "11- Show books"
		print "12- Show users"
		print "13- Exit"
		print " "
		t=input("Enter no:-")

		
		if t == 1:
			another_admin()
			

			
		elif t == 2:
			admin()
			
				


			
			
		

		elif t == 3:
			add_user()
			
			
		elif t == 4:
			del_student()
		
			
		elif t == 5:
			student__login()


		elif t == 6:
			show_record()
			

		

		elif t == 7:
			store()


		elif t == 8:
			fine()


		elif t == 9:
			show_fine()

		elif t == 10:
			del_book()


		elif t == 11:
			show_books()

		
		elif t == 12:
			show_users()

	
		else:
			print " "
			print "			You are about to exit!"
			print "				fuckoff"
			break