from crypt import methods
from fileinput import filename
from functools import reduce
# from msilib.schema import Condition
from unicodedata import category
# from turtle import pos
from flask import jsonify, render_template, flash, redirect, send_file, url_for, session
from importlib_metadata import method_cache
from app import app
from app.forms import EditUserForm, GoodsForm, LoginForm
from flask_login import current_user, login_required, login_user
from app.models import Cart, Goods, Orders, User
from flask_login import logout_user
from flask import request  # for next page after login
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse  # next page after login
from app import db
from app.forms import RegistrationForm


@app.route('/')
def frontpage():
    return render_template('index.html')


@app.route('/load')
def frontpage2():
    return render_template('create_goods')


@app.route('/load1')
def frontpage1():
    return render_template('create_goods')


@app.before_request
def calculate_cart():
    if current_user.is_authenticated:
        carts = Cart.query.filter_by(
            buyer_id=current_user.id, checkout_status=False)
        session['cart_count'] = len(carts.all())

@app.route('/index')
# @login_required #doesnt allow users not logged in to view contents and add next redirection to ntercept user's request and reach there after they logged in
def index():

    goods = Goods.query.all()

    male_goods = Goods.query.filter_by(category="Male", soldstatus=False)
    female_goods = Goods.query.filter_by(category="Female", soldstatus=False)
    cart_goods = db.session.query(Goods).join(Cart).filter(Goods.gid == Cart.good_id, Cart.checkout_status ==
                                                      False, Goods.soldstatus == False, Cart.buyer_id == current_user.id).all()
    cart_goods = [good.gid for good in cart_goods]
    return render_template('products.html', title='Home', male_goods=male_goods.all(), female_goods=female_goods.all(), cart_goods = cart_goods)


