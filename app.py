import os, json, datetime
from flask import Flask, request, jsonify, render_template, redirect, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# os.environ['APP_SETTINGS']
app.config.from_object("config.DevelopmentConfig")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *


#  __________________
# |                  |
# |  Templates       |
# |__________________|

@app.route('/')
def home():
    data = {
        'breadcrumb_title':         'Página principal',
        'breadcrumb_button':        '<i class="fas fa-fw fa-info-circle fa-sm text-white-50 mr-2"></i>Sobre el proyecto',
        'breadcrumb_button_url':    '#'
    }
    return render_template('pages/home.html', data=data)

# ================================
# ==== DPTO. RECURSOS HUMANOS ====
# ================================

# ==== EMPLEADOS ====

@app.route('/empleados/add', methods=['GET'])
def empleados_add():
    """
    Empleados: añadir empleado
    ----
    En esta rutina mostraremos una página con un formulario para crear
    un nuevo empleado.
    """
    data = {
        'title':                    "Añadir empleado",
        'breadcrumb_title':         "Recursos Humanos",
        'breadcrumb_subtitle':      '<i class="fas fa-fw fa-user mr-2"></i>Empleados',
        'breadcrumb_button':        '<i class="fas fa-fw fa-arrow-left fa-sm text-white-50 mr-2"></i>Volver a empleados',
        'breadcrumb_button_url':    '/empleados',
        'database_name':            'empleado',
        'database_name_plural':     'empleados',
        'card_title':               "Crear nuevo empleado",
        'edit':                     False,  # el formulario será de creación
        # no son necesarios más datos en este caso
    }
    return render_template('pages/empleados_form.html', data=data)


@app.route('/empleados', methods=['GET'])
def empleados_all():
    """
    Empleados: mostrar la información de todos los empleados
    ----
    En esta rutina mostraremos la información de todos los empleados
    """
    try:
        empleados = Empleado.query.all()
        empleados = [empleado.serialize() for empleado in empleados]
        success = True
    except:
        success = False

    data = {
        'title':                    "Empleados",
        'breadcrumb_title':         "Recursos Humanos",
        'breadcrumb_subtitle':      '<i class="fas fa-fw fa-user mr-2"></i>Empleados',
        'breadcrumb_button':        '<i class="fas fa-fw fa-plus fa-sm text-white-50 mr-2"></i>Añadir empleado',
        'breadcrumb_button_url':    '/empleados/add',
        'database_name':            'empleado',
        'database_name_plural':     'empleados',
        'card_title':               "Listado de empleados",
        'error':                    f'No hemos podido obtener la información de los empleados' if not success else None,
        'empleados':                empleados if success else None
    }
    return render_template('pages/empleados_list.html', data=data)


@app.route('/empleados/<dni>', methods=['GET'])
def empleados_detail(dni):
    """
    Empleados: mostrar información de un empleado
    ----
    En esta rutina mostraremos la información de un empleado
    """
    # primero recopilamos la información de la BD
    exists = False
    try:
        empleado = Empleado.query.filter_by(dni=dni).first()
        empleado = empleado.serialize()
    except:
        empleado = None

    data = {
        'title':                    f"Empleado #{dni}",
        'breadcrumb_title':         "Recursos Humanos",
        'breadcrumb_subtitle':      '<i class="fas fa-fw fa-user mr-2"></i>Empleados',
        'breadcrumb_button':        '<i class="fas fa-fw fa-arrow-left fa-sm text-white-50 mr-2"></i>Volver a empleados',
        'breadcrumb_button_url':    '/empleados',
        'database_name':            'empleado',
        'database_name_plural':     'empleados',
        'card_title':               f"Detalle del empleado #{dni}",
        # Mostrar un mensaje de error si no existe el empleado
        'error':                    f'No se ha encontrado un empleado con DNI {dni}' if not empleado else None,
        'empleado':                 empleado
    }
    return render_template('pages/empleados_detail.html', data=data)


@app.route('/empleados/<dni>/edit', methods=['GET'])
def empleados_edit(dni, api_resp=None):
    """
    Empleados: editar información de un empleado
    ----
    En esta rutina permitiremos la edición de la información de un empleado
    """
    # primero recopilamos la información de la BD
    try:
        empleado = Empleado.query.filter_by(dni=dni).first()
        empleado = empleado.serialize()
    except:
        empleado = None

    data = {
        'title':                    f"Editar empleado #{dni}",
        'breadcrumb_title':         "Recursos Humanos",
        'breadcrumb_subtitle':      '<i class="fas fa-fw fa-user mr-2"></i>Empleados',
        'breadcrumb_button':        '<i class="fas fa-fw fa-arrow-left fa-sm text-white-50 mr-2"></i>Volver a empleados',
        'breadcrumb_button_url':    '/empleados',
        'database_name':            'empleado',
        'database_name_plural':     'empleados',
        'card_title':               f"Editar empleado #{dni}",
        'error':                    f'No se ha encontrado un empleado con DNI {dni}' if not empleado else None,
        'edit':                     True,   # el formulario será de edición
        # cargamos la información existente en el formulario
        'edit_data':                empleado
    }
    return render_template('pages/empleados_form.html', data=data)


# ==== EVALUACIONES ====

@app.route('/evaluaciones', methods=['GET'])
def evaluaciones_all():
    """
    Evaluaciones: mostrar la información de todas las evaluaciones
    ----
    En esta rutina mostraremos la información de todas las evaluaciones
    """
    try:
        evaluaciones = Evaluacion.query.all()
        evaluaciones = [evaluacion.serialize() for evaluacion in evaluaciones]
        success = True
    except:
        success = False

    data = {
        'title':                    "Evaluaciones",
        'breadcrumb_title':         "Recursos Humanos",
        'breadcrumb_subtitle':      '<i class="fas fa-fw fa-star-half-alt mr-2"></i>Evaluaciones',
        'breadcrumb_button':        '<i class="fas fa-fw fa-plus fa-sm text-white-50 mr-2"></i>Crear evaluación',
        'breadcrumb_button_url':    '/evaluaciones/add',
        'database_name':            'evaluacion',
        'database_name_plural':     'evaluaciones',
        'card_title':               "Listado de evaluaciones",
        'error':                    f'No hemos podido obtener la información de las evaluaciones' if not success else None,
        'evaluaciones':             evaluaciones if success else None
    }
    return render_template('pages/evaluaciones_list.html', data=data)


@app.route('/empleados/<dni>/evals', methods=['GET'])
def empleados_evals_all(dni):
    """
    Evaluaciones: mostrar la información de todas las evaluaciones de un empleado
    ----
    En esta rutina mostraremos la información de todas las evaluaciones de un empleado
    """
    try:
        evaluaciones = Evaluacion.query.filter_by(dni=dni)
        evaluaciones = [evaluacion.serialize() for evaluacion in evaluaciones]
    except:
        evaluaciones = None

    data = {
        'title':                    f"Evaluaciones de empleado #{dni}",
        'breadcrumb_title':         "Recursos Humanos",
        'breadcrumb_subtitle':      '<i class="fas fa-fw fa-user mr-2"></i>Empleados',
        'breadcrumb_button':        f'<i class="fas fa-fw fa-arrow-left fa-sm text-white-50 mr-2"></i>Volver a empleado #{dni}',
        'breadcrumb_button_url':    f'/empleados/{dni}',
        'database_name':            'empleado',
        'database_name_plural':     'empleados',
        'card_title':               f"Evaluaciones del empleado #{dni}",
        # Mostrar un mensaje de error si no existe el empleado
        'error':                    f'No hemos podido obtener la información de las evaluaciones del empleado con DNI {dni}' if not evaluaciones else None,
        'empleado':                 evaluaciones
    }
    return render_template('pages/evaluaciones_list.html', data=data)


