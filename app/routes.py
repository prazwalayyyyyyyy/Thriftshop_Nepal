from crypt import methods
from fileinput import filename
# from turtle import pos
from flask import jsonify, render_template, flash, redirect, send_file, url_for
from importlib_metadata import method_cache
from app import app
from app.forms import EditUserForm, GoodsForm, LoginForm
from flask_login import current_user, login_required, login_user
from app.models import Goods, User
from flask_login import logout_user
from flask import request #for next page after login
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse #next page after login
from app import db
from app.forms import RegistrationForm

@app.route('/')
@app.route('/index')
@login_required #doesnt allow users not logged in to view contents and add next redirection to ntercept user's request and reach there after they logged in 
def index():
    posts = [
        {
            'author': {'username': 'Aliz'},
            'body': 'Handsome guy indeed'
        },
        {
            'author': {'username': 'faf'},
            'body': 'OHOO curls'
        }   
    ]
    goods=Goods.query.all()
    # import pdb; pdb.set_trace()
    return render_template('index.html', title='Home', posts=posts, goods=goods)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)




@app.route('/goods/create', methods=['POST', 'GET'])
@login_required
def create_goods():
    # breakpoint
    # import pdb;pdb.set_trace()
    form=GoodsForm()
    if request.method == 'POST' and form.validate_on_submit() and current_user.user_type in ['seller', 'admin']:
        filename = secure_filename(form.photo.data.filename)
        form.photo.data.save('uploads/'+filename)
        gds = Goods(photo=filename, name=form.name.data, descripton=form.descripton.data, price=form.price.data, creater=current_user)
        db.session.add(gds)
        db.session.commit()    
        return redirect(url_for('index'))    
    return render_template('creategoods.html', form=form)

@app.route('/images/<filename>')
def get_file(filename):
    filename=f'../uploads/{filename}'
    return send_file(filename, mimetype='image/gif')

@app.route('/goods/edit/<id>', methods=['GET','POST'])
def edit_goods(id):
    good = Goods.query.filter_by(id=id).first()
            # user = User.query.filter_by(username=form.username.data).first()  
    if good.creater.username != current_user.username and  current_user.user_type !='admin':
        flash('You are not Authorized to perform edit operation')
        return redirect(url_for('index'))
    form=GoodsForm(obj=good)
    if request.method == 'POST':
        post_data={**form.data}
        del post_data['submit']
        del post_data['csrf_token']
        # import pdb; pdb.set_trace()
        gds = Goods.query.filter_by(id=id).update(post_data)
        db.session.commit() 
        flash('Successfully edited')
        return redirect(url_for('index'))
    # form.populate_obj(good)
    return render_template('editgoods.html', form=form)

@app.route('/goods/delete/<id>')
def delete_goods(id):
    good = Goods.query.filter_by(id=id).delete()
            # user = User.query.filter_by(username=form.username.data).first()
    # if good.creater.username != current_user.username and  current_user.user_type !='admin':
    #     flash('You are not Authorized to perform edit operation')
    #     return redirect(url_for('index'))
    # form=GoodsForm(obj=good)
    # if request.method == 'POST':
    #     post_data={**form.data}
    #     # del post_data['submit']
    #     # del post_data['csrf_token']
    #     # import pdb; pdb.set_trace()
    #     gds = Goods.query.filter_by(id=id).delete(post_data)
    db.session.commit() 
    #     flash('Successfully edited')
    #     return redirect(url_for('index'))
    # # form.populate_obj(good)
    return redirect(url_for('index'))

@app.route('/users/edit/<id>')
def edit_users(id):
    user = User.query.filter_by(id=id).first()
            # user = User.query.filter_by(username=form.username.data).first()
    if current_user.user_type != 'admin':
        flash('You are not Authorized to perform edit operation')
        return redirect(url_for('index'))
    form=EditUserForm(obj=user)
    # form.populate_obj(good)
    return render_template('editusers.html', form=form)

@app.route('/users')
def get_users():
    user = User.query.all()
    return render_template('users.html', users=user)
