from route.function_route import *

admin_route = Blueprint('admin_route', __name__)


@admin_route.route('/admin/index')
def admin_index():
    # check if signed in then show lower users lista
    if session.get('signed_in'):
        user = User.get(session.get('username'))
        if user is not None:
            if user.role == 'admin':
                data = User.query.all()
            else:
                data = User.query.filter(User.username == session.get('username')).all()
            return render_template('admin/index.html', users=data, role=session['role'], title = 'Admin index')
    return redirect('/admin/login')


@admin_route.route('/admin/edit/<id>', methods=['GET', 'POST'])
def admin_edit(id):
    if session.get('signed_in'):
        user = User.query.get(id)
        if user:
            if request.method == 'POST':
                update_data = {'id': id,
                               'email': request.form['email'],
                               'fullname': request.form['fullname'],
                               'mobile': request.form['mobile'],
                               'role': request.form['role']
                               }
                User.update(data=update_data)
                return redirect('/admin/index')
            # show info first
            return render_template('admin/edit.html', data=user.as_dict(), role=session['role'], title = 'Edit account')
        return render_template('admin/edit.html', data=None, role=session['role'], title = 'Edit account')
    return redirect('/admin/login')


@admin_route.route('/admin/details/<id>')
def admin_details(id):
    if session.get('signed_in'):
        # find that user by id
        user = User.query.get(id)
        if user:
            if user.username == session['username'] or session['role'] == 'admin':
                return render_template('admin/detail.html', data=user.as_dict(), role=session['role'], title = 'Account details')
            else:
                flash('Access denied')
                return render_template('admin/detail.html', data=None, role=session['role'], title = 'Account details')
        flash('User not found')
        return render_template('admin/detail.html', data=None, role=session['role'], title = 'Account details')
    return redirect('/admin/login')


@admin_route.route('/admin/delete/<id>', methods=['GET', 'POST'])
def admin_delete(id):
    # won't delete, only change is_Active to False
    if session.get('signed_in'):

        # find user with id
        user = User.get(id)
        if request.method == 'POST':
            User.deactivate(id)
            return redirect('/admin/index')
        if user:
            return render_template('admin/delete.html', data=user.as_dict(), role=session['role'], title = 'Delete account')
        # need some more code for confirmation

        return render_template('admin/delete.html', data=None, role=session['role'], title = 'Delete account')
    return redirect('/admin/login')


@admin_route.route('/admin/password/<id>', methods=['GET', 'POST'])
def change_password(id):
    if session.get('signed_in'):
        # find user with id
        user = User.query.get(id)

        if user:
            return render_template('admin/change_password.html', title='Change Password', data=user,
                                   role=session['role'])

        if request.method == 'POST':
            # check if old password field is same with user.password
            if User.login(username=user.username, password=request.form['old_password']):
                if request.form['new_password'] == request.form['confirm_password']:
                    User.update({
                        'id': user.id,
                        'password': request.form['new_password']
                    })
                    flash('Successfully changed password')
                else:
                    flash('Wrong password!')
                    return render_template('admin/change_password.html', title='Change Password', data=user,
                                           role=session['role'])
            return redirect('/admin/index')
    return redirect('/admin/login')


@admin_route.route('/manage')
@admin_route.route('/admin')
@admin_route.route('/admin/')
def manage():
    if session.get('signed_in'):
        return render_template('admin/manage.html', role=session['role'], title = 'Manage')
    return redirect('/admin/login')
