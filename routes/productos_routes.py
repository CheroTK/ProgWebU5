from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import mysql  
from app.utils.decorators import roles_required  # Si tienes decoradores personalizados

productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/productos')
def lista_productos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos")
    productos = cur.fetchall()
    cur.close()
    return render_template('productos/lista.html', productos=productos)

@productos_bp.route('/productos/agregar', methods=['GET', 'POST'])
@login_required
@roles_required(['admin', 'editor'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        categoria = request.form['categoria']    # <-- Nuevo
        precio = request.form['precio']
        stock = request.form['stock']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO productos (nombre, descripcion, categoria, precio, stock) VALUES (%s, %s, %s, %s, %s)', 
                    (nombre, descripcion, categoria, precio, stock))
        mysql.connection.commit()
        cur.close()
        flash('Producto agregado correctamente')
        return redirect(url_for('productos.lista_productos'))
    return render_template('productos/formulario.html', accion='Agregar')

@productos_bp.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@roles_required(['admin', 'editor'])
def editar_producto(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        categoria = request.form['categoria']
        precio = request.form['precio']
        stock = request.form['stock']
        cur.execute('UPDATE productos SET nombre=%s, descripcion=%s, categoria=%s, precio=%s, stock=%s WHERE id=%s', 
                    (nombre, descripcion, categoria, precio, stock, id))
        mysql.connection.commit() 
        cur.close()
        flash('Producto actualizado')
        return redirect(url_for('productos.lista_productos'))
    cur.execute('SELECT * FROM productos WHERE id=%s', (id,))
    producto = cur.fetchone()
    cur.close()
    return render_template('productos/formulario.html', accion='Editar', producto=producto)

@productos_bp.route('/productos/eliminar/<int:id>')
@login_required
@roles_required(['admin', 'editor'])
def eliminar_producto(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM productos WHERE id=%s', (id,))
    mysql.connection.commit()
    cur.close()
    flash('Producto eliminado')
    return redirect(url_for('productos.lista_productos'))
