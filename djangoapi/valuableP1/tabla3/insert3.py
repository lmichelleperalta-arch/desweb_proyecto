import psycopg

from myLib import p1settings
#Creamos la conexion
def connect():
    conn = psycopg.connect(dbname= p1settings.POSTGRES_DB, 
                        user = p1settings.POSTGRES_USER, 
                        password = p1settings.POSTGRES_PASSWORD, 
                        host = p1settings.POSTGRES_HOST, 
                        port = p1settings.POSTGRES_PORT)

#    conn.close()
    return conn

print("Connected")

#Hacemos na consulta basica
def insert3():
    conn = connect()
    cur = conn.cursor()
    consv="""
            INSERT INTO lau.lugares
                (nombre, geom)
            VALUES
                (%s,st_geometryfromtext(%s,25830))
            """
    #PARA EVITAR ENTRADA DE COSAS MALICIOSAS SE PONE %s y los valores se ponen aparte
    #Con una lista metemos ls valores
    cur.execute(consv, ['CentroideFalso','POINT (391035.85 4304833.42)'])
    #Cerramos el cursor
    conn.commit()
    cur.close()
    conn.close()
    print("Inserted")