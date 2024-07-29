from flask import *

app = Flask(__name__)
from  src.dbconnection import *


@app.route('/login', methods=['get'])
def login():
    name = request.args.get('uname')
    email = request.args.get('password')
    print(name)

    res = ("SELECT * FROM `login` WHERE `User_name`=%s AND `Password`=%s AND `type`='user'")
    v = (name, email)
    ss = selectone(res, v)
    print(ss)
    if ss is not None:
        print(ss)
        return jsonify({'m': ss['L_id'], 'res': "true",'type':ss['type']})
    else:
        print("kkkkkk")
        return jsonify({'res': "false"})

@app.route('/booknow', methods=['get'])
def booknow():
    print (request.args.get)
    accno = request.args.get('accno')
    lid = request.args.get('lid')
    ifsc = request.args.get('ifsc')
    bank = request.args.get('bank')
    pin = request.args.get('pin')
    tid = request.args.get('tid')
    sid = request.args.get('sid')
    date = request.args.get('date')
    rate = request.args.get('rate')


    qry="SELECT `balance` FROM `account` WHERE `accno`=%s AND `ifsc`=%s AND `bank`=%s AND `pin`=%s"
    val=(accno,ifsc,bank,pin)
    ss=selectone(qry,val)
    print(ss)
    if ss is not None:
        print(ss)
        b=int(ss['balance'])
        if b<int(rate):
            return jsonify({'res': "Insufficient Balance"})
        else:
            qry="UPDATE `account` SET `balance`=`balance`-%s WHERE `accno`=%s"
            val=(rate,accno)
            iud(qry,val)

            qry="INSERT INTO `booking` VALUES(NULL,%s,%s,%s,%s,'booked')"
            val=(lid,tid,sid,date)
            iud(qry,val)

            return jsonify({ 'res': "true"})
    else:
        print("kkkkkk")
        return jsonify({'res': "Invalid account details"})


@app.route('/booknow1', methods=['get'])
def booknow1():
    print (request.args.get)
    accno = request.args.get('accno')
    lid = request.args.get('lid')
    ifsc = request.args.get('ifsc')
    bank = request.args.get('bank')
    pin = request.args.get('pin')
    tid = request.args.get('tid')
    sid = request.args.get('sid')
    date = request.args.get('date')
    rate = request.args.get('rate')
    p = request.args.get('p')
    des = request.args.get('des')
    print(des,"==========================")
    print(des,"==========================")
    print(des,"==========================")
    print(des,"==========================")

    qry="SELECT `balance` FROM `account` WHERE `accno`=%s AND `ifsc`=%s AND `bank`=%s AND `pin`=%s"
    val=(accno,ifsc,bank,pin)
    ss=selectone(qry,val)
    print(ss)
    if ss is not None:
        print(ss)
        b=int(ss['balance'])
        if b<int(rate):
            return jsonify({'res': "Insufficient Balance"})
        else:
            qry="UPDATE `account` SET `balance`=`balance`-%s WHERE `accno`=%s"
            val=(rate,accno)
            iud(qry,val)


            qry="INSERT INTO `booking` VALUES(NULL,%s,%s,%s,%s,'tbooked')"
            val=(lid,tid,sid,date)
            id=iud(qry,val)
            lis=["GK","LB","CB","RB","LF","CF","RF"]
            if(des=="Football 5s"):
                lis = ["GK", "LB",  "RB", "LF",  "RF"]
            t=["T1","T2"]
            for i in t:
                for j in lis:
                    if i=="T1" and j==p:

                        q="INSERT INTO `team` VALUES(NULL,%s,%s,%s)"
                        v=(id,i+"-"+j,lid)
                        iud(q,v)
                    else:
                        q = "INSERT INTO `team` VALUES(NULL,%s,%s,0)"
                        v = (id, i + "-" + j)
                        iud(q, v)
            return jsonify({ 'res': "true"})
    else:
        print("kkkkkk")
        return jsonify({'res': "Invalid account details"})


@app.route('/register', methods=['get'])
def register():
    print(request.args)
    name = request.args.get('name')
    lname = request.args.get('lname')
    email = request.args.get('email')
    phone = request.args.get('phone')
    uname = request.args.get('uname')
    password = request.args.get('password')
    qry = "insert into login values(null,%s,%s,'user')"
    val = (uname, password)
    id = iud(qry, val)
    q = ("INSERT INTO `user` VALUES(NULL,%s,%s,%s,%s,%s)")
    val = (str(id), name,lname,email,phone)
    iud(q, val)
    return jsonify({'res': "true"})