@app.route('/evaluaciones/<id>', methods=['GET'])
def evaluaciones_detail(id):
    """
    Evaluaciones: mostrar información de una evaluacion
    ----
    En esta rutina mostraremos la información de una evaluacion
    """
    # primero recopilamos la información de la BD
    try:
        evaluacion = Evaluacion.query.filter_by(id=id).first()
        evaluacion = evaluacion.serialize()
    except:
        evaluacion = None

    data = {
        'title':                    f"Evaluación #{id}",
        'breadcrumb_title':         "Recursos Humanos",
        'breadcrumb_subtitle':      '<i class="fas fa-fw fa-star-half-alt mr-2"></i>Evaluaciones',
        'breadcrumb_button':        '<i class="fas fa-fw fa-arrow-left fa-sm text-white-50 mr-2"></i>Volver a evaluaciones',
        'breadcrumb_button_url':    '/evaluaciones',
        'database_name':            'evaluacion',
        'database_name_plural':     'evaluaciones',
        'card_title':               f"Detalle de la evaluación #{id}",
        'error':                    f'No se ha encontrado una evaluación con ID #{id}' if not evaluacion else None,
        'evaluacion':               evaluacion
    }
    return render_template('pages/evaluaciones_detail.html', data=data)


@app.route('/evaluaciones/add', methods=['GET'])
def evaluaciones_add(api_resp=None):
    """
    Evaluaciones: añadir evaluacion
    ----
    En esta rutina mostraremos una página con un formulario para crear
    una nueva evaluación.
    """
    data = {
        'title':                    "Añadir evaluación",
        'breadcrumb_title':         "Recursos Humanos",
        'breadcrumb_subtitle':      '<i class="fas fa-fw fa-star-half-alt mr-2"></i>Evaluaciones',
        'breadcrumb_button':        '<i class="fas fa-fw fa-arrow-left fa-sm text-white-50 mr-2"></i>Volver a evaluaciones',
        'breadcrumb_button_url':    '/evaluaciones',
        'database_name':            'evaluacion',
        'database_name_plural':     'evaluaciones',
        'card_title':               f"Añadir evaluación",
        'edit':                     False,  # el formulario será de creación
        # no son necesarios más datos en este caso
    }
    return render_template('pages/evaluaciones_form.html', data=data)


@app.route('/evaluaciones/<id>/edit', methods=['GET'])
def evaluaciones_edit(id, api_resp=None):
    """
    Evaluaciones: editar información de una evaluacion
    ----
    En esta rutina permitiremos la edición de la información de un proyecto
    """
    # primero recopilamos la información de la BD
    try:
        evaluacion = Evaluacion.query.filter_by(id=id).first()
        evaluacion = evaluacion.serialize()
    except Exception as e:
        print(str(e))
        evaluacion = None

    data = {
        'title':                    f"Editar evaluación {id}",
        'breadcrumb_title':         "Recursos Humanos",
        'breadcrumb_subtitle':      '<i class="fas fa-fw fa-star-half-alt mr-2"></i>Evaluaciones',
        'breadcrumb_button':        '<i class="fas fa-fw fa-arrow-left fa-sm text-white-50 mr-2"></i>Volver a evaluaciones',
        'breadcrumb_button_url':    '/evaluaciones',
        'database_name':            'evaluacion',
        'database_name_plural':     'evaluaciones',
        'card_title':               f"Editar evaluación #{id}",
        'error':                    f'No se ha encontrado una evaluación con ID {id}' if not evaluacion else None,
        'edit':                     True,  # el formulario será de edición
        # cargamos la información existente en el formulario
        'edit_data':                evaluacion
    }
    return render_template('pages/evaluaciones_form.html', data=data)


# ================================
# ==== DPTO. I+D Y PRODUCCIÓN ====
# ================================

# ==== PROYECTOS ====

@app.route('/proyectos/add', methods=['GET'])
def proyectos_add():
    """
    Proyectos: añadir proyecto
    ----
    En esta rutina mostraremos una página con un formulario para crear
    un nuevo proyecto.
    """
    data = {
        'title':                    "Añadir proyecto",
        'breadcrumb_title':         "I+D y Producción",
        'breadcrumb_subtitle':      '<i class="fas fa-fw fa-lightbulb mr-2"></i>Proyectos',
        'breadcrumb_button':        '<i class="fas fa-fw fa-arrow-left fa-sm text-white-50 mr-2"></i>Volver a proyectos',
        'breadcrumb_button_url':    '/proyectos',
        'database_name':            'proyecto',
        'database_name_plural':     'proyectos',
        'card_title':               "Crear nuevo proyecto",
        'edit':                     False,  # el formulario será de creación
        # no son necesarios más datos en este caso
    }
    return render_template('pages/proyectos_form.html', data=data)


@app.route('/proyectos', methods=['GET'])
def proyectos_all():
    """
    Proyectos: mostrar la información de todos los proyectos
    ----
    En esta rutina mostraremos la información de todos los proyectos
    """
    try:
        proyectos = Proyecto.query.all()
        proyectos = [proyecto.serialize() for proyecto in proyectos]
        success = True
    except:
        success = False

    data = {
        'title':                    "Proyectos",
        'breadcrumb_title':         "I+D y Producción",
        'breadcrumb_subtitle':      '<i class="fas fa-fw fa-lightbulb mr-2"></i>Proyectos',
        'breadcrumb_button':        '<i class="fas fa-fw fa-plus fa-sm text-white-50 mr-2"></i>Crear proyecto',
        'breadcrumb_button_url':    '/proyectos/add',
        'database_name':            'proyecto',
        'database_name_plural':     'proyectos',
        'card_title':               "Listado de proyectos",
        'error':                    f'No hemos podido obtener la información de los proyectos' if not success else None,
        'proyectos':                proyectos if success else None
    }
    return render_template('pages/proyectos_list.html', data=data)


@app.route('/proyectos/<id>', methods=['GET'])
def proyectos_detail(id):
    """
    Proyectos: mostrar información de un proyecto
    ----
    En esta rutina mostraremos la información de un proyecto
    """
    # primero recopilamos la información de la BD
    try:
        proyecto = Proyecto.query.filter_by(id=id).first()
        proyecto = proyecto.serialize()
    except:
        proyecto = None

    data = {
        'title':                    f"Proyecto #{id}",
        'breadcrumb_title':         "I+D y Producción",
        'breadcrumb_subtitle':      '<i class="fas fa-fw fa-lightbulb mr-2"></i>Proyectos',
        'breadcrumb_button':        '<i class="fas fa-fw fa-arrow-left fa-sm text-white-50 mr-2"></i>Volver a proyectos',
        'breadcrumb_button_url':    '/proyectos',
        'database_name':            'proyecto',
        'database_name_plural':     'proyectos',
        'card_title':               f"Detalle del proyecto #{id}",
        # Mostrar un mensaje de error si no existe el proyecto
        'error':                    f'No se ha encontrado un proyecto con ID {id}' if not proyecto else None,
        'proyecto':                 proyecto
    }
    return render_template('pages/proyectos_detail.html', data=data)


