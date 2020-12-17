from flask import Flask, render_template, redirect, url_for, request
import sqlite3
app = Flask(__name__)

#method to insert student details into the database

def insertstudentdetails(details):
    ids = [
        'reg_firstname',
        'reg_lastname',
        'reg_password',
        'reg_password_confirm',
        'reg_email',
        'reg_Dob',
        'reg_phno',
        'reg_ssc',
        'reg_sscboard',
        'reg_yop_ssc',
        'reg_inter',
        'reg_yop_inter',
        'reg_board',
        'reg_ug',
        'reg_university',
        'reg_yop_board',
        'reg_cv'
    ]
    #try and except to minimize any error
    try:
        #details are student details
        #table name studentdetails
        #connecting to database
        with sqlite3.connect('database.db') as db:
            cursor = db.cursor()
            #write sql statement
            statement = 'insert into studentdetails values('
            for i in ids:
                try:
                    if i == 'reg_cv':
                        statement += '\''+str(details[i])+'\''
                    else:
                        statement += '\''+str(details[i])+'\''+','
                except:
                    pass
            statement += ')'
            #execute the statement
            cursor.execute(statement)
    except Exception as e:
        print(e)
#to insert recruiter details
def insertrecruiterdetails(details):
    ids = [
        'reg_Companyname',
        'reg_CompanyId',
        'reg_password',
        'reg_password_confirm',
        'reg_email',
        'reg_phnnumber',
        'reg_address',
        'reg_criteria',
        'reg_date',
        'reg_Job'

    ]
    #try and except to minimize any error
    try:
        #details are student details
        #table name studentdetails
        #connecting to database
        with sqlite3.connect('database.db') as db:
            cursor = db.cursor()
            #write sql statement
            statement = 'insert into recruiterdetails values('
            for i in ids:
                try:
                    if i == 'reg_Job':
                        statement += '\''+str(details[i])+'\''
                    else:
                        statement += '\''+str(details[i])+'\''+','
                except:
                    pass
            statement += ')'
            #execute the statement
            cursor.execute(statement)
    except Exception as e:
        print(e)

@app.route('/',methods = ['GET','POST'])
def home():
    if request.method == 'POST':
        print('in post')
        try:
            if request.form['buttons'] == 'Login / Sign Up':
                return redirect('/login')
        except:
            pass
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            with sqlite3.connect('database.db') as db:
                #getting password for the given username from student side
                try:
                    statement = 'select reg_password from studentdetails where reg_email = \'{}\''.format(username)
                    cursor = db.cursor()
                    cursor.execute(statement)
                    val = cursor.fetchone()
                    print(val)
                    if val[0] == password:
                        studentid = username
                        st = 'delete from user'
                        cursor.execute(st)
                        st = 'insert into user values(\"{}\")'.format(username)
                        cursor.execute(st)
                        return redirect('/studentlogin')
                except:
                    pass
                statement = 'select reg_password from recruiterdetails where reg_email = \'{}\''.format(username)
                cursor = db.cursor()
                cursor.execute(statement)
                val = cursor.fetchone()
                print(val)
                if val[0] == password:
                    st = 'delete from user'
                    cursor.execute(st)
                    st = 'insert into user values(\"{}\")'.format(username)
                    cursor.execute(st)
                    return redirect('/recruiterhome')
        except:
            pass
        try:
            if request.form['buttons'] == 'Click Here':
                return redirect('/forgotpassword')
        except:
            pass
        try:
            if request.form['buttons'] == 'Create account for Student':
                return redirect('/studentregister')
        except:
            pass
        try:
            if request.form['buttons'] == 'Create account for Recruiter':
                return redirect('/recruiterregistration')
        except:
            pass
    return render_template('login.html', error=error)


@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgetpassword():
    if request.method == 'POST':
        username = request.form['reg_email']
        passwoord = request.form['reg_password']
        cpassword = request.form['reg_password_confirm']
        if username != "" and passwoord != "" and cpassword != "":
            with sqlite3.connect('database.db') as db:
                statement = 'update studentdetails set reg_password=\"{}\" , reg_password_confirm=\"{}\"'.format(passwoord,cpassword)
                cursor = db.cursor()
                cursor.execute(statement)
            return redirect('/login')
    return render_template('forgotpass.html')

