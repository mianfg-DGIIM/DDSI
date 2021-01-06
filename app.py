import os, json, datetime
from flask import Flask, request, jsonify, render_template, redirect, make_response
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config.from_object("config.DevelopmentConfig")  # os.environ['APP_SETTINGS']
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
        'breadcrumb_button':        '<i class="fas fa-info-circle fa-sm text-white-50 mr-2"></i>Sobre el proyecto',
        'breadcrumb_button_url':    '#'
    }
    return render_template('pages/home.html', data=data)

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
        'breadcrumb_subtitle':      '<i class="fas fa-lightbulb mr-2"></i>Proyectos',
        'breadcrumb_button':        '<i class="fas fa-arrow-left fa-sm text-white-50 mr-2"></i>Volver a proyectos',
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
        'breadcrumb_subtitle':      '<i class="fas fa-lightbulb mr-2"></i>Proyectos',
        'breadcrumb_button':        '<i class="fas fa-plus fa-sm text-white-50 mr-2"></i>Crear proyecto',
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
        'breadcrumb_subtitle':      '<i class="fas fa-lightbulb mr-2"></i>Proyectos',
        'breadcrumb_button':        '<i class="fas fa-arrow-left fa-sm text-white-50 mr-2"></i>Volver a proyectos',
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
        'breadcrumb_subtitle':      '<i class="fas fa-lightbulb mr-2"></i>Proyectos',
        'breadcrumb_button':        '<i class="fas fa-arrow-left fa-sm text-white-50 mr-2"></i>Volver a proyectos',
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
        'breadcrumb_subtitle':      '<i class="fas fa-pills mr-2"></i>Productos',
        'breadcrumb_button':        '<i class="fas fa-arrow-left fa-sm text-white-50 mr-2"></i>Volver a productos',
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
        'breadcrumb_subtitle':      '<i class="fas fa-pills mr-2"></i>Productos',
        'breadcrumb_button':        '<i class="fas fa-plus fa-sm text-white-50 mr-2"></i>Crear producto',
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
        'breadcrumb_subtitle':      '<i class="fas fa-pills mr-2"></i>Productos',
        'breadcrumb_button':        '<i class="fas fa-arrow-left fa-sm text-white-50 mr-2"></i>Volver a productos',
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
        'breadcrumb_subtitle':      '<i class="fas fa-pills mr-2"></i>Productos',
        'breadcrumb_button':        '<i class="fas fa-arrow-left fa-sm text-white-50 mr-2"></i>Volver a productos',
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
        'breadcrumb_subtitle':      '<i class="fas fa-dolly-flatbed mr-2"></i>Procesos productivos',
        'breadcrumb_button':        '<i class="fas fa-arrow-left fa-sm text-white-50 mr-2"></i>Volver a productos',
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
        procesos_productivos = [proceso_productivo.serialize() for proceso_productivo in procesos_productivos]
        success = True
    except:
        success = False
    
    data = {
        'title':                    "Procesos productivos",
        'breadcrumb_title':         "I+D y Producción",
        'breadcrumb_subtitle':      '<i class="fas fa-dolly-flatbed mr-2"></i>Procesos productivos',
        'breadcrumb_button':        '<i class="fas fa-plus fa-sm text-white-50 mr-2"></i>Crear proceso productivo',
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
        'breadcrumb_subtitle':      '<i class="fas fa-dolly-flatbed mr-2"></i>Procesos productivos',
        'breadcrumb_button':        '<i class="fas fa-arrow-left fa-sm text-white-50 mr-2"></i>Volver a procesos productivos',
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
        'breadcrumb_subtitle':      '<i class="fas fa-dolly-flatbed mr-2"></i>Procesos productivos',
        'breadcrumb_button':        '<i class="fas fa-arrow-left fa-sm text-white-50 mr-2"></i>Volver a procesos productivos',
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

# ==== PROYECTOS ====

@app.route('/api/proyectos/get/all')
def api_proyectos_get_all():
    try:
        proyectos=Proyecto.query.all()
        return jsonify([proyecto.serialize() for proyecto in proyectos])
    except Exception as e:
        return str(e)

@app.route('/api/proyectos/get/<id>', methods=['POST'])
def api_proyectos_get(id):
    try:
        proyecto=Proyecto.query.filter_by(id=id).first()
        return jsonify(proyecto.serialize())
    except Exception as e:
        return str(e)

@app.route('/api/proyectos/add', methods=['POST'])
def api_proyectos_add():
    # decodificar datos recibidos (en JSON)
    data = json.loads(request.form['data'])
    
    id          = data['id']
    nombre		= data['nombre']
    descripcion	= data['descripcion']
    categoria	= data['categoria']
    estado		= ProyectoEstados(int(data['estado']))

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
                id          = id,
                nombre		= nombre,
                descripcion	= descripcion,
                categoria	= categoria,
                estado		= estado
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
    
    nombre		= data['nombre']
    descripcion	= data['descripcion']
    categoria	= data['categoria']
    estado		= ProyectoEstados(int(data['estado']))

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
            proyecto.nombre         = nombre
            proyecto.descripcion    = descripcion
            proyecto.categoria      = categoria
            proyecto.estado         = estado
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
    
    id                  = data['id']
    nombre              = data['nombre']
    descripcion         = data['descripcion']
    cod_distribucion	= data['cod_distribucion']
    precio_venta		= float('0'+data['precio_venta'])
    origen              = data['origen']

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
                id                  = id,
                nombre              = nombre,
                descripcion         = descripcion,
                cod_distribucion	= cod_distribucion,
                precio_venta		= precio_venta,
                origen              = origen
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
    
    nombre              = data['nombre']
    descripcion         = data['descripcion']
    cod_distribucion	= data['cod_distribucion']
    precio_venta		= float('0'+data['precio_venta'])

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
            producto.nombre             = nombre
            producto.descripcion        = descripcion
            producto.cod_distribucion   = cod_distribucion
            producto.precio_venta       = precio_venta
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
    
    id              = data['id']
    nombre          = data['nombre']
    descripcion     = data['descripcion']
    fecha_inicio	= data['fecha_inicio']
    fecha_fin		= data['fecha_fin']
    ctd_producida   = float('0'+data['ctd_producida'])
    fabrica         = data['fabrica']

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
        d, m, y = fecha_inicio.split('/')
        fecha_inicio = datetime.datetime(int(y), int(m), int(d))
        d, m, y = fecha_fin.split('/')
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
                id              = id,
                nombre          = nombre,
                descripcion     = descripcion,
                fecha_inicio	= fecha_inicio,
                fecha_fin		= fecha_fin,
                ctd_producida   = ctd_producida,
                fabrica         = fabrica
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
    
    nombre          = data['nombre']
    descripcion     = data['descripcion']
    fecha_inicio	= data['fecha_inicio']
    fecha_fin		= data['fecha_fin']
    ctd_producida   = float('0'+data['ctd_producida'])

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
        d, m, y = fecha_inicio.split('/')
        fecha_inicio = datetime.datetime(int(y), int(m), int(d))
        d, m, y = fecha_fin.split('/')
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
            proceso_productivo = ProcesoProductivo.query.filter_by(id=id).first()
            proceso_productivo.nombre           = nombre
            proceso_productivo.descripcion      = descripcion
            proceso_productivo.fecha_inicio     = fecha_inicio
            proceso_productivo.fecha_fin        = fecha_fin
            proceso_productivo.ctd_producida    = ctd_producida
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


if __name__ == '__main__':
    app.run()