@app.route('/proyectos/<id>/edit', methods=['GET'])
def proyectos_edit(id):
    """
    Proyectos: editar información de un proyecto
    ----
    En esta rutina permitiremos la edición de la información de un proyecto
    """
    # primero recopilamos la información de la BD
    try:
        proyecto = Proyecto.query.filter_by(id=id).first()
        proyecto = proyecto.serialize()
    except:
        proyecto = None

    data = {
        'title':                    f"Editar proyecto #{id}",
        'breadcrumb_title':         "I+D y Producción",
        'breadcrumb_subtitle':      '<i class="fas fa-fw fa-lightbulb mr-2"></i>Proyectos',
        'breadcrumb_button':        '<i class="fas fa-fw fa-arrow-left fa-sm text-white-50 mr-2"></i>Volver a proyectos',
        'breadcrumb_button_url':    '/proyectos',
        'database_name':            'proyecto',
        'database_name_plural':     'proyectos',
        'card_title':               f"Editar proyecto #{id}",
        'error':                    f'No se ha encontrado un proyecto con ID {id}' if not proyecto else None,
        'edit':                     True,   # el formulario será de edición
        # cargamos la información existente en el formulario
        'edit_data':                proyecto
    }
    return render_template('pages/proyectos_form.html', data=data)


# ==== PRODUCTOS ====

@app.route('/productos/add', methods=['GET'])
def productos_add():
    data = {
        'title':                    "Añadir producto",
        'breadcrumb_title':         "I+D y Producción",
        'breadcrumb_subtitle':      '<i class="fas fa-fw fa-pills mr-2"></i>Productos',
        'breadcrumb_button':        '<i class="fas fa-fw fa-arrow-left fa-sm text-white-50 mr-2"></i>Volver a productos',
        'breadcrumb_button_url':    '/productos',
        'database_name':            'producto',
        'database_name_plural':     'productos',
        'card_title':               "Crear nuevo producto",
        'edit':                     False,  # el formulario será de creación
        # no son necesarios más datos en este caso
    }
    return render_template('pages/productos_form.html', data=data)


@app.route('/productos', methods=['GET'])
def productos_all():
    try:
        productos = Producto.query.all()
        productos = [producto.serialize() for producto in productos]
        success = True
    except:
        success = False

    data = {
        'title':                    "Productos",
        'breadcrumb_title':         "I+D y Producción",
        'breadcrumb_subtitle':      '<i class="fas fa-fw fa-pills mr-2"></i>Productos',
        'breadcrumb_button':        '<i class="fas fa-fw fa-plus fa-sm text-white-50 mr-2"></i>Crear producto',
        'breadcrumb_button_url':    '/productos/add',
        'database_name':            'producto',
        'database_name_plural':     'productos',
        'card_title':               "Listado de productos",
        'error':                    f'No hemos podido obtener la información de los productos' if not success else None,
        'productos':                productos if success else None
    }
    return render_template('pages/productos_list.html', data=data)


@app.route('/productos/<id>', methods=['GET'])
def productos_detail(id):
    # primero recopilamos la información de la BD
    try:
        producto = Producto.query.filter_by(id=id).first()
        producto = producto.serialize()
    except:
        producto = None

    data = {
        'title':                    f"Producto #{id}",
        'breadcrumb_title':         "I+D y Producción",
        'breadcrumb_subtitle':      '<i class="fas fa-fw fa-pills mr-2"></i>Productos',
        'breadcrumb_button':        '<i class="fas fa-fw fa-arrow-left fa-sm text-white-50 mr-2"></i>Volver a productos',
        'breadcrumb_button_url':    '/productos',
        'database_name':            'producto',
        'database_name_plural':     'productos',
        'card_title':               f"Detalle del producto #{id}",
        # Mostrar un mensaje de error si no existe el producto
        'error':                    f'No se ha encontrado un producto con ID {id}' if not producto else None,
        'producto':                 producto
    }

    print(data)
    return render_template('pages/productos_detail.html', data=data)


@app.route('/productos/<id>/edit', methods=['GET'])
def productos_edit(id):
    # primero recopilamos la información de la BD
    try:
        producto = Producto.query.filter_by(id=id).first()
        producto = producto.serialize()
    except:
        producto = None

    data = {
        'title':                    f"Editar producto #{id}",
        'breadcrumb_title':         "I+D y Producción",
        'breadcrumb_subtitle':      '<i class="fas fa-fw fa-pills mr-2"></i>Productos',
        'breadcrumb_button':        '<i class="fas fa-fw fa-arrow-left fa-sm text-white-50 mr-2"></i>Volver a productos',
        'breadcrumb_button_url':    '/productos',
        'database_name':            'producto',
        'database_name_plural':     'productos',
        'card_title':               f"Editar producto #{id}",
        'error':                    f'No se ha encontrado un producto con ID {id}' if not producto else None,
        'edit':                     True,   # el formulario será de edición
        # cargamos la información existente en el formulario
        'edit_data':            producto
    }
    return render_template('pages/productos_form.html', data=data)


# ==== PROCESOS PRODUCTIVOS ====

@app.route('/procesos-productivos/add', methods=['GET'])
def procesos_productivos_add():
    data = {
        'title':                    "Añadir proceso productivo",
        'breadcrumb_title':         "I+D y Producción",
        'breadcrumb_subtitle':      '<i class="fas fa-fw fa-dolly-flatbed mr-2"></i>Procesos productivos',
        'breadcrumb_button':        '<i class="fas fa-fw fa-arrow-left fa-sm text-white-50 mr-2"></i>Volver a procesos productivos',
        'breadcrumb_button_url':    '/procesos-productivos',
        'database_name':            'proceso-productivo',
        'database_name_plural':     'procesos-productivos',
        'card_title':               "Crear nuevo proceso productivo",
        'edit':                     False,  # el formulario será de creación
        # no son necesarios más datos en este caso
    }
    return render_template('pages/procesos_productivos_form.html', data=data)


@app.route('/procesos-productivos', methods=['GET'])
def procesos_productivos_all():
    try:
        procesos_productivos = ProcesoProductivo.query.all()
        procesos_productivos = [proceso_productivo.serialize(
        ) for proceso_productivo in procesos_productivos]
        success = True
    except:
        success = False

    data = {
        'title':                    "Procesos productivos",
        'breadcrumb_title':         "I+D y Producción",
        'breadcrumb_subtitle':      '<i class="fas fa-fw fa-dolly-flatbed mr-2"></i>Procesos productivos',
        'breadcrumb_button':        '<i class="fas fa-fw fa-plus fa-sm text-white-50 mr-2"></i>Crear proceso productivo',
        'breadcrumb_button_url':    '/procesos-productivos/add',
        'database_name':            'proceso-productivo',
        'database_name_plural':     'procesos-productivos',
        'card_title':               "Listado de procesos productivos",
        'error':                    f'No hemos podido obtener la información de los procesos productivos' if not success else None,
        'procesos_productivos':     procesos_productivos if success else None
    }
    return render_template('pages/procesos_productivos_list.html', data=data)


@app.route('/procesos-productivos/<id>', methods=['GET'])
def procesos_productivos_detail(id):
    # primero recopilamos la información de la BD
    try:
        proceso_productivo = ProcesoProductivo.query.filter_by(id=id).first()
        proceso_productivo = proceso_productivo.serialize()
    except:
        proceso_productivo = None

    data = {
        'title':                    f"Proceso productivo #{id}",
        'breadcrumb_title':         "I+D y Producción",
        'breadcrumb_subtitle':      '<i class="fas fa-fw fa-dolly-flatbed mr-2"></i>Procesos productivos',
        'breadcrumb_button':        '<i class="fas fa-fw fa-arrow-left fa-sm text-white-50 mr-2"></i>Volver a procesos productivos',
        'breadcrumb_button_url':    '/procesos-productivos',
        'database_name':            'proceso-productivo',
        'database_name_plural':     'procesos-productivos',
        'card_title':               f"Detalle del proceso productivo #{id}",
        # Mostrar un mensaje de error si no existe el proceso productivo
        'error':                    f'No se ha encontrado un proceso productivo con ID {id}' if not proceso_productivo else None,
        'proceso_productivo':       proceso_productivo
    }

    print(data)
    return render_template('pages/procesos_productivos_detail.html', data=data)


