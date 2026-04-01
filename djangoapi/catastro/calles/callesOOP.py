from psycopg.rows import dict_row

from myLib.connect import connect
from myLib.p1Settings import EPSG_CODE


class CallesOOP():
    def __init__(self):
        self.conn=connect()
        self.cur=self.conn.cursor()
    def disconnect(self):
        self.cur.close()
        self.conn.close()


    def insert(self, dataDict):
        try: 
            
            nombre = dataDict["nombre"]
            longitud = dataDict["longitud"]
            estado = dataDict["estado"]
            geom = dataDict["geom"]

            # Validar geometría
            cons_val_geom = """
            SELECT 
            ST_IsValid(g),
            ST_IsSimple(g)
            FROM (
                SELECT ST_SnapToGrid(ST_GeomFromText(%s,%s),0.0001) g
            ) a 
            """
            self.cur.execute(cons_val_geom, [geom, EPSG_CODE])
            valida_geom, simple_geom = self.cur.fetchone()

            if not valida_geom or not simple_geom:
                self.disconnect()
                return {
                    "ok": False,
                    "message": "Geometria invalida",
                    "data": None
                }
            
            # Verificar intersección con otras lineas 
            cons_relate = """
            SELECT id            
            FROM lau.calles c
            WHERE ST_Relate(
                c.geom,
                ST_SnapToGrid(ST_GeomFromText(%s,%s),0.0001),
                'T********'
            )
            """

            self.cur.execute(cons_relate, [geom, EPSG_CODE])
            row = self.cur.fetchone()

            if row is not None:
                self.disconnect()
                return {
                    "ok": False,
                    "message": "La geometria cruza con una linea existente",
                    "data": None
                }

            # Insertar si pasa validaciones
            cons_insert="""
            INSERT INTO lau.calles 
                (nombre, longitud,estado, geom)
            VALUES
                (%s,%s,%s,ST_GeomFromText(%s,%s))
            RETURNING id
            """
            entrada = [nombre, longitud, estado, geom, EPSG_CODE]

            self.cur.execute(cons_insert, entrada)

            new_id = self.cur.fetchone()[0]

            self.conn.commit()
            self.disconnect()

            return {
                "ok": True,
                "message": "Data inserted",
                "data": [{"id": new_id}]
            }

        except Exception as e:
            self.disconnect()
            return {
                "ok": False,
                "message": str(e),
                "data": None
            }

    def select(self, asDict=True):
        if asDict:
            #The rows are dicts
            self.cur=self.conn.cursor(row_factory=dict_row)
        
        cons="""
        SELECT 
            nombre, longitud,estado, st_astext(geom)
        FROM 
            lau.calles
        WHERE
            id=%s
        """
        self.cur.execute(cons, [0])
        l=self.cur.fetchall()
        print(l)
        print('First row:')
        print(l[0])
        self.disconnect()
        print("Selected")

    def delete(self, dataDict):
        try: 
            idValue = dataDict["id"]

            conn=connect()
            cur=conn.cursor()

            # 2. comprobar si existe el id
            sql_check = "SELECT id FROM lau.calles WHERE id=%s"
            self.cur.execute(sql_check, (dataDict["id"],))
            if self.cur.rowcount == 0:
                return {
                    "ok": False,
                    "message": "Geometria no encontrada",
                    "data": None }

            cons="""
            DELETE FROM
                lau.calles   
            WHERE
                id=%s
            """
            cur.execute(cons, [idValue])
            rows=self.cur.rowcount # 

            return { "ok":True,"message":"Data deleted",
                "data":[{"rows_deleted":rows}]}

        except Exception as e:
            self.disconnect()

            return {"ok":False,"message":str(e),
            "data":None}


    def update(self, dataDict):

        try:

            idValue = dataDict["id"]
            nombre = dataDict["nombre"]
            longitud = dataDict["longitud"]
            estado = dataDict["estado"]
            geom = dataDict["geom"]

            
            # 2. comprobar si existe el id
            sql_check = "SELECT id FROM lau.calles WHERE id=%s"
            self.cur.execute(sql_check, (dataDict["id"],))
            if self.cur.rowcount == 0:
                return {
                    "ok": False,
                    "message": "Geometria no encontrada",
                    "data": None }

            # Validar geometría
            cons_val_geom = """
            SELECT 
            ST_IsValid(g),
            ST_IsSimple(g)
            FROM (
                SELECT ST_SnapToGrid(ST_GeomFromText(%s,%s),0.0001) g
            ) a
            """

            self.cur.execute(cons_val_geom, [geom, EPSG_CODE])
            valida_geom, simple_geom = self.cur.fetchone()

            if not valida_geom or not simple_geom:
                self.disconnect()
                return {
                    "ok": False,
                    "message": "Geometria invalida",
                    "data": None
                }

            # Verificar intersección con otras calles por eso el where debe ser diferente de ella misma<>
            cons_relate = """
            SELECT id
            FROM lau.calles c
            WHERE id <> %s
            AND ST_Relate(
                c.geom,
                ST_SnapToGrid(ST_GeomFromText(%s,%s),0.0001),
                'T********') """

            self.cur.execute(cons_relate, [idValue, geom, EPSG_CODE])

            row = self.cur.fetchone()

            if row is not None:
                self.disconnect()
                return {
                    "ok": False,
                    "message": "La geometria cruza con una linea existente",
                    "data": None
                }

            # UPDATE
            cons_update = """
            UPDATE lau.calles
            SET 
                nombre = %s,
                longitud = %s,
                estado = %s,
                geom = ST_SnapToGrid(ST_GeomFromText(%s,%s),0.0001) WHERE id = %s"""

            entrada = [nombre, longitud, estado, geom, EPSG_CODE, idValue]

            self.cur.execute(cons_update, entrada)

            rows = self.cur.rowcount

            self.conn.commit()
            self.disconnect()

            return {
                "ok": True,
                "message": "Data updated",
                "data": [{"rows_updated": rows}]
            }

        except Exception as e:

            self.disconnect()

            return {
                "ok": False,
                "message": str(e),
                "data": None}

