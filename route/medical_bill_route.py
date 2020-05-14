from flask import *

from app import Medical_bill, Sickness, Symptom, Patient, User, Drug

medical_bill_route = Blueprint('medical_bill_route', __name__)


@medical_bill_route.route('/admin/medical_bill/index')
def medical_bill_index():
    # check if signed in then show lower users list
    if session.get('signed_in'):
        medical_bills = Medical_bill.query.all()
        data = []
        for medical_bill in medical_bills:
            patient = Patient.query.get(medical_bill.patient_id)
            data.append({
                'id': medical_bill.id,
                'name': patient.name,
                'phone': patient.phone,
                'address': patient.address,
                'sickness': Sickness.query.get(medical_bill.sickness_id).sickness,
                'symptoms': medical_bill.symptoms_id,

            })
        if data:
            return render_template('admin/medical_bill/index.html', data=data)
        return render_template('admin/medical_bill/index.html', data=None)
    return redirect('/admin/login')


# @medical_bill_route.route('/admin/medical_bill/search_patient', methods = ['POST', 'GET'])
# def patient_search():
#     # check if signed in then show lower users list
#     if session.get('signed_in'):
#         if request.method == 'POST':
#             username = request.form['username']
#             user = User.query.get(request.form['username']).first()
#             patient = Patient.query.filter(Patient.account_id == User.query.get(request.form['username'])).first()
#             if patient:
#                 return render_template('admin/medical_bill/create.html', patient=patient)
#         return render_template('admin/medical_bill/create.html', patient=None)
#     return redirect('/admin/login')


@medical_bill_route.route('/admin/medical_bill/create', methods=['GET', 'POST'])
def create_medical_bill():
    # check if signed in then show lower users list
    if session.get('signed_in'):
        if request.method == 'POST':
            patient = None
            # search patient information if have registered before

            drugs = request.form.getlist('drug')
            qty = request.form.getlist('quantity')

            if request.form['name'] == '' or request.form['phone'] == '' or request.form['address'] == '' and \
                    request.form['username'] != '':
                patient = Patient.query.filter(
                    Patient.account_id == User.query.filter(
                        User.username == request.form['username']).first().id).first()

                return render_template('admin/medical_bill/create.html', sicknesses=Sickness.query.all(),
                                       symptoms=Symptom.query.all(),
                                       drugs=Drug.query.all(),
                                       patient=patient)
            else:  # create new patient profile
                patient = Patient.create(name=request.form['name'],
                                         phone=request.form['phone'],
                                         address=request.form['address'])
            symptom_id = ''
            for symptom in request.form.getlist('symptom'):
                if symptom_id != '':
                    symptom_id += ', '
                symptom_id += symptom

            medical_bill = Medical_bill.create(symptoms_id=symptom_id,
                                               sickness_id=request.form['sickness'],
                                               patient_id=patient.id)

            # create medical bill detail

            if medical_bill is not None:
                flash('Successfully added new medical_bill')
                redirect('/admin/medical_bill/index')
        return render_template('admin/medical_bill/create.html', sicknesses=Sickness.query.all(),
                               symptoms=Symptom.query.all(),
                               drugs = Drug.query.all(),
                               patient=None)

    return redirect('/admin/login')


@medical_bill_route.route('/admin/medical_bill/details/<id>', methods=['get', 'post'])
def medical_bill_details(id):
    if session.get('signed_in'):

        # find that medical_bill by id
        medical_bill = Medical_bill.query.get(id)
        if medical_bill:
            # in jinja use items() to unpack key and value from dict
            return render_template('admin/medical_bill/detail.html', data=medical_bill.as_dict())
        flash('Medical_bill not found')
    return redirect('/admin/login')


@medical_bill_route.route('/admin/medical_bill/edit/<id>', methods=['GET', 'POST'])
def medical_bill_edit(id):
    if session.get('signed_in'):
        medical_bill = Medical_bill.query.get(id)
        if medical_bill:
            if request.method == 'POST':
                update_data = {'id': id,
                               'medical_bill': request.form['name'],
                               }
                Medical_bill.update(data=update_data)
                return redirect('/admin/medical_bill/index')
            # show info first
            return render_template('admin/medical_bill/edit.html', data=medical_bill.as_dict())
        return render_template('admin/medical_bill/edit.html', data=None)
    return redirect('/admin/login')
