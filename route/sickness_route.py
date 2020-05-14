from flask import *

from app import Sickness

sickness_route = Blueprint('sickness_route', __name__)


@sickness_route.route('/admin/sickness/index')
def sickness_index():
    # check if signed in then show lower users list
    if session.get('signed_in'):
        data = Sickness.query.all()
        return render_template('admin/sickness/index.html', data=data)
    return redirect('/admin/login')


@sickness_route.route('/admin/sickness/create', methods=['GET', 'POST'])
def create_sickness():
    # check if signed in then show lower users list
    if session.get('signed_in'):
        if request.method == 'POST':
            result = Sickness.create(sickness=request.form['name'])
            if result is not None:
                flash('Successfully added new sickness')
        return render_template('admin/sickness/create.html')
    return redirect('/admin/login')


@sickness_route.route('/admin/sickness/details/<id>', methods=['get', 'post'])
def sickness_details(id):
    if session.get('signed_in'):

        # find that sickness by id
        sickness = Sickness.query.get(id)
        if sickness:
            # in jinja use items() to unpack key and value from dict
            return render_template('admin/sickness/detail.html', data=sickness.as_dict())
        flash('Sickness not found')
        return render_template('admin/sickness/detail.html', data=None)
    return redirect('/admin/login')


@sickness_route.route('/admin/sickness/edit/<id>', methods=['GET', 'POST'])
def sickness_edit(id):
    if session.get('signed_in'):
        sickness = Sickness.query.get(id)
        if sickness:
            if request.method == 'POST':
                update_data = {'id': id,
                               'sickness': request.form['name'],
                               }
                Sickness.update(data=update_data)
                return redirect('/admin/sickness/index')
            # show info first
            return render_template('admin/sickness/edit.html', data=sickness.as_dict())
        flash('Sickness not found')
        return render_template('admin/sickness/edit.html', data=None)
    return redirect('/admin/login')



@sickness_route.route('/admin/sickness/delete/<id>', methods=['GET', 'POST'])
def sickness_delete(id):
    if session.get('signed_in'):
        # won't delete, only change is_Active to False
        # find user with id
        sickness = Sickness.query.get(id)
        if request.method == 'POST':
            Sickness.delete(id)
            return redirect('/admin/sickness/index')
        if sickness:
            return render_template('admin/sickness/delete.html', data=sickness.as_dict())
        # need some more code for confirmation
        flash('Sickness not found')
        return render_template('admin/sickness/delete.html', data=None)
    return redirect('/admin/login')