## Estructura para diccionario         
    def selectAsDict(self, dataDict):
        try:

            # leer dataDict
            idValue = dataDict['id']     
            # 2. Cursor como diccionario
            self.cur = self.conn.cursor(row_factory=dict_row)

            # 2. comprobar si existe el id
            sql_check = "SELECT id FROM lau.calles WHERE id=%s"
            self.cur.execute(sql_check, (dataDict["id"],))
            if self.cur.rowcount == 0:
                return {
                    "ok": False,
                    "message": "Geometria no encontrada",
                    "data": None }
            
            # ejecutar SQL
            cons="""
            SELECT 
                id 
            FROM 
                lau.calles
            WHERE
                id=%s
            """
            self.cur.execute(cons, [idValue])
            # fetch o rowcount
            rows = self.cur.fetchall()
            #Desconectar
            self.disconnect()
            # 4. Respuesta obligatoria
            if not rows:
                return {"ok": True,
                    "message": "Not Data Found",
                    "data": None}
            #Si si hay datos y todo sale bien
            return {"ok": True,
                "message": "Data Selected",
                "data":rows}#El cero para que solo muestre el ID 

        except Exception as e:

            self.disconnect()

            return {
                "ok": False,
                "message": str(e),
                "data": None
            }
#Estructura select para tupla, no usamos el self.cur = self.conn.cursor(row_factory=dict_row) porque
#Eso es lo que lo conviente en diccionario, solo mostramos el id en la consulta. 

    def selectAsTuple(self, dataDict):
        try:

            # leer dataDict
            idValue = dataDict['id']      

            # 2. comprobar si existe el id
            sql_check = "SELECT id FROM lau.calles WHERE id=%s"
            self.cur.execute(sql_check, (dataDict["id"],))
            if self.cur.rowcount == 0:
                return {
                    "ok": False,
                    "message": "Geometria no encontrada",
                    "data": None }

            # ejecutar SQL
            cons="""
            SELECT 
                id
            FROM 
                lau.calles
            WHERE
                id=%s
            """
            self.cur.execute(cons, [idValue])
            # fetch o rowcount
            rows = self.cur.fetchall()
            #Desconectar
            self.disconnect()
            # 4. Respuesta obligatoria

            if not rows:
                return {"ok": True,
                    "message": "Not Data Found",
                    "data": None}
            #Si si hay datos y todo sale bien
            return {"ok": True,
                "message": "Data Selected",
                "data": rows} #El cero para que solo muestre el ID 

        except Exception as e:

            self.disconnect()
            return {
                "ok": False,
                "message": str(e),
                "data": None
            }


            
