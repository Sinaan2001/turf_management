import functools
import os

from flask import *
from werkzeug.utils import secure_filename

from src.dbconnection import *
app = Flask(__name__)
app.secret_key="1234"

def login_required(func):
	@functools.wraps(func)
	def secure_function():
		if "lid" not in session:
			return render_template('login.html')
		return func()
	return secure_function

@app.route('/')
def login():
    return render_template("login_index.html")

@app.route('/logincode',methods=['post'])
def logincode():
    un=request.form['textfield']
    ps=request.form['textfield2']
    a="select * from login where User_name=%s and Password=%s"
    val=(un,ps)
    s=selectone(a,val)
    if s is None:
        return '''<script>alert("invalid username or password");window.location='/'</script>'''
    elif s['type']=="admin":
        session['lid']=s['L_id']
        return '''<script>alert("Welcome Admin");window.location='/admin_home'</script>'''
    elif s['type']=="turf":
        session['lid'] = s['L_id']
        return '''<script>alert("Welcome Turf");window.location='/Turf_home'</script>'''
    else:
        return '''<script>alert("invalid!!!!");window.location='/'</script>'''

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect('/')

#======================================================ADMIN============================================================
@app.route('/admin_home')
@login_required
def admin_home():
    return render_template('admin/aindex.html')

@app.route('/Approve_Turf')
@login_required
def Approve_Turf():
    qry="SELECT `turf`.*,`login`.* FROM `turf` JOIN `login` ON `turf`.`l_id`=`login`.`L_id` WHERE `login`.`type`='pending'"
    res=selectall(qry)
    return render_template('admin/Approve_Turf.html',data=res)

@app.route('/accept_turf')
@login_required
def accept_turf():
    id=request.args.get('id')
    qry="UPDATE `login` SET `type`='turf' WHERE `L_id`=%s"
    iud(qry,id)
    return '''<script>alert("Accepted successfully");window.location='/Approve_Turf'</script>'''

@app.route('/reject_turf')
@login_required
def reject_turf():
    id=request.args.get('id')
    qry="UPDATE `login` SET `type`='reject' WHERE `L_id`=%s"
    iud(qry,id)
    return '''<script>alert("Reject successfully");window.location='/Approve_Turf'</script>'''

@app.route('/View_Complaint')
@login_required
def View_Complaint():
    qry="SELECT `turf`.*,`login`.* FROM `turf` JOIN `login` ON `turf`.`l_id`=`login`.`L_id` WHERE `login`.`type`='turf'"
    res=selectall(qry)
    return render_template('admin/View_Complaint.html',data=res)

@app.route('/View_turf_Complaint',methods=['post'])
@login_required
def View_turf_Complaint():
    id=request.form['select']
    qry1="SELECT `complaint`.*,`user`.* FROM `complaint` JOIN `user` ON `complaint`.`l_id`=`user`.`l_id` WHERE `complaint`.`t_id`=%s"
    res1=selectall2(qry1,id)

    qry="SELECT `turf`.*,`login`.* FROM `turf` JOIN `login` ON `turf`.`l_id`=`login`.`L_id` WHERE `login`.`type`='turf'"
    res=selectall(qry)
    return render_template('admin/View_Complaint.html',val=res1,data=res)

@app.route('/Send_Reply')
@login_required
def Send_Reply():
    id=request.args.get('id')
    session['comid']=id
    return render_template('admin/Send_Reply.html')

@app.route('/reply_post',methods=['post'])
@login_required
def reply_post():
    rply=request.form['textfield']
    qry="UPDATE `complaint` SET `reply`=%s WHERE `c_id`=%s"
    val=(rply,session['comid'])
    iud(qry,val)
    return '''<script>alert("Sended successfully");window.location='/View_Complaint'</script>'''

@app.route('/View_Accept_Turf')
@login_required
def View_Accept_Turf():
    qry="SELECT `turf`.*,`login`.* FROM `turf` JOIN `login` ON `turf`.`l_id`=`login`.`L_id` WHERE `login`.`type`='turf'"
    res=selectall(qry)
    return render_template('admin/View_Accept_Turf.html',data=res)

