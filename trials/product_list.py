#!/usr/bin/python3
"""Start web application with two routings
"""

from models import storage
from models.category import Category
from models.product import Product
from models.user import User
from models.orderItem import OrderItem
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

@app.route('/', methods=['GET'])
def products_list():
    """Render template with products
    """
    path = 'test.html'
    products = storage.all(Product)
    # sort Product object alphabetically by name
    sorted_products = sorted(products.values(), key=lambda product: product.product_name)
    return render_template(path, sorted_products=sorted_products)

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



@app.route('/add_order_item', methods=['GET', 'POST'])
def add_order_item():
    if request.method == 'POST':
        # Extract product ID and quantity from the form
        product_id = int(request.form.get('product_id'))
        quantity = int(request.form.get('quantity'))

        # Retrieve the product from the database
        product = storage.get(Product, product_id)

        if product:
            # Calculate the price based on the product's price and quantity
            price = product.price * quantity

            # Create a new OrderItem object with the provided information
            new_order_item = OrderItem(product_id=product_id, quantity=quantity, price=price)

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
