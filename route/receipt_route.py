import datetime

from flask import *

from app import Medical_bill, Patient, Drug, Medical_details, Receipt
from route.function_route import equal_datetime

receipt_route = Blueprint('receipt_route', __name__)


def get_drugs_of_medical_bill(medical_bill_id):
    data = {'drugs_cost': 0,
            'drugs': []}
    bill_details = Medical_details.query.filter(Medical_details.bill_id == medical_bill_id)
    for bill in bill_details:
        drug = Drug.query.get(bill.drug_id)
        data['drugs_cost'] += bill.quantity * drug.price_out
        data['drugs'].append({
            'drug': drug.name,
            'price': drug.price_out,
            'quantity': bill.quantity,
            'sum': bill.quantity * drug.price_out,
        })
    return data


def get_patient_bill(patient_id):
    patient = Patient.query.get(patient_id).as_dict()
    if patient is not None:
        # return Suitable medical bill
        for patient_medical_bill in Medical_bill.query.filter(Medical_bill.patient_id == patient['id']).all():
            if equal_datetime(patient_medical_bill.examination_date, datetime.datetime.now()):
                return patient_medical_bill


def get_patient_of_today(is_examined=False, is_received_receipt=False):
    temp = Patient.query.all()
    patients = []
    # filter the patient of today and have been examined
    for result in temp:
        if equal_datetime(result.examination_date,
                          datetime.datetime.now()) and result.is_examined == is_examined and result.is_received_receipt == is_received_receipt:
            # if equal_datetime(result.examination_date, datetime.datetime(2020, 5, 15)) and result.is_examined is True:
            patients.append(result)
    return patients


def get_receipt_detail(receipt):
    medical_bill = Medical_bill.query.get(receipt.medical_bill_id)
    patient = Patient.query.get(medical_bill.patient_id)
    detail = {
        'id': receipt.id,
        'name': patient.name,
        'phone': patient.phone,
        'address': patient.address,
        'sickness': medical_bill.sickness,
        'drugs_cost': 0,
        'fee': receipt.fee,

        'drugs': [],
    }
    drugs_of_bill = get_drugs_of_medical_bill(receipt.medical_bill_id)
    detail['drugs'] = drugs_of_bill['drugs']
    detail['drugs_cost'] = drugs_of_bill['drugs_cost']
    return detail


@receipt_route.route('/admin/receipt/index')
def receipt_index():
    # check if signed in then show lower users list
    if session.get('signed_in'):
        receipts = Receipt.query.all()
        data = []
        for receipt in receipts:
            data.append(get_receipt_detail(receipt))

        if data:
            return render_template('admin/receipt/index.html', data=data, role=session['role'],
                                   title='Receipt index')
        return render_template('admin/receipt/index.html', data=None, role=session['role'],
                               title='Receipt index')
    return redirect('/admin/login')


@receipt_route.route('/admin/receipt/create', methods=['GET', 'POST'])
def create_receipt():
    # check if signed in then show lower users list
    if session.get('signed_in'):
        patients = get_patient_of_today(is_examined=True)

        patient = None
        if request.method == 'POST':
            # patient selected
            if request.form['fee'] != '':
                # minimum fee is 100000
                fee = int(request.form['fee'])
                if fee < 100000:
                    fee = 100000
                receipt = Receipt.create(medical_bill_id=get_patient_bill(request.form['patient']).id,
                                         fee=fee)
                if receipt:
                    # patient has received receipt
                    Patient.received_receipt(request.form['patient'])
                    flash('Receipt was added successfully')
                    return render_template('admin/receipt/create.html',
                                           patients=get_patient_of_today(is_examined=True),
                                           patient=None, role=session['role'], title='Add Receipt')
            # search patient information and load it
            if request.form['patient'] != '':
                patient = Patient.query.get(request.form['patient']).as_dict()
                patient_medical_bill = get_patient_bill(request.form['patient'])
                patient['sickness'] = patient_medical_bill.sickness
                patient['drug_cost'] = 0
                patient['medical_bill_id'] = patient_medical_bill.id
                patient['drugs'] = []

                # filter drugs of this patient
                for bill_detail in Medical_details.query.filter(
                        Medical_details.bill_id == patient_medical_bill.id).all():
                    drug = Drug.query.get(bill_detail.drug_id)
                    patient['drugs'].append({
                        'drug': drug.name,
                        'quantity': bill_detail.quantity,
                        'price': drug.price_out
                    })
                    patient['drug_cost'] += drug.price_out * bill_detail.quantity

                return render_template('admin/receipt/create.html',
                                       patients=patients,
                                       patient=patient, role=session['role'], title='Add Receipt')

        return render_template('admin/receipt/create.html',
                               patient=None,
                               patients=patients, role=session['role'], title='Add Receipt')

    return redirect('/admin/login')


@receipt_route.route('/admin/receipt/details/<id>', methods=['get', 'post'])
def receipt_details(id):
    if session.get('signed_in'):
        # find that receipt by id
        receipt = Receipt.query.get(id)
        data = get_receipt_detail(receipt)
        return render_template('admin/receipt/detail.html', data=data,
                               role=session['role'], title='Receipt details')
        flash('Receipt not found')
    return redirect('/admin/login')


@receipt_route.route('/admin/receipt/edit/<id>', methods=['GET', 'POST'])
def receipt_edit(id):
    if session.get('signed_in'):
        receipt = Receipt.query.get(id)
        if receipt:
            if request.method == 'POST':
                update_data = {'id': id,
                               'fee': request.form['fee']}
                Receipt.update(update_data)
                return redirect('/admin/receipt/index')
            # show info first
            data = get_receipt_detail(receipt)

            return render_template('admin/receipt/edit.html', data=data, role=session['role'],
                                   title='Receipt edit')
    return redirect('/admin/login')
