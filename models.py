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
    index = db.Column(db.Float())

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
        good_index = index >= 0 and index <= 1

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
    sueldo = db.Column(db.Float())
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
        good_money = sueldo >= 0
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


# ================================
# ==== DPTO. CONTABILIDAD ====
# ================================


class ClaseOperacion(enum.Enum):    
    COMPRA		= 0
    VENTA	    = 1
    NOMINA  	= 2


    def __str__(self):
        keys = {
            0: "Compra",
            1: "Venta",
            2: "Nómina"
        }
        
        return keys[self.value]


class Proveedor(db.Model):
    __tablename__ = 'proveedores'

    CIF_pro = db.Column(db.String(), primary_key = True)
    nombre = db.Column(db.String())
    direccion = db.Column(db.String())

    def __init__(self, CIF_pro, nombre, direccion):
        self.CIF_pro = CIF_pro
        self.nombre = nombre
        self.direccion = direccion
    
    def __repr__(self):
        return f'<Proveedor {self.CIF_pro} - {self.nombre}>'
    
    def serialize(self):
        return{
            'CIF_pro':         self.CIF_pro,
            'nombre':          self.nombre,
            'direccion':       self.direccion
        }


class Cliente(db.Model):
    __tablename__ = 'clientes'

    CIF_cli = db.Column(db.String(), primary_key = True)
    nombre = db.Column(db.String())
    direccion = db.Column(db.String())

    def __init__(self, CIF_pro, nombre, direccion):
        self.CIF_cli = CIF_pro
        self.nombre = nombre
        self.direccion = direccion
    
    def __repr__(self):
        return f'<Proveedor {self.CIF_cli} - {self.nombre}>'
    
    def serialize(self):
        return{
            'CIF_cli':         self.CIF_cli,
            'nombre':          self.nombre,
            'direccion':       self.direccion
        }


class Recibo(db.Model):
    __tablename__ = 'recibos'

    CIF_pro = db.Column(db.String())
    NumeroRegistro = db.Column(db.Integer(), primary_key=True)
    FechaCom = db.Column(db.Date())
    ImporteCom = db.Column(db.Float())
    IdOp = db.Column(db.Integer())

    def __init__(self, CIF_pro, NumeroRegistro, FechaCom, ImporteCom, IdOp):
        self.CIF_pro = CIF_pro
        self.NumeroRegistro = NumeroRegistro
        self.FechaCom = FechaCom
        self.ImporteCom = ImporteCom
        self.IdOp = IdOp
    
    @classmethod
    def validate(self, CIF_pro, NumeroRegistro, FechaCom, ImporteCom):
        if len(NumeroRegistro)>0:
            b1 = Recibo.query.filter_by(NumeroRegistro = int(NumeroRegistro)).first() == None
        else:
            b1 = True
        b2 = len(CIF_pro) == 9
        #b3 = Mercancia.query.filter_by(NumeroRegistro = NumeroRegistro).first() != None
        b3 = True
        b4 = len(CIF_pro) > 0 and len(NumeroRegistro) > 0 and len(FechaCom) > 0 and len(ImporteCom) > 0
        reason = ""

        if not b1:
            reason = reason + "Número de registro ya usado para un recibo. "
        if not b2:
            reason = reason + "Longitud de CIF no apropiada. "
        #if not b3:
            #reason = reason + "Número de registro no asignado a ninguna mercancía. "
        if not b4:
            reason = reason + "Todos los campos tienen que ser rellenados. "
        

        return b1 and b2 and b3 and b4, reason

    
    def __repr__(self):
        return f'<Recibo {self.CIF_pro} - {self.NumeroRegistro}>'

    def serialize(self):
        return{
            'CIF_pro':         self.CIF_pro,
            'NumeroRegistro':  self.NumeroRegistro,
            'FechaCom':        self.FechaCom,
            'ImporteCom':      self.ImporteCom,
            'IdOp':            self.IdOp
        }


