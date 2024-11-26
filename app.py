from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = 'almacen.db'

# Conectar a la base de datos
def connect_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Inicialización de la base de datos
def init_db():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS producto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )''')
        conn.commit()

# Función para crear un producto
def create_product(descripcion, cantidad, precio):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO producto (descripcion, cantidad, precio) 
                          VALUES (?, ?, ?)''', (descripcion, cantidad, precio))
        conn.commit()

# Función para obtener todos los productos
def get_all_products():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM producto')
        return cursor.fetchall()

# Función para obtener un producto específico
def get_product(product_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM producto WHERE id = ?', (product_id,))
        return cursor.fetchone()

# Función para actualizar un producto
def update_product(product_id, descripcion, cantidad, precio):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''UPDATE producto SET descripcion = ?, cantidad = ?, precio = ? 
                          WHERE id = ?''', (descripcion, cantidad, precio, product_id))
        conn.commit()

# Función para eliminar un producto
def delete_product(product_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM producto WHERE id = ?', (product_id,))
        conn.commit()

# Rutas de la aplicación

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
    init_db()  # Inicializar la base de datos
    app.run(debug=True)
