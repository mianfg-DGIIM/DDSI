import os, json
from flask import Flask, request, jsonify, render_template, redirect, make_response
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config.from_object("config.DevelopmentConfig")  # os.environ['APP_SETTINGS']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *


@app.route('/')
def hello():
    return "Esta es la página principal"

#  __________________
# |                  |
# |  Templates       |
# |__________________|

@app.route('/proyectos/add', methods=['GET'])
def proyectos_add(api_resp=None):
    """
    Proyectos: añadir proyecto
    ----
    En esta rutina mostraremos una página con un formulario para crear
    un nuevo proyecto.
    """
    data = {
        'edit':     False,  # el formulario será de creación
        # no son necesarios más datos en este caso
        # si la API nos ha devuelto algún error
        'error':    api_resp['msg'] if api_resp else None
    }
    return render_template('proyectos_form.html', data=data)

@app.route('/proyectos/all', methods=['GET'])
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
        'error':        f'No hemos podido obtener la información de los proyectos' if not success else None,
        'proyectos':    proyectos if success else None
    }
    return render_template('proyectos_all.html', data=data)

@app.route('/proyectos/<id>', methods=['GET'])
def proyectos_detail(id):
    """
    Proyectos: mostrar información de un proyecto
    ----
    En esta rutina mostraremos la información de un proyecto
    """
    # primero recopilamos la información de la BD
    exists = False
    try:
        proyecto = Proyecto.query.filter_by(id=id).first()
        proyecto = proyecto.serialize()
    except:
        proyecto = None

    if proyecto: exists = True

    data = {
        # Mostrar un mensaje de error si no existe el proyecto
        'error':    f'No se ha encontrado un proyecto con ID {id}' if not exists else None,
        'proyecto': proyecto
    }
    return render_template('proyectos_detail.html', data=data)

@app.route('/proyectos/<id>/edit', methods=['GET'])
def proyectos_edit(id, api_resp=None):
    """
    Proyectos: editar información de un proyecto
    ----
    En esta rutina permitiremos la edición de la información de un proyecto
    """
    # primero recopilamos la información de la BD
    try:
        proyecto = Proyecto.query.filter_by(id=id).first()
        exists = True   # el proyecto existe
    except:
        exists = False  # el proyecto no existe
    
    if not exists:
        error = f'No se ha encontrado un proyecto con ID {id}'
    elif api_resp:
        error = api_resp['msg']
    else:
        error = None
    
    data = {
        'error':        error,
        'edit':         True,   # el formulario será de edición
        # cargamos la información existente en el formulario
        'edit_data':    proyecto.serialize(),
        'api_resp':     api_resp    # si la página la carga la API (WIP)
    }
    return render_template('proyectos_form.html', data=data)

#  __________________
# |                  |
# |  API             |
# |__________________|

@app.route('/api/test', methods=['POST'])
def api_test():
    print(request)

    return jsonify({'code': 200, 'message': 'testing'})

@app.route('/api/proyectos/add', methods=['POST'])
def api_proyectos_add():
    # decodificar datos recibidos (en JSON)
    data = json.loads(request.form['data'])
    
    nombre		= data['nombre']
    descripcion	= data['descripcion']
    categoria	= data['categoria']
    estado		= ProyectoEstados(int(data['estado']))

    # server-side validation
    #   Aquí insertamos una validación que tenga que efectuarse en el
    #   lado del servidor, i.e., comprobar que un ID referencia a un
    #   objeto que existe en la BD, etc. Esto que aparece aquí es de
    #   prueba, para que veáis cómo implementarlo (lo eliminaré)
    valid = categoria.startswith('TEST')

    response = {}

    if valid:
        try:
            proyecto=Proyecto(
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
    else:
        response['category'] = 'constraint'
        response['message'] = f"La categoría {categoria} no empieza por TEST (para pruebas)"

    return jsonify(response)

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

@app.route('/api/proyectos/edit/<id>', methods=['POST'])
def api_proyectos_edit(id):
    # decodificar datos recibidos (en JSON)
    data = json.loads(request.form['data'])
    
    nombre		= data['nombre']
    descripcion	= data['descripcion']
    categoria	= data['categoria']
    estado		= ProyectoEstados(int(data['estado']))

    # server-side validation
    valid = categoria.startswith('TEST')

    response = {}

    if valid:
        try:
            proyecto=Proyecto(
                nombre		= nombre,
                descripcion	= descripcion,
                categoria	= categoria,
                estado		= estado
            )
            db.session.add(proyecto)
            db.session.commit()
            response['category'] = 'success'
            response['message'] = f"Proyecto actualizado con ID: {proyecto.id}"
            response['data'] = {
                'redirect':     f"/proyectos/{proyecto.id}"
            }
        except Exception as e:
            response['category'] = 'error'
            response['message'] = "Server insertion error: " + str(e)
    else:
        response['category'] = 'constraint'
        response['message'] = f"La categoría {categoria} no empieza por TEST (para pruebas)"

    return jsonify(response)


if __name__ == '__main__':
    app.run()
