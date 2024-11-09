from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def connect_db():
    conn = sqlite3.connect('almacen.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM producto')
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="producto"')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS producto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def create_product(descripcion, cantidad, precio):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO producto (descripcion, cantidad, precio) VALUES (?, ?, ?)",
                   (descripcion, cantidad, precio))
    conn.commit()
    conn.close()

def get_all_products():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM producto")
    products = cursor.fetchall()
    conn.close()
    return products

def get_product(product_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM producto WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    conn.close()
    return product

def update_product(product_id, descripcion, cantidad, precio):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE producto SET descripcion = ?, cantidad = ?, precio = ? WHERE id = ?",
                   (descripcion, cantidad, precio, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM producto WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    products = get_all_products()
    return render_template('index.html', products=products)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        create_product(descripcion, cantidad, precio)
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/update/<int:product_id>', methods=['GET', 'POST'])
def update(product_id):
    product = get_product(product_id)
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        update_product(product_id, descripcion, cantidad, precio)
        return redirect(url_for('index'))
    return render_template('update.html', product=product)

@app.route('/delete/<int:product_id>')
def delete(product_id):
    delete_product(product_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  
    app.run(debug=True)