@app.route('/search_turf', methods=['get'])
def search_turf():
    t=request.args.get('t')
    p=request.args.get('p')

    if t=="" and p=="":
        lati = request.args.get("lati")
        lon = request.args.get("lon")
        print(lati,lon,"===============")
        if lati=="" or str(lati)=="None":
            lati="11.135876580281767"
            lon="75.89733123779297"
        qry = "SELECT `turf`.*,`rate`.*, (3959 * ACOS ( COS ( RADIANS(%s) ) * COS( RADIANS( `latitude`) ) * COS( RADIANS( `longitude` ) - RADIANS(%s) ) + SIN ( RADIANS(%s) ) * SIN( RADIANS( `latitude` ) ))) AS user_distance FROM `turf` JOIN `rate` ON `rate`.`t_id`=`turf`.`l_id` ORDER BY  user_distance "
        v=(lati,lon,lati)
        res = selectall2(qry,v)
        print(res)
        for i in res:
            print(i)
        return str(res)
    qry = "SELECT * FROM `turf` JOIN `rate` ON `turf`.`l_id`=`rate`.`t_id` WHERE `rate`.`description` LIKE '"+t+"%' AND `place`='"+p+"'"
    res = selectall(qry)
    print(res)
    return str(res)

@app.route('/view_booking', methods=['get'])
def view_booking():
    lid=request.args.get('id')
    from datetime import datetime
    qry="SELECT `turf`.`t_name`,`slot`.`slot`,slot_id,`booking`.`date`,`rate`.`description`,`booking`.`status`,booking.b_id,DATEDIFF(`booking`.`date`,CURDATE()) AS d FROM `rate` JOIN `booking` ON `booking`.`t_id`=`rate`.`rate_id` JOIN `slot` ON `slot`.`slot_id`=`booking`.`s_id` JOIN `turf` ON `turf`.`l_id`=`rate`.`t_id` WHERE `booking`.`u_id`=%s and booking.status!='tbooked' and booking.date>=curdate()"
    res=selectall2(qry,lid)
    result=[]
    h = int(datetime.now().strftime("%H"))
    d = datetime.now().strftime("%Y-%m-%d")
    for i in res:

        if i['date'] == d:
            sid = int(i['slot_id']) + 6
            if h < sid:
                result.append(i)

        else:
            result.append(i)
    print (result)
    return str(result)

    print (res)
    return str(res)
@app.route('/deletebooking', methods=['get'])
def deletebooking():
    bid=request.args.get('bid')
    q="DELETE FROM `booking` WHERE `b_id`=%s"
    iud(q,bid)
    return str({"res":"true"})
@app.route('/deletetbooking', methods=['get'])
def deletetbooking():
    bid=request.args.get('bid')
    uid=request.args.get('uid')
    q="UPDATE `team` SET `uid`=0 WHERE `sid`=%s AND `uid`=%s"
    iud(q,(bid,uid))
    return str({"res":"true"})
@app.route('/select_sloat', methods=['get'])
def select_sloat():
    d=request.args.get('d')
    t=request.args.get('t')
    print (d,t)
    qry="SELECT * FROM `slot`"
    res=selectall(qry)
    if d=="":

        return str("")
    result=[]
    from datetime import datetime

    date = datetime.now().strftime("%Y-%m-%d")
    h = int(datetime.now().strftime("%H")) - 6

    print (date, h)
    if date==d:
        for i in res:
            qry = "SELECT * FROM `booking` WHERE `t_id`=%s AND `s_id`=%s AND `date`=%s AND `status`!='canceled'"
            val = (t, i['slot_id'], d)
            res = selectone(qry, val)
            i['s'] = "0"
            print (res)
            if res is not None:
                i['s'] = "1"
            elif int(i['slot_id'])<=h:
                i['s']="1"
            result.append(i)
    else:

        for i in res:

            qry = "SELECT * FROM `booking` WHERE `t_id`=%s AND `s_id`=%s AND `date`=%s AND `status`!='canceled'"
            val=(t, i['slot_id'],d)
            res = selectone(qry,val)
            i['s']="0"
            print (res)
            if res is not None:
                i['s']="1"

            result.append(i)
    print (result)
    return str(result)
