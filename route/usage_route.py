from flask import *

from app import Usage

usage_route = Blueprint('usage_route', __name__)


@usage_route.route('/admin/usage/index')
def usage_index():
    # check if signed in then show lower users list
    if session.get('signed_in'):
        data = Usage.query.all()
        if data:
            return render_template('admin/usage/index.html', data=data, role=session['role'], title = 'Usage index')
        return render_template('admin/usage/index.html', data=None, role=session['role'], title = 'Usage index')
    return redirect('/admin/login')


@usage_route.route('/admin/usage/create', methods=['GET', 'POST'])
def create_usage():
    # check if signed in then show lower users list
    if session.get('signed_in'):
        if request.method == 'POST':
            result = Usage.create(usage=request.form['name'])
            if result is not None:
                flash('Successfully added new usage')
        return render_template('admin/usage/create.html', role=session['role'], title = 'Add usage')
    return redirect('/admin/login')


@usage_route.route('/admin/usage/details/<id>', methods=['get', 'post'])
def usage_details(id):
    if session.get('signed_in'):

        # find that usage by id
        usage = Usage.query.get(id)
        if usage:
            # in jinja use items() to unpack key and value from dict
            return render_template('admin/usage/detail.html', data=usage.as_dict(), role=session['role'], title = 'Usage details')
        flash('Usage not found')
    return redirect('/admin/login')


@usage_route.route('/admin/usage/edit/<id>', methods=['GET', 'POST'])
def usage_edit(id):
    if session.get('signed_in'):
        usage = Usage.query.get(id)
        if usage:
            if request.method == 'POST':
                update_data = {'id': id,
                               'usage': request.form['name'],
                               }
                Usage.update(data=update_data)
                return redirect('/admin/usage/index')
            # show info first
            return render_template('admin/usage/edit.html', data=usage.as_dict(), role=session['role'], title = 'Edit usage')
        return render_template('admin/usage/edit.html', data=None, role=session['role'], title = 'Edit usage')
    return redirect('/admin/login')
