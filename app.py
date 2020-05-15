import datetime

from flask import *
from flask_sqlalchemy import SQLAlchemy

# import route


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phongmach.db'
db = SQLAlchemy(app)


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), unique=True, nullable=True)
    username = db.Column(db.String(100), unique=True)
    fullname = db.Column(db.String(125), nullable=False)
    password = db.Column(db.String(125), nullable=False)
    mobile = db.Column(db.String(32))
    is_active = db.Column(db.Boolean, index=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)
    role = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return "<User '{}'>".format(self.username)

    def as_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'fullname': self.fullname,
            'role': self.role,
            'mobile': self.mobile,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'last_login': self.last_login.strftime('%Y-%m-%d %H:%M:%S'),
            'password': self.password
        }

    @classmethod
    def get(cls, username):
        if username == None:
            return None
        user = User.query.filter(User.username == username).first()
        if user is not None:
            return user
        return None

    @classmethod
    def create(cls, username, fullname, password, mobile, role='user', email=None):
        user = User(
            username=username,
            fullname=fullname,
            role=role,
            mobile=mobile,
            password=password,
            is_active=True,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            last_login=datetime.datetime.now(),
        )
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def login(cls, username, password, email=''):
        user = User.query.filter(username == username or email == email).first()
        if user.password == password:
            return user
        else:
            return None

    @classmethod
    def update(cls, data):
        try:
            user_data = {}
            for key in data:
                if hasattr(cls, key):
                    user_data[key] = data[key]
            user_data['updated_at'] = datetime.datetime.now()
            if 'id' not in user_data:
                user = User.query.filter_by(email=user_data.get('email'))
                user.update(user_data)
            else:
                user = User.query.filter_by(id=user_data.get('id'))
                user.update(user_data)
            db.session.commit()
            return User.query.get(user_data['id']).as_dict()
        except:
            return None

    @classmethod
    def delete(cls, user_id):
        try:
            User.query.filter_by(id=user_id).delete()
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False

    @classmethod
    def deactivate(cls, user_id):
        user = User.query.get(user_id)
        user.is_active = False
        db.session.commit()
        return True


class Drug(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "drug"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(125), nullable=False)
    price_in = db.Column(db.Float, nullable=False)
    price_out = db.Column(db.Float, nullable=False)
    effect = db.Column(db.String(125))

    def __repr__(self):
        return "<drug '{}'>".format(self.name)

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'effect': self.effect
            , 'price_in': self.price_in,
            'price_out': self.price_out
        }

    @classmethod
    def create(cls, name, effect='', price_in=0, price_out=0):
        drug = Drug(
            name=name,
            effect=effect
            , price_in=price_in,
            price_out=price_out
        )
        db.session.add(drug)
        db.session.commit()
        return drug

    @classmethod
    def delete(cls, drug_id):
        try:
            Drug.query.filter_by(id=drug_id).delete()
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False

    @classmethod
    def update(cls, data):
        try:
            drug_data = {}
            for key in data:
                if hasattr(cls, key):
                    drug_data[key] = data[key]
            if 'id' not in drug_data:
                drug = Drug.query.filter_by(name=drug_data.get('name'))
                drug.update(drug_data)
            else:
                drug = Drug.query.filter_by(id=drug_data.get('id'))
                drug.update(drug_data)
            db.session.commit()
            return Drug.query.get(drug_data['id']).as_dict()
        except:
            return None


class Patient(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "patient"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(125), nullable=False)
    phone = db.Column(db.String(11), nullable=True)
    address = db.Column(db.String(120), nullable=False)
    examination_date = db.Column(db.DateTime)

    def __repr__(self):
        return "<patient '{}'>".format(self.name)

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'address': self.address
        }

    @classmethod
    def create(cls, name, phone, address):
        patient = Patient(
            name=name,
            phone=phone,
            address=address,
            examination_date=datetime.datetime.now()
        )
        db.session.add(patient)
        db.session.commit()
        return patient

    # @classmethod
    # def delete(cls, patient_id):
    #     try:
    #         Patient.query.filter_by(id=patient_id).delete()
    #         db.session.commit()
    #         return True
    #     except Exception as e:
    #         db.session.rollback()
    #         return False

    @classmethod
    def update(cls, data):
        try:
            patient_data = {}
            for key in data:
                if hasattr(cls, key):
                    patient_data[key] = data[key]
            if 'id' not in patient_data:
                patient = Patient.query.filter_by(name=patient_data.get('name'))
                patient.update(patient_data)
            else:
                patient = Patient.query.filter_by(id=patient_data.get('id'))
                patient.update(patient_data)
            db.session.commit()
            return Patient.query.get(patient_data['id']).as_dict()
        except:
            return None