@app.route('/studentregister', methods=['GET', 'POST'])
def studentregister():
    ids = [
        'reg_firstname',
        'reg_lastname',
        'reg_password',
        'reg_password_confirm',
        'reg_email',
        'reg_Dob',
        'reg_phno',
        'reg_ssc',
        'reg_sscboard',
        'reg_yop_ssc',
        'reg_inter',
        'reg_yop_inter',
        'reg_board',
        'reg_ug',
        'reg_university',
        'reg_yop_board',
        'reg_cv'
    ]
    studentdetails = {}
    #getting student details from html and storing in studentdails dictionery
    if request.method == 'POST':
        for i in ids:
            try:
                studentdetails[i] = request.form[i]
            except:
                studentdetails[i] = None
        #inserting the collected information to the database
        #call above method

        insertstudentdetails(studentdetails)

        #after registering successfully redirecting to login page

        return redirect('/login')

    return render_template('register.html')


@app.route('/createstudentdatabase')
def createstudentdatabase():
    try:
        with sqlite3.connect('database.db') as db:
            statement = '''create table studentdetails(
                reg_firstname,
                reg_lastname,
                reg_password,
                reg_password_confirm,
                reg_email,
                reg_Dob,
                reg_phno,
                reg_ssc,
                reg_sscboard,
                reg_yop_ssc,
                reg_inter,
                reg_yop_inter,
                reg_board,
                reg_ug,
                reg_university,
                reg_yop_board,
                reg_cv
            )'''

            cursor = db.cursor()

            try:
                cursor.execute(statement)
            except Exception as e:
                print(e)
    except:
        return 'some error occured'
    return 'created table'



#details in student database
@app.route('/checkstudentdb')
def checkstudentdb():
    s = ''
    try:
        with sqlite3.connect('database.db') as db:
            statement = 'select * from studentdetails'
            cursor = db.cursor()
            cursor.execute(statement)
            data = cursor.fetchall()
            for i in data:
                s += str(i)
    except:
        return 'some error'
    return s


#recruiter registration page
#should pass the methos
@app.route('/recruiterregistration', methods=['GET', 'POST'])
def recruiterregister():
    ids = [
        'reg_Companyname',
        'reg_CompanyId',
        'reg_password',
        'reg_password_confirm',
        'reg_email',
        'reg_phnnumber',
        'reg_address',
        'reg_criteria',
        'reg_date',
        'reg_Job',

    ]
    recruiterdetails = {}
    if request.method == 'POST':
        #check whether the details are available 
        for i in ids:
            try:
                recruiterdetails[i] = request.form[i]
            except:
                recruiterdetails[i] = None
        insertrecruiterdetails(recruiterdetails)
        return redirect('/login')
    #method to insert these values

    return render_template('register1.html')

#create table for recruiters

@app.route('/createrecruiterdatabase')
def createrecruiterdatabase():
    try:
        with sqlite3.connect('database.db') as db:
            statement = '''create table recruiterdetails(
                reg_Companyname,
                reg_CompanyId,
                reg_password,
                reg_password_confirm,
                reg_email,
                reg_phnnumber,
                reg_address,
                reg_criteria,
                reg_date,
                reg_Job
            )'''

            cursor = db.cursor()

            try:
                cursor.execute(statement)
            except Exception as e:
                print(e)
    except:
        return 'some error occured'
    return 'created table'


#checking recruiter detail database
@app.route('/checkrecruiterdb')
def checkrecruitertdb():
    s = ''
    try:
        with sqlite3.connect('database.db') as db:
            statement = 'select * from recruiterdetails'
            cursor = db.cursor()
            cursor.execute(statement)
            data = cursor.fetchall()
            for i in data:
                s += str(i)
    except:
        return 'some error'
    return s

@app.route('/about')
def about():
    return render_template('index2.html')

@app.route('/contact')
def contact():
    return render_template('contact.html.html')

