from django.contrib.gis.geos import GEOSGeometry 
from django.forms.models import model_to_dict
from django.db import connection

from catastrodj import models
from catastrodj.models import Predio
from scripts.p1.myLib import p1Settings

from djangoapi.settings import EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION


def insert(d:dict):
    try:
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
        #check if the geometry intersects any existing building
        query=""" 
            select id from catastrodj_predio where ST_relate(
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
        b=Predio(**d)
        b.save()
        d=model_to_dict(b)
        d['geom']=g.wkt
        d['data_creation']=d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")
        return {'ok': True, 'message':'Predio insertado', 'data': [d]}
    
    except Exception as e:
        return {"ok": False, "Message": str(e), "data": None}

def delete(d:dict):
    #create the geometry with geos
    f=Predio.objects.filter(id=d['id'])
    l=list(f)
    if len(l)<1:
        return {"ok":False, "Message": f"No Predio with the id {d['id']}", "data":None}
    b:Predio=l[0]
    b.delete()
    return {'ok':True, 'Message': f"Predio deleted: 1",
            'data':[{'id':d["id"]}]}

    #g=GEOSGeometry(d['geom'], srid=p1Settings.EPSG_CODE)

def update(d:dict):
    try:
        cur=connection.cursor()
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
        #check if the geometry intersects any existing catastrodj_predio
        query=""" 
            select id from catastrodj_predio WHERE id <> %s AND ST_relate(
                geom,
                %s,
                'T********'
            )
        """
        cur.execute(query, [d['id'], simple_wkb_geometry])
        r=cur.fetchall()

        if len(r)>0:
            return {'ok': False, 'message':'The geometry interior intersects with the following geometries id', 'data': r}

        #create the geometry with geos
        f=Predio.objects.filter(id=d['id'])
        l=list(f)
        if len(l)>0:
            b:Predio=l[0]
        else:
            return {'ok':False, "Mesage": f"No Predios found with id {d['id']}", 'data':None}

        b.geom=g
        b.description=d['description']
        b.save()
        d=model_to_dict(b)
        d['geom']=g.wkt
        d['data_creation']=d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")

        return {'ok':True, 'Message': f"Updated buildings: {len(l)}",
                'data':[d]}
    
    except Exception as e:
        return {"ok": False, "Message": str(e), "data": None}

# def select(d:dict):
#     try:
#         #create the geometry with geos
#         f=Predio.objects.filter(id=d['id'])
#         l=list(f)
#         b:Predio=l[0] #we take the first element of the list, since there should be only one element with the given id, if there are more, we will return an error message

#         if len(l)<1: # if there is no predios with the given id, we return an error message
#             return {"ok":False, "Message": f"No Predio with the id {d['id']}", "data":None}
#         d=model_to_dict(b)
#         g=GEOSGeometry(d['geom'], srid=EPSG_FOR_GEOMETRIES)
#         d['geom']=g.wkt
#         d['data_creation']=d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")
#         return {'ok':True, 'Message': f"Retriewed Predio: {len(l)}",
#                 'data':[d]}
#     except Exception as e:
#         return {"ok":False, "Message": str(e), "data":None}

##Devuelve un diccionario de un id
def selectAsDicts(d:dict):
    try:
        #create the geometry with geos
        id=d['id'] #leer el id
        csql=Predio.objects.filter(id=id).values()#Consula ORM que es equivalente al sql SELECT * FROM predio WHERE id = id; 
        #si ponemos .values() devuelve diccionarios directamente
        l = list(csql)
        if len(l)<1: # if there is no predios with the given id, we return an error message
            return {"ok":False, "Message": f"No Predio with the id {d['id']}", "data":None}

        for r in l:
            g = GEOSGeometry(r['geom'], srid=EPSG_FOR_GEOMETRIES)
            r['geom'] = g.wkt
            r['data_creation'] = r['data_creation'].strftime("%Y-%m-%d %H:%M:%S")

        return {"ok": True,
            "Message": f"Retrieved Predio: {len(l)}",
            "data": l}
    except Exception as e:
        return {"ok": False, "Message": str(e), "data": None}
    
##Devuelve un diccionario de con todos los id sin implementar .values -> camino largo para convertir a diccionario
def selectallAsDicts():
    try:
        f = Predio.objects.all()
        l = list(f) #Convierten el resultado a lista
        data = []
        for b in l:
            d = model_to_dict(b) #Convierten el modelo a diccionario con model_to_dict
            g = GEOSGeometry(d['geom'], srid=EPSG_FOR_GEOMETRIES)
            d['geom'] = g.wkt
            d['data_creation'] = d['data_creation'].strftime("%Y-%m-%d %H:%M:%S")
            data.append(d)
        return { "ok": True,
            "Message": f"Retrieved Predios: {len(data)}",
            "data": data}
    except Exception as e:
        return {"ok": False, "Message": str(e), "data": None}

def selectAsTuples():
    try:
        qs = Predio.objects.values_list(
            'id', 'description', 'area','perimeter','nombre',"geom",'data_creation' )
        
        l = list(qs)

        return {
            "ok": True,
            "Message": f"Retrieved Predios: {len(l)}",
            "data": l }

    except Exception as e:
        return {"ok": False, "Message": str(e), "data": None}

def run():
    d_of_values= {
        'description':'UPV Edificio 1', 
        'area':2000,
        'perimeter':200,
        'nombre':100,
        'geom':'POLYGON((0 0, 10 0, 10 10, 0 11, 0 0))'
    }
    
    print(insert(d_of_values))
    print(delete(d_of_values))
