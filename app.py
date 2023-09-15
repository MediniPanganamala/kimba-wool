import atexit
from flask import Flask, render_template, request, redirect, url_for, session, g,flash
import sqlite3

app = Flask(__name__)
app.secret_key = "kimbaw001"  


def init_db():
    conn = sqlite3.connect('database.db', check_same_thread=False)
    return conn


def close_db():
    if hasattr(g, 'db'):
        g.db.close()

atexit.register(close_db)


@app.before_request
def before_request():
    g.db = init_db()


def initialize_database():
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 1
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            price REAL NOT NULL,
            image_url TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart_items (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    conn.commit()
    conn.close()


@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('home.html')

@app.route('/admin/signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        if request.form['secret_key'] == '211':
            username = request.form['username']
            password = request.form['password']
            with g.db:
                cursor = g.db.cursor()               
                cursor.execute("SELECT * FROM admins WHERE username = ?", (username,))
                existing_user = cursor.fetchone()
                if existing_user:
                    return "Username already exists"
                else:
                    cursor.execute("INSERT INTO admins (username, password) VALUES (?, ?)", (username, password))
            return redirect(url_for('admin_signin'))
        else:
            return "Invalid secret key"
    return render_template('admin_signup.html')


# @app.route('/dashboard')
# def dashboard():
#     if 'username' in session:
#         username = session['username']
#         products = get_products_from_database()
#         conn = sqlite3.connect('database.db')
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM users")
#         users = cursor.fetchall()
#         conn.close()
#         return render_template('dashboard.html', username=username, users=users, products=products)
#     return redirect(url_for('home'))




@app.route('/user/signup', methods=['GET', 'POST'])
def user_signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with g.db:
            cursor = g.db.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            existing_user = cursor.fetchone()
            if existing_user:
                return "Username already exists"
            else:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            return redirect(url_for('user_signin'))
    return render_template('user_signup.html')


@app.route('/admin/signin', methods=['GET', 'POST'])
def admin_signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with g.db:
            cursor = g.db.cursor()
            cursor.execute("SELECT * FROM admins WHERE username = ? AND password = ?", (username, password))
            admin = cursor.fetchone()
            if admin:
                session['username'] = username
                return redirect(url_for('admin_dashboard'))
            else:
                return "Invalid credentials"
    return render_template('admin_signin.html')

@app.route('/user/signin', methods=['GET', 'POST'])
def user_signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with g.db:
            cursor = g.db.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()
            if user:
                session['username'] = username
                session['user_id'] = user[0]
                return redirect(url_for('dashboard'))
            else:
                return "Invalid credentials"
    return render_template('user_signin.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'username' in session:
        username = session['username']
        conn = g.db
        cursor = conn.cursor()
        
       
        cursor.execute("SELECT * FROM admins")
        #print("printed---> Adminsss")
        admins = cursor.fetchall()
        
        
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        
        conn.close()
        
        return render_template('admin_dashboard.html', username=username, admins=admins, users=users)
    return redirect(url_for('home'))

@app.route('/admin/create_user', methods=['GET', 'POST'])
def admin_create_user():
    if 'username' in session:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            with g.db:
                cursor = g.db.cursor()
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            return redirect(url_for('admin_dashboard'))
        return render_template('admin_create_user.html')
    return redirect(url_for('home'))

@app.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
def admin_edit_user(user_id):
    if 'username' in session:
        if request.method == 'POST':
            new_username = request.form['new_username']
            new_password = request.form['new_password']
            with g.db:
                cursor = g.db.cursor()
                cursor.execute("UPDATE users SET username=?, password=? WHERE id=?", (new_username, new_password, user_id))
            return redirect(url_for('admin_dashboard'))
        else:
            conn = g.db
            cursor = conn.cursor()
           
            cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
            #user = cursor.fetchone()  
           # print("user info------------------",user)
            user_data = cursor.fetchone()
            user = {
                'id': user_data[0],
                'username': user_data[1]
            }

            conn.close()
            return render_template('admin_edit_user.html', user=user)
    return redirect(url_for('home'))


@app.route('/admin/delete_user/<int:user_id>', methods=['GET', 'POST'])
def admin_delete_user(user_id):
    if 'username' in session:
        if request.method == 'POST':
            with g.db:
                cursor = g.db.cursor()
                cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
            return redirect(url_for('admin_dashboard'))
        else:
            return "Invalid request method"
    return redirect(url_for('home'))


@app.route('/cart')
def cart():
    if 'username' in session:
        username = session['username']
        user_id = get_user_id_from_username(username)
        
       
        cart_items = get_cart_items(user_id)
        
        return render_template('cart.html', username=username, cart_items=cart_items)
    
    return redirect(url_for('home'))


def get_products_from_database():
    with g.db:
        cursor = g.db.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
    return products

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']     
        products = get_products_from_database()
        #print("proddddddd", products)
        #print("usernameeeeeee", username)
        return render_template('dashboard.html', username=username, products=products)

    return redirect(url_for('home'))

def get_user_id_from_username(username):
    with g.db:
        cursor = g.db.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user_id = cursor.fetchone()
        if user_id:
            return user_id[0]
        return None


def get_cart_items(user_id):
    with g.db:
        cursor = g.db.cursor()
        cursor.execute("""
        SELECT ci.id, ci.quantity, ci.product_id, p.price
        FROM cart_items ci
        JOIN products p ON ci.product_id = p.id
        WHERE ci.user_id = ?
        """, (user_id,))
        
        cart_items = cursor.fetchall()

        cart_items_dicts = [{'id': item[0], 'quantity': item[1], 'product_id': item[2], 'price': item[3]} for item in cart_items]

    return cart_items_dicts


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'username' in session:
        user_id = get_user_id_from_username(session['username'])
        quantity = int(request.form['quantity'])
      
        with g.db:
            cursor = g.db.cursor()
            cursor.execute("INSERT INTO cart_items (user_id, product_id, quantity) VALUES (?, ?, ?)",
                           (user_id, product_id, quantity))
        
        return redirect(url_for('dashboard'))
    return redirect(url_for('home'))

@app.route('/delete_item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    if 'username' in session:
        user_id = get_user_id_from_username(session['username'])
        print("user_idd ", user_id)
        print("Received request to delete item with ID:", item_id)  

        with g.db:
            cursor = g.db.cursor()
            try:
                
                cursor.execute("SELECT * FROM cart_items WHERE user_id=? AND id=?", (user_id, item_id))
                cart_item = cursor.fetchone()

                if cart_item:
                    
                    cursor.execute("DELETE FROM cart_items WHERE id=?", (item_id,))
                    g.db.commit()
                    print("Item deleted successfully")
                    flash('Cart item removed successfully', 'success')
                else:
                    print("Item does not belong to the user")
                    flash('Cart item does not belong to you', 'error')

            except Exception as e:
                print("Error deleting item:", str(e))
                g.db.rollback()

        return redirect(url_for('cart'))
    else:
        flash('User not logged in', 'error')
        return redirect(url_for('home'))



@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        initialize_database()
    app.run(debug=True)


