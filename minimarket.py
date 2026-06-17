from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import datetime
import random

# ---------- CREAR LA APLICACIÓN ----------
app = Flask(__name__)
app.secret_key = 'clave_secreta_2026'  # Cambiar en producción

# ---------- USUARIO ADMIN (hardcodeado) ----------
ADMIN_USER = {
    'username': 'admin',
    'password': 'admin123'   # ¡Cambiar en producción!
}

# ---------- PRODUCTOS (en memoria) ----------
PRODUCTOS = [
    {"id": 1, "nombre": "Galleta soda", "peso": "6 unidades (222 gr)", "precio": 3.30, "img": "i1.jpg"},
    {"id": 2, "nombre": "Coca Cola", "peso": "500 ml", "precio": 3.50, "img": "i2.jpg"},
    {"id": 3, "nombre": "Leche Gloria", "peso": "390 gr", "precio": 4.20, "img": "i3.jpg"},
    {"id": 4, "nombre": "Yogurt Laive", "peso": "1000 gr", "precio": 6.50, "img": "i4.jpg"},
    {"id": 5, "nombre": "Pan en bolsa", "peso": "500 gr", "precio": 8.50, "img": "i5.jpg"},
    {"id": 6, "nombre": "Galletas de vainilla", "peso": "6 unidades (222 gr)", "precio": 4.70, "img": "i6.jpg"},
    {"id": 7, "nombre": "Atún en lata", "peso": "140 gr", "precio": 5.80, "img": "i7.jpg"},
    {"id": 8, "nombre": "Café Kirma", "peso": "180 gr", "precio": 21.90, "img": "i8.jpg"},
    {"id": 9, "nombre": "Huevos", "peso": "15 unidades", "precio": 9.50, "img": "i9.jpg"},
    {"id": 10, "nombre": "Chocolate Triangulo", "peso": "30 gr", "precio": 2.50, "img": "i10.jpg"},
    {"id": 11, "nombre": "Gaseosa KR", "peso": "1500 ml", "precio": 3.50, "img": "i11.jpg"},
    {"id": 12, "nombre": "Gaseosa sprite", "peso": "1500 ml", "precio": 6.50, "img": "i12.jpg"},
    {"id": 13, "nombre": "Galletas oreo", "peso": "432 gr", "precio": 8.20, "img": "i13.jpg"},
    {"id": 14, "nombre": "Mayonesa", "peso": "190 gr", "precio": 5.80, "img": "i14.jpg"},
    {"id": 15, "nombre": "Mermelada", "peso": "320 gr", "precio": 5.50, "img": "i15.jpg"},
    {"id": 16, "nombre": "Jamón San Fernando", "peso": "200 gr", "precio": 9.50, "img": "i16.jpg"},
    {"id": 17, "nombre": "Margarina Manti", "peso": "225 gr", "precio": 3.50, "img": "i17.jpg"},
    {"id": 18, "nombre": "Mantequilla Laive", "peso": "200 gr", "precio": 7.50, "img": "i18.jpg"},
    {"id": 19, "nombre": "Café Ecco", "peso": "80 gr", "precio": 8.50, "img": "i19.jpg"},
    {"id": 20, "nombre": "Café Altomayo", "peso": "170 gr", "precio": 25.10, "img": "i20.jpg"},
]

# ---------- CLIENTES (en memoria) ----------
CLIENTES = [
    {"id": 1, "nombre": "Ana Gómez", "email": "ana@gmail.com", "telefono": "987654321", "fecha_registro": "14/06"},
    {"id": 2, "nombre": "Carlos Ruíz", "email": "carlos@gmail.com", "telefono": "912345678", "fecha_registro": "16/06"}
]
next_cliente_id = 3

