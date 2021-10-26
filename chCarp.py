import pymysql
import datetime as dt
import smtplib
import cv2
import pyautogui
from PIL import Image
import pytesseract
import numpy as np


from time import strftime
myDB= pymysql.connect(host="localhost",user="root",passwd="",port=3306,database="car_parking")
myCursor = myDB.cursor()
class MainApp():
    myCursor.execute("select Charges from charges where vehicle= 'Bike' ")
    charb = myCursor.fetchone()
    bikech = int(charb[0])
    myCursor.execute("select Charges from charges where vehicle= 'Car' ")
    charc = myCursor.fetchone()
    carch = int(charc[0])
    myCursor.execute("select Pass from charges where vehicle= 'Bike' ")
    pb = myCursor.fetchone()
    bikep =int(pb[0])
    myCursor.execute("select Pass from charges where vehicle= 'Car' ")
    pc = myCursor.fetchone()
    carp = int(pc[0])
    def login(self):
        while True:
            print("                        ======= CAR PARKING =======")
            print(" ")
            try:
                a = input("                        Enter Your ID: ")
                b = input("                        Enter password: ")
                myCursor.execute("select * from login where user_id = '{}' and PASSWORD = '{}'".format(a,b))
                data = myCursor.fetchone()
                print(" ")
                if data[4] == "Admin":
                    print("                          Welome",data[3])
                    myCursor.execute("select count(id) from car_slot")
                    sc = myCursor.fetchone()
                    myCursor.execute("select count(id) from bike_slot")
                    sb = myCursor.fetchone()
                    car = int(sc[0])
                    bike = int(sb[0])
                    if car == 0:
                        self.carslot()
                    if bike == 0:
                        self.bikeslot()
                    while True:
                        print(" ")
                        print("                        1. View Records")
                        print("                        2. Manage Agents")
                        print("                        3. Update charges")
                        print("                        4. logout")
                        
                        print(" ")
                        ch = input("                        Enter your choice: ")
                        if ch == '1':
                            self.view_record()
                        if ch == '2':
                            self.ManageAgent()
                        
                        if ch == '3':
                            self.charges()
                        if ch == '4':
                            break;
                        else:
                            print("                        plz Enter the given choice")
                            continue;
                           
                elif data[4] == "Agent":
                    self.mail()
                    while True:
                        print("                          Welcome",data[3])
                        print(" ")
                        print("                        1. Generate Receipt")
                        print("                        2. Collect Revenue")
                        print("                        3. Check Available Slots")
                        print("                        4. Generate Pass")
                        print("                        5. logout")
                        print(" ")
                        ch = input("                        Enter your choice: ")
                        if ch == '1':
                            self.generateR(data[0])
                        if ch == '2':
                            self.collectR()
                        if ch == '3':
                            self.avaislot()
                        if ch == '4':
                            self.generatepass()
                        if ch == '5':
                            break;
                        else:
                            print("                        plz Enter the given choice")
                            continue;
            except:
                print("                        plz enter valid credential")
                continue;
    def view_record(self):
        while  True:
            try:
                print("                          View Record")
                print(" ")
                print("                        1. Today's Record")
                print("                        2. Record Date-wise")
                print("                        3. Record By Vehicle no.")
                print("                        4. Total Revenue")
                print("                        5. Pass Record")
                print("                        6. Exit")
                print(" ")
                ch = input("                        Enter your choice: ")
                if ch == '1':
                    dnow = datetime.date.today()
                    print("                       ",dnow)
                    myCursor.execute("select * from record where Entry_date = '{}'".format(dnow))
                    data = myCursor.fetchall()
                    print(" ")
                    print("                        Id  RC number    Entry date    Entry time    Exit date    Exit time    Agent id    Charges    Vehicle")
                    for i in data:
                         print("                      ",i[0]," ",i[1][:10]," ",i[2],"  ",i[3],"     ",i[4],"  ",i[5],"   ",i[6],"         ",i[7],"       ",i[8] )
                if ch == '2':
                    d = input("                        Enter date(YYYY-MM-DD): ")
                    myCursor.execute("select * from record where Entry_date = '{}'".format(d))
                    data = myCursor.fetchall()
                    print(" ")
                    print("                        Id  RC number    Entry date    Entry time    Exit date    Exit time    Agent id    Charges    Vehicle")
                    for i in data:
                         print("                        ",i[0]," ",i[1][:10]," ",i[2],"  ",i[3],"     ",i[4],"  ",i[5],"   ",i[6],"         ",i[7],"       ",i[8] )
                if ch == '3':
                    rc = input("                        Enter RC number: ")
                    myCursor.execute("select * from record where RC_number = '{}'".format(rc))
                    data = myCursor.fetchall()
                    print(" ")
                    print("                        Id  RC number    Entry date    Entry time    Exit date    Exit time    Agent id    Charges    Vehicle")
                    for i in data:
                         print("                        ",i[0]," ",i[1][:10]," ",i[2],"  ",i[3],"     ",i[4],"  ",i[5],"   ",i[6],"         ",i[7],"       ",i[8] )
                if ch == '4':
                    myCursor.execute("select sum(Charges) from pass_1 where Vehicle  = 'Bike'")
                    datab = myCursor.fetchone()
                    myCursor.execute("select sum(Charges) from pass_1 where Vehicle  = 'Car'")
                    datac = myCursor.fetchone()
                    myCursor.execute("select sum(charges) from record where Vehicle  = 'Car'")
                    datarc = myCursor.fetchone()
                    myCursor.execute("select sum(charges) from record where Vehicle  = 'Bike'")
                    datarb = myCursor.fetchone()
                    myCursor.execute("select count(Vehicle) from record where Vehicle  = 'Car'")
                    cdatac = myCursor.fetchone()
                    myCursor.execute("select count(Vehicle) from record where Vehicle  = 'Bike'")
                    cdatab = myCursor.fetchone()
                    myCursor.execute("select count(Vehicle) from pass_1 where Vehicle  = 'Bike'")
                    cpdatab = myCursor.fetchone()
                    myCursor.execute("select count(Vehicle) from pass_1 where Vehicle  = 'Car'")
                    cpdatac = myCursor.fetchone()
                    print("  ")
                    print("                        Vehicle  No. of Reciept  No. of  pass   Revenue by Reciept  Revenue by Pass")
                    print("                        Bike    ",cdatab[0],"             ",cpdatab[0],"            ",datarb[0],"                  ",datab[0])
                    print("                        Car     ",cdatac[0],"             ",cpdatac[0],"            ",datarc[0],"                ",datac[0])
                    print(" ")

                if ch == '5':
                    myCursor.execute("select * from pass_1")
                    data = myCursor.fetchall()
                    print(" ")
                    print("                        Id  RC number    Owner name         Gmail ID                        Exp Date")
                    for i in data:
                         print("                        ",i[0]," ",i[1]," ",i[2],"  ",i[3],"     ",i[4])
                if ch == '6':
                    break;
                else:
                    print("                        plz Enter the given choice")
                    continue;
            except:
                print("                        plz enter valid data")
                continue;
    def ManageAgent(self):
        while True:
            try:
                print("                         Manage Agent")
                print(" ")
                print("                        1. Add Agent")
                print("                        2. Remove Agent")
                print("                        3. Reset password")
                print("                        4. Exit")
                print(" ")
                ch = input("                        Enter Your choice: ")
                if ch == '1':
                    uid = input("                        Enter new user ID: ")
                    pwd = input("                        Enter password: ")
                    name = input("                        Enter Agent Name: ")
                    myCursor.execute("insert into login(user_id,PASSWORD,NAME,Role) values('{}','{}','{}','{}')".format(uid,pwd,name,"Agent"))
                    myDB.commit()
                    print("                        Agent Added")
                    continue;
                if ch == '2':
                    myCursor.execute("select id,user_id from login")
                    data1 = myCursor.fetchall()
                    print("                        Id  User id")
                    for i in data1:
                        print("                        ",i[0]," ",i[1])
                    did = int(input("                        Enter ID to DELETE: "))
                    myCursor.execute("select id from login where id='{}'".format(did))
                    data2 = myCursor.fetchone()
                    if did != 1:
                        if data2[0] == did :
                            myCursor.execute("Delete from login where id='{}'".format(did))
                            myDB.commit()
                            print(" ")
                            print("                        Agent Removed")
                            print(" ")
                    elif did == 1:
                        print(" ")
                        print("                        you can't remove admin")
                    elif data2[0] != did:
                        print(" ")
                        print("                        No record found")
                if ch == '3':
                    myCursor.execute("select id,user_id from login")
                    data1 = myCursor.fetchall()
                    print("                        Id  User id")
                    for i in data1:
                        print("                        ",i[0]," ",i[1])
                    did = int(input("                        Enter ID to reset password: "))
                    np = input("                        Enter new password: ")
                    myCursor.execute("update login set PASSWORD ='{}' where id='{}'".format(np,did))
                    myDB.commit()
                    
                if ch == '4':
                    break;
            except:
                print("                        plz enter valid data")
                continue;
    def generateR(self,agentid):
        while True:
            try:
                self.web()
                print(" ")
                print("                         Collect Receipt")
                print(" ")
                print("                        1. Car")
                print("                        2. Bike")
                print(" ")
                ch = input("                        Enter your choice: ")
                if ch == '1':
                    r = self.scan()
                    c = r.upper()
                    rc = c[:10]
                    a = strftime("%y-%m-%d %H:%M:%S")
                    endt = a.split(" ")
                    myCursor.execute("select id from car_slot where Status_car = 0")
                    slotno = myCursor.fetchone()
                    print("                        vehicle no.")
                    print("                        ",rc)
                    print("                        time",a)
                    print("                        slot no.",slotno[0])
                    print("                        agent id",agentid)
                    print(" ")
                    print("                        1. Press 1 to confirm")
                    print("                        2. press 2 to cancel")
                    print(" ")
                    cch = input("                        Enter choice: ")
                    if cch == '1':
                        myCursor.execute("insert into car_1(RC_number,Entry_date,Entry_time,Agent_id,slot_number) values('{}','{}','{}',{},{})".format(rc,endt[0],endt[1],agentid,slotno[0]))
                        myDB.commit()
                        myCursor.execute("update car_slot set Status_car = 1 where id = {}".format(slotno[0]))
                        myDB.commit()
                        print("                        === Parking ===")
                        print(" ")
                        print("                        vehicle no.")
                        print("                        ",rc)
                        print("                        time",a)
                        print("                        slot no.",slotno[0])
                        print("                        agent id",agentid)
                        print(" ")
                        break;
                    if cch == '2':
                        continue;
                
                if ch == '2':
                    r = self.scan()
                    c = r.upper()
                    rc = c[:10]
                    a = strftime("%y-%m-%d %H:%M:%S")
                    endt = a.split(" ")
                    myCursor.execute("select id from bike_slot where Status_bike = 0")
                    slotno = myCursor.fetchone()
                    print("                        vehicle no.")
                    print("                        ",rc)
                    print("                        time",a)
                    print("                        slot no.",slotno[0])
                    print("                        agent id",agentid)
                    print("                        1. Press 1 to confirm")
                    print("                        2. press 2 to cancel")
                    cch = input("                        Enter choice: ")
                    if cch == '1':
                        myCursor.execute("insert into bike_1(RC_number,Entry_date,Entry_time,Agent_id,slot_number) values('{}','{}','{}',{},{})".format(rc,endt[0],endt[1],agentid,slotno[0]))
                        myDB.commit()
                        myCursor.execute("update bike_slot set Status_bike = 1 where id = {}".format(slotno[0]))
                        myDB.commit()
                        print("                        === Parking ===")
                        print(" ")
                        print("                        vehicle no.")
                        print("                        ",rc)
                        print("                        time",a)
                        print("                        slot no.",slotno[0])
                        print("                        agent id",agentid)
                        print(" ")
                        break;
                    if cch == '2':
                        continue;
            except:
                print("                        sorry No slot available")
                break;
                
    def collectR(self):
        while True:
            try:
                print(" ")
                print("                        1. Bike")
                print("                        2. Car")
                print("                        3. Exit")
                print(" ")
                ch = input("                        Enter your choice: ")
                if ch == '1':
                    sno = input("                        Enter Unique Slot No. ")
                    myCursor.execute("select * from bike_1 where slot_number ='{}'".format(sno))
                    data = myCursor.fetchone()
                    myCursor.execute("select * from pass_1 where RC_number ='{}'".format(data[1]))
                    datap = myCursor.fetchone()
                    try:
                        if datap[1] == data[1]:
                            a = strftime("%y-%m-%d %H:%M:%S")
                            exdt = a.split(" ")
                            r = str(data[1])
                            e = str(data[2])
                            o = str(data[3])
                            d = str(data[4])
                            myCursor.execute("insert into record(RC_number,Entry_date,Entry_time,Exit_date,Exit_time,Agent_id,charges,Vehicle) values('{}','{}','{}','{}','{}','{}',{},'Bike')".format(r,e,o,exdt[0],exdt[1],d,MainApp.bikep))
                            myDB.commit()
                            myCursor.execute("update bike_slot set Status_bike = 0 where id = {}".format(data[5]))
                            myDB.commit()
                            myCursor.execute("delete from bike_1  where slot_number = {}".format(data[5]))
                            myDB.commit()
                            print(" ")
                            print("                        Charges",charge)
                            print("                        Record added")
                            print(" ")
                    except:
                        b = int(strftime("%d"))
                        c = int(strftime("%H"))
                        a = int(strftime("%M"))
                        B = str(data[2])
                        C = str(data[3])
                        time = C.split(":")
                        
                        nb = int(B[-2:])
                        nc = int(time[0])
                        ncm = int(time[1])
                        mint = a-ncm
                        date = int(nb-b)
                        hour = int(c-nc)
                        charge = 0
                        if date > 0:
                            nhour = int((24-hour)+hour)
                            charge = (nhour*MainApp.bikech)
                        if hour > 1 :
                            charge = (hour*MainApp.bikech)+(MainApp.bikech)
                        elif hour == 0:
                            charge = (MainApp.bikech)
                        a = strftime("%y-%m-%d %H:%M:%S")
                        exdt = a.split(" ")
                        r = str(data[1])
                        e = str(data[2])
                        o = str(data[3])
                        d = str(data[4])
                        myCursor.execute("insert into record(RC_number,Entry_date,Entry_time,Exit_date,Exit_time,Agent_id,charges,Vehicle) values('{}','{}','{}','{}','{}','{}',{},'Bike')".format(r,e,o,exdt[0],exdt[1],d,charge))
                        myDB.commit()
                        myCursor.execute("update bike_slot set Status_bike = 0 where id = {}".format(data[5]))
                        myDB.commit()
                        myCursor.execute("delete from bike_1  where slot_number = {}".format(data[5]))
                        myDB.commit()
                        print(" ")
                        print("                        Your Charges is",charge)
                        print("                        Record added")
                        print(" ")
                if ch == '2':
                    sno = input("                        Enter Unique Slot No. ")
                    myCursor.execute("select * from car_1 where slot_number ='{}'".format(sno))
                    data = myCursor.fetchone()
                    myCursor.execute("select * from pass_1 where RC_number ='{}'".format(data[1]))
                    datap = myCursor.fetchone()
                    try:
                        if datap[1] == data[1]:
                            a = strftime("%y-%m-%d %H:%M:%S")
                            exdt = a.split(" ")
                            r = str(data[1])
                            e = str(data[2])
                            o = str(data[3])
                            d = str(data[4])
                            myCursor.execute("insert into record(RC_number,Entry_date,Entry_time,Exit_date,Exit_time,Agent_id,charges,Vehicle) values('{}','{}','{}','{}','{}','{}',{},'Car')".format(r,e,o,exdt[0],exdt[1],d,MainApp.carp))
                            myDB.commit()
                            myCursor.execute("update car_slot set Status_car = 0 where id = {}".format(data[5]))
                            myDB.commit()
                            myCursor.execute("delete from car_1  where slot_number = {}".format(data[5]))
                            myDB.commit()
                            print(" ")
                            print("                        Your Charges is",charge)
                            print("                        Record added")
                            print(" ")
                    except:
                        b = int(strftime("%d"))
                        c = int(strftime("%H"))
                        a = int(strftime("%M"))
                        B = str(data[2])
                        C = str(data[3])
                        time = C.split(":")
                        nb = int(B[-2:])
                        nc = int(time[0])
                        ncm = int(time[1])
                        mint = a-ncm
                        date = int(nb-b)
                        hour = int(c-nc)
                        charge = 0
                        if date > 0:
                            nhour = int((24-hour)+hour)
                            charge = (nhour*MainApp.carch)
                        if hour > 0:
                            charge = (hour*MainApp.carch)+(MainApp.carch)
                        elif hour == 0:
                            charge = (MainApp.carch)
                        a = strftime("%y-%m-%d %H:%M:%S")
                        exdt = a.split(" ")
                        r = str(data[1])
                        e = str(data[2])
                        o = str(data[3])
                        d = str(data[4])
                        myCursor.execute("insert into record(RC_number,Entry_date,Entry_time,Exit_date,Exit_time,Agent_id,charges,Vehicle) values('{}','{}','{}','{}','{}','{}',{},'Car')".format(r,e,o,exdt[0],exdt[1],d,charge))
                        myDB.commit()
                        myCursor.execute("update car_slot set Status_car = 0 where id = {}".format(data[5]))
                        myDB.commit()
                        myCursor.execute("delete from car_1  where slot_number = {}".format(data[5]))
                        myDB.commit()
                        print(" ")
                        print("                        Your Charges is",charge)
                        print("                        Record added")
                        print(" ")
                if ch == '3':
                    break;
            except:
                print("                        slot is empty")
                continue;
    def avaislot(self):
        print("                        1. Bike")
        print("                        2. Car")
        ch = input("                        Enter your choice: ")
        if ch == '1':
            myCursor.execute("select * from bike_slot where Status_bike = 0")
            data = myCursor.fetchall()
            print("                        Slot No. Status_bike")
            for i in data:
                print("                        ",i[0],"      ",i[1])
        if ch == '2':
            myCursor.execute("select * from car_slot where Status_car = 0")
            data = myCursor.fetchall()
            print("                        Slot No. Status_car")
            for i in data:
                print("                        ",i[0],"      ",i[1])
    def generatepass(self):
        try:
            a = strftime("%y-%m-%d")
            now = dt.date.today()
            exp = now + dt.timedelta(days=30)
            r = input("                        Enter RC Number: ")
            rc = r.upper()
            oname = input("                        Enter Owner Name: ")
            gmail = input("                        Enter Gmail ID: ")
            veh = input("                        Enter Vehicle type: ")
            v = veh.upper()
            if v == 'BIKE':
                myCursor.execute("insert into pass_1(RC_number,Owner_name,Gmail_id,Issue_Date,Exp_Date,Vehicle,Charges) values('{}','{}','{}','{}','{}','Bike',300)".format(rc,oname,gmail,a,exp))
                myDB.commit()
                print("                        Pass Charges is 300 rupees")
                s=smtplib.SMTP('smtp.gmail.com',587)
                s.starttls()
                s.login("chandresh898951@gmail.com","sonalikha47RX")
                message=" Your pass has been generated for bike RC no. '{}' valid upto {}".format(rc,exp)
                s.sendmail("chandresh898951@gmail.com","{}".format(gmail),message)
                s.quit()
                print("                        Pass Added")
                print("                        Mail sent to '{}' ".format(oname))  
            if v == 'CAR':
                myCursor.execute("insert into pass_1(RC_number,Owner_name,Gmail_id,Issue_Date,Exp_Date,Vehicle,Charges) values('{}','{}','{}','{}','{}','Car',600)".format(rc,oname,gmail,a,exp))
                myDB.commit()
                print("                        Pass charges is 600 rupees")
                s=smtplib.SMTP('smtp.gmail.com',587)
                s.starttls()
                s.login("chandresh898951@gmail.com","sonalikha47RX")
                message=" Your pass has been generated for car RC no. '{}' valid upto {}".format(rc,exp)
                s.sendmail("chandresh898951@gmail.com","{}".format(gmail),message)
                s.quit()
                print("                        Pass Added")
                print("                        Mail sent to '{}' ".format(oname))
            
            
        except:            
            print("                        enter valid details")
        
    def carslot(self):
        x = int(input("                        Enter car slot count: "))
        for i in range(x):
            s = 0
            myCursor.execute("insert into car_slot(Status_car) values({})".format(s))
            myDB.commit()
        print("                        car slots updated")
    def bikeslot(self):
        x = int(input("                        Enter bike slot count: "))
        for i in range(x):
            s = 0
            myCursor.execute("insert into bike_slot(Status_bike) values({})".format(s))
            myDB.commit()
        print("                        bike slots updated")
    def mail(self):
        try:
            a = strftime("%y-%m-%d")
            A = a.split("-")
            myCursor.execute("select Exp_Date,Gmail_id from pass_1")
            a = myCursor.fetchall()
            for i in a:
                x= str(i[0])
                X = x.split("-")
                gm = str(i[1])
                if A[2] == X[2] and A[1] == X[1]:
                    s=smtplib.SMTP('smtp.gmail.com',587)
                    s.starttls()
                    s.login("chandresh898951@gmail.com","sonalikha47RX")
                    message="Your pass for parking has been  experied"
                    s.sendmail("chandresh898951@gmail.com","{}".format(gm),message)
                    s.quit()
                    myCursor.execute("delete from pass_1  where Gmail_id = '{}'".format(i[1]))
                    myDB.commit()
                    print("                        Mail sent to users")
        except:
            print("                        Mail not sent")
    def scan(self):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        name = 0
        img = Image.open("C:/Users/shaily/Desktop/carpch/opencv_frame_{}.png".format(name))
        output = pytesseract.image_to_string(img)
        return output

    def web(self):
        cam = cv2.VideoCapture(0)
        cv2.namedWindow("Python Webcam Screenshot App")
        img_count = 0
        while True:
            ret,frame = cam.read()
            if not ret:
                print("                        failed to grab frame")
                break;
            cv2.imshow("test",frame)
            k = cv2.waitKey(1)
            if k%256 == 27:
                print("                        Escape hit,closing the app")
                break;
            elif k%256 == 32:
                img_name = "opencv_frame_{}.png".format(img_count)
                cv2.imwrite(img_name,frame)

                print("                        image taken")
                img_count+=1
                cam.release()
                cv2.destroyAllWindows()
                break;
    def charges(self):
        print(" ")
        bch = input("                        Enter bike charges: ")
        bbch = int(bch)
        myCursor.execute("update charges set Charges ={} where vehicle='Bike' ".format(bbch))
        myDB.commit()
        cch = input("                        Enter car charges: ")
        ch = int(cch)
        myCursor.execute("update charges set Charges ={} where vehicle='Car' ".format(ch))
        myDB.commit()
        bp = input("                        Enter bike pass charges: ")
        bbp = int(bp)
        myCursor.execute("update charges set Pass ={} where vehicle='Bike' ".format(bbp))
        myDB.commit()
        cp = input("                        Enter car pass charges: ")
        p = int(cp)
        myCursor.execute("update charges set Pass ={} where vehicle='Car' ".format(p))
        myDB.commit()
        print("                        plz Restart the application to updated charges ")
        
        
              
        
        
    
        
                
            
app = MainApp()
#app.bikeslot()
#app.generateR(1)
#app.collectR()
app.login()
#app.generatepass()
#app.view_record()
#app.charges()

