import xml.etree.ElementTree as ET 
from lista_simple import Lista_simple
from objetos import*

lista_organismos = Lista_simple() # Creacion de una lista simple para organismos mediante la clase lista simple
lista_muestras = Lista_simple() 

print('Bienvenido')
ruta = input('Ingrese la ruta del archivo xml:\r\n')

archivo = ET.parse(ruta)
raiz = archivo.getroot()

contador = 0
for hijo in raiz:
    if contador == 0:
        for organismo in hijo:
            codigo = organismo.find('codigo').text
            nombre = organismo.find('nombre').text
            nuevo_organismo = Organismo(codigo,nombre)
            lista_organismos.insertar(nuevo_organismo)
        contador += 1
    else:
        for muestra in hijo:
            codigo = muestra.find('codigo').text
            descripcion = muestra.find('descripcion').text
            filas = muestra.find('filas').text
            columnas = muestra.find('columnas').text
            celdas_vivas = muestra.find('listadoCeldasVivas').text
            nueva_muestra = Muestra(codigo, descripcion, filas, columnas)
            for celda in celdas_vivas:
                fila = filas.find('fila').text
                columna = columna.find('columna').text
                codigo_organismo = codigo_organismo('codigo_organismo').text
                nueva_celda = Celda(fila, columna, codigo_organismo)
                nueva_muestra.lista_celdas_vivas.insertar(nueva_celda)
            lista_muestras.insertar(nueva_muestra)
            

lista_muestras.imprimir()