@app.route('/mymatch', methods=['get'])
def mymatch():
    lid=request.args.get('lid')
    result=[]
    from datetime import datetime
    qry = "SELECT b_id,`turf`.`t_name`,`slot`.`slot`,slot_id,`booking`.`date`,`rate`.`description`,`booking`.`status`,`booking`.`b_id` FROM `rate` JOIN `booking` ON `booking`.`t_id`=`rate`.`rate_id` JOIN `slot` ON `slot`.`slot_id`=`booking`.`s_id` JOIN `turf` ON `turf`.`l_id`=`rate`.`t_id` WHERE `booking`.`u_id`=%s and booking.status='tbooked' and booking.date>=curdate()"
    res = selectall2(qry, lid)
    print(res)

    h = int(datetime.now().strftime("%H"))
    d = datetime.now().strftime("%Y-%m-%d")
    for i in res:

        if i['date'] == d:
            sid = int(i['slot_id']) + 6
            if h < sid:
                if sid-h>2:
                    i['s']="1"
                else:
                    i['s']="0"
                result.append(i)

        else:
            i['s']="1"
            result.append(i)


    print (result)
    return str(result)
@app.route('/view_match', methods=['get'])
def view_match():
    lid=request.args.get('lid')
    result=[]

    qry = "SELECT `turf`.`t_name`,`slot`.`slot`,`booking`.`date`,`rate`.`description`,`booking`.`status`,`booking`.`b_id` FROM `rate` JOIN `booking` ON `booking`.`t_id`=`rate`.`rate_id` JOIN `slot` ON `slot`.`slot_id`=`booking`.`s_id` JOIN `turf` ON `turf`.`l_id`=`rate`.`t_id` WHERE `booking`.`u_id`!=%s and booking.status='tbooked' and `booking`.`date`>=curdate() and  `booking`.`b_id` NOT IN(SELECT `sid` FROM `team` WHERE `uid`=%s)"
    res = selectall2(qry, (lid,lid))
    print(res)
    for i in res:
        result.append(i)

    return str(result)
@app.route('/book_match', methods=['get'])
def book_match():
    lid=request.args.get('lid')
    tid=request.args.get('tid')
    p=request.args.get('p')
    q="UPDATE `team` SET `uid`=%s WHERE `tid`=%s"
    v=(lid,tid)
    iud(q,v)

    return str({"res":"true"})
@app.route('/mymatch_more', methods=['get'])
def mymatch_more():
    lid=request.args.get('lid')
    bid=request.args.get('bid')
    result=[]

    qry = "SELECT * FROM `team` WHERE `sid`=%s"
    res = selectall2(qry, bid)
    print(res)
    for i in res:
        if i['position'].split("-")[0]=="T1":
            i['t']="t1"
        else:
            i['t']="t2"
        if str(i['uid'])=="0":
            i['name']="Pending"
        else:
            q="SELECT `f_name`,`l_name`,phone FROM `user` WHERE `l_id`=%s"
            r=selectone(q,i['uid'])
            i['name']=r['f_name']+" "+r['l_name']
            if int(i['uid'])!=int(lid):
                i['name'] =i['name']+" "+str(r['phone'])
        result.append(i)

    return str(result)
@app.route('/view_match1', methods=['get'])
def view_match1():

    bid=request.args.get('bid')
    result=[]

    qry = "SELECT * FROM `team` WHERE `sid`=%s"
    res = selectall2(qry, bid)
    print(res)
    for i in res:
        if i['position'].split("-")[0]=="T1":
            i['t']="t1"
        else:
            i['t']="t2"
        if str(i['uid'])=="0":
            i['name']="Pending"
        else:
            q="SELECT `f_name`,`l_name` FROM `user` WHERE `l_id`=%s"
            r=selectone(q,i['uid'])
            i['name']=r['f_name']+" "+r['l_name']
        result.append(i)

    return str(result)


@app.route('/history', methods=['get'])
def history():

    lid=request.args.get('lid')
    result=[]
    from datetime import datetime
    qry = "SELECT `booking`.`b_id`,booking.date,`turf`.*,`slot`.`slot`,`slot`.`slot_id`,`team`.`position` FROM `team` JOIN `booking` ON `booking`.`b_id`=`team`.`sid` JOIN `slot` ON `slot`.`slot_id`=`booking`.`s_id` JOIN `rate` ON `booking`.`t_id`=`rate`.`rate_id` JOIN `turf` ON `turf`.`l_id`=`rate`.`t_id` WHERE `team`.`uid`=%s AND booking.date>=curdate()"
    res = selectall2(qry, lid)
    print(res)
    h=int(datetime.now().strftime("%H"))
    d=datetime.now().strftime("%Y-%m-%d")
    for i in res:

        if i['date']==d:
            sid=int(i['slot_id'])+6
            if h<sid:
                result.append(i)

        else:
            result.append(i)
    print (result)
    for i in result:
        if i['date'] == d:
            i['s']="0"
        else:
            i['s']="1"
    return str(result)

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
