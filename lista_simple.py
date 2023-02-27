from nodo import Nodo

class Lista_simple:

    def __init__(self):
        self.primero = None
        self.ultimo = None

    def insertar(self, dato):
        nodo = Nodo(dato)
        if self.primero is None:
            self.primero = nodo
            self.ultimo = self.primero
        else:
            self.ultimo.siguiente = nodo
            self.ultimo = nodo
    
    def imprimir(self):
        actual = self.primero
        while actual:
            print(actual.dato.codigo)
            actual = actual.siguiente


