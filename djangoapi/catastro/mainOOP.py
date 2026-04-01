import sys
from calles.callesOOP import CallesOOP
from vertices.verticesOOP import VerticesOOP
from predio.predioOOP import PredioOOP
from myLib.p1Settings import EPSG_CODE

def main():
    # sys.argv[0] es siempre el nombre del archivo (main.py)
    # Por eso verificamos que haya al menos 3 elementos (nombre + p1 + p2)
    if len(sys.argv) == 3:
        tableName = sys.argv[1]
        functionName = sys.argv[2]     
    else:
        print("Error: You mus give two parameters tableName and functionName to execute the addecuate function.")
        sys.exit(0)


    if tableName not in ["calles", "vertices", "predio"]:
        print("Error: The available table names are calles, vertices, predio")
        sys.exit(0)
    
    if functionName not in ["insert", "select", "selectAsDict", "update", "delete", "selectAsTuple"]:
        print("Error the available function names are insert, select, delete or update")
        sys.exit(0)

    if tableName == "calles":
        b=CallesOOP()
        if functionName=="insert":
            params = {
                    "nombre": "Calle Camino de Vera",
                    "longitud":"1498.1",
                    "estado": "Regular",
                    "geom": "LINESTRING(391037 4304834,391040 4304837)"}
                
            res = b.insert(params)
            print(res)
        elif functionName=="selectAsDict":
            res = b.selectAsDict({"id":1})
            print(res)
        elif functionName=="selectAsTuple":
            res = b.selectAsTuple({"id":1})
            print(res)
        elif functionName=="update":
            params = {
                "id":10,"nombre":"Calle Test Update",
                    "longitud":200,"estado":"Bueno",
                    "geom":"LINESTRING(3910457 4304954,391150 4304957)"}
            res = b.update(params)
            print(res)
        elif functionName=="delete":
            res = b.delete({"id":13})
            print(res)

    elif tableName=="vertices":
        b=VerticesOOP()
        if functionName=="insert":
            params = {
                "nombre": "Vertice Prueb",
                "geom": "POINT(391117.21  4304784.80)",
                "ano": "1985"}
            res = b.insert(params)
            print(res)
        elif functionName=="selectAsDict":
            res = b.selectAsDict({"id":2})
            print(res)
        elif functionName=="selectAsTuple":
            res = b.selectAsTuple({"id":2})
            print(res)
        elif functionName=="update":
            params = {
                "id":4,"nombre": "Vertice Test",
                "geom": "POINT(391077.43 4304847.92)",
                "ano": "1985"}
            res = b.update(params)
            print(res)
        elif functionName=="delete":
            res = b.delete({"id":2})
            print(res)

    elif tableName=="predio":
            b=PredioOOP()
            if functionName=="insert":
                params = {
                    "nombre": "Predio 3",
                    "direccion":"Calle Turia 85",
                    "codman": "C033",
                    "geom": "POLYGON((391081.1 4304779.1, 391132.8 4304807.2, 391134.7 4304776.8, 391081.1 4304779.1))"}
                
                res = b.insert(params)
                print(res)
            elif functionName=="select":
                b.select()
            elif functionName=="selectAsDict":
                res = b.selectAsDict({"id":6})
                print(res)
            elif functionName=="selectAsTuple":
                res = b.selectAsTuple({"id":2})
                print(res)
            elif functionName=="update":
                params = {"id":6,"nombre": "Predio 86",
                    "direccion":"Calle Blazco I. 11","codman": "A011",
                    "geom": "POLYGON((391081.1 4304779.1, 391132.8 4304807.2, 391134.7 4304776.8, 391081.1 4304779.1))"}
                res = b.update(params)
                print(res)
            elif functionName=="delete":
                res = b.delete({"id":2})
                print(res)

if __name__ == "__main__":
    main()

