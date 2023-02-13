class Nodo():
    def __init__(self, valor = None, id = -1):
        self.valor = valor
        self.siguiente = None
        self.id = id

    def get_valor(self):
        return str(self.valor)
        
    
    def set_valor(self, valor):
        self.valor = valor
    
    def get_sigueinte(self):
        return self.siguiente
    
    def set_siguiente(self, siguiente):
        self.siguiente = siguiente

    print("hola mundo")