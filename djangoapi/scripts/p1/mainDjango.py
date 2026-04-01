"""
This files can be executed in the following way:

    python manage.py runscript script_without_extension

The scripts must be in the folder scripts

You can pass parameters to the scritp in the following way:+

    python manage.py runscript mainDjango --script-args nombreTabla funcion

All parameters are received in string format

"""
import sys
from scripts.p1.catastrodjModels import prediodj
from scripts.p1.catastrodjModels import callesdj
from scripts.p1.catastrodjModels import iglesiasdj

def run(*args):
    """python manage.py runscript scripts.p1.mainDjango --script-args tabla operacion"""
    print(__file__)
    print("Operacion realizada con exito")

    if len(args) == 2:
        tableName = args[0]
        functionName = args[1]     
    else:
        print("Error: You mus give two parameters tableName and functionName to execute the addecuate function.")
        sys.exit(0)

    if tableName not in ["catastrodj_predio", "catastrodj_iglesias", "catastrodj_calles"]:
        print("Error: The available table names are catastrodj_iglesias,catastrodj_predio, catastrodj_calles ")
        sys.exit(0)
    
    if functionName not in ["insert", "selectAsTuples", "selectAsDicts", "update", "delete", "selectallAsDicts" ]:
        print("Error the available function names are insert, selectAsDicts,selectallAsDicts, delete, selectAsTuples,  or update")
        sys.exit(0)

    if tableName == "catastrodj_predio":
        
        if functionName=="insert":
            d_of_values= {
            'description':'Plaza del Ayuntamiento', 
            #'area': 1000,
            #'perimeter': 100,
            'nombre':'Plaza del Ayuntamiento de Valencia',
            "geom": "POLYGON((725651.91608285112306476 4372246.56803378276526928, 725688.79413162509445101 4372252.33022890333086252, 725696.8612047943752259 4372249.56437524501234293, 725704.92827796365600079 4372247.48998500220477581, 725721.06242430221755058 4372242.64974110014736652, 725733.04779015376698226 4372202.08388744946569204, 725708.38559503620490432 4372199.08754598628729582, 725685.10632674768567085 4372196.78266793768852949, 725653.0685218753060326 4372197.24364354740828276, 725651.91608285112306476 4372246.56803378276526928))"}
            print(prediodj.insert(d_of_values))

        elif functionName=="selectAsDicts":
            d_of_values= {'id':6 }
            print(prediodj.selectAsDicts(d_of_values))

        elif functionName=="selectallAsDicts":
            print(prediodj.selectallAsDicts())

        elif functionName=="selectAsTuples":
            print(prediodj.selectAsTuples())

        elif functionName=="update":
            d_of_values= {
            'id':6,
            'description':'Plaza de la Mercé', 
            'nombre':'Plaza de la Mercé',
            "geom": "POLYGON((725548.11759233695920557 4372529.77307381853461266, 725544.2847252048086375 4372506.64370319340378046, 725563.18472520145587623 4372503.33950738981366158, 725579.17703289084602147 4372498.97796892933547497, 725582.08472519810311496 4372524.48636053316295147, 725548.11759233695920557 4372529.77307381853461266))"}
             
            print(prediodj.update(d_of_values))

        elif functionName=="delete":
            d_of_values= {
            'id':5 }
            print(prediodj.delete(d_of_values))

    elif tableName=="catastrodj_calles":
        
        if functionName=="insert":
            d_of_values= {
            'description':'Carrer del Ing Fausto Elio', 
            'estado':'Excelente',
            'nombre':"Calle del Ing Fausto Elio",
            "geom": 'LINESTRING(729364.82720704528037459 4373071.69422757066786289, 729388.08874550263863057 4373291.62150025926530361, 729418.75168256019242108 4373512.60611560381948948, 729481.13489933218806982 4373887.96275889500975609, 729506.51112310402095318 4374047.62150012515485287, 729512.85517904697917402 4374063.481639982201159, 729522.37126296130008996 4374078.28443718235939741)' }
            print(callesdj.insert(d_of_values))

        elif functionName=="selectAsDicts":
            d_of_values= {'id':3 }
            print(callesdj.selectAsDicts(d_of_values))
        
        elif functionName=="selectallAsDicts":
            print(callesdj.selectallAsDicts())

        elif functionName=="selectAsTuples":
            print(callesdj.selectAsTuples())

        elif functionName=="update":
            d_of_values= {
            'id':2,
            'description':'Cam Campiño de Altobuey', 
            'estado':'Excelente',
            'nombre':"Avda Blazco Ibañez",
            "geom": 'LINESTRING(729189.30832595785614103 4372357.98793399147689342, 729024.36287144164089113 4372420.37115076370537281, 728219.72510934644378722 4372699.50961225293576717, 728167.9153191460063681 4372720.65646539535373449, 728154.16986460296902806 4372705.85366819519549608, 728129.85098348837345839 4372698.45226959511637688, 728110.81881565961521119 4372718.54178008157759905, 728099.1880464309360832 4372725.94317868165671825, 727640.30133322556503117 4372893.00331851188093424, 727436.23420039471238852 4372961.73059122730046511)'}
            #"geom": 'LINESTRING(729053.88182943419087678 4372724.38670734222978354, 729188.0125611413968727 4373107.95353661011904478)' }
            print(callesdj.update(d_of_values))

        elif functionName=="delete":
            d_of_values= {
            'id':1 }
            print(callesdj.delete(d_of_values))

    elif tableName=="catastrodj_iglesias":
       
        if functionName=="insert":
            d_of_values= {
            'description':'Iglesia la Merced', 
            'ano':2014,
            'nombre':"Capilla la Merced",
            "geom": 'POINT(725694.0 4372215.2)'}
            print(iglesiasdj.insert(d_of_values))
            
        elif functionName in ["selectAsDicts"]:
            d_of_values= {'id':3 }
            print(iglesiasdj.selectAsDicts(d_of_values))

        elif functionName in ["selectallAsDicts"]:
            print(iglesiasdj.selectallAsDicts())

        elif functionName in ["selectAsTuples"]:
            print(iglesiasdj.selectAsTuples())

        elif functionName in ["update"]:
            d_of_values= {
            'id':4,
            'description':'Capilla UPV Campus Vera', 
            'ano':1988,
            'nombre':"Capilla UPV Campus Vera",
            "geom": 'POINT(725694.0 4372215.2)' }
            print(iglesiasdj.update(d_of_values))

        elif functionName in [ "delete"]:
            d_of_values= {
            'id':1 }
            print(iglesiasdj.delete(d_of_values))

if __name__ == "__main__":
    run()

