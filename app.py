import datetime

from flask import Flask, request, flash, session, redirect, jsonify
from flask.templating import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phongmach.db'
db = SQLAlchemy(app)
level = ['user', 'moderator', 'admin']


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

    @classmethod
    def deactivate(cls, user_id):
        user = User.query.get(user_id)
        user.is_active = False
        db.session.commit()
        return True


class Drug(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "drug"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(125), nullable=False)
    effect = db.Column(db.String(125))

    def __repr__(self):
        return "<drug '{}'>".format(self.name)

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'effect': self.effect
        }

    @classmethod
    def create(cls, name, effect=''):
        drug = Drug(
            name=name,
            effect=effect
        )
        db.session.add(drug)
        db.session.commit()
        drug.password = ''
        return drug

    @classmethod
    def delete(cls, drug_id):
        try:
            Drug.query.filter_by(id=drug_id).delete()
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False

    @classmethod
    def update(cls, data):
        try:
            drug_data = {}
            for key in data:
                if hasattr(cls, key):
                    drug_data[key] = data[key]
            if 'id' not in drug_data:
                drug = Drug.query.filter_by(name=drug_data.get('name'))
                drug.update(drug_data)
            else:
                drug = Drug.query.filter_by(id=drug_data.get('id'))
                drug.update(drug_data)
            db.session.commit()
            return Drug.query.get(drug_data['id']).as_dict()
        except:
            return None


@app.route('/')
@app.route('/index')
@app.route('/homepage')
def homepage():
    return render_template('Homepage.html')


# can be used for user login too ... working
@app.route('/login', methods=['GET', 'POST'])
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
            return render_template('admin/login.html')

        # successful
        session['signed_in'] = True
        session['username'] = result.username
        flash('You were successfully signed in')
        return redirect('index')
    return render_template('admin/login.html')


# can be used to sign up for normal user too ... working
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
        return render_template('admin/register.html', user=user)
    return render_template('admin/register.html', title='Login')


@app.route('/admin/index')
def admin_index():
    # check if signed in then show lower users list
    if session.get('signed_in'):
        user = User.get(session.get('username'))
        if user is not None:
            if user.role == 'admin':
                data = user.query.all()
            if user.role == 'moderator':
                data = User.query.filter(User.role == 'user' or User.role == 'moderator').all()
            return render_template('admin/index.html', users=data)
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


@app.route('/admin/edit/<id>', methods=['GET', 'POST'])
def admin_edit(id):
    user = User.query.get(id)

    if user:

        if lower_level(user):
            return render_template('admin/index.html')

        if request.method == 'POST':
            update_data = {'id': id,
                           'email': request.form['email'],
                           'fullname': request.form['fullname'],
                           'mobile': request.form['mobile'],
                           }
            User.update(data=update_data)
            return redirect('/admin/index')
        # show info first
        return render_template('admin/edit.html', data=user.as_dict())

    return render_template('admin/edit.html', data=None)


@app.route('/admin/details/<id>')
def admin_details(id):
    # find that user by id
    user = User.query.get(id)
    if user:
        if lower_level(user):
            return render_template('admin/detail.html', data=None)

        # in jinja use items() to unpack key and value from dict
        return render_template('admin/detail.html', data=user.as_dict())
    flash('User not found')
    return render_template('admin/detail.html', data=None)


@app.route('/admin/delete/<id>', methods=['GET', 'POST'])
def admin_delete(id):
    # won't delete, only change is_Active to False

    # find user with id
    user = User.get(id)
    if request.method == 'POST':
        User.deactivate(id)
        return redirect('/admin/index')
    if user:
        if lower_level(user):
            return render_template('admin/index.html')
        return render_template('admin/delete.html', data=user.as_dict())
    # need some more code for confirmation

    return render_template('admin/delete.html', data=None)


@app.route('/admin/drug/index')
def drug_index():
    # check if signed in then show lower users list
    if session.get('signed_in'):
        data = Drug.query.all()
        return render_template('admin/drug/index.html', drugs=data)
    return redirect('homepage')


@app.route('/admin/drug/create', methods=['GET', 'POST'])
def create_drug():
    # check if signed in then show lower users list
    if session.get('signed_in'):
        test = request.method
        if request.method == 'POST':
            result = Drug.create(name=request.form['name'],
                                 effect=request.form['effect'])
            if result is not None:
                flash('Successfully added new drug')
                render_template('admin/drug/create.html')
        return render_template('admin/drug/create.html')
    return redirect('/admin/login')


@app.route('/admin/drug/details/<id>', methods=['get', 'post'])
def drug_details(id):
    # find that user by id
    drug = Drug.query.get(id)
    if drug:
        # in jinja use items() to unpack key and value from dict
        return render_template('admin/drug/detail.html', data=drug.as_dict())
    flash('Drug not found')
    return render_template('admin/drug/detail.html', data=None)



@app.route('/admin/drug/edit/<id>', methods=['GET', 'POST'])
def drug_edit(id):
    drug = Drug.query.get(id)

    if drug:
        if request.method == 'POST':
            update_data = {'id': id,
                           'name':request.form['name'],
                           'effect':request.form['effect']
                           }
            Drug.update(data=update_data)
            return redirect('/admin/drug/index')
        # show info first
        return render_template('admin/drug/edit.html', data=drug.as_dict())

    return render_template('admin/drug/edit.html', data=None)

@app.route('/admin/drug/delete/<id>', methods=['GET', 'POST'])
def drug_delete(id):
    # won't delete, only change is_Active to False

    # find user with id
    drug = Drug.query.get(id)
    if request.method == 'POST':
        Drug.delete(id)
        return redirect('/admin/drug/index')
    if drug:
        return render_template('admin/drug/delete.html', data=drug.as_dict())
    # need some more code for confirmation

    return render_template('admin/drug/delete.html', data=None)


def lower_level(user):
    # if that user level is higher than not allow to make action
    # if current user's level is higher then return False
    current_user = User.get(session.get('username'))
    if level.index(current_user.role) < level.index(user.role):
        flash('You cannot access to this user information due to higher level')
        return True
    return False


# just for testing
@app.route('/admin/showall')
def show_all_user():
    users = User.query.all()
    result = []
    for user in users:
        result.append(user.as_dict())
    result.append({'length': len(result)})
    return jsonify(result)


@app.route('/admin/drug/showall')
def show_all_drug():
    drugs = Drug.query.all()
    result = []
    for drug in drugs:
        result.append(drug.as_dict())
    result.append({'length': len(result)})
    return jsonify(result)


db.create_all()
if __name__ == '__main__':
    app.run(debug=True)
