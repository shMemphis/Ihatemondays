from flask import Flask, render_template, request, redirect, flash, abort
import pymysql
import flask_login
from dynaconf import Dynaconf
app = Flask(__name__)
conf = Dynaconf(
    settings_file = ('settings.toml')
)

app.secret_key = conf.secret_key
login_manager.init_app(app)
login_manager.logi_view=('/signin')


def connect_db():
    conn = pymysql.connect(
        host ="10.100.34.80",
        database = "shilaire_i_hate_mondays",
        user ='shilaire',
        password =conf.password,
        autocommit= True,
        cursorclass= pymysql.cursors.DictCursor
    )

    return conn

class User:
    is_authenticated = True
    is_anonymous = False
    is_active = True

    def __init__(self, user_id, username, email, first_name, last_name):
        self.id = user_id
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def get_id(self):
        return str(self.id)
##Classes

@app.route("/")
def home():
    return render_template("homepage.html.jinja")

@app.route('/browse')
def product_browse():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `product` ;")

    results = cursor.fetchall()

    return render_template("browse.html.jinja", products =results)

app.secret_key = conf.secret_key

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    conn=connect_db()
    cursor=conn.cursor()
    cursor.execute(f"SELECT * FROM `Costomer`   WHERE `id` = {user_id};")
    result = cursor.fetchone()

    cursor.close()
    conn.close()
    
    if result is not None:
        return User(result["id]"], result["username"], result["email"], result["first_name"], result["last_name"])


@app.route("/product/<product_id>")
def product_page(product_id):
    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM `Product` WHERE `id` = {product_id};")

    result = cursor.fetchone()
    if result is not None:
        return render_template("product.html.jinja", product = result)
    else:
        abort(404)


@app.route("/signin",methods =["POST","GET"])
def sign_up():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        conn =connect_db()
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM `Customer` WHERE `username`= `{username};")

        result =cursor.fetchone()

    if result is None:
        flash ("Your username/password is incorrect")
        
    elif password != result["password"]:
        flash ("Your username/password is incorrect")

    else:
        user = User(result["id]"], result["username"], result["email"], result["first_name"], result["last_name"])

        flask_login.login_user(user)

        return redirect("/")

    return render_template ("signin.html.jinja")

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect ("/")
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
   product = next((item for item in product if item['id'] == product_id), None)
   if product:
       cart.append(product)
   return redirect(url_for('view_cart'))
@app.route('/cart')
def view_cart():
   total = sum(item['price'] for item in cart)
   return render_template('cart.html', cart=cart, total=total)
@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
   global cart
   cart = [item for item in cart if item['id'] != product_id]
   return redirect(url_for('view_cart'))
@app.route('/clear_cart')
def clear_cart():
   global cart
   cart = []
   return redirect(url_for('view_cart'))

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    # Connect to the database and fetch the product to add to the cart
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM products WHERE id = %s', (product_id,))
    product = cursor.fetchone()  # Fetch the product as a dict
    cursor.close()
    connection.close()

    # Initialize cart if it doesn't exist
    if 'cart' not in session:
        session['cart'] = []

    # Add product to cart
    session['cart'].append(product)
    session.modified = True  # Ensure the session is saved

    return redirect(url_for('view_cart'))

@app.route('/cart')
def view_cart():
    cart = session.get('cart', [])
    total = sum(item['price'] for item in cart)  # Calculate total price

    # Render the cart page with cart data and total
    return render_template('cart.html', cart=cart, total=total)

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    
    # Filter out the product to remove it
    cart = [item for item in cart if item['id'] != product_id]
    
    # Update the cart in session
    session['cart'] = cart
    session.modified = True
    
    return redirect(url_for('view_cart'))

@app.route('/clear_cart')
def clear_cart():
    session['cart'] = []  # Empty the cart
    session.modified = True
    return redirect(url_for('view_cart'))

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    # Fetch the product from the database
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM products WHERE id = %s', (product_id,))
    product = cursor.fetchone()
    cursor.close()
    connection.close()

    # Initialize cart if it doesn't exist
    if 'cart' not in session:
        session['cart'] = []

    # Add product to the cart
    session['cart'].append(product)
    session.modified = True  # Mark session as modified to persist changes

    # Redirect to the cart page
    return redirect(url_for('view_cart'))
@app.route('/cart')
def view_cart():
    cart = session.get('cart', [])
    total = sum(item['price'] for item in cart)  # Calculate the total price

    return render_template('cart.html', cart=cart, total=total)


