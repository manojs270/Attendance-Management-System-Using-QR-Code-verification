from ast import While
from sre_constants import SUCCESS
import cv2
from flask import Flask ,render_template, request, redirect, url_for, session
from datetime import datetime
from urllib import response
from flask_mysqldb import MySQL
import MySQLdb.cursors
import hashlib
import random  
import string
from pymysql import NULL
import qrcode
from pyzbar.pyzbar import decode
import os
import mysql.connector
import time
import uuid


app = Flask(__name__)

app.secret_key = 'secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'square'

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="square"
)

mycursor = mydb.cursor()
# cursor = MySQL.connect.cursor(MySQLdb.cursors.DictCursor)
# Intialize MySQL
mysqls = MySQL(app)


@app.route('/classroom/', methods=['GET', 'POST'])
def room_login():
    msg = ''
    # Check if "emailid" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'roomno' in request.form and 'password' in request.form:
        # Create variables for easy access
        roomno = request.form['roomno']
        password = request.form['password']
        result = hashlib.md5(password.encode())
        password = result.hexdigest()
        # Check if account exists using MySQL
        cursor = mysqls.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM room WHERE room_no = %s AND password = %s',(roomno, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['room_no'] = account['room_no']
            render_template('classroom_index.html')
            # Redirect to home page
            qrcodes()
            
            return render_template('classroom_index.html')
            
        else:
            # Account doesnt exist or emailid/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('class_login.html', msg=msg)


@app.route('/teacher/', methods=['GET', 'POST'])
def teacher_login():
    msg = ''
    # Check if "emailid" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'emails' in request.form and 'password' in request.form:
        # Create variables for easy access
        emails = request.form['emails']
        password = request.form['password']
        result = hashlib.md5(password.encode())
        password = result.hexdigest()
        # Check if account exists using MySQL
        cursor = mysqls.connection.cursor(MySQLdb.cursors.DictCursor)
        result = {}
        cursor.execute('SELECT * FROM teacher WHERE email_id = %s AND password = %s', (emails, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['email_id'] = account['email_id']
            
            nam = account['name']
            email = account['email_id']
            phone = account['phone_no']
            qualification = account['qualification']
            course = account['course']
            subject = account['subject']
            mycursor.execute('SELECT id FROM subject WHERE name LIKE %s',[subject])
            subid = mycursor.fetchall()
            subi = subid[0][0]
            mycursor.execute('SELECT student_id,student_average,student_total,teacher_total FROM attendence WHERE teacher_id LIKE %s',[session['id']])
            prints = mycursor.fetchall()
            for abc in prints:
                subid = abc[0]
                subat = int(abc[1])
                stuto = int(abc[2])
                teachs = int(abc[3])
                avgs = int((stuto/teachs)*100)
                mycursor.execute('update attendence SET student_total = %s,student_average = %s WHERE student_id = %s AND subject_id = %s', (stuto,avgs,subid,subi))
                # Fetch one record and return result
                print("successfully working")
                mydb.commit()
            mycursor.execute('SELECT student_id,student_average FROM attendence WHERE teacher_id LIKE %s',[session['id']])
            prin = mycursor.fetchall()
            result = {}
            for da in prin:
                stuid = da[0]
                subat = da[1]
                mycursor.execute('SELECT name FROM student WHERE id LIKE %s',[stuid])
                subname = mycursor.fetchall()
                for x in subname:
                    print(x[0])
                    subn = x[0]
                result.update({subn: subat})
                # Redirect to home page
            return render_template('teacher_index.html', msg=msg,nam = nam,email=email,phone=phone,qualification=qualification,course=course,subject=subject,result=result)
            
        else:
            # Account doesnt exist or emailid/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('teacher_login.html', msg=msg)


@app.route('/student/', methods=['GET', 'POST'])
def student_login():
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])

    msg = ''
    # Check if "emailid" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'emails' in request.form and 'password' in request.form:
        # Create variables for easy access
        emails = request.form['emails']
        password = request.form['password']
        result = hashlib.md5(password.encode())
        password = result.hexdigest()
        print(password)
        # Check if account exists using MySQL
        cursor = mysqls.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student WHERE email = %s AND password = %s', (emails, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        if account:
            macaddr = account['student_mac']
            email = account['email']
            print(macaddr)
            # If account exists in accounts table in out database
            if(macaddr == mac):
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['id']
                session['email'] = account['email']
                nam = account['name']
                email = account['email']
                phone = account['phone_number']
                course = account['course']
                semester = account['semester']
                mycursor.execute('SELECT subject_id,student_average FROM attendence WHERE student_id LIKE %s',[session['id']])
                prin = mycursor.fetchall()
                result = {}
                for da in prin:
                    subid = da[0]
                    subat = da[1]
                    mycursor.execute('SELECT name FROM subject WHERE id LIKE %s',[subid])
                    subname = mycursor.fetchall()
                    for x in subname:
                        print(x[0])
                        subn = x[0]
                    result.update({subn: subat})
                return render_template('student_index.html',nam = nam, email = email,phone=phone,course=course,semester=semester,result=result)
            elif(macaddr == '0'):
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['id']
                session['email'] = account['email']
                # Redirect to home page
                # details()
                nam = account['name']
                email = account['email']
                phone = account['phone_number']
                course = account['course']
                semester = account['semester']
                mycursor.execute('SELECT subject_id,student_average FROM attendence WHERE student_id LIKE %s',[session['id']])
                prin = mycursor.fetchall()
                result = {}
                for da in prin:
                    subid = da[0]
                    subat = da[1]
                    print(subat)
                    mycursor.execute('SELECT name FROM subject WHERE id LIKE %s',[subid])
                    subname = mycursor.fetchall()
                    for x in subname:
                        subn = x[0]
                        print(subn)
                    result.update({subn: subat})
                mycursor.execute('UPDATE student SET student_mac = %s WHERE id = %s',(mac,session['id']))
                # Fetch one record and return result
                mydb.commit()
                return render_template('student_index.html',nam = nam, email = email,phone=phone,course=course,semester=semester,result=result)
            else:
                print('wrong mac')
                msg = 'Your device mac address did not match! Use the device used before else contact ADMIN'
        else:
                    # Account doesnt exist or emailid/password incorrect
                    msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('student_login.html', msg=msg)


