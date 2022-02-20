from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3
from datetime import datetime, date
#import totaldays

app = Flask(__name__)
app.secret_key = "secret"

#Login
@app.route('/')
def login():
    if "red" in session:
        return redirect(url_for(session["red"]))
    return render_template("login.html")

#Credentials Checking
@app.route('/check', methods=["GET", "POST"])
def check():
    if "red" in session:
        return redirect(url_for(session["red"]))
    else:
        if request.method == "POST":
            a = request.form.get("username")
            b = request.form.get("password")
            connect = sqlite3.connect('TurtlesHospital.db')
            cursor = connect.cursor()
            X = cursor.execute("select * from credentials where username='%s' and password='%s' and role='%s'" % (a, b, "admission"))
            for x in X:
                if x[0]==a and x[1]==b and x[2]=="admission":
                    cursor.execute("update credentials set logtime='%s' where username='%s'" % (datetime.utcnow(), a))
                    connect.commit()
                    session["username"] = request.form.get("username")
                    session["red"] = "admission"                    # red = Redirect
                    return redirect(url_for("ade"))
            X = cursor.execute("select * from credentials where username='%s' and password='%s' and role='%s'" % (a, b, "pharmacist"))
            for x in X:
                if x[0]==a and x[1]==b and x[2]=="pharmacist":
                    cursor.execute("update credentials set logtime='%s' where username='%s'" % (datetime.utcnow(), a))
                    connect.commit()
                    session["username"] = request.form.get("username")
                    session["red"] = "pharmacist"                   # red = Redirect
                    return redirect(url_for("pharmacist"))
            X = cursor.execute("select * from credentials where username='%s' and password='%s' and role='%s'" % (a, b, "diagnostic"))
            for x in X:
                if x[0]==a and x[1]==b and x[2]=="diagnostic":
                    cursor.execute("update credentials set logtime='%s' where username='%s'" % (datetime.utcnow(), a))
                    connect.commit()
                    session["username"] = request.form.get("username")
                    session["red"] = "diagnostic"                   # red = Redirect
                    return redirect(url_for("diagnostic"))
            else:
                return redirect('/')

#Logout
@app.route('/logout')
def logout():
    if "username" or "red" in session:
        session.pop("username", None)
        session.pop("red", None)
        return render_template("login.html")
    else:
        return render_template("login.html")


#ADMISSION HOME
@app.route('/ade')
def ade():
    if "red" in session and "admission" in session["red"]:
        return render_template('ade.html')
    else:
        return redirect('/')

#Create patient
@app.route('/ade/create', methods=['GET', 'POST'])
def ade_create():
    if "red" in session and "admission" in session["red"]:
        if request.method == "POST":
            try:
                ssnId = request.form['ssnId']
                name = request.form["name"]
                age = request.form["age"]
                doa = request.form["doa"]
                tob = request.form["tob"]
                address = request.form["address"]
                city = request.form["city"]
                state = request.form["stt"]
                with sqlite3.connect("TurtlesHospital.db") as con:
                    cur = con.cursor()
                    cur.execute("INSERT into patient (SSNId, Name, Age, DOA, TOB, Address, City, State, Status) values (?,?,?,?,?,?,?,?,?)", (ssnId, name, age, doa, tob, address, city, state, 'Active'))
                    con.commit()
                    session['msg'] = "Patient creation initiated successfully"
            except:
                session['err'] = "We can not add the patient to the list"
            finally:
                return redirect(url_for('ade'))
                con.close()
        else:
            return render_template('ade_create.html')
    else:
        return redirect('/')

#View all patients
@app.route('/ade/view', methods=['GET', 'POST'])
def ade_view():
    if "red" in session and "admission" in session["red"]:
        try:
            with sqlite3.connect("TurtlesHospital.db") as con:
                cur = con.cursor()
                patients = cur.execute("SELECT * FROM patient")
        except:
            session['err'] = "Can not fetch the patient's details"
        finally:
            return render_template("ade_view.html", patients=patients)
            con.close()
    else:
        return redirect('/')

