from flask import Flask, render_template, request, redirect, url_for
from database import Product, User, Order, OrderItem, engine, session

app = Flask(__name__)

@app.route('/')
def home():
    products = session.query(Product).all()
    return render_template('home.html', products=products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = session.query(Product).get(product_id)
    order_item = OrderItem(product=product, quantity=1)
    session.add(order_item)
    session.commit()
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    order_items = session.query(OrderItem).all()
    return render_template('cart.html', order_items=order_items)

@app.route('/checkout', methods=['POST'])
def checkout():
    user = User(username='testuser', password='testpassword')
    session.add(user)
    session.commit()
    order = Order(user=user, total_price=100)
    session.add(order)
    session.commit()
    for order_item in session.query(OrderItem).all():
        order_item.order = order
        session.commit()
    return redirect(url_for('thank_you'))

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)
