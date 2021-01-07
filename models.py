from app import db
from sqlalchemy.orm import relationship
import enum


# ================================
# ==== DPTO. RECURSOS HUMANOS ====
# ================================

class EmpleadoEstados(enum.Enum):
    ACTIVO      = 1
    INACTIVO    = 0

    def __str__(self):
        keys = {
            1: "Activo",
            0: "Inactivo"
        }

        return keys[self.value]


class Evaluacion(db.Model):
    __tablename__ = 'evaluaciones'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String())
    dni = db.Column(db.String(), db.ForeignKey('empleados.dni'), nullable=False)
    fechaIni = db.Column(db.String())
    fechaFin = db.Column(db.String())
    conclusion = db.Column(db.String())
    index = db.Column(db.Integer)

    def __init__(self, nombre, dni, fechaIni, fechaFin, conclusion, index):
        self.nombre     = nombre
        self.dni        = dni
        self.fechaIni   = fechaIni
        self.fechaFin   = fechaFin
        self.conclusion = conclusion
        self.index      = index

    def __repr__(self):
        return f'<Eval {self.id} - {self.dni}>'

    def serialize(self):
        return {
            'id':			self.id,
            'nombre':		self.nombre,
            'dni':          self.dni,
            'fechaIni':	    self.fechaIni,
            'fechaFin':	    self.fechaFin,
            'conclusion':   self.conclusion,
            'index':        self.index
        }

    @classmethod
    def validate(self, dni, fechaIni, fechaFin, conclusion, index):
        good_dni = Empleado.query.filter_by(dni=dni).first()
        print(Empleado.query.filter_by(dni=dni).first(), dni)
        if(fechaFin):
            good_date = fechaIni < fechaFin
        else:
            good_date = true
        good_index = int(index) >= 0 and int(index) <= 10

        reason = "none"
        if not good_dni:
            reason = "No existe un empleado con ese dni"
        if not good_date:
            reason = "Fecha incoherente"
        if not good_index:
            reason = "Índice fuera de rango"

        return good_date and good_index and good_dni, reason


class Empleado(db.Model):
    __tablename__ = 'empleados'

    dni = db.Column(db.String(), primary_key=True)
    nombre = db.Column(db.String())
    puesto = db.Column(db.String())
    sueldo = db.Column(db.String())
    duracion = db.Column(db.String())
    fechaInicio = db.Column(db.String())
    actividad = db.Column(db.Enum(EmpleadoEstados))

    evaluaciones = relationship(
        Evaluacion, cascade="all,delete", backref="empleado")

    def __init__(self, dni, nombre, puesto, sueldo, duracion, fechaInicio, actividad):
        self.dni = dni
        self.nombre = nombre
        self.puesto = puesto
        self.sueldo = sueldo
        self.duracion = duracion
        self.fechaInicio = fechaInicio
        self.actividad = actividad

    def __repr__(self):
        return f'<Empleado {self.dni} - {self.nombre}>'

    def serialize(self):
        return {
            'dni':			self.dni,
            'nombre':		self.nombre,
            'puesto':	    self.puesto,
            'sueldo':       self.sueldo,
            'duracion':	    self.duracion,
            'fechaInicio':  self.fechaInicio,
            'actividad':		{
                'value':    self.actividad.value,
                'verbose':  str(self.actividad)
            }
        }

    @classmethod
    def validate(self, dni, sueldo):
        good_name = Empleado.query.filter_by(dni=dni)
        good_money = int(sueldo) >= 0
        reason = "none"
        if not good_name:
            reason = "Ya existe un empleado con ese DNI"
        if not good_money:
            reason = "El sueldo no puede ser negativo"

        return (good_name and good_money), reason


# ================================
# ==== DPTO. I+D Y PRODUCCIÓN ====
# ================================

class ProyectoEstados(enum.Enum):
    INICIAL = 0
    EN_PROCESO = 1
    EN_PAUSA = 2
    FINALIZADO = 3
    FRACASO = 4

    def __str__(self):
        keys = {
            0: "Inicial",
            1: "En proceso",
            2: "En pausa",
            3: "Finalizado",
            4: "Fracaso"
        }

        return keys[self.value]


class ProcesoProductivo(db.Model):
    __tablename__ = 'proceso_productivo'

    id = db.Column(db.String(), primary_key=True)
    nombre = db.Column(db.String())
    descripcion = db.Column(db.String())
    fecha_inicio = db.Column(db.Date())
    fecha_fin = db.Column(db.Date())
    ctd_producida = db.Column(db.Float())
    fabrica = db.Column(db.String(), db.ForeignKey('producto.id'), nullable=False)

    def __init__(self, id, nombre, descripcion, fecha_inicio, fecha_fin, ctd_producida, fabrica):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.ctd_producida = ctd_producida
        self.fabrica = fabrica

    def __repr__(self):
        return f'<ProcesoProductivo {self.id} - {self.nombre}'

    def serialize(self):
        return {
            'id':               self.id,
            'nombre':           self.nombre,
            'descripcion':      self.descripcion,
            'fecha_inicio':     self.fecha_inicio.strftime("%Y-%m-%d"),
            'fecha_fin':        self.fecha_fin.strftime("%Y-%m-%d"),
            'ctd_producida':    self.ctd_producida,
            'fabrica':          self.fabrica
        }


class Producto(db.Model):
    __tablename__ = 'producto'

    id = db.Column(db.String(), primary_key=True)
    nombre = db.Column(db.String())
    descripcion = db.Column(db.String())
    cod_distribucion = db.Column(db.String())
    precio_venta = db.Column(db.Float)
    origen = db.Column(db.String(), db.ForeignKey(
        'proyecto.id'), nullable=False)
    # backref para cascading, también puede usarse para consultar directamente
    procesos_productivos = relationship(
        ProcesoProductivo, cascade="all,delete", backref="producto")

    def __init__(self, id, nombre, descripcion, cod_distribucion, precio_venta, origen):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.cod_distribucion = cod_distribucion
        self.precio_venta = precio_venta
        self.origen = origen

    def __repr__(self):
        return f'<Proyecto {self.id} - {self.nombre}>'

    def serialize(self):
        return {
            'id':                   self.id,
            'nombre':               self.nombre,
            'descripcion':          self.descripcion,
            'cod_distribucion':     self.cod_distribucion,
            'precio_venta':         self.precio_venta,
            'origen':               self.origen,
            'procesos_productivos': self.procesos_productivos
        }


class Proyecto(db.Model):
    __tablename__ = 'proyecto'

    id = db.Column(db.String(), primary_key=True)
    nombre = db.Column(db.String())
    descripcion = db.Column(db.String())
    categoria = db.Column(db.String())
    estado = db.Column(db.Enum(ProyectoEstados))
    # backref para cascading, también puede usarse para consultar directamente
    productos = relationship(
        Producto, cascade="all,delete", backref="proyecto")

    def __init__(self, id, nombre, descripcion, categoria, estado):
        self.id = id
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
            },
            'productos':    self.productos
        }