#Update patient
@app.route('/ade/update/<int:pid>', methods=['GET', 'POST'])
def ade_update(pid):
    if "red" in session and "admission" in session["red"]:
        if request.method == "POST":
            try:
                name = request.form["name"]
                age = request.form["age"]
                doa = request.form["doa"]
                tob = request.form["tob"]
                address = request.form["address"]
                city = request.form["city"]
                state = request.form["stt"]
                with sqlite3.connect("TurtlesHospital.db") as con:
                    cur = con.cursor()
                    cur.execute(
                        "update patient set Name='%s', Age='%s', DOA='%s', TOB='%s', Address='%s', City='%s', State='%s' where pid='%d'" % (name, age, doa, tob, address, city, state, pid))
                    con.commit()
                    cur.execute("SELECT * FROM patient WHERE pid='%d'" % (pid))
                    # patient = cur.fetchone()
                    session['msg'] = "Patient update initiated successfully"
            except:
                session['err'] = "Can not update patient's details. Please try again!"
            finally:
                return redirect(url_for('ade'))
                con.close()
        else:
            try:
                with sqlite3.connect("TurtlesHospital.db") as con:
                    cur = con.cursor()
                    cur.execute("SELECT * FROM patient WHERE pid='%d'" % (pid))
                    patient = cur.fetchone()
            except:
                session['err'] = "We can not fetch patient's data"
            finally:
                return render_template("ade_update.html", patient=patient)
                con.close()
    else:
        return redirect('/')

#Delete patient
@app.route('/ade/delete/<int:pid>')
def ade_delete(pid):
    if "red" in session and "admission" in session["red"]:
        try:
            with sqlite3.connect("TurtlesHospital.db") as con:
                today = date.today()
                cur = con.cursor()
                cur.execute("UPDATE patient SET Status='%s', Dis_Time='%s' WHERE pid='%d'" % ('Discharged', today.strftime("%d/%m/%Y"), pid))
                session['msg'] = "Patient deletion initiated successfully"
        except:
            session['err'] = "We can not delete patient's data right now. Please try again!"
        finally:
            return redirect(url_for('ade'))
            con.close()
    else:
        return redirect('/')

#Search patient
@app.route('/ade/search', methods=["GET", "POST"])
def ade_search():
    if "red" in session and "admission" in session["red"]:
        if request.method == "POST":
            userPid = int(request.form['pid'])
            try:
                with sqlite3.connect("TurtlesHospital.db") as con:
                    cur = con.cursor()
                    cur.execute("SELECT * FROM patient WHERE pid='%d'" % userPid)
                    patient = cur.fetchone()
                    cur.execute("SELECT * FROM issue1 WHERE pid='%d'" % userPid)
                    issuedMeds = cur.fetchall()
                    medicines2 = []
                    for medicine in issuedMeds:
                        medicines2.append(medicine[2])
                    cur.execute("SELECT * FROM issue2 WHERE pid='%d'" % userPid)
                    issuedTests = cur.fetchall()
                    tests = []
                    for test in issuedTests:
                        tests.append(test[2])
                    if patient is None:
                        session['err'] = 'No such patient!'
            except:
                session['err'] = "We can not fetch patient's data right now. Please try again!"
            finally:
                return render_template('ade_search.html', patient=patient, meds=medicines2, tests=tests)
                con.close()
        else:
            session['err'] = ' '
            return render_template("ade_search.html")
    else:
        return redirect('/')

