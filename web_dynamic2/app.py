#!/usr/bin/python3
""" Starts a Flash Web Application """
from flask import Flask, render_template
app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

@app.route('/index.html', strict_slashes=False)
@app.route('/home', strict_slashes=False)
@app.route('/', strict_slashes=False)
def home():
    """ Prints a Message when / is called """
    return render_template('index.html')


@app.route('/about.html', strict_slashes=False)
def about():
    """ Prints a Message when /hbnb is called """
    return render_template('about.html')


@app.route('/cart.html', strict_slashes=False)
def cart():
    """ Prints a Message when /c is called """
    return render_template('cart.html')


@app.route('/page3.html', strict_slashes=False)
def page3():
    """ Prints a Message when /python is called """
    return render_template('page3.html')


@app.route('/single.html', strict_slashes=False)
def single():
    """ display a HTML page only if n is an integer """
    return render_template('single.html')


@app.route('/proced.html', strict_slashes=False)
def proced():
    """ display a HTML page only if n is an integer """
    return render_template('proced.html')

@app.route('/thankyou.html', strict_slashes=False)
def thankyou():
    """ display a HTML page only if n is an integer """
    return render_template('thankyou.html')


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000, debug=True)