class Factura(db.Model):
    __tablename__ = 'facturas'

    CIF_cli = db.Column(db.String())
    IDlote = db.Column(db.Integer(), primary_key=True)
    FechaVen = db.Column(db.Date())
    ImporteVen = db.Column(db.Float())
    IdOp = db.Column(db.Integer())

    def __init__(self, CIF_cli, IDlote, FechaVen, ImporteVen, IdOp):
        self.CIF_cli = CIF_cli
        self.IDlote = IDlote
        self.FechaVen = FechaVen
        self.ImporteVen = ImporteVen
        self.IdOp = IdOp
    
    @classmethod
    def validate(self, CIF_cli, IDlote, FechaVen, ImporteVen):
        if len(IDlote)>0:
            b1 = Factura.query.filter_by(IDlote = int(IDlote)).first() == None
        else:
            b1 = True
        b2 = len(CIF_cli) == 9
        #b3 = Lote.query.filter_by(IDlote = IDlote).first() != None
        b3 = True
        b4 = len(CIF_cli) > 0 and len(IDlote) > 0 and len(FechaVen) > 0 and len(ImporteVen) > 0
        reason = ""
        print("Longitud id lote: ", len(IDlote))
        if b4:
            print("Todos mayor")
        else:
            print("Alguno 0")

        if not b1:
            reason = reason + "ID de lote ya usado. "
        if not b2:
            reason = reason + "Longitud de CIF no apropiada. "
        #if not b3:
            #reason = reason + "Identificador no asignado a ningún lote. "
        if not b4:
            reason = reason + "Todos los campos tienen que ser rellenados. "
        

        return b1 and b2 and b3 and b4, reason
    
    def __repr__(self):
        return f'<Recibo {self.CIF_cli} - {self.IDlote}>'

    def serialize(self):
        return{
            'CIF_cli':         self.CIF_cli,
            'IDlote':          self.IDlote,
            'FechaVen':        self.FechaVen,
            'ImporteVen':      self.ImporteVen,
            'IdOp':            self.IdOp
        }


class Nomina(db.Model):
    __tablename__ = 'nominas'

    IBAN = db.Column(db.String())
    fecha = db.Column(db.Date(), primary_key = True)
    sueldo = db.Column(db.Float())
    DNI = db.Column(db.String(), primary_key = True)
    IdOp = db.Column(db.Integer())

    def __init__(self, IBAN, fecha, sueldo, DNI, IdOp):
        self.IBAN = IBAN
        self.fecha = fecha
        self.sueldo = sueldo
        self.DNI = DNI
        self.IdOp = IdOp
    
    @classmethod
    def validate(self, IBAN, fecha, sueldo, DNI):
        if len(DNI)>0 and len(fecha)>0:
            b1 = Nomina.query.filter_by(DNI = DNI, fecha = fecha).first() == None
        else:
            b1 = True
        b2 = len(DNI) == 9
        #b3 = Empleado.query.filter_by(dni = dni).first() != None
        b3 = True
        b4 = len(IBAN) > 0 and len(fecha) > 0 and len(sueldo) > 0 and len(DNI) > 0
        reason = ""

        if not b1:
            reason = reason + "Nómina ya registrada. "
        if not b2:
            reason = reason + "Longitud de DNI no apropiada. "
        #if not b3:
            #reason = reason + "DNI no asignado a ningún empleado. "
        if not b4:
            reason = reason + "Todos los campos tienen que ser rellenados. "

        return b1 and b2 and b3 and b4, reason
    
    def __repr__(self):
        return f'<Nomina {self.IBAN} - {self.fecha}>'
    
    def serialize(self):
        return{
            'IBAN':         self.IBAN,
            'fecha':        self.fecha,
            'sueldo':       self.sueldo,
            'DNI':          self.DNI,
            'IdOp':         self.IdOp
        }




class BalanceCuentas(db.Model):
    __tablename__ = 'balances'

    IdOp = db.Column(db.Integer(), primary_key = True)
    balance = db.Column(db.Float())
    claseOp = db.Column(db.Enum(ClaseOperacion))

    def __init__(self, IdOp, balance, claseOp):
        self.IdOp = IdOp
        self.balance = balance
        self.claseOp = claseOp
    
    def __repr__(self):
        return f'<Balance {self.IdOp} - {self.balance}>'
    
    def serialize(self):
        return{
            'IdOp':         self.IdOp,
            'balance':      self.balance,
            'claseOp':		{
                'value':    self.claseOp.value,
                'verbose':  str(self.claseOp)
            }
        }





# ================================
# ======= DPTO. ALMACENAJE =======
# ================================



