from shop import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), unique=False, nullable=False)
    last_name = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)
    profile = db.Column(db.String(180), unique=False, nullable=False, default='profile.jpg')

    def __repr__(self):
        return '<User %r>' % self.username


class Users(db.Model):
    userid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    #vendor_flag = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    items = db.relationship('Item', backref='users', lazy=True)
    carts = db.relationship('Cart', backref='users', lazy=True)

    def __init__(self, first_name, last_name, email, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = password

    def __repr__(self):
        return f"User('{self.userid}','{self.first_name}','{self.last_name}')"


class Categories(db.Model):
    categoryid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(100), nullable=False)
    category_desc = db.Column(db.String(255), nullable=False)

    def __init__(self, category_name, category_desc):
        self.category_name = category_name
        self.category_desc = category_desc

    def __repr__(self):
        return f"Category: '{self.category_name}' /n", \
               f"Description: '{self.category_desc}' /n"


class Item(db.Model):
    itemid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    item_desc = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    # create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    userid = db.Column(db.Integer, db.ForeignKey('users.userid'), nullable=False)

    # categoryid = db.Column(db.Integer, db.ForeignKey('category.categoryid'), nullable=False)

    # cartdetails = db.relationship('CartDetails', backref='item', lazy=True)

    # Note: defaults to '1' for category id and user id
    def __init__(self, item_name, filename, item_desc, price, userid=1, categoryid=1):
        self.item_name = item_name
        self.filename = filename
        self.item_desc = item_desc
        self.price = price
        self.userid = userid
        self.categoryid = categoryid

    def __repr__(self):
        return f"Item('{self.itemid}','{self.item_name}','{self.filename}','{self.price}')"


class Cart(db.Model):
    cartid = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # update_time = db.Column(db.DateTime, nullable=True)
    userid = db.Column(db.DateTime, db.ForeignKey('users.userid'), nullable=True)

    def __init__(self, userid=0):
        self.userid = userid

    def __repr__(self):
        return f"Cart ID: {self.cartid}/n", \
               f"Create Time: {self.create_time}/n"


class CartDetails(db.Model):
    cartdetailsid = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    cartid = db.Column(db.Integer, db.ForeignKey('cart.cartid'), nullable=False)
    itemid = db.Column(db.Integer, db.ForeignKey('item.itemid'), nullable=False)

    def __init__(self, itemid, quantity, cartid):
        # checking to see if Cart by cartid already exists
        cart = Cart.query.filter_by(cartid=cartid).first()

        # if not instantiate new Cart object
        if cart is None:
            cart = Cart()
            cartid = cart.cartid
        else:
            cartid = cart.cartid

        self.itemid = itemid
        self.quantity = quantity
        self.cartid = cartid

    def __repr__(self):
        return f"Item ID: '{self.itemid}'/n", \
               f"Quantity: '{self.quantity}'/n", \
               f"Cart ID: '{self.cartid}'/n"



db.create_all()