#student home page
@app.route('/studentlogin')
def studentlogin():
    return render_template('training.html.html')

@app.route('/checkrender',methods = ['GET','POST'])
def checkrender():
    studentid = ''
    studentgpa = 0
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        stat = 'select * from user'
        cursor.execute(stat)
        data = cursor.fetchone()
        #print(data)
        studentid = data[0]
        stat = 'select * from studentdetails where reg_email = \"{}\"'.format(studentid)
        cursor.execute(stat)
        data = cursor.fetchone()
        try:
            studentgpa = float(data[13])
        except:
            pass
    print(studentgpa)
    studentappplied = {}
    try:
        with sqlite3.connect('database.db') as db:
            cursor = db.cursor()
            statement = '''select * from appliedjobs'''
            cursor.execute(statement)
            data = cursor.fetchall()
            #print(data)
            for i in data:
                if i[0] not in studentappplied:
                    studentappplied[i[0]] = [i[1]]
                else:
                    studentappplied[i[0]].append(i[1])
    except Exception as e:
        print(e)
    if request.method == 'POST':
        #print(studentappplied,studentid)
        compid = request.form.get('apply')
        try:
            with sqlite3.connect('database.db') as db:
                cursor = db.cursor()
                statement = '''insert into appliedjobs values("{}","{}")'''.format(studentid,compid)
                cursor.execute(statement)
                return redirect('/application')
        except:
            pass
    ids = [
        'reg_Companyname',
        'reg_CompanyId',
        'reg_password',
        'reg_password_confirm',
        'reg_email',
        'reg_phnnumber',
        'reg_address',
        'reg_criteria',
        'reg_date',
        'reg_Job',

    ]
    output = '<table border=\"1\" style="width:100%">'
    output += '''<tr border=\"0\">
        <th>Company Name</th>
        <th>Company ID</th>
        <th>Company Email</th>
        <th>Company Phone No</th>
        <th>Eligibility Criteria</th>
        <th>Job</th>
        <th>Your Eligibility</th>
    </tr>'''
    try:
        with sqlite3.connect('database.db') as db:
            statement = 'select * from recruiterdetails'
            cursor = db.cursor()
            cursor.execute(statement)
            data = cursor.fetchall()
            indexes = [0,1,4,5,7,9]
            for i in data:
                tmp = '<tr>'
                eligible = False
                for j in indexes:
                    tmp += '<td>{}</td>'.format(i[j])
                try:
                    if studentgpa >= float(i[7]):
                        tmp += '<td>Eligible</td>'
                        eligible = True
                    else:
                        tmp += '<td>Not Eligible</td>'
                except:
                    tmp += '<td>Not Eligible</td>'
                if not eligible:
                    tmp += '<td>Cannot Apply</td>'
                else:
                    try:
                        print('student id',studentappplied[studentid])
                        if i[4] in studentappplied[studentid]:
                            tmp +='''
                            <td>
                                Applied
                            </td>
                            '''
                        else:
                            tmp +='''
                            <td>
                                <form action = "" method = "post">
                                <button type="submit" name="apply" value = "{}">apply</button>
                                </form>
                            </td>
                            '''.format(i[4])

                    except:
                        tmp +='''
                            <td>
                                <form action = "" method = "post">
                                <button type="submit" name="apply" value = "{}">apply</button>
                                </form>
                            </td>
                            '''.format(i[4])
                    tmp += '</tr>'
                output += tmp
    except:
        pass
    output += '</table>'
    output += '<a href = \"studentlogin\">Go to Home</a>'
    return output

@app.route('/applied')
def applied():
    try:
        with sqlite3.connect('database.db') as db:
            statement = '''create table appliedjobs(
                studentid,companyid
            )'''
            cursor = db.cursor()
            try:
                cursor.execute(statement)
            except Exception as e:
                print(e)
    except:
        return 'some error occured'
    return 'created table'

@app.route('/checkapplied')
def checkapplied():
    s = ''
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        statement = '''select * from appliedjobs'''
        cursor.execute(statement)
        A = cursor.fetchall()
        for i in A:
            s += str(i)
    return s