@app.route('/procesos-productivos/<id>/edit', methods=['GET'])
def procesos_productivos_edit(id):
    # primero recopilamos la información de la BD
    try:
        proceso_productivo = ProcesoProductivo.query.filter_by(id=id).first()
        proceso_productivo = proceso_productivo.serialize()
    except:
        proceso_productivo = None

    data = {
        'title':                    f"Editar proceso productivo #{id}",
        'breadcrumb_title':         "I+D y Producción",
        'breadcrumb_subtitle':      '<i class="fas fa-fw fa-dolly-flatbed mr-2"></i>Procesos productivos',
        'breadcrumb_button':        '<i class="fas fa-fw fa-arrow-left fa-sm text-white-50 mr-2"></i>Volver a procesos productivos',
        'breadcrumb_button_url':    '/procesos-productivos',
        'database_name':            'proceso-productivo',
        'database_name_plural':     'procesos-productivos',
        'card_title':               f"Editar proceso productivo #{id}",
        'error':                    f'No se ha encontrado un proceso productivo con ID {id}' if not proceso_productivo else None,
        'edit':                     True,   # el formulario será de edición
        # cargamos la información existente en el formulario
        'edit_data':                proceso_productivo
    }
    return render_template('pages/procesos_productivos_form.html', data=data)


#  __________________
# |                  |
# |  API             |
# |__________________|

# ================================
# ==== DPTO. RECURSOS HUMANOS ====
# ================================

# ==== EMPLEADOS ====

@app.route('/api/empleados/add', methods=['POST'])
def api_empleados_add():
    data = json.loads(request.form['data'])

    dni = data['dni']
    nombre = data['nombre']
    puesto = data['puesto']
    sueldo = data['sueldo']
    fechaInicio = data['fechaInicio']
    duracion = data['duracion']
    actividad = EmpleadoEstados(int(data['actividad']))

    valid, reason = Empleado.validate(dni, sueldo)

    response = {}

    if valid:
        try:
            empleado = Empleado(
                dni=dni,
                nombre=nombre,
                puesto=puesto,
                sueldo=sueldo,
                duracion=duracion,
                fechaInicio=fechaInicio,
                actividad=actividad
            )
            db.session.add(empleado)
            db.session.commit()
            response['category'] = 'success'
            response['message'] = f"Empleado añadido con DNI: {empleado.dni}"
            response['data'] = {
                'redirect': f"/empleados/{empleado.dni}"
            }
        except Exception as e:
            response['category'] = 'error'
            response['message'] = "Server insertion error: " + str(e)
    else:
        response['category'] = 'constraint'
        response['message'] = reason

    return jsonify(response)


@app.route('/api/empleados/edit/<dni>', methods=['POST'])
def api_empleados_edit(dni):
    data = json.loads(request.form['data'])
    nombre = data['nombre']
    puesto = data['puesto']
    sueldo = data['sueldo']
    fechaInicio = data['fechaInicio']
    duracion = data['duracion']
    actividad = EmpleadoEstados(int(data['actividad']))

    # server-side validation
    valid, reason = Empleado.validate(dni, sueldo)

    response = {}

    if valid:
        try:
            empleado = Empleado.query.filter_by(dni=dni).first()
            empleado.nombre = nombre
            empleado.puesto = puesto
            empleado.sueldo = sueldo
            empleado.fechaInicio = fechaInicio
            empleado.duracion = duracion
            empleado.actividad = actividad
            db.session.commit()
            response['category'] = 'success'
            response['message'] = f"Empleado actualizado con DNI: {empleado.dni}"
            response['data'] = {
                'redirect': f"/empleados/{empleado.dni}"
            }
        except Exception as e:
            response['category'] = 'error'
            response['message'] = "Server insertion error: " + str(e)
    else:
        response['category'] = 'constraint'
        response['message'] = reason

    return jsonify(response)


@app.route('/api/empleados/delete/<dni>', methods=['POST', 'GET'])
def api_empleado_delete(dni):
    response = {}

    try:
        empleado = Empleado.query.filter_by(dni=dni).first()
        db.session.delete(empleado)
        db.session.commit()
        response['category'] = 'success'
        response['message'] = f"Empleado eliminado con DNI: {empleado.dni}"
        response['data'] = {
            'redirect':     f"/empleados"
        }
    except Exception as e:
        response['category'] = 'error'
        response['message'] = "Server deletion error: " + str(e)

    return jsonify(response)


# ==== EMPLEADOS ====

@app.route('/api/evaluaciones/add', methods=['POST'])
def api_evaluaciones_add():
    data = json.loads(request.form['data'])
    nombre = data['nombre']
    dni = data['dni']
    fechaIni = data['fechaIni']
    fechaFin = data['fechaFin']
    conclusion = data['conclusion']
    index = data['index']

    valid, reason = Evaluacion.validate(dni, fechaIni,fechaFin,conclusion,index)

    response = {}
    if valid:
        try:
            evaluacion = Evaluacion(
                nombre=nombre,
                dni=dni,
                fechaIni=fechaIni,
                fechaFin=fechaFin,
                conclusion=conclusion,
                index=index

            )
            db.session.add(evaluacion)
            db.session.commit()
            response['category'] = 'success'
            response['message'] = f"Evaluación creada con ID: {evaluacion.id}"
            response['data'] = {
                'redirect':     f"/evaluaciones/{evaluacion.id}"
            }
        except Exception as e:
            response['category'] = 'error'
            response['message'] = "Server insertion error: " + str(e)
    else:
        response['category'] = 'constraint'
        response['message'] = reason

    return jsonify(response)


@app.route('/api/evaluaciones/edit/<id>', methods=['POST'])
def api_evaluaciones_edit(id):
    data = json.loads(request.form['data'])
    nombre = data['nombre']
    fechaIni = data['fechaIni']
    fechaFin = data['fechaFin']
    conclusion = data['conclusion']
    index = data['index']
    # WIP aquí no pillamos el DNI, pero bueno
    dni = Evaluacion.query.filter_by(id=id).first().dni

    response = {}

    valid, reason = Evaluacion.validate(dni,fechaIni,fechaFin,conclusion,index)

    if valid:
        try:
            evaluacion = Evaluacion.query.filter_by(id=id).first()
            evaluacion.nombre = nombre
            evaluacion.fechaIni = fechaIni
            evaluacion.fechaFin = fechaFin
            evaluacion.conclusion = conclusion
            evaluacion.index = index
            db.session.commit()
            response['category'] = 'success'
            response['message'] = f"Evaluación actualizada con ID: {evaluacion.id}"
            response['data'] = {
                'redirect':     f"/evaluaciones/{evaluacion.id}"
            }
        except Exception as e:
            response['category'] = 'error'
            response['message'] = "Server insertion error: " + str(e)
    else:
        response['category'] = 'constraint'
        response['message'] = reason

    return jsonify(response)


# ================================
# ==== DPTO. I+D Y PRODUCCIÓN ====
# ================================

# ==== PROYECTOS ====

@app.route('/api/proyectos/get/all')
def api_proyectos_get_all():
    try:
        proyectos = Proyecto.query.all()
        return jsonify([proyecto.serialize() for proyecto in proyectos])
    except Exception as e:
        return str(e)


@app.route('/api/proyectos/get/<id>', methods=['POST'])
def api_proyectos_get(id):
    try:
        proyecto = Proyecto.query.filter_by(id=id).first()
        return jsonify(proyecto.serialize())
    except Exception as e:
        return str(e)


