from route.function_route import *

admin_route = Blueprint('admin_route', __name__)

@admin_route.route('/admin/index')
def admin_index():
    # check if signed in then show lower users lista
    if session.get('signed_in'):
        user = User.get(session.get('username'))
        if user is not None:
            if user.role == 'admin':
                data = user.query.all()
            if user.role == 'moderator':
                data = User.query.filter(User.role == 'user' or User.role == 'moderator').all()
            return render_template('admin/index.html', users=data)
    return redirect('/admin/login')


@admin_route.route('/admin/edit/<id>', methods=['GET', 'POST'])
def admin_edit(id):
    if session.get('signed_in'):
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
    return redirect('/admin/login')


@admin_route.route('/admin/details/<id>')
def admin_details(id):
    if session.get('signed_in'):
        # find that user by id
        user = User.query.get(id)
        if user:
            if lower_level(user):
                return render_template('admin/detail.html', data=None)

            # in jinja use items() to unpack key and value from dict
            return render_template('admin/detail.html', data=user.as_dict())
        flash('User not found')
        return render_template('admin/detail.html', data=None)
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
            if lower_level(user):
                return render_template('admin/index.html')
            return render_template('admin/delete.html', data=user.as_dict())
    # need some more code for confirmation

        return render_template('admin/delete.html', data=None)
    return redirect('/admin/login')

@admin_route.route('/manage')
@admin_route.route('/admin')
@admin_route.route('/admin/')
def manage():
    if session.get('signed_in'):
        return render_template('admin/manage.html')
    return redirect('/admin/login')


