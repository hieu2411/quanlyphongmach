from flask import *

from app import Medical_bill, Symptom, Patient, Drug, Medical_details, Usage, Statistic

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
                'sickness': medical_bill.sickness,
                'symptoms': medical_bill.symptoms_id,
            })
        if data:
            return render_template('admin/medical_bill/index.html', data=data, role=session['role'], title = 'Medical bill index')
        return render_template('admin/medical_bill/index.html', data=None, role=session['role'], title = 'Medical bill index')
    return redirect('/admin/login')


@medical_bill_route.route('/admin/medical_bill/create', methods=['GET', 'POST'])
def create_medical_bill():
    # check if signed in then show lower users list
    if session.get('signed_in'):
        patients = Patient.query.all()
        patient = None
        if request.method == 'POST':
            # patient selected

            if request.form['new_sickness'] != '' or request.form['sickness'] != '' or request.form['symptom'] != '' or \
                    request.form['drug'] != '':
                patient_id = request.form['patient']
                symptoms = ''
                for symptom in request.form.getlist('symptom'):
                    if symptoms != '':
                        symptoms += ', '
                    symptoms += symptom

                data = []
                for drug in request.form.getlist('drug'):
                    if drug != '':
                        temp = []
                        temp.append(drug)
                        data.append(temp)
                quantity = request.form.getlist('quantity')
                usages = request.form.getlist('usage')
                for i in range(len(data)):
                    qty = quantity[i]
                    if qty != '':
                        data[i].append(qty)
                for i in range(len(data)):
                    usage = usages[i]
                    if usage != '':
                        data[i].append(usage)

                medical_bill = Medical_bill.create(symptoms_id=symptoms,
                                                   sickness=request.form['sickness'],
                                                   patient_id=patient_id)
                medical_bill_id = medical_bill.id

                # create medical bill detail
                for obj in data:
                    drug_id = obj[0]
                    qty = obj[1]
                    usage = obj[2]
                    medical_bill_detail = Medical_details.create(bill_id=medical_bill_id,
                                                                 drug_id=drug_id,
                                                                 quantity=qty,
                                                                 usage=usage)
                    Statistic.create(drug_id=drug_id, qty=qty)

                if medical_bill is not None:
                    flash('Successfully added new medical_bill')
                    # EDIT redirect to medical_bill detail [id]
                    return redirect('/admin/medical_bill/index')

            # search patient information and load it
            if request.form['patient'] != '':
                patient = Patient.query.get(request.form['patient'])

                return render_template('admin/medical_bill/create.html',
                                       symptoms=Symptom.query.all(),
                                       drugs=Drug.query.all(),
                                       usages=Usage.query.all(),
                                       patients=patients,
                                       patient=patient, role=session['role'], title = 'Add medical bill')

        return render_template('admin/medical_bill/create.html',
                               symptoms=Symptom.query.all(),
                               drugs=Drug.query.all(),
                               usages=Usage.query.all(),
                               patient=None,
                               patients=patients, role=session['role'], title = 'Add medical bill')

    return redirect('/admin/login')


@medical_bill_route.route('/admin/medical_bill/details/<id>', methods=['get', 'post'])
def medical_bill_details(id):
    if session.get('signed_in'):

        # find that medical_bill by id
        data = None
        medical_bill = Medical_bill.query.get(id).as_dict()
        patient = Patient.query.get(medical_bill['patient_id']).as_dict()
        medical_bill_details = Medical_details.query.filter(Medical_details.bill_id == medical_bill['id']).all()
        drug_qty_usage = []
        for medical_detail in medical_bill_details:
            drug = Drug.query.get(medical_detail.drug_id)
            drug_qty_usage.append({
                'drug': drug.name + ' - số lượng: ' + str(medical_detail.quantity) + ' - ' + medical_detail.usage,
            })
        if medical_bill:
            # in jinja use items() to unpack key and value from dict
            data = {
                'id': medical_bill['id'],
                'name': patient['name'],
                'phone': patient['phone'],
                'address': patient['address'],
                'sickness': medical_bill['sickness'],
                'symptoms': medical_bill['symptoms'],
                'date': medical_bill['examination_date'],
            }
            return render_template('admin/medical_bill/detail.html', data=data, drug_qty_usage=drug_qty_usage,
                                   role=session['role'], title = 'Medical bill details')
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

            medical_bill = Medical_bill.query.get(id).as_dict()
            patient = Patient.query.get(medical_bill['patient_id']).as_dict()
            medical_bill_details = Medical_details.query.filter(Medical_details.bill_id == medical_bill['id']).all()
            drug_qty_usage = []
            for medical_detail in medical_bill_details:
                drug = Drug.query.get(medical_detail.drug_id)
                drug_qty_usage.append({
                    'drug': drug.name + ' - số lượng: ' + str(medical_detail.quantity) + ' - ' + medical_detail.usage,
                })
            if medical_bill:
                # in jinja use items() to unpack key and value from dict
                data = {
                    'id': medical_bill['id'],
                    'name': patient['name'],
                    'phone': patient['phone'],
                    'address': patient['address'],
                    'sickness': medical_bill['sickness'],
                    'symptoms': medical_bill['symptoms'],
                    'date': medical_bill['examination_date'],
                }
            return render_template('admin/medical_bill/edit.html', data=data, role=session['role'], title = 'Medical bill edit')
        return render_template('admin/medical_bill/edit.html', data=None, role=session['role'], title = 'Medical bill edit')
    return redirect('/admin/login')