class Symptom(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "symptom"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    symptom = db.Column(db.String(125), nullable=False)

    def __repr__(self):
        return "<symptom '{}'>".format(self.symptom)

    def as_dict(self):
        return {
            'id': self.id,
            'symptom': self.symptom,
        }

    @classmethod
    def create(cls, symptom):
        symptom = Symptom(
            symptom=symptom,
        )
        db.session.add(symptom)
        db.session.commit()
        return symptom

    @classmethod
    def update(cls, data):
        try:
            symptom_data = {}
            for key in data:
                if hasattr(cls, key):
                    symptom_data[key] = data[key]
            if 'id' not in symptom_data:
                symptom = Symptom.query.filter_by(symptom=symptom_data.get('symptom'))
                symptom.update(symptom_data)
            else:
                symptom = Symptom.query.filter_by(id=symptom_data.get('id'))
                symptom.update(symptom_data)
            db.session.commit()
            return Symptom.query.get(symptom_data['id']).as_dict()
        except:
            return None


class Sickness(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "sickness"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sickness = db.Column(db.String(125), nullable=False)

    def __repr__(self):
        return "<sickness '{}'>".format(self.sickness)

    def as_dict(self):
        return {
            'id': self.id,
            'sickness': self.sickness,
        }

    @classmethod
    def create(cls, sickness):
        sickness = Sickness(
            sickness=sickness,
        )
        db.session.add(sickness)
        db.session.commit()
        return sickness

    @classmethod
    def update(cls, data):
        try:
            sickness_data = {}
            for key in data:
                if hasattr(cls, key):
                    sickness_data[key] = data[key]
            if 'id' not in sickness_data:
                sickness = Sickness.query.filter_by(sickness=sickness_data.get('sickness'))
                sickness.update(sickness_data)
            else:
                sickness = Sickness.query.filter_by(id=sickness_data.get('id'))
                sickness.update(sickness_data)
            db.session.commit()
            return Sickness.query.get(sickness_data['id']).as_dict()
        except:
            return None


class Sickness_symptom(db.Model):  # a sickness should have which symptoms
    """ User Model for storing user related details """
    __tablename__ = "sickness_symptom"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sickness_id = db.Column(db.Integer, nullable=False)
    symptom_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<sickness_symptom '{}'>".format(self.id)

    def as_dict(self):
        return {
            'id': self.id,
            'sickness_id': self.sickness_id,
            'symptom_id': self.symptom_id
        }

    @classmethod
    def create(cls, sickness_id, symptom_id):
        sickness_symptom = Sickness_symptom(
            sickness_id=sickness_id,
            symptom_id=symptom_id
        )
        db.session.add(sickness_symptom)
        db.session.commit()
        return sickness_symptom

    @classmethod
    def update(cls, data):
        try:
            sickness_symptom_data = {}
            for key in data:
                if hasattr(cls, key):
                    sickness_symptom_data[key] = data[key]
            if 'id' not in sickness_symptom_data:
                sickness_symptom = Sickness_symptom.query.filter(
                    sickness_id=sickness_symptom_data.get('sickness_id'),
                    symptom_id=sickness_symptom_data.get('symptom_id'),

                )
                sickness_symptom.update(sickness_symptom_data)
            else:
                sickness_symptom = Sickness_symptom.query.filter_by(id=sickness_symptom_data.get('id'))
                sickness_symptom.update(sickness_symptom_data)
            db.session.commit()
            return Sickness_symptom.query.get(sickness_symptom_data['id']).as_dict()
        except:
            return None


class Medical_bill(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "medical_bill"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # change symptom id to symptom
    symptoms_id = db.Column(db.String(120), nullable=False)  # list of symptoms seperate by ' '
    sickness_id = db.Column(db.Integer, nullable=True)  # may add later
    patient_id = db.Column(db.Integer,
                           nullable=False)  # if profile haven't been created then created at the time bill is created
    examination_date = db.Column(db.DateTime)

    def __repr__(self):
        return "<medical_bill '{}'>".format(self.id)

    def as_dict(self):
        return {
            'id': self.id,
            'symptoms': self.symptoms_id,
            'sickness_id': self.sickness_id,
            'patient_id': self.patient_id,
            'examination_date': self.examination_date,
        }

    @classmethod
    def create(cls, symptoms_id, sickness_id=None, patient_id=None):
        medical_bill = Medical_bill(
            symptoms_id=symptoms_id,
            sickness_id=sickness_id,
            patient_id=patient_id,
            examination_date=datetime.datetime.now()
        )
        db.session.add(medical_bill)
        db.session.commit()
        return medical_bill

    @classmethod
    def update(cls, data):
        try:
            medical_bill_data = {}
            for key in data:
                if hasattr(cls, key):
                    medical_bill_data[key] = data[key]
            if 'id' not in medical_bill_data:
                medical_bill = Medical_bill.query.filter_by(patient_id=medical_bill_data.get('patient_id'))
                medical_bill.update(medical_bill_data)
            else:
                medical_bill = Medical_bill.query.filter_by(id=medical_bill_data.get('id'))
                medical_bill.update(medical_bill_data)
            db.session.commit()
            return Medical_bill.query.get(medical_bill_data['id']).as_dict()
        except:
            return None


class Medical_details(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "medical_details"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bill_id = db.Column(db.Integer, nullable=False)
    drug_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    usage = db.Column(db.String(120))

    def __repr__(self):
        return "<medical_details '{}'>".format(self.id)

    def as_dict(self):
        return {
            'id': self.id,
            'bill_id': self.bill_id,
            'drug_id': self.drug_id,
            'quantity': self.quantity,
            'usage': self.usage,
        }

    @classmethod
    def create(cls, bill_id, drug_id=None, quantity=0, usage=None):
        medical_details = Medical_details(
            bill_id=bill_id,
            drug_id=drug_id,
            quantity=quantity,
            usage=usage
        )
        db.session.add(medical_details)
        db.session.commit()
        return medical_details

    @classmethod
    def update(cls, data):
        try:
            medical_details_data = {}
            for key in data:
                if hasattr(cls, key):
                    medical_details_data[key] = data[key]
            if 'id' not in medical_details_data:
                return None
            else:
                medical_details = Medical_details.query.filter_by(id=medical_details_data.get('id'))
                medical_details.update(medical_details_data)
            db.session.commit()
            return Medical_details.query.get(medical_details_data['id']).as_dict()
        except:
            return None


class Usage(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "usage"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usage = db.Column(db.String(125), nullable=False)

    def __repr__(self):
        return "<usage '{}'>".format(self.usage)

    def as_dict(self):
        return {
            'id': self.id,
            'usage': self.usage,
        }

    @classmethod
    def create(cls, usage):
        usage = Usage(
            usage=usage,
        )
        db.session.add(usage)
        db.session.commit()
        return usage

    @classmethod
    def update(cls, data):
        try:
            usage_data = {}
            for key in data:
                if hasattr(cls, key):
                    usage_data[key] = data[key]
            if 'id' not in usage_data:
                usage = Usage.query.filter_by(usage=usage_data.get('usage'))
                usage.update(usage_data)
            else:
                usage = Usage.query.filter_by(id=usage_data.get('id'))
                usage.update(usage_data)
            db.session.commit()
            return Usage.query.get(usage_data['id']).as_dict()
        except:
            return None

class Receipt(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "receipt"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    medical_bill_id = db.Column(db.Integer, nullable=False)
    fee = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<receipt '{}'>".format(self.id)

    def as_dict(self):
        return {
            'id': self.id,
            'medical_bill_id': self.medical_bill_id,
            'fee':self.fee
        }

    @classmethod
    def create(cls, medical_bill_id, fee = 50000):
        receipt = Receipt(
            medical_bill_id = medical_bill_id,
            fee = fee
        )
        db.session.add(receipt)
        db.session.commit()
        return receipt

    @classmethod
    def update(cls, data):
        try:
            receipt_data = {}
            for key in data:
                if hasattr(cls, key):
                    receipt_data[key] = data[key]
            if 'id' not in receipt_data:
                receipt = Receipt.query.filter_by(receipt=receipt_data.get('medical_bill_id'))
                receipt.update(receipt_data)
            else:
                receipt = Receipt.query.filter_by(id=receipt_data.get('id'))
                receipt.update(receipt_data)
            db.session.commit()
            return Receipt.query.get(receipt_data['id']).as_dict()
        except:
            return None


class Statistic(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "statistic"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime)
    drug_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    profit = db.Column(db.Float)

    def __repr__(self):
        return "<statistic '{}'>".format(self.id)

    def as_dict(self):
        return {
            'id': self.id,
            'drug_id': self.drug_id,
            'quantity': self.quantity,
            'profit': self.profit,
            'date': self.date
        }

    @classmethod
    def create(cls, drug_id, qty):
        drug = Drug.query.get(drug_id).as_dict()
        statistic = Statistic(
            drug_id=drug_id,
            quantity=qty,
            profit=(float(drug['price_out']) - float(drug['price_in'])) * int(qty),
            date=datetime.datetime.now()
        )
        db.session.add(statistic)
        db.session.commit()
        return statistic

    @classmethod
    def update(cls, data):
        try:
            statistic_data = {}
            for key in data:
                if hasattr(cls, key):
                    statistic_data[key] = data[key]
            if 'id' not in statistic_data:
                return None
            else:
                statistic = Statistic.query.filter_by(id=statistic_data.get('id'))
                statistic.update(statistic_data)
            db.session.commit()
            return Statistic.query.get(statistic_data['id']).as_dict()
        except:
            return None


from route.symptom_route import symptom_route
from route.sickness_route import sickness_route
from route.user_route import user_route
from route.function_route import function_route
from route.admin_route import admin_route
from route.drug_route import drug_route
from route.usage_route import usage_route
from route.medical_bill_route import medical_bill_route
from route.patient_route import patient_route

app.register_blueprint(user_route)
app.register_blueprint(symptom_route)
app.register_blueprint(sickness_route)
app.register_blueprint(function_route)
app.register_blueprint(admin_route)
app.register_blueprint(drug_route)
app.register_blueprint(usage_route)
app.register_blueprint(medical_bill_route)
app.register_blueprint(patient_route)

db.create_all()
if __name__ == '__main__':
    app.run(debug=True)
