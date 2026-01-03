from flask import Blueprint, render_template, request, redirect, flash, url_for
from .models import UserInfo
from flask_login import login_required,login_user,current_user,logout_user
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
import re
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        uid = request.form.get('login_id')
        password = request.form.get('password')

        if not uid or not password:
            flash('Enter username/email and password', 'error')
            return redirect(url_for('auth.login'))

        user = UserInfo.query.filter(
            (UserInfo.user_name == uid) |
            (UserInfo.email == uid)
        ).first()

        if not user:
            flash('Please sign up first', 'error')
            return redirect(url_for('auth.signup'))

        if not check_password_hash(user.password, password):
            flash('Incorrect password', 'error')
            return redirect(url_for('auth.login'))

        login_user(user, remember=True)
        flash('Login successful', category='success')
        return redirect(url_for('views.home'))

    return render_template('login.html', user=current_user)

@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        password_confirm = request.form.get('passwordConfirm')
        contact= request.form.get('contact')
        bio = request.form.get('bio')
        user_name = request.form.get('user_name')

        user=UserInfo.query.filter_by(email=email).first()
        if user:
            flash('Email alreday exist , please log in',category='error')
            return redirect(url_for('auth.login'))

            
        if password != password_confirm:
            flash('Confim password are not same',category='error')
        elif first_name == None:
            flash('Provide first name',category='error')
        elif last_name == None:
            flash('Provide the last name',category='error')
        elif len(password)<4:
            flash('Password must be greater than 4 character',category='error')
        else:
            flash('account created successfully',category='success')
            hash_pass= generate_password_hash(password,method='pbkdf2:sha256')

            new_user = UserInfo(user_name=user_name,first_name=first_name,last_name=last_name,email=email,password=hash_pass,bio = bio,contact = contact)
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember= True)
            return redirect(url_for('views.home',user=current_user))
        
        if not is_valid_username(user_name):
            flash('Special character are not allowed',category='error')
            


       
        print(email, first_name, last_name, password)
        
    return render_template('signup.html',user=current_user)


def is_valid_username(username):
    pattern = r'^[a-zA-Z0-9_]+$'
    return re.match(pattern, username)

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.welcome'))