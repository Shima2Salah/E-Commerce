#!/usr/bin/python3
""" Starts a Flash Web Application """
from flask import Flask, render_template
app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


@app.route('/home', strict_slashes=False)
@app.route('/', strict_slashes=False)
def hello_hbnb():
    """ Prints a Message when / is called """
    return render_template('index.html')


'''@app.route('/about', strict_slashes=False)
def hbnb():
    """ Prints a Message when /hbnb is called """
    return render_template('about.html')


@app.route('/cart', strict_slashes=False)
def c_is_fun():
    """ Prints a Message when /c is called """
    return render_template('cart.html')


@app.route('/products', strict_slashes=False)
def python_is_cool():
    """ Prints a Message when /python is called """
    return render_template('page3.html')


@app.route('/product_details', strict_slashes=False)
def number_templa():
    """ display a HTML page only if n is an integer """
    return render_template('single.html')


@app.route('/payment_details', strict_slashes=False)
def number_tempte():
    """ display a HTML page only if n is an integer """
    return render_template('proced.html')

@app.route('/thank_you', strict_slashes=False)
def number_template():
    """ display a HTML page only if n is an integer """
    return render_template('thankyou.html')'''


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