@app.route('/createuser')
def createuser():
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        statement = 'create table user(\"username\")'
        cursor.execute(statement)
    return 'yes'


@app.route('/recruiterhome')
def recruiterhome():
    recruiterid = ''
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        stat = 'select * from user'
        cursor.execute(stat)
        data = cursor.fetchone()
        #print(data)
        recruiterid = data[0]
    print(recruiterid)
    studentappplied = {}
    try:
        with sqlite3.connect('database.db') as db:
            cursor = db.cursor()
            statement = '''select * from appliedjobs'''
            cursor.execute(statement)
            data = cursor.fetchall()
            print(data)
            for i in data:
                if i[1] not in studentappplied:
                    studentappplied[i[1]] = [i[0]]
                else:
                    studentappplied[i[1]].append(i[0])
    except Exception as e:
        print(e)
    #print(studentappplied)
    ids = [
        'reg_firstname',
        'reg_lastname',
        'reg_password',
        'reg_password_confirm',
        'reg_email',
        'reg_Dob',
        'reg_phno',
        'reg_ssc',
        'reg_sscboard',
        'reg_yop_ssc',
        'reg_inter',
        'reg_yop_inter',
        'reg_board',
        'reg_ug',
        'reg_university',
        'reg_yop_board',
        'reg_cv'
    ]
    output = '<table border=\"1\" style="width:100%">'
    output += '''<tr border=\"0\">
        <th>First Name</th>
        <th>Last Name</th>
        <th>Email</th>
        <th>Phone No</th>
    </tr>'''
    try:
        with sqlite3.connect('database.db') as db:
            statement = 'select * from studentdetails'
            cursor = db.cursor()
            cursor.execute(statement)
            data = cursor.fetchall()
            indexes = [0,1,4,6]
            for i in data:
                tmp = '<tr>'
                try:
                    print(i[4])
                    if i[4] in studentappplied[recruiterid]:
                        
                        for j in indexes:
                            tmp += '<td>{}</td>'.format(i[j])
                except:
                    pass
                
                tmp += '</tr>'
                output += tmp
    except:
        pass
    output += '</table>'

    output += '<a href = \"login\">Logout<a>'
    return output

@app.route('/mocktest')
def mocktest():
    return render_template('test.html')

@app.route('/files')
def files():
    return render_template('files.html')


@app.route('/videogallery')
def videogallery():
    return render_template('video gallery.html')

@app.route('/application')
def application():
    return render_template('application.html')

@app.route('/editstudentdetails',methods = ['GET','POST'])
def editdetails():
    ids = [
        'reg_firstname',
        'reg_lastname',
        'reg_phno',
        'reg_ssc',
        'reg_sscboard',
        'reg_yop_ssc',
        'reg_inter',
        'reg_yop_inter',
        'reg_board',
        'reg_ug',
        'reg_university',
        'reg_yop_board',
    ]
    #request.form['reg_firstname'] = 'sainath'
    data = []
    studentid = ''
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        stat = 'select * from user'
        cursor.execute(stat)
        data = cursor.fetchone()
        #print(data)
        studentid = data[0]
        stat = 'select * from studentdetails where reg_email = \"{}\"'.format(studentid)
        cursor.execute(stat)
        data = cursor.fetchone()
    #print(data)
    if request.method == 'POST':
        #print('post')
        #print(request.form['reg_firstname'])
        statement = 'update studentdetails set '
        b = False
        for i in ids:
            if request.form[i] != "":
                b = True
                statement += i +'= \"{}\"'.format(request.form[i])
        statement += ' where reg_email = \"{}\"'.format(studentid)
        with sqlite3.connect('database.db') as db:
            cursor =db.cursor()
            if b:cursor.execute(statement)
        #print(statement)
        return redirect('/studentlogin')
    return render_template('editstudentdetails.html',firstname=data[0],lastname=data[1],phoneno=data[6]
    ,sscgpa=data[7],sscboard=data[8],boardyop=data[9],intergpa=data[10],interyop=data[11],interboard=data[12],uggpa=data[13],
    affliated=data[14],ugyop=data[15]
    )