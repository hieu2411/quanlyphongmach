from flask import *

from app import Symptom

symptom_route = Blueprint('symptom_route', __name__)


@symptom_route.route('/admin/symptom/index')
def symptom_index():
    # check if signed in then show lower users list
    if session.get('signed_in'):
        data = Symptom.query.all()
        if data:
            return render_template('admin/symptom/index.html', data=data, role=session['role'], title = 'Symptom index')
        return render_template('admin/symptom/index.html', data=None, role=session['role'], title = 'Symptom index')
    return redirect('/admin/login')


@symptom_route.route('/admin/symptom/create', methods=['GET', 'POST'])
def create_symptom():
    # check if signed in then show lower users list
    if session.get('signed_in'):
        if request.method == 'POST':
            result = Symptom.create(symptom=request.form['name'])
            if result is not None:
                flash('Successfully added new symptom')
        return render_template('admin/symptom/create.html', role=session['role'], title = 'Add symptom')
    return redirect('/admin/login')


@symptom_route.route('/admin/symptom/details/<id>', methods=['get', 'post'])
def symptom_details(id):
    if session.get('signed_in'):

        # find that symptom by id
        symptom = Symptom.query.get(id)
        if symptom:
            # in jinja use items() to unpack key and value from dict
            return render_template('admin/symptom/detail.html', data=symptom.as_dict(), role=session['role'], title = 'Symptom detail')
        flash('Symptom not found')
    return redirect('/admin/login')


@symptom_route.route('/admin/symptom/edit/<id>', methods=['GET', 'POST'])
def symptom_edit(id):
    if session.get('signed_in'):
        symptom = Symptom.query.get(id)
        if symptom:
            if request.method == 'POST':
                update_data = {'id': id,
                               'symptom': request.form['name'],
                               }
                Symptom.update(data=update_data)
                return redirect('/admin/symptom/index')
            # show info first
            return render_template('admin/symptom/edit.html', data=symptom.as_dict(), role=session['role'], title = 'Edit symptom')
        return render_template('admin/symptom/edit.html', data=None, role = session['role'], title = 'Edit symptom')
    return redirect('/admin/login')


@symptom_route.route('/admin/symptom/delete/<id>', methods=['GET', 'POST'])
def symptom_delete(id):
    if session.get('signed_in'):

        # won't delete, only change is_Active to False

        # find user with id
        symptom = Symptom.query.get(id)
        if request.method == 'POST':
            Symptom.delete(id)
            return redirect('/admin/symptom/index')
        if symptom:
            return render_template('admin/symptom/delete.html', data=symptom.as_dict(), role=session['role'], title = 'Symptom details')
        # need some more code for confirmation

    return redirect('/admin/login')
