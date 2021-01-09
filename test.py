import pandas as pd
import datetime, numpy
from models import *
from app import db


def load_data(filename):
    return pd.read_csv(filename).to_numpy()


def populate_proyectos():
    data = load_data('testbed/proyectos.csv')

    for d in data:
        try:
            proyecto = Proyecto(
                id          = str(d[0]),
                nombre      = str(d[1]),
                descripcion = str(d[2]),
                categoria   = str(d[3]),
                estado      = ProyectoEstados(int(d[4]))
            )
            db.session.add(proyecto)
            db.session.commit()
        except:
            pass

def populate_productos():
    data = load_data('testbed/productos.csv')

    for d in data:
        try:
            producto = Producto(
                id                  = d[0],
                nombre              = d[1],
                descripcion         = d[2],
                cod_distribucion	= d[3],
                precio_venta		= float(d[4]),
                origen              = d[5]
            )
            db.session.add(producto)
            db.session.commit()
        except:
            pass

def populate_procesos_productivos():
    data = load_data('testbed/procesos_productivos.csv')

    for d in data:
        t_d = lambda d, i: int(d.split('/')[i])
        try:
            proceso_productivo = ProcesoProductivo(
                id              = d[0],
                nombre          = d[1],
                descripcion     = d[2],
                fecha_inicio	= datetime.datetime(t_d(d[3], 2), t_d(d[3], 1), t_d(d[3], 0)),
                fecha_fin		= datetime.datetime(t_d(d[4], 2), t_d(d[4], 1), t_d(d[4], 0)),
                ctd_producida   = float(d[5]),
                fabrica         = d[6]
            )
            db.session.add(proceso_productivo)
            db.session.commit()
        except:
            pass

def populate_nominas():
    data = load_data('testbed/nominas.csv')

    for d in data:
        try:
            nomina=Nomina(
                IBAN		= d[0],
                fecha	    = d[1],
                sueldo	    = float(d[2]),
                DNI		    = d[3],
                IdOp        = int(d[4])
            )
            db.session.add(nomina)
            db.session.commit()
        except:
            pass

def populate_facturas():
    data = load_data('testbed/facturas.csv')

    for d in data:
        try:
            factura=Factura(
                CIF_cli		    = d[0],
                IDlote	        = int(d[1]),
                FechaVen	    = d[2],
                ImporteVen		= float(d[3]),
                IdOp            = int(d[4])
            )
            db.session.add(factura)
            db.session.commit()
        except:
            pass

def populate_recibos():
    data = load_data('testbed/recibos.csv')

    for d in data:
        try:
            recibo=Recibo(
                CIF_pro		    = d[0],
                NumeroRegistro	= int(d[1]),
                FechaCom	    = d[2],
                ImporteCom		= float(d[3]),
                IdOp            = int(d[4])
            )
            db.session.add(recibo)
            db.session.commit()
        except:
            pass

def populate_balances():
    data = load_data('testbed/balances.csv')

    for d in data:
        try:
            balance=BalanceCuentas(
                IdOp	        = int(d[0]),
                balance	        = float(d[1]),
                claseOp	        = ClaseOperacion(int(d[2])),
            )
            db.session.add(balance)
            db.session.commit()
        except:
            pass

def populate_clientes():
    data = load_data('testbed/clientes.csv')

    for d in data:
        try:
            cliente=Cliente(
                CIF_cli	        = d[0],
                nombre	        = d[1],
                direccion	    = d[2],
            )
            db.session.add(cliente)
            db.session.commit()
        except:
            pass

def populate_proveedores():
    data = load_data('testbed/proveedores.csv')

    for d in data:
        try:
            proveedor=Proveedor(
                CIF_pro	        = d[0],
                nombre	        = d[1],
                direccion	    = d[2],
            )
            db.session.add(proveedor)
            db.session.commit()
        except:
            pass



if __name__ == '__main__':
    # I+D y Producción
    populate_proyectos()
    populate_productos()
    populate_procesos_productivos()
    populate_nominas()
    populate_facturas()
    populate_recibos()
    populate_balances()
    populate_clientes()
    populate_recibos()