@app.route('/api/proyectos/add', methods=['POST'])
def api_proyectos_add():
    # decodificar datos recibidos (en JSON)
    data = json.loads(request.form['data'])

    id = data['id']
    nombre = data['nombre']
    descripcion = data['descripcion']
    categoria = data['categoria']
    estado = ProyectoEstados(int(data['estado']))

    # server-side validation
    #   Aquí insertamos una validación que tenga que efectuarse en el
    #   lado del servidor, i.e., comprobar que un ID referencia a un
    #   objeto que existe en la BD, etc.
    valid = True

    response = {}
    response['category'] = 'constraint'

    # comprobaciones de restricciones semánticas
    response['message'] = "Le faltan campos: "
    if (id == ""):
        response['message'] += "debe introducir un ID, "
        valid = False
    if (nombre == ""):
        response['message'] += "debe introducir un nombre, "
        valid = False
    if (categoria == ""):
        response['message'] += "debe introducir una categoría, "
        valid = False

    # comprobaciones de restricciones en BD
    if valid:
        response['message'] = "No se puede insertar: "
        if (Proyecto.query.filter_by(id=id).count() > 0):
            response['message'] += "el identificador ya existe, "
            valid = False

    # eliminar la última coma
    response['message'] = response['message'][:-2] + "."

    if valid:
        try:
            proyecto = Proyecto(
                id=id,
                nombre=nombre,
                descripcion=descripcion,
                categoria=categoria,
                estado=estado
            )
            db.session.add(proyecto)
            db.session.commit()
            response['category'] = 'success'
            response['message'] = f"Proyecto añadido con ID: {proyecto.id}"
            response['data'] = {
                'redirect':     f"/proyectos/{proyecto.id}"
            }
        except Exception as e:
            response['category'] = 'error'
            response['message'] = "Server insertion error: " + str(e)

    return jsonify(response)


@app.route('/api/proyectos/edit/<id>', methods=['POST'])
def api_proyectos_edit(id):
    # decodificar datos recibidos (en JSON)
    data = json.loads(request.form['data'])

    nombre = data['nombre']
    descripcion = data['descripcion']
    categoria = data['categoria']
    estado = ProyectoEstados(int(data['estado']))

    valid = True

    response = {}
    response['category'] = 'constraint'

    # comprobaciones de restricciones semánticas
    response['message'] = "Le faltan campos: "
    if (id == ""):
        response['message'] += "debe introducir un ID, "
        valid = False
    if (nombre == ""):
        response['message'] += "debe introducir un nombre, "
        valid = False
    if (categoria == ""):
        response['message'] += "debe introducir una categoría, "
        valid = False

    # eliminar la última coma
    response['message'] = response['message'][:-2] + "."

    if valid:
        try:
            proyecto = Proyecto.query.filter_by(id=id).first()
            proyecto.nombre = nombre
            proyecto.descripcion = descripcion
            proyecto.categoria = categoria
            proyecto.estado = estado
            db.session.commit()
            response['category'] = 'success'
            response['message'] = f"Proyecto actualizado con ID: {proyecto.id}"
            response['data'] = {
                'redirect':     f"/proyectos/{proyecto.id}"
            }
        except Exception as e:
            response['category'] = 'error'
            response['message'] = "Server update error: " + str(e)

    return jsonify(response)


@app.route('/api/proyectos/delete/<id>', methods=['POST'])
def api_proyectos_delete(id):
    response = {}

    try:
        proyecto = Proyecto.query.filter_by(id=id).first()
        db.session.delete(proyecto)
        db.session.commit()
        response['category'] = 'success'
        response['message'] = f"Proyecto eliminado con ID: {proyecto.id}"
        response['data'] = {
            'redirect':     f"/proyectos"
        }
    except Exception as e:
        response['category'] = 'error'
        response['message'] = "Server deletion error: " + str(e)

    return jsonify(response)


# ===== PRODUCTOS =====

@app.route('/api/productos/add', methods=['POST'])
def api_productos_add():
    # decodificar datos recibidos (en JSON)
    data = json.loads(request.form['data'])

    id = data['id']
    nombre = data['nombre']
    descripcion = data['descripcion']
    cod_distribucion = data['cod_distribucion']
    precio_venta = float('0'+data['precio_venta'])
    origen = data['origen']

    # server-side validation
    #   Aquí insertamos una validación que tenga que efectuarse en el
    #   lado del servidor, i.e., comprobar que un ID referencia a un
    #   objeto que existe en la BD, etc.
    valid = True

    response = {}
    response['category'] = 'constraint'

    # comprobaciones de restricciones semánticas
    response['message'] = "Le faltan campos: "
    if (id == ""):
        response['message'] += "debe introducir un ID, "
        valid = False
    if (nombre == ""):
        response['message'] += "debe introducir un nombre, "
        valid = False
    if (cod_distribucion == ""):
        response['message'] += "debe introducir un código de distribución, "
        valid = False
    if (precio_venta <= 0):
        response['message'] += "debe introducir un precio de venta, "
        valid = False
    if (origen == ""):
        response['message'] += "debe introducir un ID de proyecto de origen, "

    # comprobaciones de restricciones en BD
    if valid:
        response['message'] = "No se puede insertar: "
        if (Producto.query.filter_by(id=id).count() > 0):
            response['message'] += "el identificador ya existe, "
            valid = False
        if (Proyecto.query.filter_by(id=origen).count() == 0):
            response['message'] += f"no existe ningún proyecto con ID #{origen}, "
            valid = False

    # eliminar la última coma
    response['message'] = response['message'][:-2] + "."

    if valid:
        try:
            producto = Producto(
                id=id,
                nombre=nombre,
                descripcion=descripcion,
                cod_distribucion=cod_distribucion,
                precio_venta=precio_venta,
                origen=origen
            )
            db.session.add(producto)
            db.session.commit()
            response['category'] = 'success'
            response['message'] = f"Producto añadido con ID: {producto.id}"
            response['data'] = {
                'redirect':     f"/productos/{producto.id}"
            }
        except Exception as e:
            response['category'] = 'error'
            response['message'] = "Server insertion error: " + str(e)

    return jsonify(response)


@app.route('/api/productos/edit/<id>', methods=['POST'])
def api_productos_edit(id):
    # decodificar datos recibidos (en JSON)
    data = json.loads(request.form['data'])

    nombre = data['nombre']
    descripcion = data['descripcion']
    cod_distribucion = data['cod_distribucion']
    precio_venta = float('0'+data['precio_venta'])

    valid = True

    response = {}
    response['category'] = 'constraint'

    # comprobaciones de restricciones semánticas
    response['message'] = "Le faltan campos: "
    if (nombre == ""):
        response['message'] += "debe introducir un nombre, "
        valid = False
    if (cod_distribucion == ""):
        response['message'] += "debe introducir un código de distribución, "
        valid = False
    if (precio_venta <= 0):
        response['message'] += "debe introducir un precio de venta, "
        valid = False

    # eliminar la última coma
    response['message'] = response['message'][:-2] + "."

    if valid:
        try:
            producto = Producto.query.filter_by(id=id).first()
            producto.nombre = nombre
            producto.descripcion = descripcion
            producto.cod_distribucion = cod_distribucion
            producto.precio_venta = precio_venta
            db.session.commit()
            response['category'] = 'success'
            response['message'] = f"Producto actualizado con ID: {producto.id}"
            response['data'] = {
                'redirect':     f"/productos/{producto.id}"
            }
        except Exception as e:
            response['category'] = 'error'
            response['message'] = "Server update error: " + str(e)

    return jsonify(response)


