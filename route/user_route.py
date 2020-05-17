from flask import *
from app import  Symptom,  Drug, User
user_route = Blueprint('user_route', __name__)




@user_route.route('/')
@user_route.route('/index')
@user_route.route('/homepage')
def homepage():
    return render_template('homepage.html')



# can be used for user login too ... working
@user_route.route('/login', methods=['GET', 'POST'])
@user_route.route('/admin/login', methods=['GET', 'POST'])
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
        current = User.get(session['username'])
        if current.role == 'user':
            return redirect('/index')
        else:
            return redirect('/admin/index')
        return redirect('/index')
    if request.method == 'POST':
        # check user and password, can sign in by username and email
        result = User.login(username=request.form['username'],
                            password=request.form['password'])

        # wrong login information
        if result == None:
            flash('Incorrect username or password')
            return render_template('admin/login.html', role = session['role'],  title = 'Login')

        # successful
        session['signed_in'] = True
        session['username'] = result.username
        session['role'] = result.role
        flash('You were successfully signed in')
        return redirect('/admin/index')
    return render_template('admin/login.html', title = 'Login')


# can be used to sign up for normal user too ... working
@user_route.route('/admin/register', methods=['GET', 'POST'])
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
        return redirect('/admin/index')
    # if current logging in user's role is admin then allow to create more admin and moderator, otherwise only allow to create moderator
    if session.get('signed_in'):
        user = User.get(session.get('username'))
        return render_template('admin/register.html', user=user, role = session['role'], title = 'Register')
    return render_template('admin/register.html', user = None, role = session['role'], title = 'Register')


@user_route.route('/logout')
@user_route.route('/admin/logout')
def logout():
    session['signed_in'] = False
    session['username'] = None
    session['role'] = None
    # if had created another admin account then automatically delete the default admin account
    if len(User.query.filter(User.role == 'admin').all()) > 1 and User.get('admin') is not None:
        id = User.get('admin').id
        User.delete(id)
    return redirect('/index')


@user_route.route('/admin/showall')
def all():
    data = []
    users = User.query.all()
    for user in users:
        data.append({
            'user': user.username,
            'password':user.password,
            'session[username]':session['username'],
            'session[loged_in]':session['signed_in'],
            'session[role]':session['role']
        })
    return jsonify(data)