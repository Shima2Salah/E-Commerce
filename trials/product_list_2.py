#!/usr/bin/python3
"""Start web application with two routings
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
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
app.secret_key = "5NrvVndJur7iZLj0Kgg2A1T1h5XGKOv2LmWzX1B8Vxo"

@app.route('/', methods=['GET'])
def products_list():
    products = storage.all(Product)
    sorted_products = sorted(products.values(), key=lambda product: product.product_name)
    return render_template('test.html', sorted_products=sorted_products)

@app.route('/cat', strict_slashes=False)
def product_category():
    """ displays a HTML page with a list of products by categories """
    categories = storage.all(Category).values()
    categories = sorted(categories, key=lambda k: k.name)
    st_ct = []
    for category in categories:
        st_ct.append([category, sorted(category.products, key=lambda k: k.product_name)])
    return render_template('test2.html',
                           categories=st_ct,
                           h_1="Categories")

@app.route('/add_order_item/<int:product_id>', methods=['GET', 'POST'])
def add_order_item(product_id):
    print(product_id)
    if request.method == 'POST':
        # If the request method is POST, process the form submission
        product_id = int(request.form.get('product_id'))
        quantity = int(request.form.get('quantity'))
        print(product_id)
        # Retrieve the product from the database based on the product_id
        product = storage.get(Product, product_id)

        if product and int(quantity) > 0:
            # Calculate the price of the order item
            price = product.price * int(quantity)
            order_item = {'product_id': product_id, 'quantity': quantity, 'price': price}

            # Check if there's an existing order in the session
            if 'order' not in session:
                session['order'] = []

            # Add the new order item to the session
            session['order'].append(order_item)
            print(session.keys()) # Debug: Print all keys in the session
            print(session.get('order')) # Debug: Print the 'order' key in the session
            # Redirect to the page displaying all order items
            return redirect(url_for('all_order_items'))
        else:
            # If the product is not found, return an error message
            return 'Product not found'
    else:
        # If the request method is GET, render the form for adding order items
        return render_template('add_order_item.html', product_id=product_id)

@app.route('/all_order_items', methods=['GET', 'POST'])
def all_order_items():
    if request.method == 'POST':
        # Handle the POST request here
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')

        # Your logic to add the product to the order and calculate total price

        # Redirect to the GET request to display all order items
        return redirect(url_for('all_order_items'))
    else:
        # Handle the GET request here
        if 'order' in session: 
            order_items = session['order']
            total_price = sum(item['price'] for item in order_items)
            return render_template('all_order_items.html', order_items=order_items, total_price=total_price)
        else:
            return render_template('all_order_items.html', order_items=[], total_price=0)


@app.route('/order_more_items')
def order_more_items():
    return redirect(url_for('products_list'))

# Route for registering user

@app.route('/register_user')
def register():
    return redirect(url_for('register_user'))

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

'''@app.route('/all_order_items', methods=['GET'])
def all_order_items():
    # Check if there's an existing order in the session
    if 'order' in session: 
        order_items = session['order']
        total_price = sum(item['price'] for item in order_items)
        return render_template('all_order_items.html', order_items=order_items, total_price=total_price)
    else:
        return 'No order items found in the session'''
