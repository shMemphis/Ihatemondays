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