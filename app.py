import datetime

from flask import Flask, request, flash, session, redirect, jsonify
from flask.templating import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phongmach.db'
db = SQLAlchemy(app)


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), unique=True, nullable=True)
    username = db.Column(db.String(100), unique=True)
    fullname = db.Column(db.String(125), nullable=False)
    password = db.Column(db.String(125), nullable=False)
    mobile = db.Column(db.String(32))
    is_active = db.Column(db.Boolean, index=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)
    role = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return "<User '{}'>".format(self.username)

    def as_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'fullname': self.fullname,
            'role': self.role,
            'mobile': self.mobile,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'last_login': self.last_login.strftime('%Y-%m-%d %H:%M:%S'),
        }

    @classmethod
    def get(cls, username, email=''):
        user = User.query.filter(username == username or email == email).first()
        if user is not None:
            user.password = ''
        return user

    @classmethod
    def create(cls, username, fullname, password, mobile, role='user'):
        user = User(
            username=username,
            fullname=fullname,
            role=role,
            mobile=mobile,
            password=password,
            is_active=True,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            last_login=datetime.datetime.now(),
        )
        db.session.add(user)
        db.session.commit()
        user.password = ''
        return user

    @classmethod
    def login(cls, username, password, email=''):
        user = User.query.filter(username == username or email == email).first()
        if user.password == password:
            user.password = ''
            return user
        else:
            return None

    @classmethod
    def update(cls, data):
        try:
            user_data = {}
            for key in data:
                if hasattr(cls, key):
                    user_data[key] = data[key]
            user_data['updated_at'] = datetime.datetime.now()
            if 'id' not in user_data:
                user = User.query.filter_by(email=user_data.get('email'))
                user.update(user_data)
            else:
                user = User.query.filter_by(id=user_data.get('id'))
                user.update(user_data)
            db.session.commit()
            return User.query.get(user_data['id']).as_dict()
        except:
            return None

    @classmethod
    def delete(cls, user_id):
        try:
            User.query.filter_by(id=user_id).delete()
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False


@app.route('/')
@app.route('/index')
@app.route('/homepage')
def homepage():
    return render_template('Homepage.html')


@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    # check if this is the first launch then allow to login with 'admin' 'admin'
    if len(User.query.filter(User.role == 'admin').all()) == 0:
        User.create(username='admin',
                    password='admin',
                    fullname='admin',
                    mobile='0',
                    role='admin')
    # check if already signed in or not

    if session.get('signed_in') == True:
        return redirect('index')
    if request.method == 'POST':
        # check user and password, can sign in by username and email
        result = User.login(username=request.form['username'],
                            password=request.form['password'],
                            email=request.form['username'])

        # wrong login information
        if result == None:
            flash('Incorrect username or password')
            return render_template('Admin/login.html')

        # successful
        session['signed_in'] = True
        session['username'] = result.username
        flash('You were successfully signed in')
        return redirect('index')
    return render_template('Admin/login.html')


@app.route('/admin/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = User.query.all()
        User.create(username=request.form['username'],
                    password=request.form['password'],
                    mobile=request.form['mobile'],
                    role=request.form['role'],
                    fullname=request.form['fullname'])
        # show message
        flash('You were successfully signed up, please sign in')
        return redirect('index')
    # if current logging in user's role is admin then allow to create more admin and moderator, otherwise only allow to create moderator
    if session.get('signed_in'):
        user = User.get(session.get('username'))
        return render_template('Admin/register.html', user=user)
    return render_template('Admin/register.html', title='Login')


@app.route('/admin/index')
def index():
    # check if signed in then show lower users list
    if session.get('signed_in'):
        user = User.get(session.get('username'))
        if user is not None:
            if user.role == 'admin':
                data = user.query.all()
            if user.role == 'moderator':
                data = User.query.filter(User.role == 'user' or User.role == 'moderator').all()
            return render_template('Admin/index.html', users=data)
    return redirect('homepage')

@app.route('/logout')
@app.route('/admin/logout')
def logout():
    session['signed_in'] = False
    session['username'] = None
    # if had created another admin account then automatically delete the default admin account
    if len(User.query.filter(User.role == 'admin').all()) > 1 and User.get('admin') is not None:
        id = User.get('admin').id
        User.delete(id)
    return redirect('/index')


@app.route('/admin/edit')
def edit():
    return render_template('Admin/edit.html')


@app.route('/admin/delete')
def delete():
    return render_template('Admin/delete.html')


@app.route('/admin/details')
def details():
    return render_template('Admin/details.html')



# def take_apopointment():
# #     # if loged in ...
# #     if session['signed_in']:
# #         ...
# #     else:
# #         return redirect('/signup')
# #     # if not ...

# just for testing
@app.route('/admin/showalluser')
def show_all_user():
    users = User.query.all()
    result = []
    for user in users:
        result.append(user.as_dict())
    result.append({'length':len(result)})
    return jsonify(result)

db.create_all()
if __name__ == '__main__':
    app.run(debug=True)
