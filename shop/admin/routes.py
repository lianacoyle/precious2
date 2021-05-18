from flask import render_template, session, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from shop import app, db, bcrypt, photos, search
from .forms import RegistrationForm, LoginForm, UploadForm
from .models import User, Users, Category, Item, Cart, CartDetails
import os
from shop.products.forms import Addproducts

UPLOAD_FOLDER = 'shop/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

#root/home page
@app.route("/")
@app.route("/precious")
def precious():
    items = Item.query.all()
    return render_template('adm/home.html', items=items)


@app.route('/result')
def result():
    searchword = request.args.get('q')
    items = Item.query.msearch(searchword, fields=['item_name', 'item_desc'], limit=3)
    return render_template('products/result.html', items=items)


@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    items = Item.query.all()
    return render_template('adm/index.html', title='Admin Page', items=items)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, username=form.username.data,
                    email=form.email.data, password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.first_name.data}! Thank you for registering.','success')
        return redirect(url_for('login'))
    return render_template('adm/register.html', form=form, title="Registration page")


# Go to this endpoint to see what is in the User table
@app.route("/viewUsers")
def viewUsers():
    return render_template('adm/viewUsers.html', values=User.query.all())


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method =="POST" and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            session['name'] = user.first_name
            flash(f'Welcome {form.email.data} You are logged in now', 'success')
            return redirect(request.args.get('next') or url_for('precious'))
        else:
            flash('Wrong Password please try again', 'danger')
    return render_template('adm/login.html', form=form, title="Login Page")

@app.route('/DevPage')
def DevPage():
    return render_template('adm/Dev_Page.html')

@app.route('/profile')
def profile():
    return "future profile page"


@app.route("/contact")
def contact():
    return render_template('adm/Contactus.html')

@app.route('/shopping')
def shopping():
    return render_template('products/shopping.html', items=Item.query.all())

# This method routes to a page view of the item
# *** 'itemPage.html' is very basic and needs to be worked on ***
@app.route('/shopping/<itemid>')
def showItem(itemid):
    item = Item.query.filter_by(itemid=itemid).first()
    return render_template('products/itemPage.html', item=item)

@app.route('/cart/<cartid>')
def showCart(cartid):
    return render_template('cart/cart.html')


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        if not request.form['fname'] or not request.form['lname'] or not request.form['uname'] \
                or not request.form['email'] or not request.form['pword']:
            flash('Please enter all the fields', 'error')
        else:
            first_name = request.form["fname"]
            last_name = request.form["lname"]
            username = request.form["uname"]
            email = request.form["email"]
            password = request.form["pword"]
            password_check = request.form["cpword"]
            print('form entries')
            '''
            found_user = Users.query.filter_by(email=email).first()
            if found_user:
                flash("Account for that email already exists!")
                return redirect(url_for("login"))

            else:
            '''
            usr = Users(first_name, last_name, email, username, password)
            print('object instantiated')
            db.session.add(usr)
            db.session.commit()
            print('user object committed')
            print(usr)
            flash("Account successfully created!")
            return redirect(url_for("viewUsers"))

    return render_template('adm/createAccount.html')


@app.route("/logout")
def logout():
    session.pop('email', default=None)
    session.pop('name', default=None)
    session.pop('ShoppingCart', default=None)
    return redirect(request.referrer)
    #return "You have completed a successful logout!"


# user upload page

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/uua")
@app.route('/userUpload')
def upload_form():
    form = UploadForm(request.form)
    return render_template('adm/userUpload.html', form=form)

@app.route('/uploader', methods=['GET', 'POST'])
def upload():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))

    # lookup user id for logged in user
    email = session['email']
    user = User.query.filter_by(email=email).first()
    user_id = user.id

    form = UploadForm(request.form)
    categories = Category.query.all()
    if request.method == 'POST':
        photos.save(request.files.get('item_file'))
        filename = secure_filename(request.files.get('item_file').filename)
        item_name = request.form.get('item_name')
        item_desc = request.form.get('item_desc')
        item_price = request.form.get('item_price')
        category_id = request.form.get('category')
        print(f"category: {category_id}")
        print(f"User ID: {user_id}")

        item = Item(item_name, filename, item_desc, item_price, category_id, user_id)
        db.session.add(item)
        db.session.commit()
        flash(f'The listing {item_name} has been added to your database', "success")
        return redirect(url_for("shopping"))

    return render_template('adm/userUpload.html', form=form, categories=categories)


@app.route('/updateitem/<int:id>', methods=['GET','POST'])
def updateitem(id):
    categories = Category.query.all()
    item = Item.query.get_or_404(id)
    category = request.form.get('category')
    form = UploadForm(request.form)
    if request.method == "POST":
        item.item_name = form.item_name.data
        item.item_desc = form.item_desc.data
        item.price = form.item_price.data
        item.category_id = category
        db.session.commit()
        flash(f'Your listing has been updated','success')
        return redirect('admin')



    form.item_name.data = item.item_name
    form.item_desc.data = item.item_desc
    form.item_price.data = item.price

    return render_template('products/updateitem.html', form=form, categories=categories,
                           item=item)

@app.route("/viewItems")
def viewItems():
    return render_template('products/viewItems.html', values=Item.query.all())

@app.route('/addcat', methods=['GET','POST'])
def addcat():
    if request.method == "POST":
        getcategory = request.form.get('category')
        cat = Category(name=getcategory)
        db.session.add(cat)
        flash(f'The Category {getcategory} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html')

@app.route("/viewCats")
def viewCategories():
    return render_template('products/viewCategories.html', values=Category.query.all())

# shopping cart page
@app.route("/scn")
@app.route('/shoppingCart')
def upload_cart():
    form = UploadForm(request.form)
    return render_template('cart/shoppingCart.html', form=form)

