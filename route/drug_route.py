from flask import *

from app import Drug

drug_route = Blueprint('drug_route', __name__)


@drug_route.route('/admin/drug/index')
def drug_index():
    # check if signed in then show lower users list
    if session.get('signed_in'):
        data = Drug.query.all()
        return render_template('admin/drug/index.html', data=data, role=session['role'], title = 'Drug index')
    return redirect('/admin/login')


@drug_route.route('/admin/drug/create', methods=['GET', 'POST'])
def create_drug():
    # check if signed in then show lower users list
    if session.get('signed_in'):
        if request.method == 'POST':
            result = Drug.create(name=request.form['name'], )
            if result is not None:
                flash('Successfully added new drug')
        return render_template('admin/drug/create.html', role=session['role'], title = 'Add drug')
    return redirect('/admin/login')


@drug_route.route('/admin/drug/details/<id>', methods=['get', 'post'])
def drug_details(id):
    if session.get('signed_in'):

        # find that user by id
        drug = Drug.query.get(id)
        if drug:
            # in jinja use items() to unpack key and value from dict
            return render_template('admin/drug/detail.html', data=drug.as_dict(), role=session['role'], title = 'Drug details')
        flash('Drug not found')
        return render_template('admin/drug/detail.html', data=None, role=session['role'], title = 'Drug details')
    return redirect('/admin/login')


@drug_route.route('/admin/drug/edit/<id>', methods=['GET', 'POST'])
def drug_edit(id):
    if session.get('signed_in'):

        drug = Drug.query.get(id)

        if drug:
            if request.method == 'POST':
                update_data = {'id': id,
                               'name': request.form['name'],
                               'effect': request.form['effect']
                               }
                Drug.update(data=update_data)
                return redirect('/admin/drug/index')
            # show info first
            return render_template('admin/drug/edit.html', data=drug.as_dict(), role=session['role'], title = 'Edit drug')

        return render_template('admin/drug/edit.html', data=None, role=session['role'], title = 'Edit drug')
    return redirect('/admin/login')


@drug_route.route('/admin/drug/delete/<id>', methods=['GET', 'POST'])
def drug_delete(id):
    if session.get('signed_in'):

        # won't delete, only change is_Active to False

        # find user with id
        drug = Drug.query.get(id)
        if request.method == 'POST':
            Drug.delete(id)
            return redirect('/admin/drug/index')
        if drug:
            return render_template('admin/drug/delete.html', data=drug.as_dict(), role=session['role'], title = 'Delete drug')
        # need some more code for confirmation

        return render_template('admin/drug/delete.html', data=None, role=session['role'], title = 'Delete drug')
    return redirect('/admin/login')
