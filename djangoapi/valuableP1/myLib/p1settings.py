import os

##Crear parametros de conexion
# POSTGRES_USER = os.getenv('POSTGRES_USER') # podemos asignar la variable de entorno que definimos en .env
# POSTGRES_PASSWORD = 'postgres'
# POSTGRES_HOST = 'postgis' # ES El nombre del servicio porque estamos dentro del docker
# POSTGRES_PORT = 5432
# POSTGRES_DB = 'postgres'

POSTGRES_USER = os.getenv('POSTGRES_USER') # podemos asignar la variable de entorno que definimos en .env
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = 'tarea1'