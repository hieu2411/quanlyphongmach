import random

from flask import *

from app import Symptom, Drug, User, Sickness, Sickness_symptom, Usage, Patient

function_route = Blueprint('function_route', __name__)

# mnurse lap ds khm , tra cuu benh nhan
# cashier lap hoa don
# accountant thong ke doanh thu
# doctor lap phieu kham benh
# admin can view all others information, but others can only see, edit their own information
level = ['user', 'nurse', 'doctor', 'cashier', 'accountant','admin']


def lower_level(user):
    # if that user level is higher than not allow to make action
    # if current user's level is higher then return False
    current_user = User.get(session.get('username'))
    if level.index(current_user.role) < level.index(user.role):
        flash('You cannot access to this user information due to higher level')
        return True
    return False


# just for testing
@function_route.route('/admin/showall')
def show_all_user():
    users = User.query.all()
    result = []
    for user in users:
        result.append(user.as_dict())
    result.append({'length': len(result)})
    return jsonify(result)


@function_route.route('/admin/drug/showall')
def show_all_drug():
    drugs = Drug.query.all()
    result = []
    for drug in drugs:
        result.append(drug.as_dict())
    result.append({'length': len(result)})
    return jsonify(result)


@function_route.route('/admin/drug/create_all')
def dump_drug():
    if len(Drug.query.all()) < 2:
        for i in range(1, 50):
            price_in = random.randint(5000, 20000)
            drug = Drug.create(
                name='drug name ' + str(i),
                effect='drug effect ' + str(i),
                price_in=price_in,
                price_out = price_in + 1000
            )
        return redirect('/admin/drug/index')

@function_route.route('/admin/create_all')
def dump_admin():
    if len(User.query.all()) < 2:
        for i in range(1, 20):
            if i % 2 == 0:
                user = User.create(
                    username='hieu24111' + str(i),
                    fullname='fullname admin ' + str(i),
                    mobile='0000000000',
                    role='admin',
                    password='hieu2411'
                )
            else:
                user = User.create(
                    username='hieu24111' + str(i),
                    fullname='fullname admin ' + str(i),
                    mobile='0000000000',
                    role='moderator',
                    password='hieu2411'
                )
    return redirect('/admin/index')

@function_route.route('/admin/symptom/create_all')
def dump_symptom():
    if len(Symptom.query.all()) < 2:
        symptoms = [
            'Ho',
            'Sốt',
            'Nhức đầu',
            'Sổ mũi',
            'Đau bụng',
            'Đau ngực',
            'Khó thở'
        ]
        for symptom in symptoms:
            Symptom.create(symptom)
    return redirect('/admin/symptom/index')

@function_route.route('/admin/sickness/create_all')
def dump_sickness():
    if len(Sickness.query.all()) < 2:
        sicknesses = [
            'Cảm',
            'Đau họng',
            'Rối loạn tiêu hoá',
            'Ung thư',
            'Tiêu chảy',
        ]
        for sickness in sicknesses:
            Sickness.create(sickness)
    return redirect('/admin/sickness/index')

@function_route.route('/admin/usage/create_all')
def dump_usage():
    if len(Usage.query.all()) < 2:
        usages = [
            'Uống ngày 3 bữa sau khi ăn',
            'Uống ngày 3 bữa trước khi ăn',
            'Uống ngày 2 bữa sau khi ăn',
            'Uống ngày 2 bữa trước khi ăn',
            'Uống vào buổi sáng',
            'Uống vào buổi tối',
            'Thoa lên vết thương',
            'Nhỏ',
            'Tiêm',
        ]
        for usage in usages:
            Usage.create(usage)
    return redirect('/admin/usage/index')

@function_route.route('/admin/patient/create_all')
def dump_patient():
    if len(Patient.query.all()) < 2:
        for i in range(10):
            user = User.create(username='patient000' + str(i),
                               fullname='Patient no ' + str(i),
                               password='hieu2411',
                               role='user',
                               mobile='012345678'
                               )
            patient = Patient.create(account_id=user.id, name=user.fullname, phone=user.mobile,
                                     address=user.fullname + ' address')
    return redirect('/admin/patient/index')

@function_route.route('/admin/sickness_symptom/showall')
def sickness_symptom_show():
    sicknesses = Sickness.query.all()
    result = []
    for sickness in sicknesses:
        data = Sickness_symptom.query.filter(Sickness_symptom.sickness_id == sickness.id).all()
        if len(data) > 0:
            symptoms = []
            for symptom in data:
                temp = Symptom.query.filter(Symptom.id == symptom.symptom_id).first()
                symptoms.append(temp.as_dict())
            result.append({
                'sickness': sickness.as_dict(),
                'symptom': symptoms
            })
    return jsonify(result)

@function_route.route('/admin/current')
def current_login():
    username = session['username']
    user = User.get(username)
    if user:
        return jsonify(user.as_dict())
    return 'None'

@function_route.route('/admin/dump_all')
def dump_all():
    if len(Drug.query.all()) < 2:
        for i in range(1, 50):
            price_in = random.randint(5000, 20000)
            drug = Drug.create(
                name='drug name ' + str(i),
                effect='drug effect ' + str(i),
                price_in=price_in,
                price_out=price_in + 1000
            )

    if len(Symptom.query.all()) < 2:
        symptoms = [
            'Ho',
            'Sốt',
            'Nhức đầu',
            'Sổ mũi',
            'Đau bụng',
            'Đau ngực',
            'Khó thở'
        ]
        for symptom in symptoms:
            Symptom.create(symptom)

    if len(Sickness.query.all()) < 2:
        sicknesses = [
            'Cảm',
            'Đau họng',
            'Rối loạn tiêu hoá',
            'Ung thư',
            'Tiêu chảy',
        ]
        for sickness in sicknesses:
            Sickness.create(sickness)

    if len(Usage.query.all()) < 2:
        usages = [
            'Uống ngày 3 bữa sau khi ăn',
            'Uống ngày 3 bữa trước khi ăn',
            'Uống ngày 2 bữa sau khi ăn',
            'Uống ngày 2 bữa trước khi ăn',
            'Uống vào buổi sáng',
            'Uống vào buổi tối',
            'Thoa lên vết thương',
            'Nhỏ',
            'Tiêm',
        ]
        for usage in usages:
            Usage.create(usage)

    return 'done'