@app.route('/api/productos/delete/<id>', methods=['POST'])
def api_productos_delete(id):
    response = {}

    try:
        producto = Producto.query.filter_by(id=id).first()
        db.session.delete(producto)
        db.session.commit()
        response['category'] = 'success'
        response['message'] = f"Producto eliminado con ID: {producto.id}"
        response['data'] = {
            'redirect':     f"/productos"
        }
    except Exception as e:
        response['category'] = 'error'
        response['message'] = "Server deletion error: " + str(e)

    return jsonify(response)


# ==== PROCESOS PRODUCTIVOS ====

@app.route('/api/procesos-productivos/add', methods=['POST'])
def api_procesos_productivos_add():
    # decodificar datos recibidos (en JSON)
    data = json.loads(request.form['data'])

    id = data['id']
    nombre = data['nombre']
    descripcion = data['descripcion']
    fecha_inicio = data['fecha_inicio']
    fecha_fin = data['fecha_fin']
    ctd_producida = float('0'+data['ctd_producida'])
    fabrica = data['fabrica']

    # server-side validation
    #   Aquí insertamos una validación que tenga que efectuarse en el
    #   lado del servidor, i.e., comprobar que un ID referencia a un
    #   objeto que existe en la BD, etc.
    valid = True

    response = {}
    response['category'] = 'constraint'

    # comprobaciones de restricciones semánticas
    response['message'] = "Le faltan campos: "
    if (id == ""):
        response['message'] += "debe introducir un ID, "
        valid = False
    if (nombre == ""):
        response['message'] += "debe introducir un nombre, "
        valid = False
    if (fecha_inicio == ""):
        response['message'] += "debe introducir una fecha de inicio, "
        valid = False
    if (fecha_fin == ""):
        response['message'] += "debe introducir una fecha de fin, "
        valid = False
    if (ctd_producida <= 0):
        # si no introduce o introduce mal, se coloca a 0.0
        ctd_producida = 0.0
    if (fabrica == ""):
        response['message'] += "debe introducir el ID del producto que fabrica, "

    # compilamos las fechas para asignar
    try:
        y, m, d = fecha_inicio.split('-')
        fecha_inicio = datetime.datetime(int(y), int(m), int(d))
        y, m, d = fecha_fin.split('-')
        fecha_fin = datetime.datetime(int(y), int(m), int(d))
    except:
        response['message'] += "debe introducir las fechas siguiendo el formato adecuado, "
        valid = False

    # comprobaciones de restricciones en BD
    if valid:
        response['message'] = "No se puede insertar: "
        if (ProcesoProductivo.query.filter_by(id=id).count() > 0):
            response['message'] += "el identificador ya existe, "
            valid = False
        if (Producto.query.filter_by(id=fabrica).count() == 0):
            response['message'] += f"no existe ningún producto con ID #{origen}, "
            valid = False
        if (fecha_inicio > fecha_fin):
            response['message'] += "la fecha de inicio debe ser anterior o igual a la de fin, "
            valid = False

    # eliminar la última coma
    response['message'] = response['message'][:-2] + "."

    if valid:
        try:
            proceso_productivo = ProcesoProductivo(
                id=id,
                nombre=nombre,
                descripcion=descripcion,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                ctd_producida=ctd_producida,
                fabrica=fabrica
            )
            db.session.add(proceso_productivo)
            db.session.commit()
            response['category'] = 'success'
            response['message'] = f"Proceso productivo añadido con ID: {proceso_productivo.id}"
            response['data'] = {
                'redirect':     f"/procesos-productivos/{proceso_productivo.id}"
            }
        except Exception as e:
            response['category'] = 'error'
            response['message'] = "Server insertion error: " + str(e)

    return jsonify(response)


@app.route('/api/procesos-productivos/edit/<id>', methods=['POST'])
def api_procesos_productivos_edit(id):
    # decodificar datos recibidos (en JSON)
    data = json.loads(request.form['data'])

    print("============DATA:============",data)
    nombre = data['nombre']
    descripcion = data['descripcion']
    fecha_inicio = data['fecha_inicio']
    fecha_fin = data['fecha_fin']
    ctd_producida = float('0'+data['ctd_producida'])

    # server-side validation
    #   Aquí insertamos una validación que tenga que efectuarse en el
    #   lado del servidor, i.e., comprobar que un ID referencia a un
    #   objeto que existe en la BD, etc.
    valid = True

    response = {}
    response['category'] = 'constraint'

    # comprobaciones de restricciones semánticas
    response['message'] = "Le faltan campos: "
    if (nombre == ""):
        response['message'] += "debe introducir un nombre, "
        valid = False
    if (fecha_inicio == ""):
        response['message'] += "debe introducir una fecha de inicio, "
        valid = False
    if (fecha_fin == ""):
        response['message'] += "debe introducir una fecha de fin, "
        valid = False
    if (ctd_producida <= 0):
        # si no introduce o introduce mal, se coloca a 0.0
        ctd_producida = 0.0

    # compilamos las fechas para asignar
    try:
        y, m, d = fecha_inicio.split('-')
        fecha_inicio = datetime.datetime(int(y), int(m), int(d))
        y, m, d = fecha_fin.split('-')
        fecha_fin = datetime.datetime(int(y), int(m), int(d))
    except:
        response['message'] += "debe introducir las fechas siguiendo el formato adecuado, "
        valid = False

    # comprobaciones de restricciones en BD
    if valid:
        response['message'] = "No se puede insertar: "
        if (fecha_inicio > fecha_fin):
            response['message'] += "la fecha de inicio debe ser anterior o igual a la de fin, "
            valid = False

    # eliminar la última coma
    response['message'] = response['message'][:-2] + "."

    if valid:
        try:
            proceso_productivo = ProcesoProductivo.query.filter_by(
                id=id).first()
            proceso_productivo.nombre = nombre
            proceso_productivo.descripcion = descripcion
            proceso_productivo.fecha_inicio = fecha_inicio
            proceso_productivo.fecha_fin = fecha_fin
            proceso_productivo.ctd_producida = ctd_producida
            db.session.commit()
            response['category'] = 'success'
            response['message'] = f"Proceso productivo actualizado con ID: {proceso_productivo.id}"
            response['data'] = {
                'redirect':     f"/procesos-productivos/{proceso_productivo.id}"
            }
        except Exception as e:
            response['category'] = 'error'
            response['message'] = "Server update error: " + str(e)

    return jsonify(response)


@app.route('/api/procesos-productivos/delete/<id>', methods=['POST'])
def api_procesos_productivos_delete(id):
    response = {}

    try:
        proceso_productivo = ProcesoProductivo.query.filter_by(id=id).first()
        db.session.delete(proceso_productivo)
        db.session.commit()
        response['category'] = 'success'
        response['message'] = f"Proceso productivo eliminado con ID: {proceso_productivo.id}"
        response['data'] = {
            'redirect':     f"/procesos-productivos"
        }
    except Exception as e:
        response['category'] = 'error'
        response['message'] = "Server deletion error: " + str(e)

    return jsonify(response)



# ================================
# ==== DPTO. CONTABILIDAD ====
# ================================



#  __________________
# |                  |
# |  Templates       |
# |__________________|

@app.route('/nominas/add', methods=['GET'])
def nominas_add(api_resp=None):
    """
    Nóminas: añadir nomina
    ----
    En esta rutina mostraremos una página con un formulario para insertar una nueva nómina.
    """
    data = {
        'title':                    "Añadir nómina",
        'breadcrumb_title':         "Contabilidad",
        'breadcrumb_subtitle':      '<i class="fas fa-fw fa-user mr-2"></i>Nóminas',
        'breadcrumb_button':        '<i class="fas fa-fw fa-arrow-left fa-sm text-white-50 mr-2"></i>Volver a nóminas',
        'breadcrumb_button_url':    '/nominas',
        'database_name':            'nomina',
        'database_name_plural':     'nominas',
        'card_title':               "Crear nómina",
        'edit':                     False,  # el formulario será de creación
        # no son necesarios más datos en este caso
    }
    return render_template('nominas_form.html', data=data)

