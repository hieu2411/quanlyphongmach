from flask import Flask, request
from flask.templating import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phongmach.db'
db = SQLAlchemy(app)


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True)
    fullname = db.Column(db.String(125), nullable=False)
    password = db.Column(db.String(125), nullable=False)
    mobile = db.Column(db.String(32))
    is_active = db.Column(db.Boolean, index=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)

    def __repr__(self):
        return "<User '{}'>".format(self.username)

    def as_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'fullname': self.fullname,
            'mobile': self.mobile,
            """'sso_user_id': self.sso_user_id,"""
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'last_login': self.last_login.strftime('%Y-%m-%d %H:%M:%S'),
        }


@app.route('/')
@app.route('/homepage')
def homepage():
    return render_template('Homepage.html')


@app.route('/login')
def login():
    print()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        return homepage()
    return render_template('Home/register.html', title='Login')


@app.route('/index')
def index():
    return render_template('Home/index.html')


@app.route('/edit')
def edit():
    return render_template('Home/edit.html')


@app.route('/delete')
def delete():
    return render_template('Home/delete.html')


@app.route('/details')
def details():
    return render_template('Home/details.html')


def take_apopointment():
    # if loged in ...

    # if not ...
    print()


db.create_all()
if __name__ == '__main__':
    app.run(debug=True)
