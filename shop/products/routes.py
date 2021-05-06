from flask import redirect, render_template, url_for, flash, request
from shop import db, app, photos
from .models import Brand, Category
from .forms import Addproducts
import secrets





'''
@app.route('/addbrand', methods=['GET','POST'])
def addbrand():
    if request.method=="POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The brand {getbrand} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', brands='brands')
'''

@app.route('/addcat', methods=['GET','POST'])
def addcat():
    if request.method=="POST":
        getbrand = request.form.get('category')
        cat = Category(name=getbrand)
        db.session.add(cat)
        flash(f'The Category {getbrand} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html')


@app.route('/addproduct', methods=['POST', 'GET'])
def addproduct():
    #brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)
    if request.method == "POST":
        photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        #photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        #photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
    return render_template('products/addproduct.html', title="Add Product page", form=form, categories=categories)