@app.route('/squares/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('emailid', None)
   # Redirect to login page
   return render_template('mainindex.html')

@app.route('/qrcode')
def qrcodes():
    render_template('classroom_index.html')
    fname = session['room_no']
    length = 3
    randomstr =''.join((random.choice(string.ascii_lowercase) for x in range(length)))
    mycursor.execute('update room SET qrvalue = %s WHERE room_no LIKE %s', [randomstr,fname])
    # Fetch one record and return result
    mydb.commit()
    lis = [fname,randomstr]
    print(lis)
    img = qrcode.make(lis)
    path = img.save('./static/assets/img/qrcodes/'+fname+'.png')
    print("successfully changed")
    return render_template('classroom_index.html')

@app.route('/mark attendance')
def student_cam():
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    refresh = camera = True
    while camera == True:
        SUCCESS, frame = cap.read()
        cv2.imshow('Place the code inside camera frame',frame)
        cv2.waitKey(1)
        for code in decode(frame):
            val = code.data.decode('utf-8')
            x = val[2]
            y = val[3]
            z = val[4]
            roomno = f'{(x+y+z)}'
            a=val[9]
            b=val[10]
            c=val[11]
            qrval = f'{(a+b+c)}'
            cursor = mysqls.connection.cursor(MySQLdb.cursors.DictCursor)
            mycursor.execute('SELECT qrvalue FROM room WHERE room_no LIKE %s',[roomno])
            fetch = mycursor.fetchone()
            for da in fetch:
                q1 = da[0]
                q2 = da[1]
                q3 = da[2]
                qrvals = f'{(q1+q2+q3)}'
            
            if(qrval == qrvals):
                cursor.execute('SELECT * FROM attendence WHERE student_id LIKE %s', [session['id']])
                details = cursor.fetchone()
                print(details)

                mycursor.execute('INSERT INTO buffer (student_id, room_no) VALUES (%s, %s)', [session['id'], roomno])
                    # Fetch one record and return result
                mydb.commit()
                print('successfully comitted')
                exit
                camera = False
    mycursor.execute('SELECT subject_id,student_average FROM attendence WHERE student_id LIKE %s',[session['id']])
    prin = mycursor.fetchall()
    result = {}
    for da in prin:
        subid = da[0]
        subat = da[1]
        mycursor.execute('SELECT name FROM subject WHERE id LIKE %s',[subid])
        subname = mycursor.fetchall()
        for x in subname:
            print(x[0])
            subn = x[0]
        result.update({subn: subat})
            
    print('scanned successfully')
    return render_template('student_index.html',result=result)

@app.route('/attendance')
def teacher_cam():
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    camera = True
    while camera == True:
        SUCCESS, frame = cap.read()
        cv2.imshow('Place the code inside camera frame',frame)
        cv2.waitKey(1)
        for code in decode(frame):
            val = code.data.decode('utf-8')
            x = val[2]
            y = val[3]
            z = val[4]
            roomno = f'{(x+y+z)}'
            print(roomno)
            a=val[9]
            b=val[10]
            c=val[11]
            qrval = f'{(a+b+c)}'
            #to fetch all the details of attendance
           
            cursor = mysqls.connection.cursor(MySQLdb.cursors.DictCursor)
            mycursor.execute('SELECT qrvalue FROM room WHERE room_no LIKE %s',[roomno])
            fetch = mycursor.fetchone()
            for da in fetch:
                q1 = da[0]
                q2 = da[1]
                q3 = da[2]
                qrvals = f'{(q1+q2+q3)}'
            mycursor.execute('SELECT subject FROM teacher WHERE email_id LIKE %s',[session['email_id']])
            sub = mycursor.fetchall()
            subname = sub[0][0]

            mycursor.execute('SELECT id FROM subject WHERE name LIKE %s',[subname])
            subid = mycursor.fetchall()
            subi = subid[0][0]
            # print(subi)
            if(qrval == qrvals):
                mycursor.execute('SELECT COUNT(*) FROM buffer WHERE room_no LIKE %s',[roomno])
                subs = mycursor.fetchall()
                i=subs[0][0]
                mycursor.execute('SELECT COUNT(*) FROM attendence WHERE subject_id LIKE %s',[subi])
                teacount = mycursor.fetchall()
                con = teacount[0][0]
                print(con)
                mycursor.execute('SELECT teacher_total FROM attendence WHERE subject_id like %s order by teacher_total DESC',[subi])
                tea = mycursor.fetchall()
                print(tea)
                if(tea != []):
                    teach = tea[0][0]
                    teach = int(teach)
                    teach = teach+1
                    mycursor.execute('SELECT * FROM attendence WHERE subject_id LIKE %s',[subi])
                    upda = mycursor.fetchall()
                    print(upda)
                    
                    for f in (range(i)):
                        #to fetch buffer
                        if(upda != []):
                            mycursor.execute('update attendence SET teacher_total = %s WHERE subject_id = %s', (teach,subi))
                                # Fetch one record and return result
                            mydb.commit()
                            mycursor.execute('SELECT student_id FROM buffer WHERE room_no LIKE %s order by student_id ASC',[roomno])
                            acce = mycursor.fetchall()
                            print(acce)
                            # print(attend)
                            substu = acce[0][0]
                            print(substu)
                            mycursor.execute('SELECT student_total FROM attendence WHERE student_id LIKE %s AND subject_id like %s',([substu,subi]))
                            attend = mycursor.fetchall()
                            print(attend)
                            if(attend!= []):
                                stud = attend[0][0]
                                stud = int(stud)
                                stud = stud+1
                                average = int((stud/teach)*100)
                                print('successful')
                                mycursor.execute('update attendence SET student_total = %s,student_average = %s WHERE student_id = %s AND subject_id = %s', (stud,average,substu,subi))
                                # Fetch one record and return result
                                mydb.commit()
                                mycursor.execute('UPDATE attendence SET room_no = %s WHERE student_id = %s',('',substu))
                                # Fetch one record and return result
                                mydb.commit()
                                mycursor.execute('DELETE from buffer WHERE student_id LIKE %s',[substu])
                                # Fetch one record and return result
                                mydb.commit()
                            else:
                                stud = 1
                                print(teach)
                                average = int((stud/teach)*100)
                                mycursor.execute('INSERT into attendence (teacher_id, student_id, subject_id, teacher_total, student_total,student_average) VALUES (%s, %s, %s, %s, %s, %s)', (session['id'],substu,subi,teach, stud,average))
                                # Fetch one record and return result
                                mydb.commit()
                                print('done!')
                                mycursor.execute('DELETE from buffer WHERE student_id LIKE %s',[substu])
                                # Fetch one record and return result
                                mydb.commit()
                else:
                    for d in (range(i)):
                        mycursor.execute('SELECT student_id FROM buffer WHERE room_no LIKE %s order by student_id ASC',[roomno])
                        acce = mycursor.fetchall()
                        print(acce)
                        # print(attend)
                        substu = acce[0][0]
                        print(substu)
                        teach = 1
                        stud = 1
                        average = 100
                        mycursor.execute('INSERT into attendence (teacher_id, student_id, subject_id, teacher_total, student_total,student_average) VALUES (%s, %s, %s, %s, %s, %s)', (session['id'],substu,subi,teach, stud,average))
                        # Fetch one record and return result
                        mydb.commit()
                        print('done!')
                        mycursor.execute('UPDATE buffer SET room_no = %s, student_id = %s WHERE student_id = %s',('','',substu))
                        # Fetch one record and return result
                        mydb.commit()
                        
                exit
                camera = False
    mycursor.execute('SELECT student_id,student_average,student_total FROM attendence WHERE teacher_id LIKE %s',[session['id']])
    prints = mycursor.fetchall()
    for abc in prints:
        subid = abc[0]
        subat = abc[1]
        stuto = int(abc[2])
        avgs = int((stuto/teach)*100)
        mycursor.execute('update attendence SET student_total = %s,student_average = %s WHERE student_id = %s AND subject_id = %s', (stuto,avgs,subid,subi))
        # Fetch one record and return result
        print("successfully working")
        mydb.commit()
    mycursor.execute('SELECT subject_id,student_average FROM attendence WHERE teacher_id LIKE %s',[session['id']])
    prin = mycursor.fetchall()
    result = {}
    for da in prin:
        subid = da[0]
        subat = da[1]
        mycursor.execute('SELECT name FROM subject WHERE id LIKE %s',[subid])
        subname = mycursor.fetchall()
        for x in subname:
            print(x[0])
            subn = x[0]
        result.update({subn: subat})
    render_template('teacher_index.html',result=result)
            
            
    print('scanned successfully')
    return render_template('teacher_index.html',result=result)

@app.route('/')
def index():
    if 'loggedin' in session and session['room_no']:
        # User is loggedin show them the home page
        return render_template('classroom_index.html', emailid=session['room_no'])
    # User is not loggedin redirect to login page
    #return redirect(url_for('room_login'))
   
    elif 'loggedin' in session and session['email_id']:
        # User is loggedin show them the home page
        return render_template('teacher_index.html', emailid=session['email_id'])
    # User is not loggedin redirect to login page
    #return redirect(url_for('room_login'))
    elif 'loggedin' in session and session['email']:
        # User is loggedin show them the home page
        return render_template('student_index.html', emailid=session['email'])
    # User is not loggedin redirect to login page
    else:
        return render_template('mainindex.html')   

if __name__ == '__main__':
   app.run(debug = True)


# @app.route('/student')
# def attendance():
#     #cursor = mysqls.connection.cursor(MySQLdb.cursors.DictCursor)
#     mycursor.execute('SELECT COUNT(*) FROM attendence WHERE student_id LIKE %s',[session['id']])
#     con = mycursor.fetchall()
#     mycursor.execute('SELECT subject_id,student_average FROM attendence WHERE student_id LIKE %s',[session['id']])
#     prin = mycursor.fetchall()
#     result = {}
#     str = 'sub'
#     for da in prin:
#         subid = da[0]
#         subat = da[1]
#         mycursor.execute('SELECT name FROM subject WHERE id LIKE %s',[subid])
#         subname = mycursor.fetchall()
#         for x in subname:
#             print(x[0])
#             subn = x[0]
#         result.update({subn: subat})
#     return render_template('student_index.html',result=result)

