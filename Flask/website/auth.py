from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User
from . import db

from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():

    if  request.method == 'POST':

        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username = username).first()

        if not user:
            user = User.query.filter_by(email = username).first()
           
        if user:

            if  check_password_hash(user.password, password):

                login_user(user, remember = True)
                return redirect(url_for('views.home'))
            else:
                print('Inccorect password')
                flash('Inccorect password')

        else:
            print('User not exist')
            flash('User not exist')


    return render_template("login.html")

@auth.route('/logout')
# @login_required
def logout():

    if current_user.is_authenticated:
        logout_user()
        return "Logout"
    else:
        return redirect(url_for('auth.login'))

    # logout_user()
    # return "Logout"

@auth.route('/register', methods = ['GET', 'POST'])
def register():

    if request.method == 'POST':

        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if User.query.filter_by(email = email).first():
            flash('Email in use')
        elif User.query.filter_by(username = username).first():
            flash('Username in use')
        elif password1 != password2:
            flash('Not same password')
        elif not email or not username or not password2:
            flash('Empty feild')
        else:
            addUser(User(email = email, username = username, password = generate_password_hash(password2, method = 'sha256')))
            return redirect(url_for('views.home'))

        print(email)
        print(username)
        print(password1)
        print(password2)

    return render_template("register.html")

def Brodcast(msg):
    print(msg)


def addUser(user):
    db.session.add(user)
    db.session.commit()

    login_user(user, remember = True)