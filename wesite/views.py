from flask import Blueprint,render_template,request,redirect,url_for,flash
from flask_login import login_required,current_user
from .models import Blog,UserInfo,UserMixin
from . import db
views=Blueprint('views',__name__)

@views.route('/')
def welcome():
    return render_template('welcome.html',user=current_user)


@views.route('/home')
@login_required
def home():
    blog=Blog.query.filter_by(dlt=False).all()

    return render_template('home.html',user=current_user,blogs=blog)

@views.route('/profile')
@login_required
def profile():
    blogs= Blog.query.filter_by(created_by=current_user.id).all()
    return render_template('profile.html',user=current_user,blogs=blogs)

@views.route('/create',methods=['GET','POST'])
@login_required

def create():
    if request.method=='POST':
        title= request.form.get('title')
        blog= request.form.get('content')

        data=Blog(title=title,mini_blog=blog,created_by=current_user.id)

        db.session.add(data)
        db.session.commit()
        flash('Blog published',category='success')
        return redirect(url_for('views.home'))
    return render_template('create.html',user=current_user)

@views.route('home/blog/<int:id>',methods=['POST','GET'])
@login_required

def view_blog(id):
    blog = Blog.query.get_or_404(id)
    return render_template('view_blog.html',blog=blog,user=current_user)

@ views.route('/profile/edit>',methods=['POST','GET'])
@login_required

def edit_profile():
    if request.method=='POST':
        current_user.first_name=request.form.get('first_name')
        current_user.last_name=request.form.get('last_name')
        current_user.contact=request.form.get('contact')
        current_user.bio=request.form.get('bio')
        db.session.commit()

        flash('Profile edited successfully','success')
        return redirect(url_for('views.profile'))
    
    return render_template('edit_profile.html',user=current_user)