import datetime
import random

from flask import *

from app import Symptom, Drug, User, Usage, Patient, db, Medical_bill

function_route = Blueprint('function_route', __name__)

# mnurse lap ds khm , tra cuu benh nhan
# cashier lap hoa don
# accountant thong ke doanh thu
# doctor lap phieu kham benh
# admin can view all others information, but others can only see, edit their own information
level = ['nurse', 'doctor', 'cashier', 'accountant', 'admin']


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
                price_out=price_in + 1000
            )
        return redirect('/admin/drug/index')


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
        for i in range(1, 20):
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

    if len(User.query.all()) < 2:
        User.create(username='hieu2411',
                    password='hieu2411',
                    fullname='ho phuoc hieu',
                    mobile='0903171998',
                    role='admin',
                    email='p.hieu2411@gmail.com')
        roles = ['nurse', 'accountant', 'doctor', 'cashier']
        for role in roles:
            User.create(username=role,
                        password='hieu2411',
                        fullname=role,
                        mobile='0123456789',
                        role=role,
                        email=role + '@gmail.com')
    if len(Patient.query.all()) < 10:
        for day in range(1,30):
            now = datetime.datetime.now()
            # 2 patient for a day
            for i in range(2):
                db.session.remove()
                patient = Patient(
                    name='Patient number ' + str(now.month) + '/' +str(day),
                    phone='0123456789',
                    address='address ' + str(i),
                    is_examined=False,
                    examination_date = datetime.datetime(2020, now.month, day)
                )
                db.session.add(patient)
                db.session.commit()
    return 'done'


def equal_datetime(date1, date2):
    if date1.day == date2.day and date1.month == date2.month and date1.year == date2.year :
        return True
    return False