#Bills
@app.route('/ade/bill/<int:pid>', methods=['GET', 'POST'])
def ade_bill(pid):
    if request.method == 'POST':
        if request.form['bill'] == 'Room Bill':
            with sqlite3.connect("TurtlesHospital.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM patient WHERE pid='%d'" % pid)
                patientDetails = cur.fetchone()
                typeOfBed = patientDetails[5]

                today = date.today()
                cur.execute("UPDATE patient SET Status='%s', Dis_Time='%s' WHERE pid='%d'" % ('Discharged', today.strftime("%d/%m/%Y"), pid))

                cur.execute("SELECT DOA, Dis_Time FROM patient WHERE pid='%d'" % pid)
                disDate = cur.fetchone()
                disDate2 = [x.rstrip() for x in disDate]
                d = datetime.strptime(disDate2[0], '%Y-%m-%d').strftime('%d/%m/%y')
                date1 = datetime.strptime(d, '%d/%m/%y')
                date2 = datetime.strptime(disDate2[1], '%d/%m/%Y')
                Days = date2 - date1
                totalDays = Days.days

                charge = 0
                if typeOfBed == 'General Ward':
                    charge = totalDays * 2000
                elif typeOfBed == 'Semi Sharing':
                    charge = totalDays * 4000
                elif typeOfBed == 'Single Room':
                    charge = totalDays * 8000
                else:
                    session['msg'] = 'Bed price is not available!'
            return render_template('ade_bill.html', price=charge, days=totalDays, room=True, total=True, patient=patientDetails)
        elif request.form['bill'] == 'Pharmacy Bill':
            with sqlite3.connect("TurtlesHospital.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM issue1 WHERE pid='%d'" % pid)
                meds = cur.fetchall()
                medicine = {}
                medicines = []
                bill = 0
                for med in meds:
                    medicine['name'] = med[2]
                    medicine['rate'] = med[3]
                    medicine['quantity'] = med[4]
                    bill += med[3] * med[4]
                    medicines.append(medicine.copy())
            return render_template('ade_bill.html', pharmacist=True, meds=medicines, totalBill=bill, phy=True, total=True)
        elif request.form['bill'] == 'Diagnostics Bill':
            with sqlite3.connect("TurtlesHospital.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM issue2 WHERE pid='%d'" % pid)
                tests = cur.fetchall()
                report = {}
                reports = []
                bill = 0
                print(tests)
                for test in tests:
                    report['name'] = test[2]
                    report['rate'] = test[3]
                    bill += test[3]
                    reports.append(report.copy())
            return render_template('ade_bill.html', diagnostics=True, tests=reports, totalBill=bill, diag=True, total=True)
        else:
            with sqlite3.connect("TurtlesHospital.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM patient WHERE pid='%d'" % pid)
                patientDetails = cur.fetchone()
                typeOfBed = patientDetails[5]

                today = date.today()
                cur.execute("UPDATE patient SET Status='%s', Dis_Time='%s' WHERE pid='%d'" % ('Discharged', today.strftime("%d/%m/%Y"), pid))

                cur.execute("SELECT DOA, Dis_Time FROM patient WHERE pid='%d'" % pid)
                disDate = cur.fetchone()
                disDate2 = [x.rstrip() for x in disDate]
                d = datetime.strptime(disDate2[0], '%Y-%m-%d').strftime('%d/%m/%y')
                date1 = datetime.strptime(d, '%d/%m/%y')
                date2 = datetime.strptime(disDate2[1], '%d/%m/%Y')
                Days = date2 - date1
                totalDays = Days.days

                charge = 0
                if typeOfBed == 'General Ward':
                    price = 2000
                    charge = totalDays * price
                elif typeOfBed == 'Semi Sharing':
                    price = 4000
                    charge = totalDays * price
                elif typeOfBed == 'Single Room':
                    price = 8000
                    charge = totalDays * price
                else:
                    session['msg'] = 'Bed price is not available!'
                cur.execute("SELECT * FROM issue1 WHERE pid='%d'" % pid)
                meds = cur.fetchall()
                medicine = {}
                medicines = []
                phyBill = 0
                for med in meds:
                    medicine['name'] = med[2]
                    medicine['rate'] = med[3]
                    medicine['quantity'] = med[4]
                    phyBill += med[3]*med[4]
                    medicines.append(medicine.copy())
                cur.execute("SELECT * FROM issue2 WHERE pid='%d'" % pid)
                tests = cur.fetchall()
                report = {}
                reports = []
                diagBill = 0
                for test in tests:
                    report['name'] = test[2]
                    report['rate'] = test[3]
                    diagBill += test[3]
                    reports.append(report.copy())
            return render_template('ade_bill.html', billTotal=True, total=True, days=totalDays, patient=patientDetails, tests=reports, meds=medicines, price=price, roomBill=charge, phyBill=phyBill, diagBill=diagBill)
    else:
        return redirect(url_for('ade_view'))


