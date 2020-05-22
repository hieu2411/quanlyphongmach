from flask import *

from app import Patient
from route.receipt_route import get_patient_of_today

patient_route = Blueprint('patient_route', __name__)


@patient_route.route('/admin/patient/index')
def patient_index():
    # check if signed in then show lower users list
    if session.get('signed_in'):
        data = get_patient_of_today()
        return render_template('admin/patient/index.html', data=data, role = session['role'], title = 'Patient index')
    return redirect('/admin/login')


@patient_route.route('/admin/patient/create', methods=['GET', 'POST'])
def create_patient():
    # check if signed in then show lower users list
    if session.get('signed_in'):
        if request.method == 'POST':
            result = Patient.create(name=request.form['name'],
                                    phone=request.form['phone'],
                                    address=request.form['address'], )
            if result is not None:
                flash('Successfully added new patient')
        return render_template('admin/patient/create.html', role = session['role'], title = 'Add patient')
    return redirect('/admin/login')


@patient_route.route('/admin/patient/edit/<id>', methods=['GET', 'POST'])
def patient_edit(id):
    if session.get('signed_in'):
        patient = Patient.query.get(id)
        if patient:
            if request.method == 'POST':
                update_data = {'id': id,
                               'name': request.form['name'],
                               'phone': request.form['phone'],
                               'address': request.form['address']
                               }
                Patient.update(data=update_data)
                return redirect('/admin/patient/index')
            # show info first
            return render_template('admin/patient/edit.html', data=patient.as_dict(), role = session['role'], title = 'Edit patient')
        flash('Patient not found')
        return render_template('admin/patient/edit.html', data=None, role = session['role'], title = 'Edit patient')
    return redirect('/admin/login')


@patient_route.route('/admin/patient/details/<id>', methods=['get', 'post'])
def patient_details(id):
    if session.get('signed_in'):

        # find that user by id
        patient = Patient.query.get(id)
        if patient:
            # in jinja use items() to unpack key and value from dict
            return render_template('admin/patient/detail.html', data=patient.as_dict(), role = session['role'], title = 'Patient details')
        flash('Patient not found')
        return render_template('admin/patient/detail.html', data=None, role = session['role'], title = 'Patient details')
    return redirect('/admin/login')
