#!/usr/bin/python3
"""Start web application with two routings
"""

from models import storage
from models.category import Category
from models.color import Color
from decimal import Decimal
from models.order import Order
from models.orderItem import OrderItem
from models.product import Product
from models.size import Size
from models.user import User
from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)

app.secret_key = "NGSRyqDd5CAysMuGmrSqWfoldit1W0Tvd2SlubsTFJA"

@app.route('/', methods=['GET'])
def products_list():
    """Render template with products
    """
    user_ip = request.remote_addr
    path = 'test.html'
    products = storage.all(Product)
    # sort Product object alphabetically by name
    sorted_products = sorted(products.values(), key=lambda product: product.product_name)
    return render_template(path, sorted_products=sorted_products, user_ip=user_ip)

@app.route('/cat', strict_slashes=False)
def product_category():
    print(session.keys()) # Debug: Print all keys in the session
    print(session.get('order')) # Debug: Print the 'order' key in the session
    """ displays a HTML page with a list of products by categories """
    categories = storage.all(Category).values()
    categories = sorted(categories, key=lambda k: k.name)
    st_ct = []
    for category in categories:
        st_ct.append([category, sorted(category.products, key=lambda k: k.product_name)])
    return render_template('test2.html',
                           categories=st_ct,
                           h_1="Categories")



@app.route('/add_order_item', methods=['GET', 'POST'])
def add_order_item():
    if request.method == 'POST':
        # Extract product ID and quantity from the form
        order_id = int(request.form.get('order_id'))
        product_id = int(request.form.get('product_id'))
        quantity = int(request.form.get('quantity'))

        # Retrieve the product from the database
        product = storage.get(Product, product_id)

        if product:
            # Calculate the price based on the product's price and quantity
            price = product.price * quantity

            # Create a new OrderItem object with the provided information
            new_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=quantity, price=price)

            # Add the new order item to the database session
            storage.new(new_order_item)

            # Commit the changes to the database
            storage.save()

            return redirect(url_for('success_page'))
        else:
            return 'Product not found'
    else:
        # Render the HTML form for adding an order item
        return render_template('add_order_item.html')

'''@app.route('/add_order_item', methods=['GET', 'POST'])
def add_order_item():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        product = storage.get(Product, product_id)

        if product:
            price = product.price * quantity
            order_item = {'product_id': product_id, 'quantity': quantity, 'price': price}

            # Check if there's an existing order in the session
            if 'order' not in session:
                session['order'] = []

            # Add the new order item to the session
            session['order'].append(order_item)

            return redirect(url_for('all_order_items'))
        else:
            return 'Product not found'
    else:
        return render_template('add_order_item.html')'''



@app.route('/order_item', methods=['GET', 'POST'])
def order_item():
    if request.method == 'POST':
        # Extract user ID, order ID, product ID, and quantity from the form
        user_id = int(request.form.get('user_id'))
        order_id = int(request.form.get('order_id'))
        product_id = int(request.form.get('product_id'))
        quantity = int(request.form.get('quantity'))

        # Retrieve the product from the database
        product = storage.get(Product, product_id)

        if product:
            # Calculate the price based on the product's price and quantity
            price = product.price * quantity

            # Check if an order already exists for the given user_id
            existing_order = storage.query(Order).filter_by(user_id=user_id).first()

            if existing_order:
                # If an order exists, add the new item's price to the existing order's total price
                existing_order.total_price = existing_order.total_price + Decimal(price)
                order = existing_order
            else:
                # If no order exists, create a new one
                order = Order(user_id=user_id, total_price=Decimal(price))
                storage.new(order)
                storage.save()

            # Create a new OrderItem object with the provided information
            new_order_item = OrderItem(order_id=order.id, product_id=product_id, quantity=quantity, price=price)

            # Add the new order item to the database session
            storage.new(new_order_item)

            # Commit the changes to the database
            storage.save()

            return redirect(url_for('success_page'))
        else:
            return 'Product not found'
    else:
        # Render the HTML form for adding an order item
        return render_template('order_item.html')


'''@app.route('/order_item', methods=['GET', 'POST'])
def order_item():
    if request.method == 'POST':
        # Extract order ID, product ID, and quantity from the form
        user_id = int(request.form.get('user_id'))
        order_id = int(request.form.get('order_id'))
        product_id = int(request.form.get('product_id'))
        quantity = int(request.form.get('quantity'))

        # Retrieve the product from the database
        product = storage.get(Product, product_id)

        if product:
            # Calculate the price based on the product's price and quantity
            price = product.price * quantity

            # Retrieve or create the Order object
            order = storage.get(Order, order_id)
            if not order:
                # If the order does not exist, create a new one
                # Assuming you have a user_id or other necessary information
                order = Order(user_id=user_id, total_price=0)
                storage.new(order)
                storage.save()

            # Create a new OrderItem object with the provided information
            new_order_item = OrderItem(order_id=order.id, product_id=product_id, quantity=quantity, price=price)

            # Add the new order item to the database session
            storage.new(new_order_item)

            # Update the total price of the order
            order.total_price = order.total_price + Decimal(price)

            # Commit the changes to the database
            storage.save()

            return redirect(url_for('success_page'))
        else:
            return 'Product not found'
    else:
        # Render the HTML form for adding an order item
        return render_template('order_item.html')'''


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        # Process the form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        contact_number = request.form.get('contact_number')
        email = request.form.get('email')
        password = request.form.get('password')
        country = request.form.get('country')
        company_name = request.form.get('company_name')
        address = request.form.get('address')
        state_or_country = request.form.get('state_or_country')
        postal_or_zip = request.form.get('postal_or_zip')
        order_notes = request.form.get('order_notes')
        
        # Create a new User instance
        new_user = User(first_name=first_name, last_name=last_name, contact_number=contact_number,
                        email=email, password=password, country=country, company_name=company_name,
                        address=address, state_or_country=state_or_country, postal_or_zip=postal_or_zip,
                        order_notes=order_notes)
        
        # Add the new user to the database
        storage.new(new_user)
        storage.save()
        
        # Redirect to a success page or back to the form
        return redirect(url_for('success_page'))
    
    # Render the registration form
    return render_template('register.html')

@app.route('/success')
def success_page():
    return render_template('success.html')



''''@app.route('/')
def products_list():
    """Render template with products
    """
    path = 'test.html'
    products = storage.all(Product)
    # sort Product object alphabetically by name
    sorted_products = sorted(products.values(), key=lambda product: product.product_name)
    return render_template(path, sorted_products=sorted_products)'''


@app.teardown_appcontext
def app_teardown(arg=None):
    """Clean-up session
    """
    storage.close()


if __name__ == '__main__':
    app.url_map.strict_slashes = False
    app.run(host='0.0.0.0', port=5000, debug=True)
