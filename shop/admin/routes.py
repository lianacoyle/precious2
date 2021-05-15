from flask import render_template, session, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from shop import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
from .models import User, Users, Categories, Item, Cart, CartDetails
import os
from shop.products.forms import Addproducts

UPLOAD_FOLDER = 'shop/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

#root/home page
@app.route("/")
@app.route("/precious")
def precious():
    return render_template('adm/home.html')

@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    #products = Addproducts.query.all()
    return render_template('adm/index.html', title='Admin Page')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, username=form.username.data,
                    email=form.email.data, password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.first_name.data} Thank you for registering','success')
        return redirect(url_for('admin'))
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
            flash ('Wrong Password please try again', 'danger')
    return render_template('adm/login.html', form=form, title="Login Page")

@app.route('/DevPage')
def DevPage():
    return render_template('adm/Dev_Page.html')

@app.route('/profile')
def profile():
    return "future profile page"

@app.route("/phot")
def phot():
    return "Photography"

@app.route("/contact")
def contact():
    return render_template('adm/Contactus.html')

@app.route("/me")
def me():
    return "PM"

@app.route("/des")
def designs():
    return "Des"

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


@app.route("/loginA", methods=["POST", "GET"])
def loginA():
    if request.method == "POST":
        session.permanent = True
        # Retrieve input values from web form
        email = request.form['email']
        password = request.form['password']
        # Look for email from login form in User table
        found_email = Users.query.filter_by(email=email).first()
        # If there is a record for that table in the email
        if found_email:
            # Get the password associated with that email
            found_password = found_email.password
            print('lookup password: {}'.format(found_password))
            print('form password: {}'.format(password))
            # If the passwords match
            if found_password.strip() == password.strip():
                # Create user session for that email
                print('the passwords matched!')
                session['email'] = email
                flash('Login Successful!', 'success')
                return redirect(url_for('precious'))

            # If the passwords don't match
            else:
                flash('Password does not match')
                print('passwords did not match')
                return redirect(url_for('create'))

        # If the emails don't match
        else:
            print("reached 'email doesn't match' else statement")
            flash('No account associated with that email')
            return redirect(url_for('create'))

    return render_template('adm/loginA.html')


@app.route("/logout")
def logout():
    session.pop('email', default=None)
    session.pop('name', default=None)
    session.pop('ShoppingCart', default=None)
    return redirect(request.referrer)
    #return "You have completed a successful logout!"

# user checkout page
@app.route("/ucos")
@app.route("/userCheckout")
def uco():
    return render_template('adm/userCheckout.html')

# user upload page

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/uua")
@app.route('/userUpload')
def upload_form():
    return render_template('adm/userUpload.html')

@app.route('/uploader', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            #flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #basedir = os.path.abspath(os.path.dirname(__file__))
            #UPLOAD_FOLDER = os.path.join(basedir, 'static\images')
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            item_name = request.form["title"]
            item_fname = file.filename
            item_desc = request.form["description"]
            item_price = float(request.form["price"])

            item = Item(item_name, item_fname, item_desc, item_price)
            db.session.add(item)
            db.session.commit()
            print('item object committed')
            flash("Item successfully created!")
            return redirect(url_for("viewItems"))

            #return redirect(url_for('upload_form',filename=filename))
    return "Congratulations Upload Complete"

@app.route("/viewItems")
def viewItems():
    return render_template('products/viewItems.html', values=Item.query.all())

# shopping cart page
@app.route("/scn")
@app.route('/shoppingCart')
def upload_cart():
    return render_template('cart/shoppingCart.html')