@app.route('/nominas', methods=['GET'])
def nomina_all():
    """
    Nóminas: mostrar la información de todas las nóminas
    ----
    En esta rutina mostraremos la información de todas las nóminas.
    """
    try:
        nominas = Nomina.query.all()
        nominas = [nomina.serialize() for nomina in nominas]
        success = True
    except:
        success = False

    data = {
        'title':                    "Nóminas",
        'breadcrumb_title':         "Contabilidad",
        'breadcrumb_subtitle':      '<i class="fas fa-fw fa-user mr-2"></i>Nóminas',
        'breadcrumb_button':        '<i class="fas fa-fw fa-plus fa-sm text-white-50 mr-2"></i>Añadir nómina',
        'breadcrumb_button_url':    '/nominas/add',
        'database_name':            'nomina',
        'database_name_plural':     'nominas',
        'card_title':               "Listado de nóminas",
        'error':                    f'No hemos podido obtener la información de las nóminas' if not success else None,
        'nominas':                  nominas if success else None
    }
    return render_template('nominas_all.html', data=data)



@app.route('/nominas/<DNI>/<fecha>/edit', methods=['GET'])
def nominas_edit(DNI, fecha, api_resp=None):
    """
    Nóminas: editar información de un nómina
    ----
    En esta rutina permitiremos la edición de la información de una nómina
    """
    # primero recopilamos la información de la BD
    try:
        nomina = Nomina.query.filter_by(DNI=DNI, fecha=fecha).first()
        exists = True   # la nómina existe
    except:
        exists = False  # la nómina no existe
    
    if not exists:
        error = f'No se ha encontrado la nómina del empleado {DNI} el {fecha}'
    elif api_resp:
        error = api_resp['msg']
    else:
        error = None
    
    data = {
        'title':                    f"Editar nómina",
        'breadcrumb_title':         "Contabilidad",
        'breadcrumb_subtitle':      '<i class="fas fa-fw fa-user mr-2"></i>Nóminas',
        'breadcrumb_button':        '<i class="fas fa-fw fa-arrow-left fa-sm text-white-50 mr-2"></i>Volver a nóminas',
        'breadcrumb_button_url':    '/nominas',
        'database_name':            'nomina',
        'database_name_plural':     'nominas',
        'card_title':               f"Editar empleado",
        'error':                    error,
        'edit':                     True,   # el formulario será de edición
        # cargamos la información existente en el formulario
        'edit_data':                nomina
    }

    return render_template('nominas_form.html', data=data)


@app.route('/nominas/<DNI>/<fecha>', methods=['GET'])
def nomina_detail(DNI, fecha):
    """
    Nóminas: mostrar información de una nómina
    ----
    En esta rutina mostraremos la información de una nómina
    """
    # primero recopilamos la información de la BD
    exists = False
    try:
        nomina = Nomina.query.filter_by(DNI=DNI, fecha=fecha).first()
        nomina = nomina.serialize()
    except:
        nomina = None

    if nomina: exists = True

    data = {
        # Mostrar un mensaje de error si no existe el nomina
        'error':    f'No se ha encontrado una nómina con DNI {DNI} y fecha {fecha}' if not exists else None,
        'nomina': nomina
    }
    return render_template('nominas_detail.html', data=data)


@app.route('/recibos/add', methods=['GET'])
def recibos_add(api_resp=None):
    """
    Recibo: añadir recibo
    ----
    En esta rutina mostraremos una página con un formulario para crear
    un nuevo recibo.
    """
    data = {
        'edit':     False,  # el formulario será de creación
        # no son necesarios más datos en este caso
        # si la API nos ha devuelto algún error
        'error':    api_resp['msg'] if api_resp else None
    }
    return render_template('recibos_form.html', data=data)

@app.route('/recibos/all', methods=['GET'])
def recibos_all():
    """
    Recibos: mostrar la información de todos los recibos
    ----
    En esta rutina mostraremos la información de todos los recibos
    """
    try:
        recibos = Recibo.query.all()
        recibos = [recibo.serialize() for recibo in recibos]
        success = True
    except:
        success = False
    
    data = {
        'error':        f'No hemos podido obtener la información de los recibos' if not success else None,
        'recibos':      recibos if success else None
    }
    return render_template('recibos_all.html', data=data)


@app.route('/facturas/add', methods=['GET'])
def facturas_add(api_resp=None):
    """
    Factura: añadir factura
    ----
    En esta rutina mostraremos una página con un formulario para crear
    una nuevo factura.
    """
    data = {
        'edit':     False,  # el formulario será de creación
        # no son necesarios más datos en este caso
        # si la API nos ha devuelto algún error
        'error':    api_resp['msg'] if api_resp else None
    }
    return render_template('facturas_form.html', data=data)

@app.route('/facturas/all', methods=['GET'])
def facturas_all():
    """
    Facturas: mostrar la información de todos las facturas
    ----
    En esta rutina mostraremos la información de todos las facturas
    """
    try:
        facturas = Factura.query.all()
        facturas = [factura.serialize() for factura in facturas]
        success = True
    except:
        success = False
    
    data = {
        'error':        f'No hemos podido obtener la información de las facturas' if not success else None,
        'facturas':      facturas if success else None
    }
    return render_template('facturas_all.html', data=data)


@app.route('/balancesCuentas/all', methods=['GET'])
def balanceCuentas_all():
    """
    Balances: mostrar la información de todos los balances
    ----
    En esta rutina mostraremos la información de todos los balances
    """
    try:
        balancesCuentas = BalanceCuentas.query.all()
        balancesCuentas = [balanceCuentas.serialize() for balanceCuentas in balancesCuentas]
        
        success = True
    except:
        success = False
    
    data = {
        'error':        f'No hemos podido obtener la información de los balances' if not success else None,
        'balancesCuentas':      balancesCuentas if success else None
    }
    return render_template('balancesCuentas_all.html', data=data)


#  __________________
# |                  |
# |  API             |
# |__________________|


