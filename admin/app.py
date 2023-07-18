import hashlib
from flask import Flask, render_template, request, redirect, session, url_for
from flaskext.mysql import MySQL
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from handler import *

app = Flask(__name__)
app.secret_key = 'Mage is the best!'

# MySQL
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = "root"
app.config['MYSQL_DATABASE_PASSWORD'] = "root"
app.config['MYSQL_DATABASE_DB'] = "square"
app.config['MYSQL_DATABASE_HOST'] = "localhost"
mysql.init_app(app)


def login_required(f):
	@wraps(f)
	def wrapped(*args, **kwargs):
		if 'authorised' not in session:
			return render_template('login.html')
		return f(*args, **kwargs)
	return wrapped


@app.context_processor
def inject_tables_and_counts():
	data = count_all(mysql)
	return dict(tables_and_counts=data)


@app.route('/')
@app.route('/index')
@login_required
def index():
	return render_template('index.html')


@app.route("/attendence")
@login_required
def attendence():
	data = fetch_all(mysql, "attendence")
	return render_template('attendence.html', data=data, table_count=len(data))


@app.route('/edit_attendence/<string:act>/<int:modifier_id>', methods=['GET', 'POST'])
@login_required
def edit_attendence(modifier_id, act):
	if act == "add":
		return render_template('edit_attendence.html', data="", act="add")
	else:
		data = fetch_one(mysql, "attendence", "id", modifier_id)
	
		if data:
			return render_template('edit_attendence.html', data=data, act=act)
		else:
			return 'Error loading #%s' % modifier_id


@app.route("/buffer")
@login_required
def buffer():
	data = fetch_all(mysql, "buffer")
	return render_template('buffer.html', data=data, table_count=len(data))


@app.route('/edit_buffer/<string:act>/<int:modifier_id>', methods=['GET', 'POST'])
@login_required
def edit_buffer(modifier_id, act):
	if act == "add":
		return render_template('edit_buffer.html', data="", act="add")
	else:
		data = fetch_one(mysql, "buffer", "id", modifier_id)
	
		if data:
			return render_template('edit_buffer.html', data=data, act=act)
		else:
			return 'Error loading #%s' % modifier_id


@app.route("/course")
@login_required
def course():
	data = fetch_all(mysql, "course")
	return render_template('course.html', data=data, table_count=len(data))


@app.route('/edit_course/<string:act>/<int:modifier_id>', methods=['GET', 'POST'])
@login_required
def edit_course(modifier_id, act):
	if act == "add":
		return render_template('edit_course.html', data="", act="add")
	else:
		data = fetch_one(mysql, "course", "id", modifier_id)
	
		if data:
			return render_template('edit_course.html', data=data, act=act)
		else:
			return 'Error loading #%s' % modifier_id


@app.route("/room")
@login_required
def room():
	data = fetch_all(mysql, "room")
	return render_template('room.html', data=data, table_count=len(data))


@app.route('/edit_room/<string:act>/<int:modifier_id>', methods=['GET', 'POST'])
@login_required
def edit_room(modifier_id, act):
	if act == "add":
		return render_template('edit_room.html', data="", act="add")
	else:
		data = fetch_one(mysql, "room", "id", modifier_id)
	
		if data:
			return render_template('edit_room.html', data=data, act=act)
		else:
			return 'Error loading #%s' % modifier_id


@app.route("/semester")
@login_required
def semester():
	data = fetch_all(mysql, "semester")
	return render_template('semester.html', data=data, table_count=len(data))


@app.route('/edit_semester/<string:act>/<int:modifier_id>', methods=['GET', 'POST'])
@login_required
def edit_semester(modifier_id, act):
	if act == "add":
		return render_template('edit_semester.html', data="", act="add")
	else:
		data = fetch_one(mysql, "semester", "id", modifier_id)
	
		if data:
			return render_template('edit_semester.html', data=data, act=act)
		else:
			return 'Error loading #%s' % modifier_id


@app.route("/student")
@login_required
def student():
	data = fetch_all(mysql, "student")
	return render_template('student.html', data=data, table_count=len(data))


