from psycopg.rows import dict_row

from myLib.connect import connect
from myLib.p1Settings import EPSG_CODE


class PredioOOP():
    def __init__(self):
        self.conn=connect()
        self.cur=self.conn.cursor()
    def disconnect(self):
        self.cur.close()
        self.conn.close()

    def insert(self, dataDict):
        try:

            nombre = dataDict["nombre"]
            direccion = dataDict["direccion"]
            codman = dataDict["codman"]
            geom = dataDict["geom"]

            # 1. Validar geometría
            cons_val_geom = """
            SELECT ST_IsValid(
                ST_SnapToGrid(ST_GeomFromText(%s,%s),0.0001)
            )
            """
            self.cur.execute(cons_val_geom, [geom, EPSG_CODE])
            valida_geom = self.cur.fetchone()[0]

            if not valida_geom:
                self.disconnect()
                return {
                    "ok": False,
                    "message": "Geometria invalida",
                    "data": None
                }

            # 2. Verificar intersección con otros polígonos
            cons_relate = """
            SELECT id
            FROM lau.predio p
            WHERE ST_Relate(
                p.geom,
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
                    "message": "La geometria cruza con un poligono existente",
                    "data": None
                }

            # 3. Insertar si pasa validaciones
            cons_insert = """
            INSERT INTO lau.predio
                (nombre, direccion, codman, geom)
            VALUES
                (%s,%s,%s,
                ST_SnapToGrid(ST_GeomFromText(%s,%s),0.0001))
            RETURNING id
            """

            entrada = [nombre, direccion, codman, geom, EPSG_CODE]

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
            
    def delete(self, dataDict):
        try:
            idValue=dataDict["id"] #Leer la fila a eliminar
            conn=connect()
            cur=conn.cursor()
            
            # 2. comprobar si existe el id
            sql_check = "SELECT id FROM lau.predio WHERE id=%s"
            self.cur.execute(sql_check, (dataDict["id"],))
            if self.cur.rowcount == 0:
                return {
                    "ok": False,
                    "message": "Geometria no encontrada",
                    "data": None }
        
            cons="""
                DELETE FROM
                    lau.predio
                WHERE
                    id=%s
                """
            #Ejecutar el sql
            cur.execute(cons, [idValue])
            rows=self.cur.rowcount # 
            conn.commit()
            cur.close()
            conn.close()
            self.disconnect()
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
            direccion = dataDict["direccion"]
            codman = dataDict["codman"]
            geom = dataDict["geom"]
                        
            # 2. comprobar si existe el id
            sql_check = "SELECT id FROM lau.predio WHERE id=%s"
            self.cur.execute(sql_check, (dataDict["id"],))
            if self.cur.rowcount == 0:
                return {
                    "ok": False,
                    "message": "Geometria no encontrada",
                    "data": None }

            # 1. Validar geometría
            cons_val_geom = """
            SELECT ST_IsValid(
                ST_SnapToGrid(ST_GeomFromText(%s,%s),0.0001)
            )
            """
            self.cur.execute(cons_val_geom, [ geom, EPSG_CODE])
            valida_geom = self.cur.fetchone()[0]

            if not valida_geom:
                self.disconnect()
                return {
                    "ok": False,
                    "message": "Geometria invalida",
                    "data": None
                }

            # 2. Verificar intersección con otros polígonos
            cons_relate = """
            SELECT id
            FROM lau.predio p
            WHERE id <> %s AND
            ST_Relate(
                p.geom,
                ST_SnapToGrid(ST_GeomFromText(%s,%s),0.0001),
                'T********'
            )
            """

            self.cur.execute(cons_relate, [idValue,geom, EPSG_CODE])
            row = self.cur.fetchone()

            if row is not None:
                self.disconnect()
                return {
                    "ok": False,
                    "message": "La geometria cruza con un poligono existente",
                    "data": None
                }


            cons_up="""
                UPDATE
                    lau.predio
                SET 
                nombre = %s, 
                direccion = %s, 
                codman = %s, 
                geom = ST_SnapToGrid(st_geometryFromText(%s,%s),0.0001)
                WHERE id=%s
                """
            entrada = [nombre, direccion, codman, geom, EPSG_CODE, idValue]

            self.cur.execute(cons_up, entrada)

            rows = self.cur.rowcount

            self.conn.commit()
            self.disconnect()

            return {
                "ok": True,
                "message": "Data Update",
                "data": [{"id": rows}]
            }

        except Exception as e:
            self.disconnect()

            return {"ok":False,"message":str(e),
            "data":None}

## Estructura para diccionario         
    def selectAsDict(self, dataDict):
        try:

            # leer dataDict
            idValue = dataDict['id']        
            # 2. Cursor como diccionario
            self.cur = self.conn.cursor(row_factory=dict_row)
            # ejecutar SQL
            cons="""
            SELECT 
                id 
            FROM 
                lau.predio
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
              # ejecutar SQL
            cons="""
            SELECT 
                id
            FROM 
                lau.predio
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