#PHARMACY HOME
@app.route('/pharmacist')
def pharmacist():
    if "red" in session and "pharmacist" in session["red"]:
        return render_template("pharmacist.html")
    else:
        return redirect('/')

#Manage inventory
@app.route('/pharmacist/manage')
def manage1():
    if "red" in session and "pharmacist" in session["red"]:
        return render_template("manage1.html")
    else:
        return redirect('/')

#Add new meds to inventory
@app.route('/pharmacist/manage/add', methods=["GET", "POST"])
def add1():
    if "red" in session and "pharmacist" in session["red"]:
        if request.method=="POST":
            a = int(request.form.get("mid"))
            b = request.form.get("mname")
            c = int(request.form.get("mprice"))
            d = int(request.form.get("quantity"))
            e = datetime.utcnow()
            connect = sqlite3.connect('TurtlesHospital.db')
            cursor = connect.cursor()
            cursor.execute("insert into master1 values (?, ?, ?, ?, ?)", (a, b, c, d, e))
            connect.commit()
            connect.close()
            return render_template("manage1.html", message="Inventory Added")
        return  render_template("add1.html")
    else:
        return redirect('/')

#List of available meds in inventory
@app.route('/pharmacist/manage/check')
def check1():
    if "red" in session and "pharmacist" in session["red"]:
        connect = sqlite3.connect('TurtlesHospital.db')
        cursor = connect.cursor()
        temp = cursor.execute("select * from master1")
        return render_template("check1.html", temp=temp)
    else:
        return redirect('/')

#Update meds in the inventory
@app.route('/pharmacist/manage/update/<int:mid>', methods=["GET", "POST"])
def update1(mid):
    if "red" in session and "pharmacist" in session["red"]:
        connect = sqlite3.connect('TurtlesHospital.db')
        cursor = connect.cursor()
        temp = cursor.execute("select * from master1 where mid='%d'" % (mid))
        if request.method=="POST":
            a = request.form.get("mname")
            b = int(request.form.get("mprice"))
            c = int(request.form.get("quantity"))
            d = datetime.utcnow()
            cursor.execute("update master1 set mname='%s', mprice='%d', quantity='%d', mdate='%s' where mid='%d'" % (a, b, c, d, mid))
            connect.commit()
            return render_template("manage1.html", message="Inventory Updated")
        return render_template("update1.html", temp=temp)
    else:
        return redirect('/')

#Delete meds from inventory
@app.route('/pharmacist/manage/delete/<int:mid>')
def delete1(mid):
    if "red" in session and "pharmacist" in session["red"]:
        connect = sqlite3.connect('TurtlesHospital.db')
        cursor = connect.cursor()
        cursor.execute("delete from master1 where mid='%d'" % (mid))
        connect.commit()
        return render_template("manage1.html", message="Inventory Removed")
    else:
        return redirect('/')