@app.route('/login', methods=['GET', 'POST'])
def login():
    #
    if current_user.is_authenticated:
        redirect_maps = {"seller": "create_goods",
                         "admin": "pending_items", "buyer": "index"}
        next_page = url_for(redirect_maps.get(current_user.user_type))
        return redirect(next_page)
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            redirect_maps = {"seller": "create_goods",
                             "admin": "pending_items", "buyer": "index"}
            next_page = url_for(redirect_maps.get(current_user.user_type))
        carts = Cart.query.filter_by(
            buyer_id=current_user.id, checkout_status=False)
        session['cart_count'] = len(carts.all())
        return redirect(next_page)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('frontpage'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, firstname=form.firstname.data,
                    lastname=form.lastname.data, user_type=form.user_type.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/additem', methods=['POST', 'GET'])
@login_required
def create_goods():
    # return ""
    form = GoodsForm()

    if request.method == 'POST' and form.validate_on_submit() and current_user.user_type in ['seller', 'admin']:
        filename = secure_filename(form.photo.data.filename)
        form.photo.data.save('uploads/'+filename)

        gds = Goods(photo=filename, name=form.name.data, seller=current_user.id,
                    buy_price=form.buy_price.data, condition=form.condition.data, category=form.category.data)
        db.session.add(gds)

        db.session.commit()
        return redirect(url_for('pending_items'))
    if current_user.user_type in ['buyer']:
        flash('You are not Authorized to perform this operation')
        return redirect(url_for('.index'))
    return render_template('additem.html', form=form)


@app.route('/images/<filename>')
def get_file(filename):
    filename = f'../uploads/{filename}'
    return send_file(filename, mimetype='image/gif')


@app.route('/pendingitem', methods=['POST', 'GET'])
@login_required
def pending_items():
    session['redirect_to'] = 'pending_items'
    goods = Goods.query.filter_by(seller=current_user.id, verifycheck=False)
    form = GoodsForm()

    return render_template('pendingitem.html', goods=goods.all(), form=form)


@app.route('/approveditem', methods=['POST', 'GET'])
@login_required
def approved_items():
    goods = Goods.query.filter_by(seller=current_user.id, verifycheck=True)
    return render_template('approveditem.html', goods=goods.all())  # form=form


@app.route('/paymentdetail', methods=['POST', 'GET'])
@login_required
def payment_details():
    return render_template('paymentdetail.html')  # form=form


@app.route('/goods/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_goods(id):
    good = Goods.query.filter_by(gid=id).first()
    # user = User.query.filter_by(username=form.username.data).first()
    if good.creater.username != current_user.username and current_user.user_type != 'admin':
        flash('You are not Authorized to perform edit operation')
        return redirect(url_for('index'))
    form = GoodsForm(obj=good)
    if request.method == 'POST':
        post_data = {**form.data}
        del post_data['submit']
        del post_data['csrf_token']
        if request.files and not isinstance(form.photo.data, str):
            filename = secure_filename(form.photo.data.filename)
            form.photo.data.save('uploads/'+filename)
            post_data.update(photo=filename)
        gds = Goods.query.filter_by(id=id).update(post_data)
        db.session.commit()
        flash('Successfully edited')
        return redirect(url_for(session.get('redirect_to', 'index')))
    # form.populate_obj(good)
    return render_template('editgoods.html', form=form)


@app.route("/cart/<action>/<good_id>", methods=["GET", "POST"])
@app.route("/cart/", methods=["GET", "POST"])
@app.route("/cart/<action>", methods=["GET", "POST"])
@login_required
def cart(action="s", good_id=0):
    if request.method == "POST":
        if action == "add":
            good_id = request.form.get("good_id")
            buyer_id = current_user.id
            if not Cart.query.filter_by(
            buyer_id=current_user.id,  good_id=good_id, checkout_status=False).first():
                cart_item = Cart(buyer_id=buyer_id, good_id=good_id)
                db.session.add(cart_item)
                db.session.commit()
            
    if action == "delete":
        Cart.query.filter_by(buyer_id=current_user.id,
                             good_id=good_id,checkout_status= False).delete()
        db.session.commit()
    
    goods = db.session.query(Goods).join(Cart).filter(
        Goods.gid == Cart.good_id, Goods.soldstatus == False, Cart.buyer_id == current_user.id, Cart.checkout_status== False)


    return render_template('cart.html', goods=goods)


@app.route('/goods/delete/<id>')
@login_required
def delete_goods(id):
    good = Goods.query.filter_by(gid=id).delete()

    db.session.commit()

    return redirect(url_for('index'))


@app.route('/checkout')
@login_required
def checkout():
    goods = db.session.query(Goods).join(Cart).filter(Goods.gid == Cart.good_id, Cart.checkout_status ==
                                                      False, Goods.soldstatus == False, Cart.buyer_id == current_user.id).all()
    sold_price = map(lambda good: good.sell_price, goods)
    buyprice = map(lambda good: good.buy_price, goods)
    checkedout_ids = [good.gid for good in goods]
    totalsellprice = sum(sold_price)
    totalbuyprice = sum(buyprice)
    order = Orders(buyer_id=current_user.id,
                   totalbuyprice=totalbuyprice, totalsellprice=totalsellprice)

    for gid in checkedout_ids:
        cart = Cart.query.filter_by(
            buyer_id=current_user.id, good_id=gid).first()
        cart.checkout_status = True
        db.session.add(cart)
    # cart = Cart.query.filter(Cart.buyer_id.in_(checkedout_ids)).update(checkout_status=True)
    db.session.add(order)

    db.session.commit()
    return render_template('#')


@app.route('/users/edit/<id>')
@login_required
def edit_users(id):
    user = User.query.filter_by(id=id).first()
    # user = User.query.filter_by(username=form.username.data).first()
    if current_user.user_type != 'admin':
        flash('You are not .Authorized to perform edit operation')
        return redirect(url_for('index'))
    form = EditUserForm(obj=user)
    # form.populate_obj(good)
    return render_template('editusers.html', form=form)


@app.route('/users/<username>')
def get_users(username):
    user = User.query.filter_by(username=username).first_or_404()
    good = [
        {'seller': user, 'body': 'Test good #1'},
        {'seller': user, 'body': 'Test good #2'}
    ]
    return render_template('user.html', users=user, goods=good)


@app.route('/admin/goodsverify', methods=['GET', 'POST'])
@login_required
def verify_goods():
    goods = Goods.query.all()
    return render_template('verify_goods.html', goods=goods)

#