@app.route('/api/nominas/add', methods=['POST'])
def api_nominas_add():

    IBAN = request.form['IBAN']
    fecha = request.form['fecha']
    sueldo = float(request.form['sueldo']
    DNI = request.form['DNI']


     
    qry = BalanceCuentas.query.order_by(BalanceCuentas.IdOp.desc()).first()

    IdOp = 0
    balance = -1*sueldo
    if qry != None:
        d = qry.serialize()
        IdOp = d['IdOp'] + 1
        balance = d['balance'] - sueldo
        

    valid = Nomina.validate(IBAN, fecha, sueldo, DNI)

    if valid:
        try:
            nomina=Nomina(
                IBAN		= IBAN,
                fecha	    = fecha,
                sueldo	    = sueldo,
                DNI		    = DNI,
                IdOp        = IdOp
            )
            balanceCuentas = BalanceCuentas(
                IdOp            = IdOp,
                balance         = balance,
                claseOp         = ClaseOperacion(2)
            )
            db.session.add(balanceCuentas)
            db.session.add(nomina)
            db.session.commit()
            category = 'success'
            msg = f"Nómina añadida con DNI: {nomina.DNI} Fecha: {nomina.fecha}"
        except Exception as e:
            category = 'error'
            msg = "Server insertion error: " + str(e)
    else:
        category = 'constraint'
        msg = f"Los datos introducidos no cumplen las restricciones."

    resp = {'msg': msg, 'category': category}

    # === WIP ===

    # NOTA: por ahora hacemos render_template, pero estoy viendo si
    #   hay alguna forma de eliminar el comportamiento por defecto de
    #   submit para mostrar el mensaje de error sin recargar (si alguien
    #   puede ayudarme lo agradecería jeje)
    
    # si se ha insertado bien, vamos a los datos
    if resp['category'] == 'success':
        return redirect(f'/nominas/all', code=302)
    # si no, volvemos a cargar la página con la información de error
    else:
        return nominas_add(api_resp=resp)

    # Realmente deberíamos hacer algo con make_response
    #   NO es una buena decisión de diseño retornar una plantilla en la API,
    #   la API debería retornar mensajes (en JSON, como en el resto)

@app.route('/api/nominas/get/all')
def api_nominas_get_all():
    try:
        nominas=Nomina.query.all()
        return jsonify([nomina.serialize() for nomina in nominas])
    except Exception as e:
        return str(e)

@app.route('/api/nominas/get/<DNI>/<fecha>', methods=['POST'])
def api_nominas_get(DNI, fecha):
    try:
        nomina=Nomina.query.filter_by(DNI=DNI, fecha=fecha).first()
        return jsonify(nomina.serialize())
    except Exception as e:
        return str(e)

# Aquí tampoco usamos make_response, aunque deberíamos
@app.route('/api/nominas/edit/<DNI>/<fecha>', methods=['POST'])
def api_nominas_edit(DNI, fecha):
    IBAN = request.form['IBAN']

    # server-side validation
    valid = True#categoria.startswith('TEST')

    if valid:
        try:
            nomina=Nomina.query.filter_by(DNI=DNI, fecha=fecha).first()
            nomina.IBAN = IBAN

            db.session.commit()
            category = 'success'
            msg = f"Proyecto modificado con DNI {nomina.DNI} y fecha {nomina.fecha}"
        except Exception as e:
            category = 'error'
            msg = "Server update error: " + str(e)
    else:
        category = 'constraint'
        msg = f"La categoría {categoria} no es válida"
    
    resp = {'msg': msg, 'category': category}

    if resp['category'] == 'success':
        return redirect(f'/nominas/{DNI}/{fecha}', code=302)
    else:
        return nominas_edit(DNI, fecha, api_resp=resp)

@app.route('/api/recibos/add', methods=['POST'])
def api_recibos_add():

    CIF_pro = request.form['CIF_pro']
    NumeroRegistro = int(request.form['NumeroRegistro'])
    FechaCom = request.form['FechaCom']
    ImporteCom = int(request.form['ImporteCom'])


     
    qry = BalanceCuentas.query.order_by(BalanceCuentas.IdOp.desc()).first()

    IdOp = 0
    balance = -1*ImporteCom
    if qry != None:
        d = qry.serialize()
        IdOp = d['IdOp'] + 1
        balance = d['balance'] - ImporteCom


    # server-side validation
    #   Aquí insertamos una validación que tenga que efectuarse en el
    #   lado del servidor, i.e., comprobar que un ID referencia a un
    #   objeto que existe en la BD, etc. Esto que aparece aquí es de
    #   prueba, para que veáis cómo implementarlo (lo eliminaré)
    valid = Recibo.validate(CIF_pro, NumeroRegistro, FechaCom, ImporteCom)

    if valid:
        try:
            recibo=Recibo(
                CIF_pro		    = CIF_pro,
                NumeroRegistro	= NumeroRegistro,
                FechaCom	    = FechaCom,
                ImporteCom		= ImporteCom,
                IdOp            = IdOp
            )
            balanceCuentas = BalanceCuentas(
                IdOp            = IdOp,
                balance         = balance,
                claseOp         = ClaseOperacion(0)
            )
            db.session.add(balanceCuentas)
            db.session.add(recibo)
            db.session.commit()
            category = 'success'
            msg = f"Recibo añadida con CIF: {recibo.CIF_pro} Número de registro: {recibo.NumeroRegistro}"
        except Exception as e:
            category = 'error'
            msg = "Server insertion error: " + str(e)
    else:
        category = 'constraint'
        msg = f"Los datos introducidos no cumplen las restricciones."

    resp = {'msg': msg, 'category': category}

    # === WIP ===

    # NOTA: por ahora hacemos render_template, pero estoy viendo si
    #   hay alguna forma de eliminar el comportamiento por defecto de
    #   submit para mostrar el mensaje de error sin recargar (si alguien
    #   puede ayudarme lo agradecería jeje)
    
    # si se ha insertado bien, vamos a los datos
    if resp['category'] == 'success':
        return redirect(f'/recibos/all', code=302)
    # si no, volvemos a cargar la página con la información de error
    else:
        return recibos_add(api_resp=resp)

    # Realmente deberíamos hacer algo con make_response
    #   NO es una buena decisión de diseño retornar una plantilla en la API,
    #   la API debería retornar mensajes (en JSON, como en el resto)


@app.route('/api/facturas/add', methods=['POST'])
def api_facturas_add():

    CIF_cli = request.form['CIF_cli']
    IDlote = int(request.form['IDlote'])
    FechaVen = request.form['FechaVen']
    ImporteVen = int(request.form['ImporteVen'])


     
    qry = BalanceCuentas.query.order_by(BalanceCuentas.IdOp.desc()).first()

    IdOp = 0
    balance = ImporteVen
    if qry != None:
        d = qry.serialize()
        IdOp = d['IdOp'] + 1
        balance = ImporteVen + d['balance']


    # server-side validation
    #   Aquí insertamos una validación que tenga que efectuarse en el
    #   lado del servidor, i.e., comprobar que un ID referencia a un
    #   objeto que existe en la BD, etc. Esto que aparece aquí es de
    #   prueba, para que veáis cómo implementarlo (lo eliminaré)
    valid = Factura.validate(CIF_cli, IDlote, FechaVen, ImporteVen)

    if valid:
        try:
            factura=Factura(
                CIF_cli		    = CIF_cli,
                IDlote	        = IDlote,
                FechaVen	    = FechaVen,
                ImporteVen		= ImporteVen,
                IdOp            = IdOp
            )
            balanceCuentas = BalanceCuentas(
                IdOp            = IdOp,
                balance         = balance,
                claseOp         = ClaseOperacion(1)

            )
            db.session.add(balanceCuentas)
            db.session.add(factura)
            db.session.commit()
            category = 'success'
            msg = f"Recibo añadida con CIF: {factura.CIF_pro} Número de registro: {factura.NumeroRegistro}"
        except Exception as e:
            category = 'error'
            msg = "Server insertion error: " + str(e)
    else:
        category = 'constraint'
        msg = f"Los datos introducidos no cumplen las restricciones."

    resp = {'msg': msg, 'category': category}

    # === WIP ===

    # NOTA: por ahora hacemos render_template, pero estoy viendo si
    #   hay alguna forma de eliminar el comportamiento por defecto de
    #   submit para mostrar el mensaje de error sin recargar (si alguien
    #   puede ayudarme lo agradecería jeje)
    
    # si se ha insertado bien, vamos a los datos
    if resp['category'] == 'success':
        return redirect(f'/facturas/all', code=302)
    # si no, volvemos a cargar la página con la información de error
    else:
        return facturas_add(api_resp=resp)

    # Realmente deberíamos hacer algo con make_response
    #   NO es una buena decisión de diseño retornar una plantilla en la API,
    #   la API debería retornar mensajes (en JSON, como en el resto)



if __name__ == '__main__':
    app.run()
