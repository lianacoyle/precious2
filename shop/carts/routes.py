from flask import render_template, session, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from shop import app, db, bcrypt
from shop.admin.models import Item
#from .forms import RegistrationForm, LoginForm
#from .models import User, Users, Categories, Item, Cart, CartDetails
import os

def MergeDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False


@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        item_id = request.form.get('item_id')
        quantity = int(request.form.get('quantity'))
        item = Item.query.filter_by(itemid=item_id).first()
        if item_id and quantity and request.method == "POST":
            DictItems = {item_id: {'name': item.item_name, 'price': item.price, 'quantity': quantity,
                                   'image': item.filename}}
            if 'ShoppingCart' in session:
                print(session['ShoppingCart'])
                if item_id in session['ShoppingCart']:
                    print("This product is already in your cart, increasing quantity")
                    quantity = int(item_id['quantity'])
                    item_id.update({'quantity': quantity + 1})
                else:
                    session['ShoppingCart'] = MergeDicts(session['ShoppingCart'], DictItems)
                    return redirect(request.referrer)

            else:
                session['ShoppingCart'] = DictItems
                return redirect(request.referrer)


    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@app.route('/carts')
def getCart():
    if 'ShoppingCart' not in session:
        return redirect(request.referrer)
    total = 0
    for key, item in session['ShoppingCart'].items():
        total += int(item['price']) * int(item['quantity'])



    return render_template('cart/carts.html', total= total)

