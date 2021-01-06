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


if __name__ == '__main__':
    # I+D y Producción
    populate_proyectos()
    populate_productos()
    populate_procesos_productivos()