@app.route('/edit_student/<string:act>/<int:modifier_id>', methods=['GET', 'POST'])
@login_required
def edit_student(modifier_id, act):
	if act == "add":
		return render_template('edit_student.html', data="", act="add")
	else:
		data = fetch_one(mysql, "student", "id", modifier_id)
	
		if data:
			return render_template('edit_student.html', data=data, act=act)
		else:
			return 'Error loading #%s' % modifier_id


@app.route("/subject")
@login_required
def subject():
	data = fetch_all(mysql, "subject")
	return render_template('subject.html', data=data, table_count=len(data))


@app.route('/edit_subject/<string:act>/<int:modifier_id>', methods=['GET', 'POST'])
@login_required
def edit_subject(modifier_id, act):
	if act == "add":
		return render_template('edit_subject.html', data="", act="add")
	else:
		data = fetch_one(mysql, "subject", "id", modifier_id)
	
		if data:
			return render_template('edit_subject.html', data=data, act=act)
		else:
			return 'Error loading #%s' % modifier_id


@app.route("/teacher")
@login_required
def teacher():
	data = fetch_all(mysql, "teacher")
	return render_template('teacher.html', data=data, table_count=len(data))


@app.route('/edit_teacher/<string:act>/<int:modifier_id>', methods=['GET', 'POST'])
@login_required
def edit_teacher(modifier_id, act):
	if act == "add":
		return render_template('edit_teacher.html', data="", act="add")
	else:
		data = fetch_one(mysql, "teacher", "id", modifier_id)
	
		if data:
			return render_template('edit_teacher.html', data=data, act=act)
		else:
			return 'Error loading #%s' % modifier_id


@app.route("/users")
@login_required
def users():
	data = fetch_all(mysql, "users")
	return render_template('users.html', data=data, table_count=len(data))


@app.route('/edit_users/<string:act>/<int:modifier_id>', methods=['GET', 'POST'])
@login_required
def edit_users(modifier_id, act):
	if act == "add":
		return render_template('edit_users.html', data="", act="add")
	else:
		data = fetch_one(mysql, "users", "id", modifier_id)
	
		if data:
			return render_template('edit_users.html', data=data, act=act)
		else:
			return 'Error loading #%s' % modifier_id


@app.route('/save', methods=['GET', 'POST'])
@login_required
def save():
	cat = ''
	if request.method == 'POST':
		post_data = request.form.to_dict()
		if 'password' in post_data:
			post_data['password'] = hashlib.md5(post_data['password'].encode('utf-8')).hexdigest()
		if post_data['act'] == 'add':
			cat = post_data['cat']
			insert_one(mysql, cat, post_data)
		elif post_data['act'] == 'edit':
			cat = post_data['cat']
			update_one(mysql, cat, post_data, post_data['modifier'], post_data['id'])
	else:
		if request.args['act'] == 'delete':
			cat = request.args['cat']
			delete_one(mysql, cat, request.args['modifier'], request.args['id'])
	return redirect("./" + cat)


@app.route('/login')
def login():
	if 'authorised' in session:
		return redirect(url_for('index'))
	else:
		error = request.args['error'] if 'error' in request.args else ''
		return render_template('login.html', error=error)


@app.route('/login_handler', methods=['POST'])
def login_handler():
	try:
		email = request.form['email']
		password = request.form['password']
		data = fetch_one(mysql, "users", "email", email)
		
		if data and len(data) > 0:
			if check_password_hash(data[3], password) or hashlib.md5(password.encode('utf-8')).hexdigest() == data[3]:
				session['authorised'] = 'authorised',
				session['id'] = data[0]
				session['name'] = data[1]
				session['email'] = data[2]
				session['role'] = data[4]
				return redirect(url_for('index'))
			else:
				return redirect(url_for('login', error='Wrong Email address or Password.'))
		else:
			return redirect(url_for('login', error='No user'))
	
	except Exception as e:
		return render_template('login.html', error=str(e))


@app.route('/logout')
@login_required
def logout():
	session.clear()
	return redirect(url_for('login'))


if __name__ == "__main__":
	app.run(debug=True,host='127.0.0.1', port=5001)
