from lista_simple import Lista_simple


class Organismo():
    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre
    
class Muestra():
    def __init__(self, codigo, descripcion, filas, columnas):
        self.codigo = codigo
        self.descripcion = descripcion
        self.filas = filas 
        self.columnas = columnas
        self.lista_celdas_vivas = Lista_simple()

class Celda():
    def __init__(self, fila, columna, codigo_organismo):
        self.fila = fila 
        self.columna = columna
        self.codigo_organismo = codigo_organismo
        