@app.route('/View_Facility')
@login_required
def View_Facility():
    id=request.args.get('id')
    qry="SELECT * FROM `facility` WHERE `T_ID`=%s"
    # qry="SELECT `turf`.`l_id`,`facility`.* FROM `turf` JOIN `facility` ON `turf`.`l_id`=`facility`.`T_ID`   WHERE `turf`.`l_id`=%s"
    res=selectall2(qry,id)
    return render_template('admin/View_Facility.html',data=res)

@app.route('/view_user')
@login_required
def view_user():
    qry="select * from `user`"
    res=selectall(qry)
    return render_template('admin/view_user.html',data=res)

#=======================================================TURF============================================================
@app.route('/Registeration')
def Registeration():
    return render_template('reg_index.html')

@app.route('/reg', methods=['POST'])
def reg():

    name=request.form['name']
    place=request.form['place']
    post=request.form['post']
    pin=request.form['pin']
    email=request.form['email']
    phone=request.form['phone']
    # lati=request.form['lati']
    # longi=request.form['longi']
    username=request.form['uname']
    password=request.form['pswd']
    img=request.files['img']

    q="INSERT INTO `login` VALUES (null,%s,%s,'pending')"
    val=(username,password)
    res=iud(q,val)

    qry="INSERT INTO `turf` VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val1=(str(res),name,place,post,pin,email,phone,0,0)
    iud(qry,val1)
    img.save("static/timg/"+str(res)+".png")
    session['rtid']=res
    return render_template("reg_index1.html")

@app.route('/reg2', methods=['POST','GET'])
def reg2():
    return render_template("reg_index1.html")
@app.route('/reg1', methods=['POST'])
def reg1():


    lati=request.form['lati']
    longi=request.form['longi']

    res=session['rtid']
    qry="UPDATE `turf` SET `latitude`=%s ,`longitude`=%s WHERE `l_id`=%s"
    v=(lati,longi,res)
    iud(qry,v)

    return '''<script>alert("Registred successfully");window.location='/'</script>'''


@app.route('/Turf_home')
@login_required
def Turf_home():
    return render_template('turf/turf_index.html')

@app.route('/turf_View_Facility')
@login_required
def turf_View_Facility():
    qry="SELECT * FROM `facility` WHERE `T_ID`=%s"
    res=selectall2(qry,session['lid'])
    return render_template('turf/View_Facility.html',data=res)

@app.route('/Add_facility')
@login_required
def Add_facility():
    return render_template('turf/Add_facility.html')

@app.route('/add_facility_post', methods=['POST'])
@login_required
def add_facility_post():
    facility=request.form['textfield']
    desc=request.form['textfield2']

    qry="insert into `facility` (`T_ID`,`facility`,`description`) values (%s,%s,%s)"
    val1=(session['lid'],facility,desc)
    iud(qry,val1)
    return '''<script>alert("Added successfully");window.location='/turf_View_Facility'</script>'''

@app.route('/delete_facility')
@login_required
def delete_facility():
    id=request.args.get('id')
    qry="DELETE FROM `facility` WHERE `F_ID`=%s"
    iud(qry,id)
    return '''<script>alert("Deleted successfully");window.location='/turf_View_Facility'</script>'''

@app.route('/view_gallery')
@login_required
def view_gallery():
    q="SELECT * FROM `gallery` WHERE `turf_id`=%s"
    res=selectall2(q,session['lid'])
    return render_template('turf/view_gallery.html',data=res)

@app.route('/delete_image')
@login_required
def delete_image():
    id=request.args.get('id')
    q="DELETE FROM `gallery` WHERE `g_id`=%s"
    res=iud(q,id)
    return '''<script>alert("Deleted successfully");window.location='/view_gallery'</script>'''

@app.route('/Add_Gallery')
@login_required
def Add_Gallery():
    return render_template('turf/Add_Gallery.html')

@app.route('/add_gallery_post',methods=['post'])
@login_required
def add_gallery_post():
    img = request.files['file']
    fname = secure_filename(img.filename)
    img.save(os.path.join('static/gallery', fname))
    q="INSERT INTO `gallery` VALUES (NULL,%s,%s,CURDATE())"
    val=(session['lid'],fname)
    iud(q,val)
    return '''<script>alert("Added successfully");window.location='/view_gallery'</script>'''

@app.route('/view_rate__info')
@login_required
def view_rate__info():
    q="SELECT * FROM `rate` WHERE `t_id`=%s "
    res=selectall2(q,session['lid'])
    return render_template('turf/view_rate__info.html',data=res)

