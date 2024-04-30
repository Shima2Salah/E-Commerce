#!/usr/bin/python3
"""Start web application with two routings
"""

from flask import Flask, render_template, request, redirect, url_for, session
from models import storage
from models.category import Category
from models.color import Color
from models.order import Order
from models.orderItem import OrderItem
from models.product import Product
from models.size import Size
from models.user import User
from decimal import Decimal

app = Flask(__name__)
app.secret_key = "NGSRyqDd5CAysMuGmrSqWfoldit1W0Tvd2SlubsTFJA"

@app.route('/', methods=['GET'])
def products_list():
    products = storage.all(Product)
    sorted_products = sorted(products.values(), key=lambda product: product.product_name)
    return render_template('test.html', sorted_products=sorted_products)

@app.route('/add_order_item', methods=['GET', 'POST'])
def add_order_item():

    if request.method == 'POST':
        product_id = int(request.form.get('product_id'))
        quantity = int(request.form.get('quantity'))
        product = storage.get(Product, product_id)

        if product:
            price = product.price * quantity
            order_item = {'product_id': product_id, 'quantity': quantity, 'price': price}

            # Check if there's an existing order in the session
            if 'order' not in session:
                session['order'] = []

            # Add the new order item to the session
            session['order'].append(order_item)
            print(session.keys()) # Debug: Print all keys in the session
            print(session.get('order'))
            return redirect(url_for('register_user'))
        else:
            return 'Product not found'

    else:
        return render_template('add_order_item2.html')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        # Process the form data
        user_data = {
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name'),
            'contact_number': request.form.get('contact_number'),
            'email': request.form.get('email'),
            'password': request.form.get('password'),
            'country': request.form.get('country'),
            'company_name': request.form.get('company_name'),
            'address': request.form.get('address'),
            'state_or_country': request.form.get('state_or_country'),
            'postal_or_zip': request.form.get('postal_or_zip'),
            'order_notes': request.form.get('order_notes')
        }

        # Create a new User instance
        new_user = User(**user_data)
        storage.new(new_user)
        storage.save()

        # Process the order stored in the session
        if 'order' in session:
            total_price = sum(item['price'] for item in session['order'])
            new_order = Order(user_id=new_user.id, total_price=Decimal(total_price))
            storage.new(new_order)
            storage.save()

            for item in session['order']:
                new_order_item = OrderItem(order_id=new_order.id, product_id=item['product_id'], quantity=item['quantity'], price=item['price'])
                storage.new(new_order_item)
                storage.save()

            # Clear the order from the session
            session.pop('order', None)

        return redirect(url_for('success_page'))

    return render_template('register.html')

@app.route('/success')
def success_page():
    return render_template('success.html')

@app.teardown_appcontext
def app_teardown(arg=None):
    storage.close()

if __name__ == '__main__':
    app.url_map.strict_slashes = False
    app.run(host='0.0.0.0', port=5000, debug=True)
