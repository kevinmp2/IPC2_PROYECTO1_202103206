from nodo import Nodo
import random

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
            print(actual.dato.fila)
            print(actual.dato.columna)
            print(actual.dato.codigo_organismo)
            actual = actual.siguiente

    def recorrer(self):
        actual = self.primero
        while actual:
            yield actual.dato  
            actual = actual.siguiente
