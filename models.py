from app import db
from sqlalchemy.orm import relationship
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


class ProcesoProductivo(db.Model):
    __tablename__ = 'proceso_productivo'

    id              = db.Column(db.String(), primary_key=True)
    nombre          = db.Column(db.String())
    descripcion     = db.Column(db.String())
    fecha_inicio    = db.Column(db.Date())
    fecha_fin       = db.Column(db.Date())
    ctd_producida   = db.Column(db.Float())
    fabrica         = db.Column(db.String(), db.ForeignKey('producto.id'), nullable=False)

    def __init__(self, id, nombre, descripcion, fecha_inicio, fecha_fin, ctd_producida, fabrica):
        self.id             = id
        self.nombre         = nombre
        self.descripcion    = descripcion
        self.fecha_inicio   = fecha_inicio
        self.fecha_fin      = fecha_fin
        self.ctd_producida  = ctd_producida
        self.fabrica        = fabrica
    
    def __repr__(self):
        return f'<ProcesoProductivo {self.id} - {self.nombre}'
    
    def serialize(self):
        return {
            'id':               self.id,
            'nombre':           self.nombre,
            'descripcion':      self.descripcion,
            'fecha_inicio':     self.fecha_inicio.strftime("%d/%m/%Y"),
            'fecha_fin':        self.fecha_fin.strftime("%d/%m/%Y"),
            'ctd_producida':    self.ctd_producida,
            'fabrica':          self.fabrica
        }

class Producto(db.Model):
    __tablename__ = 'producto'

    id                      = db.Column(db.String(), primary_key=True)
    nombre                  = db.Column(db.String())
    descripcion             = db.Column(db.String())
    cod_distribucion        = db.Column(db.String())
    precio_venta            = db.Column(db.Float)
    origen                  = db.Column(db.String(), db.ForeignKey('proyecto.id'), nullable=False)
    # backref para cascading, también puede usarse para consultar directamente
    procesos_productivos    = relationship(ProcesoProductivo, cascade="all,delete", backref="producto")

    def __init__(self, id, nombre, descripcion, cod_distribucion, precio_venta, origen):
        self.id                 = id
        self.nombre             = nombre
        self.descripcion        = descripcion
        self.cod_distribucion   = cod_distribucion
        self.precio_venta       = precio_venta
        self.origen             = origen
    
    def __repr__(self):
        return f'<Proyecto {self.id} - {self.nombre}>'
    
    def serialize(self):
        return {
            'id':               self.id,
            'nombre':           self.nombre,
            'descripcion':      self.descripcion,
            'cod_distribucion': self.cod_distribucion,
            'precio_venta':     self.precio_venta,
            'origen':           self.origen
        }

class Proyecto(db.Model):
    __tablename__ = 'proyecto'

    id          = db.Column(db.String(), primary_key=True)
    nombre      = db.Column(db.String())
    descripcion = db.Column(db.String())
    categoria   = db.Column(db.String())
    estado      = db.Column(db.Enum(ProyectoEstados))
    # backref para cascading, también puede usarse para consultar directamente
    productos   = relationship(Producto, cascade="all,delete", backref="proyecto")

    def __init__(self, id, nombre, descripcion, categoria, estado):
        self.id             = id
        self.nombre         = nombre
        self.descripcion    = descripcion
        self.categoria      = categoria
        self.estado         = estado

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
