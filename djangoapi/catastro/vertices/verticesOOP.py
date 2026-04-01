from psycopg.rows import dict_row

from myLib.connect import connect
from myLib.p1Settings import EPSG_CODE


class VerticesOOP():
    def __init__(self):
        self.conn=connect()
        self.cur=self.conn.cursor()
    def disconnect(self):
        self.cur.close()
        self.conn.close()


    def insert(self, dataDict):
        try:
            nombre = dataDict["nombre"]
            geom = dataDict["geom"]
            ano = dataDict["ano"]

            # 1. Validar que el punto esté dentro de un polígono
            cons_within = """
            SELECT EXISTS(
                SELECT 1 
                FROM lau.predio p
                WHERE ST_Within(
                    ST_SnapToGrid(ST_GeomFromText(%s,%s),0.0001),
                    p.geom
                )
            )
            """
            self.cur.execute(cons_within, [geom, EPSG_CODE])
            dentro = self.cur.fetchone()[0]

            if not dentro:
                self.disconnect()
                return {
                    "ok":False,
                    "message":"La geometria no esta dentro de ningun poligono"
                }

            # 3. Insertar si pasa validaciones
            cons_insert = """
            INSERT INTO lau.vertices
                (nombre, geom, ano)
            VALUES
                (%s, ST_SnapToGrid(ST_GeomFromText(%s,%s),0.0001), %s)
            RETURNING id
            """

            entrada = [nombre, geom, EPSG_CODE, ano]
            self.cur.execute(cons_insert, entrada)

            new_id = self.cur.fetchone()[0]
            self.conn.commit()

            self.disconnect()

            return {
                "ok":True,
                "message":"Data inserted",
                "data":[{"id":new_id}]
            }

        except Exception as e:
            self.disconnect()
            return {"ok":False,"message":str(e),"data":None}
        

    def delete(self, dataDict):
        try:
            idValue=dataDict["id"] #Leer la fila a eliminar
            conn=connect()
            cur=conn.cursor()

            # 2. comprobar si existe el id
            sql_check = "SELECT id FROM lau.vertices WHERE id=%s"
            self.cur.execute(sql_check, (dataDict["id"],))
            if self.cur.rowcount == 0:
                return {
                    "ok": False,
                    "message": "Geometria no encontrada",
                    "data": None }

            cons="""
                DELETE FROM
                    lau.vertices
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
            geom = dataDict["geom"]
            ano = dataDict["ano"]

            # 2. comprobar si existe el id
            sql_check = "SELECT id FROM lau.vertices WHERE id=%s"
            self.cur.execute(sql_check, (dataDict["id"],))
            if self.cur.rowcount == 0:
                return {
                    "ok": False,
                    "message": "Geometria no encontrada",
                    "data": None }

            # 2. Validar que el punto esté dentro de un polígono
            cons_within = """
            SELECT EXISTS(
                SELECT 1 
                FROM lau.predio p
                WHERE ST_Within(
                    ST_SnapToGrid(ST_GeomFromText(%s,%s),0.0001),
                    p.geom
                )
            )
            """
            self.cur.execute(cons_within, [geom, EPSG_CODE])
            dentro = self.cur.fetchone()[0]

            if not dentro:
                self.disconnect()
                return {
                    "ok":False,
                    "message":"La geometria no esta dentro de ningun poligono"
                }

            # 3. Actualizar si pasa validaciones
            cons_update="""
                UPDATE
                    lau.vertices
                SET 
                    nombre = %s,
                    geom=  ST_SnapToGrid(st_geometryFromText(%s,%s),0.0001),
                    ano = %s
                WHERE id=%s
                """
            entrada = [nombre, geom, EPSG_CODE, ano, idValue]
   
            self.cur.execute(cons_update, entrada)

            rows = self.cur.rowcount

            self.conn.commit()
            self.disconnect()

            return {"ok":True,"message":"Data updated",
            "data":[{"rows_updated":rows}]}
        
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
                lau.vertices
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
                lau.vertices
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