class Materiaprima(db.Model):
    __tablename__ = 'materiaprima'
    
    id = db.Column(db.Integer(), primary_key=True)
    nombre = db.Column(db.String())
    caracteristicas = db.Column(db.String())
    zonaAlmacenaje = db.Column(db.String())
    cantidadA = db.Column(db.Integer)

    def __init__(self, nombre, caracteristicas, zonaAlmacenaje):
        self.nombre = nombre
        self.caracteristicas = caracteristicas
        self.zonaAlmacenaje = zonaAlmacenaje
        self.cantidadA = 0

    def __repr__(self):
     return f'<Materiaprima {self.id} - {self.nombre}>'


    def serialize(self):
        return {
            'id':           self.id,
            'nombre':		self.nombre,
            'caracteristicas':	self.caracteristicas,
            'zonaAlmacenaje':	self.zonaAlmacenaje,
            'cantidadA':	self.cantidadA
        }

    @classmethod 
    def validate(self,nombre):
        good_name = not Materiaprima.query.filter_by(nombre = nombre).first()
        reason = "none"
        if not good_name:
            reason = "Ya existe una materia prima con ese nombre"

        return good_name,reason
            
        

        
class MercanciaTipos(enum.Enum):    
    AÑADIDO		= 0
    RETIRADA	= 1


    def __str__(self):
        keys = {
            0: "Añadido",
            1: "Retirada",
        }
        
        return keys[self.value]

        
class Mercancia(db.Model):
    __tablename__ = 'mercancia'
    
    numRegistro = db.Column(db.Integer(), primary_key=True)
    idmp = db.Column(db.Integer(), db.ForeignKey('materiaprima.id'), nullable = False)
    cantidad = db.Column(db.Integer)
    tipo = db.Column(db.Enum(MercanciaTipos))
    idpp = db.Column(db.String(), nullable=True)
#db.ForeignKey('proceso_productivo.id')
    
    def __init__(self, idmp, cantidad, tipo, idpp): 
        self.idmp = idmp
        self.cantidad = cantidad
        self.tipo = tipo
        self.idpp = idpp

    def __repr__(self):
     return f'<Mercancia {self.numRegistro} - {self.idmp}>'


    def serialize(self):
        return {
            'numRegistro':		self.numRegistro,
            'idmp':	self.idmp,
            'cantidad':	self.cantidad,
            'tipo':     {
                'value':    self.tipo.value,
                'verbose':  str(self.tipo)
            },
            'idpp':	self.idpp
        }

    @classmethod 
    def validate(self, idmp, cantidad, tipo, idpp): 
        reason = "none"
        good_idmp = Materiaprima.query.filter_by(id = idmp).first()

        good_quantity = True
        good_pp = True
        
        if not good_idmp:
            reason = "No existe una materia prima con ese identificador"
        else:
            if tipo == MercanciaTipos.RETIRADA:
                materia = Materiaprima.query.filter_by(id = idmp).first()

                if (materia.cantidadA < int(cantidad)):
                    good_quantity = False
                    reason = "La cantidad a retirar es mayor que la almacenada"

                good_pp = ProcesoProductivo.query.filter_by(id = idpp).first()
                if not good_pp:
                    reason = "No existe un proceso productivo con ese ID"
        return (good_idmp and good_quantity and good_pp),reason
      

                    
       
       
class LotesEstados(enum.Enum):    
    ALMACENADO	= 1
    REPARTIDO	= 0


    def __str__(self):
        keys = {
            0: "Repartido",
            1: "Almacenado",
        }
        
        return keys[self.value]             
                    
                    
         
class Lote(db.Model):
    __tablename__ = 'lote'

    id = db.Column(db.Integer(), primary_key=True)
    idproducto = db.Column(db.String(), db.ForeignKey('producto.id'), nullable=False)
    fechaProd = db.Column(db.String())
    fechaCad = db.Column(db.String())
    cantidad = db.Column(db.Integer)
    estado = db.Column(db.Enum(LotesEstados))

    def __init__(self, idproducto, fechaProd, fechaCad, cantidad, estado):
        self.idproducto = idproducto
        self.fechaProd  = fechaProd
        self.fechaCad   = fechaCad
        self.cantidad   = cantidad
        self.estado     = estado

    def __repr__(self):
     return f'<Lote {self.id}  >'


    def serialize(self):
        return {
            'id':           self.id,
            'idproducto':		self.idproducto,
            'fechaProd':	self.fechaProd,
            'fechaCad':	self.fechaCad,
            'cantidad':	self.cantidad,
            'estado': {
                'value':    self.estado.value,
                'verbose':  str(self.estado)
            }
        }

    @classmethod 
    def validate(self, idproducto, fechaProd, fechaCad):
    
        reason = "none"
        good_date = fechaProd < fechaCad
        if not good_date:
            reason = "El lote no puede caducar antes de su fecha de produccion"
            
        good_idp = Producto.query.filter_by(id = idproducto).first()
        if not good_idp:
            reason = "No existe un producto con ese identificador"

        return (good_date and good_idp),reason





