import pymysql

def obtener_conexion():
    return pymysql.connect(host='localhost', user='root', password='', db='protendencias', port= 3307, cursorclass=pymysql.cursors.DictCursor)
#cursorclass = 'DictCursor'