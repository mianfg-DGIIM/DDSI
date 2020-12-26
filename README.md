# PharmaGIIM

## Configuración en local

### 1. Backend

Conceptos clave que usará nuestro pseudo-ERP:

* **ORM (object-relational mapping):** es una forma OO (object-oriented) de trabajar con BD. Trabajamos con cada tabla como si se tratara de una clase. Más información [aquí](https://blog.bitsrc.io/what-is-an-orm-and-why-you-should-use-it-b2b6f75f5e2a).
* **Servicio Restful:** arquitectura que se basa en el uso de peticiones HTTP para ver y modificar información (GET, PUT, POST, DELETE). Más información [aquí](https://es.wikipedia.org/wiki/Transferencia_de_Estado_Representacional).

Vamos a usar:

* **PostgreSQL** como base de datos.
* **Flask** como servidor.
* **SQLAlchemy** para ORM.
  * **Alembic** para correr migraciones.

#### 1.0 TL;DR

Puedes correr directamente todo esto haciendo:

1. Clonar repositorio `mianfg/pharmagiim`:

   ```
   git clone git@github.com:mianfg/pharmagiim.git
   ```

2. Instalar PostgreSQL y crear usuario y BD: _ver apartado 1.1_.

3. Crear entorno virtual e instalar todas las dependencias:

   ```
   cd pharmagiim
   virtualenv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

   > Si no tienes `virtualenv`, instálalo:
   >
   > ```
   > pip install virtualenv
   > ```

4. Migrar base de datos:

   ```
   python manage.py db init
   python manage.py db migrate
   python manage.py db upgrade
   ```

   **Qué es una migración**
   
   Una migración es una forma de modificar la estructura de las tablas de la BD. Cada vez que insertamos, modificamos o eliminamos datos NO hay que hacer una migración, simplemente hay que hacerlo cada vez que modifiquemos las columnas de las tablas, creemos tablas, etc. En caso de modificar las tablas, debemos migrar para que el router de SQLAlchemy sepa qué hacer. En ese caso, sólo ejecutamos:
   
   ```
   python manage.py db migrate
   python manage.py db upgrade
   ```

5. Correr servidor

   ```
   python manage.py runserver
   ```

----

#### 1.1. PostgreSQL

Instalación:

```
sudo apt-get install postgresql postgresql-contrib
```

----

Configurar contraseña usuario `postgres`:

```
sudo passwd postgres
```

> Podemos ponerle `postgres`.
>
> **NOTA:** esta es una práctica **HORRIBLE**, en Internet hay miles de bots probando las combinaciones `postgres`/`postgres` para usuario/contraseña. NUNCA deberíamos hacer algo así en producción (de hecho, lo mejor sería montar otro usuario diferente para la base de datos, pero no lo vamos a hacer por simplicidad).

---

Modificamos la contraseña en la BD:

```
sudo -u postgres psql postgres
postgres=## \password postgres
Enter new password: ...
```

> Ponemos `postgres` también.

---

Creamos BD:

```
postgres=## create database <nombre_bd>;
postgres=## exit;
```

> Por ejemplo, la llamaremos `pharmagiim`.

---

Acceder a la BD:

```
psql -U postgres -d <nombre_bd>
```

---

#### 1.2 Entorno virtual de Python para Flask

Instalamos `virtualenv`. Debemos de tener disponible el gestor de paquetes de Python, `pip`. Es **MUY IMPORTANTE** que `pip` sea `pip3`, es decir, que sea el gestor de paquetes de `python3`. En toda la práctica vamos a usar `python3`.

```
pip install virtualenv
```

----

Creamos un directorio para la aplicación:

```
mkdir pharmagim; cd pharmagim
```

----

En este directorio, creamos el entorno virtual:

```
virtualenv env
```

----

Activamos el entorno virtual:

```
source env/bin/activate
```

---

instalamos todas las dependencias necesarias:

```
pip install -r requirements.txt
```

---

#### 1.3 Arrancar Flask

##### 1.3.1 Entornos de desarrollo

Creamos un archivo `config.py`:

```python
import os
basedir = os.path.abspath(os.path.dirname(__file__))

POSTGRES_USER   = 'postgres'
POSTGRES_PW     = 'postgres'
POSTGRES_URL    = 'localhost'
POSTGRES_DB     = 'pharmagiim'

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '83IO4HG1O5GH245H158H134G384TGH'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB) # os.environ['SQLALCHEMY_DATABASE_URI']
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
```

----

#### 1.3.2 Migración BD

Necesitaremos el paquete `flask_sqlalchemy` (ya lo hemos instalado, no hace falta esto):

```
pip install flask_sqlalchemy
```

----

Creamos el script que correrá Flask: `app.py`

```python
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *


@app.route("/")
def hello():
    return "Esta es la página principal"
```

----

Creamos el script para definir los modelos de la BD: `models.py`

```python
from app import db
import enum


class ProyectoEstados(enum.Enum):    
    INICIAL		= 0
    EN_PROCESO	= 1
    EN_PAUSA	= 2
    FINALIZADO	= 3
    FRACASO		= 4

    def __str__(self):
        keys = {
            0: "Inicial",
            1: "En proceso",
            2: "En pausa",
            3: "Finalizado",
            4: "Fracaso"
        }
        
        return keys[self.value]


class Proyecto(db.Model):
    __tablename__ = 'proyectos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String())
    descripcion = db.Column(db.String())
    categoria = db.Column(db.String())
    estado = db.Column(db.Enum(ProyectoEstados))

    def __init__(self, nombre, descripcion, categoria, estado):
        self.nombre = nombre
        self.descripcion = descripcion
        self.categoria = categoria
        self.estado = estado

    def __repr__(self):
        return f'<Proyecto {self.id} - {self.nombre}>'

    def serialize(self):
        return {
            'id':			self.id,
            'nombre':		self.nombre,
            'descripcion':	self.descripcion,
            'categoria':	self.categoria,
            'estado':		{
                'value':    self.estado.value,
                'verbose':  str(self.estado)
            }
        }
```

---

Creamos `manage.py`, que usará tres paquetes más (de nuevo, ya instalados):

```
pip install flask_script flask_migrate psycopg2-binary
```

---

Ahora sí, escribimos `manage.py`:

```python
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
```

----

Migramos la BD:

```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

* `init`: crea el entorno de migraciones.
* `migrate`: crea las migraciones.
* `upgrade`: aplica las migraciones.

> Ahora se ha creado la tabla en la BD.

---

##### 1.3.3 Funcionalidades básicas

Cambiaremos `app.py` por:

```python
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Proyecto


@app.route('/')
def hello():
    return "Hello World!"

@app.route('/proyectos/add')
def add_proyecto():
    nombre		= request.args.get('nombre')
    descripcion	= request.args.get('descripcion')
    categoria	= request.args.get('categoria')
    estado		= request.args.get('estado')
    
    try:
        proyecto=Proyecto(
        	nombre		= nombre,
            descripcion	= descripcion,
            categoria	= categoria,
            estado		= estado
        )
        db.session.add(proyecto)
        db.session.commit()
        return f"Proyecto añadido con ID: {proyecto.id}"
    except Exception as e:
        return str(e)

@app.route('/proyectos/get/all')
def get_proyectos_all():
    try:
        proyectos=Proyectos.query.all()
        return jsonify([proyecto.serialize() for proyecto in proyectos])
    except Exception as e:
        return str(e)
    
@app.route('/proyectos/get/<id>')
def get_proyectos_by_id(id):
    try:
        proyecto=Proyectos.query.filter_by(id=id).first()
        return jsonify(proyecto.serialize())
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run()
```

----

Ya tenemos el back listo para correr:

```
python manage.py runserver
```

----

Probamos a entrar en:

* /proyectos/add?nombre=&descripcion=....
* /proyectos/get/all
* /proyectos/get/1

----

### 2. Frontend

Tenemos nuestra API REST. Ahora basta hacer el front. Crearemos tres interfaces:

1. Mostrar todos los proyectos.
2. Mostrar detalle de un proyecto.
3. Añadir proyecto.

Usaremos:

* **Bootstrap** para agilizar el diseño. Usaremos la plantilla base.
* **JQuery** para toquetear el DOM.
* **AJAX** para la comunicación con el servidor.
* **Javascript**: evidentemente jeje (lo usan tanto JQuery como AJAX).

> NOTA: aquí vamos a modificar un poco también el back, para trabajar mejor con AJAX. Veréis perfectamente cómo funciona un servicio REST.

#### 2.1. Flask templates

> **NOTA:** todavía no he implementado los bloques, por ahora vamos a trabajar con archivos que se renderizan por completo.

Los _templates_ son archivos HTML que Flask mostrará cuando le digamos. Algunas de las funcionalidades más potentes de estas _templates_ son:

* **Bloques:** podemos meter templates en templates, y hacer una estructura no repetitiva y jerárquica de archivos HTML. Por ejemplo:

  * La estrucutra básica de un archivo HTML siempre es la misma: la meteremos en `base.html`.
  * La cabecera (no nos referimos a `head`) siempre será la misma: la meteremos en `head.html`.

* **LIQUID:** son unas etiquetas y pipes que podemos usar para meter cosas en nuestras _templates_ (lo veremos más adelante).

  > La documentación de Liquid la tenéis [aquí](https://shopify.github.io/liquid/).

Fijaos en la carpeta `templates` del directorio raíz. Hemos importado ya Bootstrap y jQuery en `base.html`. Fijaos también que hemos hecho tres _templates_ para proyectos:

* `proyectos_all.html`: mostrar todos los proyectos.
* `proyectos_detail.html`: mostrar la información de un proyecto en concreto.
* `proyectos_form.html`: formulario para proyecto (lo usaremos para crear y modificar).

Fijaos también en cómo usamos las etiquetas LIQUID (son aquellas que tienen la estructura `{% ... %}` para bloques de código, como `if`, `for`, etc. y aquellas del tipo `{{ ... }}`, que son las que sirven para "imprimir" variables en el código).

Estos datos corresponden a los `dicts` pasados al parámetro `data` de `render_template`.

#### 2.2. Formularios

Para esto, lo mejor es que veáis el código, ya que he intentado comentarlo todo en su sitio. Ved el archivo `app.py` y los distintos _templates_ en `templates/*`. Fijaros especialmente en:

* En las _templates_, hacemos una llamada POST a distintas direcciones de nuestra app, donde se pasan automáticamente los campos del formulario. Estos corresponden a lo que está dentro de la etiqueta `form`.

#### 2.3. Bootstrap

Finalmente, veréis que el HTML hace uso de **Bootstrap**. Bootstrap contiene una serie de estilos predefinidos, y clases (que en HTML se añade a cualquier etiqueta con el parámetro `class`) que nos permiten modificar cómo se ven los objetos. Por ejemplo, si un `div` tiene las clases:

```
class="text-right mb-4"
```

Viendo la documentación de Bootstrap podemos ver que:

* `text-right` nos alinea el texto a la derecha.
* `mb-4` asigna al margen inferior (`margin-bottom` en CSS) un tamaño `4` (hay desde `1` hasta `5`).
