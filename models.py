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
