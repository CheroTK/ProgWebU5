from flask import Blueprint, render_template, session
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import mysql

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html', active_page='index')

@main_bp.route('/perfil')
@login_required
def perfil():
    cur = mysql.connection.cursor()
    cur.execute("SELECT username, email, edad, altura, peso, objetivo FROM usuarios WHERE id = %s", (current_user.id,))
    user = cur.fetchone()
    cur.close()
    # Si user es None, maneja el error, pero normalmente no pasa
    user_data = {
        'username': user[0],
        'email': user[1],
        'edad': user[2],
        'altura': user[3],
        'peso': user[4],
        'objetivo': user[5]
    }
    return render_template('perfil.html', user=user_data, active_page='perfil')

@main_bp.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    if request.method == 'POST':
        edad = request.form.get('edad')
        altura = request.form.get('altura')
        peso = request.form.get('peso')
        objetivo = request.form.get('objetivo')

        # Validación sencilla
        try:
            edad_valor = int(edad)
            altura_valor = float(altura)
            peso_valor = float(peso)
        except (ValueError, TypeError):
            flash('Por favor ingresa valores válidos.', 'warning')
            return redirect(url_for('main.editar_perfil'))

        # Guardar en la base de datos
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE usuarios 
            SET edad = %s, altura = %s, peso = %s, objetivo = %s 
            WHERE id = %s
            """, (edad_valor, altura_valor, peso_valor, objetivo, current_user.id))
        mysql.connection.commit()
        cur.close()

        flash('¡Cambios guardados correctamente!', 'success')
        return redirect(url_for('main.perfil')) 

    # GET: Mostrar formulario con datos actuales
    cur = mysql.connection.cursor()
    cur.execute("SELECT edad, altura, peso, objetivo FROM usuarios WHERE id = %s", (current_user.id,))
    datos = cur.fetchone()
    cur.close()
    return render_template('editar_perfil.html', datos=datos)




@main_bp.route('/plan-ejercicio')
def plan_ejercicio():
    return render_template('plan-ejercicio.html', active_page='plan_ejercicio')

@main_bp.route('/tareas')
def tareas():
    return render_template('tareas.html', active_page='tareas')

@main_bp.route('/ejercicio-fitness')
def ejercicio_fitness():
    return render_template('EjercicioFitness.html', active_page='ejercicio_fitness')

@main_bp.route('/configuracion')
def configuracion():
    return render_template('configuracion.html', active_page='configuracion')

@main_bp.route('/amigos')
def amigos():
    return render_template('amigos.html', active_page='amigos')

@main_bp.route('/tienda')
def tienda():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre, descripcion, precio, categoria FROM productos")
    productos = cur.fetchall()
    cur.close()

    # Separar productos por categoría
    rutinas = [p for p in productos if p[4] == 'rutina']
    recetas = [p for p in productos if p[4] == 'receta']

    return render_template('tienda.html', rutinas=rutinas, recetas=recetas)

@main_bp.route('/pago')
@login_required
def pago():
    venta_id = session.get('last_venta_id')
    if not venta_id:
        # Si no hay compra reciente, regresa a tienda
        return redirect(url_for('main.tienda'))
    cur = mysql.connection.cursor()
    # Trae productos y detalles de la última venta del usuario
    cur.execute("""
        SELECT p.nombre, dv.cantidad, dv.precio_unitario
        FROM detalle_ventas dv
        JOIN productos p ON dv.producto_id = p.id
        WHERE dv.venta_id = %s
    """, (venta_id,))
    productos = cur.fetchall()
    cur.execute("SELECT total FROM ventas WHERE id = %s", (venta_id,))
    total = cur.fetchone()[0] if cur.rowcount else 0
    cur.close()
    # Limpia la sesión para que no repita el ticket
    session.pop('last_venta_id', None)
    return render_template('pago.html', productos=productos, total=total)

@main_bp.route('/acerca')
def acerca():
    return render_template('AcercaDe.html', active_page='acerca')