# ---------- DECORADOR PARA PROTEGER RUTAS ADMIN ----------
def login_required(f):
    """Redirige al login si no hay sesión de admin."""
    def wrapper(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# ---------- RUTAS DE PÁGINAS PÚBLICAS ----------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos')
def productos():
    return render_template('productos.html', productos=PRODUCTOS)

@app.route('/contactos')
def contactos():
    return render_template('contactos.html')

# ---------- LOGIN ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USER['username'] and password == ADMIN_USER['password']:
            session['admin_logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Credenciales incorrectas')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

# ---------- DASHBOARD ADMIN ----------
@app.route('/admin')
@login_required
def dashboard():
    total_productos = len(PRODUCTOS)
    precio_promedio = sum(p['precio'] for p in PRODUCTOS) / total_productos if total_productos > 0 else 0
    total_clientes = len(CLIENTES)
    
    ventas_mes = total_clientes * 35.50
    variacion_productos = total_productos - 7

    hoy = datetime.date.today()
    dias = [(hoy - datetime.timedelta(days=i)).strftime('%d/%m') for i in range(6, -1, -1)]
    ventas_diarias = [random.randint(15, 60) for _ in range(7)]

    nuevos_clientes_linea = []
    nuevos_productos_linea = []
    for dia in dias:
        cnt_c = sum(1 for c in CLIENTES if c.get('fecha_registro') == dia)
        cnt_p = sum(1 for p in PRODUCTOS if p.get('fecha_registro') == dia)
        nuevos_clientes_linea.append(cnt_c)
        nuevos_productos_linea.append(cnt_p)

    rango1 = sum(1 for p in PRODUCTOS if p['precio'] < 5)
    rango2 = sum(1 for p in PRODUCTOS if 5 <= p['precio'] <= 10)
    rango3 = sum(1 for p in PRODUCTOS if p['precio'] > 10)

    hora_actual = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    return render_template('dashboard.html',
                           total_productos=total_productos,
                           precio_promedio=precio_promedio,
                           total_clientes=total_clientes,
                           ventas_mes=ventas_mes,
                           variacion_productos=variacion_productos,
                           dias=dias,
                           ventas_diarias=ventas_diarias,
                           nuevos_clientes_linea=nuevos_clientes_linea,
                           nuevos_productos_linea=nuevos_productos_linea,
                           rango1=rango1,
                           rango2=rango2,
                           rango3=rango3,
                           hora_actual=hora_actual)

# ---------- CRUD DE PRODUCTOS (solo admin) ----------
@app.route('/admin/productos')
@login_required
def admin_productos():
    # Enviamos la variable vacía o en 0 para que el HTML viejo no se rompa si se quedó pegado
    return render_template('admin_productos.html', 
                           productos=PRODUCTOS, 
                           variacion_productos=0, 
                           precio_promedio=0, 
                           total_clientes=0, 
                           ventas_mes=0, 
                           dias=[], 
                           ventas_diarias=[], 
                           nuevos_clientes_linea=[], 
                           nuevos_productos_linea=[], 
                           hora_actual="")

@app.route('/admin/productos/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_producto():
    if request.method == 'POST':
        nuevo_id = max(p['id'] for p in PRODUCTOS) + 1 if PRODUCTOS else 1
        try:
            precio = float(request.form['precio'])
        except ValueError:
            return render_template('producto_form.html', titulo='Nuevo Producto', producto=None, error="Precio inválido")

        producto = {
            'id': nuevo_id,
            'nombre': request.form['nombre'],
            'peso': request.form['peso'],
            'precio': precio,
            'img': request.form['img'],
            'fecha_registro': datetime.date.today().strftime('%d/%m')
        }
        PRODUCTOS.append(producto)
        return redirect(url_for('admin_productos'))
    return render_template('producto_form.html', titulo='Nuevo Producto', producto=None)

@app.route('/admin/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    producto = next((p for p in PRODUCTOS if p['id'] == id), None)
    if not producto:
        return "Producto no encontrado", 404
    if request.method == 'POST':
        try:
            precio = float(request.form['precio'])
        except ValueError:
            return render_template('producto_form.html', titulo='Editar Producto', producto=producto, error="Precio inválido")

        producto['nombre'] = request.form['nombre']
        producto['peso'] = request.form['peso']
        producto['precio'] = precio
        producto['img'] = request.form['img']
        return redirect(url_for('admin_productos'))
    return render_template('producto_form.html', titulo='Editar Producto', producto=producto)

@app.route('/admin/productos/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_producto(id):
    # Corrección: Mutar la lista original sin romper referencias globales
    filtrados = [p for p in PRODUCTOS if p['id'] != id]
    PRODUCTOS.clear()
    PRODUCTOS.extend(filtrados)
    return redirect(url_for('admin_productos'))

# ---------- CRUD DE CLIENTES (solo admin) ----------
@app.route('/admin/clientes')
@login_required
def admin_clientes():
    return render_template('admin_clientes.html', clientes=CLIENTES)

@app.route('/admin/clientes/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_cliente():
    global next_cliente_id
    if request.method == 'POST':
        cliente = {
            'id': next_cliente_id,
            'nombre': request.form['nombre'],
            'email': request.form['email'],
            'telefono': request.form.get('telefono', ''),
            'fecha_registro': datetime.date.today().strftime('%d/%m')
        }
        CLIENTES.append(cliente)
        next_cliente_id += 1
        return redirect(url_for('admin_clientes'))
    return render_template('cliente_form.html', titulo='Nuevo Cliente', cliente=None)

@app.route('/admin/clientes/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_cliente(id):
    cliente = next((c for c in CLIENTES if c['id'] == id), None)
    if not cliente:
        return "Cliente no encontrado", 404
    if request.method == 'POST':
        cliente['nombre'] = request.form['nombre']
        cliente['email'] = request.form['email']
        cliente['telefono'] = request.form.get('telefono', '')
        return redirect(url_for('admin_clientes'))
    return render_template('cliente_form.html', titulo='Editar Cliente', cliente=cliente)

@app.route('/admin/clientes/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_cliente(id):
    # Corrección: Mutar la lista original sin romper referencias globales
    filtrados = [c for c in CLIENTES if c['id'] != id]
    CLIENTES.clear()
    CLIENTES.extend(filtrados)
    return redirect(url_for('admin_clientes'))

# ---------- API REST ----------
@app.route('/api/productos')
def api_productos():
    return jsonify(PRODUCTOS)

@app.route('/api/carrito/agregar', methods=['POST'])
def api_agregar():
    data = request.get_json() or {}
    producto_id = data.get('id')
    producto = next((p for p in PRODUCTOS if p['id'] == producto_id), None)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404

    carrito = session.get('carrito', {})
    key = str(producto_id)
    if key in carrito:
        carrito[key]['cantidad'] += 1
    else:
        carrito[key] = {
            'id': producto_id,
            'nombre': producto['nombre'],
            'precio': producto['precio'],
            'cantidad': 1
        }
    session['carrito'] = carrito
    session.modified = True  # Corrección: Forzar a Flask a guardar los cambios en la cookie
    return jsonify({'carrito': carrito})

@app.route('/api/carrito/eliminar', methods=['POST'])
def api_eliminar():
    data = request.get_json() or {}
    producto_id = str(data.get('id'))
    carrito = session.get('carrito', {})
    if producto_id in carrito:
        if carrito[producto_id]['cantidad'] > 1:
            carrito[producto_id]['cantidad'] -= 1
        else:
            del carrito[producto_id]
    session['carrito'] = carrito
    session.modified = True  # Corrección: Forzar a Flask a guardar los cambios en la cookie
    return jsonify({'carrito': carrito})

@app.route('/api/carrito')
def api_ver_carrito():
    return jsonify(session.get('carrito', {}))

@app.route('/api/carrito/comprar', methods=['POST'])
def api_comprar():
    session.pop('carrito', None)
    return jsonify({'mensaje': '¡Compra realizada con éxito!'})

if __name__ == '__main__':
    app.run(debug=True)