#!/usr/bin/python3
""" Starts a Flash Web Application """
'''from models import storage
from models.product import Product
from flask import Flask, render_template
app = Flask(__name__, template_folder='trials/templates')
# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/', strict_slashes=False)
def products_list():
    """ displays a HTML page with a list of products """
    products = storage.all(Product).values()
    products = sorted(products, key=lambda k: k.product_name)
    return render_template('index.html', products=products)


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)'''
    
from flask import Flask, request, jsonify, render_template
from models.product import Product
from models.engine.db_storage import DBStorage, classes

app = Flask(__name__, template_folder='trials/templates')
storage = DBStorage()

@app.before_request
def before_request():
    """Ensure a session is available before each request."""
    storage.reload()

@app.teardown_appcontext
def close_db(error):
    """Remove the current SQLAlchemy Session."""
    storage.close()

@app.route('/', methods=['GET'])
def get_products():
    products = storage.all(classes['Product'])
    # Convert products to a list of dictionaries for easier template rendering
    products_list = [product.__dict__ for product in products.values()]
    return render_template('index.html', products=products_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

'''from flask import Flask, request, jsonify, render_template
from models.product import Product
from models.engine.db_storage import DBStorage, classes

app = Flask(__name__, template_folder='trials/templates')
storage = DBStorage()

@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()

@app.route('/', methods=['GET'])
def get_products():
    products = storage.all(classes['Product'])
    # Convert products to a list of dictionaries for easier template rendering
    products_list = [product.__dict__ for product in products.values()]
    return render_template('index.html', products=products_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)'''


'''from flask import Flask, render_template
from models.engine.db_storage import DBStorage

app = Flask(__name__, template_folder='trials/templates')
storage = DBStorage()
storage.reload()

@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()

@app.route('/', methods=['GET'])
def get_products():
    products = storage.all('Product').values()
    products = sorted(products, key=lambda k: k.product_name)
    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)'''
    
'''from flask import Flask, request, jsonify, render_template
from models.product import Product
from models.engine.db_storage import DBStorage, classes

app = Flask(__name__, template_folder='trials/templates')
storage = DBStorage()

@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()

@app.route('/', methods=['GET'])
def get_products():
    products = storage.all(classes['Product'])
    products = jsonify([product.__dict__ for product in products.values()])
    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)'''

'''@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = classes['User'](**data)
    storage.new(new_user)
    storage.save()
    return jsonify({'message': 'User created'}), 201'''

'''import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Now you can access the variables using os.environ
mysql_user = os.environ.get('ECOMM_MYSQL_USER')
mysql_pwd = os.environ.get('ECOMM_MYSQL_PWD')
mysql_host = os.environ.get('ECOMM_MYSQL_HOST')
mysql_db = os.environ.get('ECOMM_MYSQL_DB')

# Configure the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{mysql_user}:{mysql_pwd}@{mysql_host}/{mysql_db}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Assuming you have a model named Color in models/color.py
#@from models.color import Color

@app.route('/')
def index():
    # Fetch colors from the database
    #colors = Color.query.all()
    return render_template('index.html')#, colors=colors)

if __name__ == '__main__':
    app.run(debug=True)'''
