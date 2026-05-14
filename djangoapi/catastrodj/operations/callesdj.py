from django.contrib.gis.geos import GEOSGeometry 
from django.forms.models import model_to_dict
from django.db import connection

from catastrodj import models
from catastrodj.models import Calles
from scripts.p1.myLib import p1Settings

from djangoapi.settings import EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION


def insert(d:dict):
    #we first get the snapped wkb format for the geometry:
    cur=connection.cursor()
    query="select st_snaptogrid(st_geomfromtext(%s, %s),%s)"
    cur.execute(query, [d['geom'],EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION])
    snapped_wkb_geometry=cur.fetchall()[0][0]

    print(f'snapped_wkb_geometry: {snapped_wkb_geometry}')

    #now we can check if it is valid as before:
    g=GEOSGeometry(snapped_wkb_geometry, srid=EPSG_FOR_GEOMETRIES)
    if g.valid:
        print("Geometría válida")
    else:
        return {'ok': False, 'message':'Invalid geometry', 'data': None}
    
    #Now we can check if it intersects with another geomtry in the same layer
    #check if the geometry intersects any existing calle
    query=""" 
        select id from catastrodj_calles where ST_relate(
            geom,
            %s,
            'T********'
        )
    """
    cur.execute(query, [snapped_wkb_geometry])
    r=cur.fetchall()

    if len(r)>0:
        return {'ok': False, 'message':'The geometry interior intersects with the following geometries id', 'data': r}

    d['geom']=g
    b=Calles(**d)
    b.save()
    d=model_to_dict(b)
    d['geom']=g.wkt
    d['data_creation']=d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")
    return {'ok': True, 'message':'Calles insertado', 'data': [d]}

def delete(d:dict):
    #create the geometry with geos
    f=Calles.objects.filter(id=d['id'])
    l=list(f)
    if len(l)<1:
        return {"ok":False, "Message": f"No Calles with the id {d['id']}", "data":None}
    b:Calles=l[0]
    b.delete()
    return {'ok':True, 'Message': f"Calles deleted: 1",
            'data':[{'id':d["id"]}]}

    #g=GEOSGeometry(d['geom'], srid=p1Settings.EPSG_CODE)

def update(d:dict):
    cur=connection.cursor()
    #Primero hacemos el snap to grid
    query="select st_snaptogrid(st_geomfromtext(%s, %s),%s)"
    cur.execute(query, [d['geom'],EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION])
    snapped_wkb_geometry=cur.fetchall()[0][0]

    print(f'snapped_wkb_geometry: {snapped_wkb_geometry}')

    # Make geometry simple (avoid self-intersections)
    query_simple = "select ST_Simplify(%s, %s)"
    cur.execute(query_simple, [snapped_wkb_geometry, ST_SNAP_PRECISION])
    simple_wkb_geometry = cur.fetchall()[0][0]

    #now we can check if it is valid as before:
    g=GEOSGeometry(simple_wkb_geometry, srid=EPSG_FOR_GEOMETRIES)
    if g.valid:
        print("Geometría válida")
    else:
        return {'ok': False, 'message':'Invalid geometry', 'data': None}
    
    #Now we can check if it intersects with another geomtry in the same layer
    #check if the geometry intersects any existing catastrodj_Calles
    query=""" 
        select id from catastrodj_Calles where ST_relate(
            geom,
            %s,
            'T********'
        )
    """
    cur.execute(query, [simple_wkb_geometry])
    r=cur.fetchall()

    if len(r)>0:
            return {'ok': False, 'message':'The geometry interior intersects with the following geometries id', 'data': r}

    #create the geometry with geos
    f=Calles.objects.filter(id=d['id'])
    l=list(f)
    if len(l)>0:
        b:Calles=l[0]
    else:
        return {'ok':False, "Mesage": f"No Calles found with id {d['id']}", 'data':None}

    b.geom=g
    b.description=d['description']
    b.save()
    d=model_to_dict(b)
    d['geom']=g.wkt
    d['data_creation']=d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")

    return {'ok':True, 'Message': f"Updated Calles: {len(l)}",
            'data':[d]}

##Devuelve un diccionario de un id
def selectAsDicts(d:dict):
    try:
        #create the geometry with geos
        id=d['id'] #leer el id
        csql=Calles.objects.filter(id=id).values()#Consula ORM que es equivalente al sql SELECT * FROM Calles WHERE id = id; 
        #si ponemos .values() devuelve diccionarios directamente
        l = list(csql)
        if len(l)<1: # if there is no Calless with the given id, we return an error message
            return {"ok":False, "Message": f"No Calles with the id {d['id']}", "data":None}

        for r in l:
            g = GEOSGeometry(r['geom'], srid=EPSG_FOR_GEOMETRIES)
            r['geom'] = g.wkt
            r['data_creation'] = r['data_creation'].strftime("%Y-%m-%d %H:%M:%S")

        return {"ok": True,
            "Message": f"Retrieved Calles: {len(l)}",
            "data": l}
    except Exception as e:
        return {"ok": False, "Message": str(e), "data": None}
    
##Devuelve un diccionario de con todos los id sin implementar .values -> camino largo para convertir a diccionario
def selectallAsDicts():
    try:
        f = Calles.objects.all()
        l = list(f) #Convierten el resultado a lista
        data = []
        for b in l:
            d = model_to_dict(b) #Convierten el modelo a diccionario con model_to_dict
            g = GEOSGeometry(d['geom'], srid=EPSG_FOR_GEOMETRIES)
            d['geom'] = g.wkt
            d['data_creation'] = d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")
            data.append(d)
        return { "ok": True,
            "Message": f"Retrieved Calless: {len(data)}",
            "data": data}
    except Exception as e:
        return {"ok": False, "Message": str(e), "data": None}

##Devuelve una lista de tuplas de con todos los id sin implementar
def selectAsTuples():
    try:
        qs = Calles.objects.values_list(
            'id', 'description', 'perimeter','estado','nombre',"geom",'data_creation' )
        
        l = list(qs)

        return {
            "ok": True,
            "Message": f"Retrieved Calless: {len(l)}",
            "data": l }

    except Exception as e:
        return {"ok": False, "Message": str(e), "data": None}

def run():
    d_of_values= {
        'description':'Calle 1 UPV', 
        'perimeter':200,
        'estado':'Malo',
        'nombre':"Calle Camino de Vera",
        "geom": 'LINESTRING(391037 4304834,391040 4304837)'   }
    
    print(insert(d_of_values))
    print(delete(d_of_values))
