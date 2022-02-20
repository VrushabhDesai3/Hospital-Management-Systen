import sqlite3

connect = sqlite3.connect('TurtlesHospital.db')
cursor = connect.cursor()
                            #CREDENTIALS: LOGIN DATA#
#cursor.execute("create table credentials (username character primary key, password character, role character, logtime datetime)")

                            # PATIENT: PATIENT TABLE RELATED TO HOSPITAL#
#cursor.execute("CREATE TABLE patient (pid INTEGER, SSNId INTEGER NOT NULL, Name TEXT NOT NULL DEFAULT 'Unknown', Age INTEGER NOT NULL, DOA TEXT NOT NULL, TOB TEXT NOT NULL, Address TEXT NOT NULL, City TEXT NOT NULL, State TEXT, Status TEXT, Dis_Time TEXT PRIMARY KEY(pid AUTOINCREMENT) )")

                            #MASTER1: MASTER TABLE FOR PHARMACY#
#cursor.execute("create table master1 (mid integer, mname characher, mprice integer, quantity integer, mdate datetime)")
                            #ISSUE1: MEDICINES ISSUED TABLE#
#cursor.execute("create table issue1 (pid integer, mid integer, mname characher, mprice integer, quantity integer, mdate datetime)")

                            #MASTER2: MASTER TABLE FOR DIAGNOSTICS#
#cursor.execute("create table master2 (tid integer, tname characher, tprice integer, tdate datetime)")
                            #ISSUE2: TESTS ISSUED TABLE#
#cursor.execute("create table issue2 (pid integer, tid integer, tname characher, tprice integer, tdate datetime)")
connect.close()