#Search patient to issue meds
@app.route('/pharmacist/issue', methods=["GET", "POST"])
def issue1():
    if "red" in session and "pharmacist" in session["red"]:
        if request.method=="POST":
            a = int(request.form.get("pid"))
            connect = sqlite3.connect('TurtlesHospital.db')
            cursor = connect.cursor()
            X = cursor.execute("select * from patient where pid='%d'" % (a))
            for x in X:
                if x[0]==a:
                    temp = cursor.execute("select mname from master1")
                    return render_template("issue1.html", pid=a, temp=temp)
            else:
                return render_template("issue1.html", message="No Such Patient")
        return render_template("issue1.html")
    else:
        return redirect('/')

#Issue new meds
@app.route('/pharmacist/issue/new/<int:pid>', methods=["GET", "POST"])
def issuenew1(pid):
    if "red" in session and "pharmacist" in session["red"]:
        if request.method == "POST":
            a = request.form.get("mname")
            b = int(request.form.get("quantity"))
            connect = sqlite3.connect('TurtlesHospital.db')
            cursor = connect.cursor()
            X = cursor.execute("select quantity from master1 where mname='%s'" % (a))
            for x in X:
                if x[0]>=b:
                    Y = cursor.execute("select * from master1 where mname='%s'" % (a))
                    for y in Y:
                        cursor.execute("insert into issue1 values (?, ?, ?, ?, ?, ?)", (pid, y[0], y[1], y[2], b, datetime.utcnow()))
                        cursor.execute("update master1 set quantity='%d' where mname='%s'" % ((y[3]-b), a))
                        connect.commit()
                        connect.close()
                        return render_template("issue1.html", message="Meds Issued")
            else:
                return render_template("issue1.html", message="Required quantity not available")
    else:
        return redirect('/')

#Issued meds
@app.route('/pharmacist/issued', methods=["GET", "POST"])
def issued1():
    if "red" in session and "pharmacist" in session["red"]:
        if request.method=="POST":
            a = int(request.form.get("pid"))
            connect = sqlite3.connect('TurtlesHospital.db')
            cursor1 = connect.cursor()
            cursor2 = connect.cursor()
            cursor3 = connect.cursor()
            X = cursor1.execute("select * from patient where pid='%d'" % (a))
            for x in X:
                if x[0]==a:
                    temp1 = cursor1.execute("select * from issue1 where pid='%d'" % (a))
                    temp2 = cursor2.execute("select mprice, quantity from issue1 where pid='%d'" % a)
                    temp3 = cursor3.execute("select * from patient where pid='%d'" % (a))
                    sum=0
                    for t in temp2:
                        sum += t[0]*t[1]
                    return render_template("issued1.html", pid=a, temp1=temp1, sum=sum, temp3=temp3)
            else:
                return render_template("issued1.html", message="No Such Patient")
        return render_template("issued1.html")
    else:
        return redirect('/')


#DIAGNOSTICS HOME
@app.route('/diagnostic')
def diagnostic():
    if "red" in session and "diagnostic" in session["red"]:
        return render_template("diagnostic.html")
    else:
        return redirect('/')

#Manage tests
@app.route('/diagnostic/manage')
def manage2():
    if "red" in session and "diagnostic" in session["red"]:
        return render_template("manage2.html")
    else:
        return redirect('/')

#Add new tests
@app.route('/diagnostic/manage/add', methods=["GET", "POST"])
def add2():
    if "red" in session and "diagnostic" in session["red"]:
        if request.method=="POST":
            a = int(request.form.get("tid"))
            b = request.form.get("tname")
            c = int(request.form.get("tprice"))
            d = datetime.utcnow()
            connect = sqlite3.connect('TurtlesHospital.db')
            cursor = connect.cursor()
            cursor.execute("insert into master2 values (?, ?, ?, ?)", (a, b, c, d))
            connect.commit()
            connect.close()
            return render_template("manage2.html", message="Test Added")
        return  render_template("add2.html")
    else:
        return redirect('/')

#List of available tests
@app.route('/diagnostic/manage/check')
def check2():
    if "red" in session and "diagnostic" in session["red"]:
        connect = sqlite3.connect('TurtlesHospital.db')
        cursor = connect.cursor()
        temp = cursor.execute("select * from master2")
        return render_template("check2.html", temp=temp)
    else:
        return redirect('/')