@app.route('/Add_rate_info')
@login_required
def Add_rate_info():
    return render_template('turf/Add_rate_info.html')

@app.route('/rate_info_post', methods=['POST'])
@login_required
def rate_info_post():
    rate=request.form['textfield']
    desc=request.form['textfield2']
    q="INSERT INTO `rate` VALUES(NULL,%s,%s,%s,CURDATE())"
    val=(str(session['lid']),rate,desc)
    res=iud(q,val)
    return '''<script>alert("Added successfully");window.location='/view_rate__info'</script>'''

@app.route('/delete_rate')
@login_required
def delete_rate():
    id=request.args.get('id')
    q="DELETE FROM `rate` WHERE `rate_id`=%s"
    res=iud(q,id)
    return '''<script>alert("Deleted successfully");window.location='/view_rate__info'</script>'''

@app.route('/Update_status')
@login_required
def Update_status():
    return render_template('turf/Update_status.html')

@app.route('/View_booking')
@login_required
def View_booking():
    qry="SELECT `booking`.*,`slot`.*,`user`.`f_name`,`l_name` FROM `booking` JOIN `slot` ON `booking`.`s_id`=`slot`.`slot_id` JOIN `user` ON `booking`.`u_id`=`user`.`l_id` WHERE `booking`.`t_id`=%s"
    res=selectall2(qry,session['lid'])
    return render_template('turf/View_booking.html',data=res)

@app.route('/accept_booking')
@login_required
def accept_booking():
    id=request.args.get('id')
    qry="UPDATE `booking` SET  `status`='Accepted' WHERE `b_id`=%s AND `t_id`=%s"
    val=(id,session['lid'])
    iud(qry,val)
    return '''<script>alert("Accepted successfully");window.location='/View_booking'</script>'''

@app.route('/reject_booking')
@login_required
def reject_booking():
    id=request.args.get('id')
    qry="UPDATE `booking` SET  `status`='Rejected' WHERE `b_id`=%s AND `t_id`=%s"
    val=(id,session['lid'])
    iud(qry,val)
    return '''<script>alert("Rejected successfully");window.location='/View_booking'</script>'''

@app.route('/view_camp_details')
def view_camp_details():
    qry="SELECT * FROM `camp_details` WHERE `t_id`=%s"
    res=selectall2(qry,str(session['lid']))
    print(res)
    return render_template('turf/view_camp_details.html',data=res)

@app.route('/add_camp_details')
def add_camp_details():
    return render_template('turf/add_camp_details.html')

@app.route('/add_camp_details_post', methods=['POST'])
def add_camp_details_post():
    type=request.form['select2']
    name=request.form['textfield']
    details=request.form['textfield2']
    time=request.form['textfield3']
    day=request.form['select']
    qry="INSERT INTO `camp_details` VALUES (NULL,%s,%s,%s,%s,%s,%s)"
    val=(str(session['lid']),type,name,details,time,day)
    iud(qry,val)
    return '''<script>alert("Added successfully");window.location='/view_camp_details'</script>'''

@app.route('/view_camp_request_and_verify')
def view_camp_request_and_verify():
    q="SELECT `camp_details`.*,`request_for_camp`.*,`user`.`f_name`,`user`.`l_name` FROM `request_for_camp` JOIN `camp_details` ON `camp_details`.`c_id`=`request_for_camp`.`c_id` JOIN `user` ON `user`.`l_id`=`request_for_camp`.`u_id` WHERE `camp_details`.`t_id`=%s"
    res=selectall2(q,str(session['lid']))
    return render_template('turf/view_camp_request_and_verify.html',data=res)

@app.route('/accept_camp_req')
def accept_camp_req():
    id=request.args.get('id')
    q="UPDATE `request_for_camp` SET `status`='Accepted' WHERE `req_id`=%s"
    iud(q,id)
    return '''<script>alert("Accepted successfully");window.location='/view_camp_request_and_verify'</script>'''

@app.route('/reject_camp_req')
def reject_camp_req():
    id=request.args.get('id')
    q="UPDATE `request_for_camp` SET `status`='Rejected' WHERE `req_id`=%s"
    iud(q,id)
    return '''<script>alert("Accepted successfully");window.location='/view_camp_request_and_verify'</script>'''


app.run(debug=True)