#Update tests
@app.route('/diagnostic/manage/update/<int:tid>', methods=["GET", "POST"])
def update2(tid):
    if "red" in session and "diagnostic" in session["red"]:
        connect = sqlite3.connect('TurtlesHospital.db')
        cursor = connect.cursor()
        temp = cursor.execute("select * from master2 where tid='%d'" % (tid))
        if request.method=="POST":
            a = request.form.get("tname")
            b = int(request.form.get("tprice"))
            c = datetime.utcnow()
            cursor.execute("update master2 set tname='%s', tprice='%d', tdate='%s' where tid='%d'" % (a, b, c, tid))
            connect.commit()
            return render_template("manage2.html", message="Test Updated")
        return render_template("update2.html", temp=temp)
    else:
        return redirect('/')

#Delete tests
@app.route('/diagnostic/manage/delete/<int:tid>')
def delete2(tid):
    if "red" in session and "diagnostic" in session["red"]:
        connect = sqlite3.connect('TurtlesHospital.db')
        cursor = connect.cursor()
        cursor.execute("delete from master2 where tid='%d'" % (tid))
        connect.commit()
        return render_template("manage2.html", message="Test Removed")
    else:
        return redirect('/')

#Search patient to issue tests
@app.route('/diagnostic/issue', methods=["GET", "POST"])
def issue2():
    if "red" in session and "diagnostic" in session["red"]:
        if request.method=="POST":
            a = int(request.form.get("pid"))
            connect = sqlite3.connect('TurtlesHospital.db')
            cursor = connect.cursor()
            X = cursor.execute("select * from patient where pid='%d'" % (a))
            for x in X:
                if x[0]==a:
                    temp = cursor.execute("select tname from master2")
                    return render_template("issue2.html", pid=a, temp=temp)
            else:
                return render_template("issue2.html", message="No Such Patient")
        return render_template("issue2.html")
    else:
        return redirect('/')

#Issue new tests
@app.route('/diagnostic/issue/new/<int:pid>', methods=["GET", "POST"])
def issuenew2(pid):
    if "red" in session and "diagnostic" in session["red"]:
        if request.method == "POST":
            a = request.form.get("tname")
            connect = sqlite3.connect('TurtlesHospital.db')
            cursor = connect.cursor()
            Y = cursor.execute("select * from master2 where tname='%s'" % (a))
            for y in Y:
                    cursor.execute("insert into issue2 values (?, ?, ?, ?, ?)", (pid, y[0], y[1], y[2], datetime.utcnow()))
                    connect.commit()
                    connect.close()
                    return render_template("issue2.html", message="Test Issued")
    else:
        return redirect('/')

#Issued tests
@app.route('/diagnostic/issued', methods=["GET", "POST"])
def issued2():
    if "red" in session and "diagnostic" in session["red"]:
        if request.method=="POST":
            a = int(request.form.get("pid"))
            connect = sqlite3.connect('TurtlesHospital.db')
            cursor1 = connect.cursor()
            cursor2 = connect.cursor()
            cursor3 = connect.cursor()
            X = cursor1.execute("select * from patient where pid='%d'" % (a))
            for x in X:
                if x[0]==a:
                    temp1 = cursor1.execute("select * from issue2 where pid='%d'" % (a))
                    temp2 = cursor2.execute("select tprice from issue2 where pid='%d'" % a)
                    temp3 = cursor3.execute("select * from patient where pid='%d'" % (a))
                    sum = 0
                    for t in temp2:
                        sum += t[0]
                    return render_template("issued2.html", pid=a, temp1=temp1, sum=sum, temp3=temp3)
            else:
                return render_template("issued2.html", message="No Such Patient")
        return render_template("issued2.html")
    else:
        return redirect('/')


#Main Function
if __name__ == "__main__":
    app.run()
