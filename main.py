import xml.etree.ElementTree as ET 
from lista_simple import Lista_simple
from objetos import*
import os 
import random


lista_organismos = Lista_simple() # Creacion de una lista simple para organismos 
lista_muestras = Lista_simple() # Creacion de una lista simple para las muestras
lista_celdas_pintadas = Lista_simple() # Creacion de una lista simple para las celdas vivas
lista_celda_pintadas_actualizadas = Lista_simple()
lista_general = Lista_simple()

fila_doctor = 0
columna_doctor = 0
color_doctor = ''

def app():

    menu_principal()

    preguntar = True

    while preguntar:
        opcion = int(input('Ingrese una opcion:\r\n'))
        if opcion == 1:
            filas = int(input('Ingrese el numero de filas:\r\n'))
            columnas = int(input('Ingrese el numero de columnas:\r\n'))

            crear_tablero(filas,columnas)

            print('░═══════════════Tablero creado exitosamente═══════════════░')

        elif opcion == 2:
            
            cargar_archivo()

            colores = ['antiquewhite4','aqua','chartreuse1','blue','orangered','yellow','deepskyblue','darkorange1','darkslategray1','deeppink','fuchsia','cadetblue1','chartreuse2','cornsilk','gold','forestgreen','gray10','gray2','indianred1','indigo','ivory1','lime','lightsalmon1','lightblue3','lightskyblue','seagreen1','slateblue1','thistle1','turquoise','webmaroon','aqua']
            for muestra in lista_muestras.recorrer():
                color = random.choice(colores)
                muestra.color = color 
                filas = muestra.filas
                columnas = muestra.columnas

                for celda in muestra.lista_celdas_vivas.recorrer():
                    celda_nueva = Celda(celda.fila, celda.columna, celda.codigo_organismo)
                    celda_nueva.color = color
                    lista_celdas_pintadas.insertar(celda_nueva)

            pintar_tablero()

        elif opcion == 3:
             fila = int(input('Ingrese la fila: '))
             columna = int(input('Ingrese la columna: '))
             organismo = str(input('Ingrese el codigo del organismo: '))
             
             global fila_doctor
             fila_doctor = fila

             global columna_doctor
             columna_doctor = columna

             color = ''

             for celda in lista_celdas_pintadas.recorrer():
                 if organismo == celda.codigo_organismo:
                     color = celda.color
                 if int(celda.fila) == fila and int(celda.columna) == columna:
                     print('Celda ocupado, intente de nuevo')
                     return
             celda_nueva = Celda(fila, columna, organismo)
             celda_nueva.color = color 
             lista_celdas_pintadas.insertar(celda_nueva)

             global color_doctor 
             color_doctor = color

             pintar_tablero()

             menu_principal()

        elif opcion == 4:
            actualizar_tablero()
            menu_principal()
        elif opcion == 5:
            crear_xml()
            menu_principal()
        elif opcion == 6:
            print('Programa, finalizado')
            break

def cargar_archivo():
    ruta = input('Ingrese la ruta del archivo:\r\n')
    archivo = ET.parse(ruta)
    raiz = archivo.getroot()

    contador = 0
    for hijo in raiz:
        if contador == 0:
            for organismo in hijo:
                codigo = organismo.findtext('codigo')
                nombre = organismo.findtext('nombre')
                nuevo_organismo = Organismo(codigo,nombre)
                lista_organismos.insertar(nuevo_organismo)
        else:
            for muestra in hijo:
                codigo = muestra.findtext('codigo')
                descripcion = muestra.findtext('descripcion')
                filas = muestra.findtext('filas')
                columnas = muestra.findtext('columnas')
                celdas_vivas = muestra.find('listadoCeldasVivas')
                nueva_muestra = Muestra(codigo, descripcion, filas, columnas)
                for celda in celdas_vivas:
                    fila = celda.findtext('fila')
                    columna = celda.findtext('columna')
                    codigo_organismo = celda.findtext('codigoOrganismo')
                    nueva_celda = Celda(fila, columna, codigo_organismo)
                    nueva_muestra.lista_celdas_vivas.insertar(nueva_celda)
                lista_muestras.insertar(nueva_muestra)
        contador += 1


def crear_tablero(filas, columnas):

    archivo = open('grafica.dot', 'w')
    archivo.write('digraph G {a0 [shape=none label=<<TABLE border="3" cellspacing="3" cellpadding="20">')

    for x in range(filas):
        archivo.write('<TR>')
        for y in range(columnas):
            archivo.write(' <TD> </TD>')
        archivo.write('</TR>')

    archivo.write('</TABLE>>];}')
    archivo.close()
    os.system('dot.exe -Tpng grafica.dot -o grafica.png')
    os.startfile('grafica.png')

def pintar_tablero():
   
    with open('grafica.dot', 'w') as archivo:
        archivo.write('\ndigraph G {a0 [shape=record label=<<TABLE border="3" cellspacing="3" cellpadding="20">')
        for muestra in lista_muestras.recorrer():
            filas = muestra.filas
            columnas = muestra.columnas
            for x in range(int(filas)):
                archivo.write('\n<TR>')
                for y in range(int(columnas)):
                    celda_pintada = False
                    for celda in lista_celdas_pintadas.recorrer():
                        if int(celda.fila) == x and int(celda.columna) == y:
                            archivo.write('\n<TD bgcolor="{}"> </TD>'.format(celda.color))
                            celda_pintada = True
                            break
                        else:
                            celda_pintada = False
                    if not celda_pintada:
                        archivo.write('\n<TD> </TD>')
                archivo.write('\n</TR>')
            break
        archivo.write('\n</TABLE>>];}')
        archivo.close()
        os.system('dot.exe -Tpng grafica.dot -o grafica.png')
        os.startfile('grafica.png')



def actualizar_tablero():
    global lista_general
    lista_general = Lista_simple()
    global fila_doctor
    global columna_doctor
    global color_doctor
    global lista_celda_pintadas_actualizadas

    pintar1 = False

    celda1 = buscar_celda(fila_doctor - 1,columna_doctor - 1)
    if celda1 != None:
        if celda1.color != color_doctor:
            f = fila_doctor - 1
            c = columna_doctor - 1
            celdita = buscar_celda(f - 1, c - 1)
            celda_agregada = Celda(celda1.fila, celda1.columna, celda1.codigo_organismo)
            celda_agregada.color = color_doctor
            lista_celda_pintadas_actualizadas.insertar(celda_agregada)

            while celdita != None:
                pintar1 = False
                #print(celdita.color)
                if celdita.color != color_doctor:
                    #print('Entro a celdita')
                    f = f - 1
                    c = c - 1 
                    celda_agregada = Celda(celdita.fila, celdita.columna, celdita.codigo_organismo)
                    celda_agregada.color = color_doctor
                    lista_celda_pintadas_actualizadas.insertar(celda_agregada)
                    celdita = buscar_celda(f - 1, c - 1)

                elif celdita.color == color_doctor:
                    pintar1 = True
                    #print(celdita.color, 'Eliffffffffffffffffffffffffffffffffffffff')
                    for c in lista_celda_pintadas_actualizadas.recorrer():
                        lista_general.insertar(c)
                    break
    #print('Pintaaaaarrrrrrr', pintar)
    #if pintar == True:
    global lista_celdas_pintadas

    for x in lista_celdas_pintadas.recorrer():
        x2 = buscar_celda_general(x.fila, x.columna)
        if x2 == None and pintar1 == False and x.fila == fila_doctor and x.columna == columna_doctor:
            continue
        elif x2 == None:  
            lista_general.insertar(x)
            
    lista_celdas_pintadas = lista_general

    celda2 = buscar_celda(fila_doctor-1,columna_doctor)
    lista_general = Lista_simple()
    nueva = Lista_simple()
    lista_celdas_pintadas_actualizadas = nueva

    pintar2 = False

    if celda2 != None:
        if celda2.color != color_doctor:
            f = fila_doctor - 1
            c = columna_doctor 
            celdita = buscar_celda(f - 1, c)
            celda_agregada = Celda(celda2.fila, celda2.columna, celda2.codigo_organismo)
            celda_agregada.color = color_doctor
            lista_celda_pintadas_actualizadas.insertar(celda_agregada)

            while celdita != None:
                pintar2 = False
                #print(celdita.color)
                if celdita.color != color_doctor:
                    #print('Entro a celdita')
                    f = f - 1
                    c = c  
                    celda_agregada = Celda(celdita.fila, celdita.columna, celdita.codigo_organismo)
                    celda_agregada.color = color_doctor
                    lista_celda_pintadas_actualizadas.insertar(celda_agregada)
                    celdita = buscar_celda(f - 1, c)

                elif celdita.color == color_doctor:
                    pintar2 = True
                    #print(celdita.color, 'Eliffffffffffffffffffffffffffffffffffffff')
                    for c in lista_celda_pintadas_actualizadas.recorrer():
                        lista_general.insertar(c)
                    break
    #print('Pintaaaaarrrrrrr', pintar)
    #if pintar == True:
    for x in lista_celdas_pintadas.recorrer():
        x2 = buscar_celda_general(x.fila, x.columna)
        if x2 == None and pintar2 == False and x.fila == fila_doctor and x.columna == columna_doctor:
            continue
        elif x2 == None:  
            lista_general.insertar(x)

    lista_celdas_pintadas = lista_general

    celda3 = buscar_celda(fila_doctor+1,columna_doctor+1)
    lista_general = Lista_simple()
    nueva = Lista_simple()
    lista_celdas_pintadas_actualizadas = nueva

    pintar3 = False

    if celda3 != None:
        if celda3.color != color_doctor:
            f = fila_doctor + 1
            c = columna_doctor + 1
            celdita = buscar_celda(f + 1, c + 1)
            celda_agregada = Celda(celda3.fila, celda3.columna, celda3.codigo_organismo)
            celda_agregada.color = color_doctor
            lista_celda_pintadas_actualizadas.insertar(celda_agregada)

            while celdita != None:
                pintar3 = False
                #print(celdita.color)
                if celdita.color != color_doctor:
                    #print('Entro a celdita')
                    f = f + 1
                    c = c + 1
                    celda_agregada = Celda(celdita.fila, celdita.columna, celdita.codigo_organismo)
                    celda_agregada.color = color_doctor
                    lista_celda_pintadas_actualizadas.insertar(celda_agregada)
                    celdita = buscar_celda(f +1, c + 1)

                elif celdita.color == color_doctor:
                    pintar3 = True
                    #print(celdita.color, 'Eliffffffffffffffffffffffffffffffffffffff')
                    for c in lista_celda_pintadas_actualizadas.recorrer():
                        lista_general.insertar(c)
                    break
    #print('Pintaaaaarrrrrrr', pintar)
    #if pintar == True:
    for x in lista_celdas_pintadas.recorrer():
        x2 = buscar_celda_general(x.fila, x.columna)
        if x2 == None and pintar3 == False and x.fila == fila_doctor and x.columna == columna_doctor:
            continue
        elif x2 == None:  
            lista_general.insertar(x)

    lista_celdas_pintadas = lista_general

    celda4 = buscar_celda(fila_doctor,columna_doctor-1)
    lista_general = Lista_simple()
    nueva = Lista_simple()
    lista_celdas_pintadas_actualizadas = nueva

    pintar4 = False

    if celda4 != None:
        if celda4.color != color_doctor:
            f = fila_doctor 
            c = columna_doctor - 1 
            celdita = buscar_celda(f, c - 1)
            celda_agregada = Celda(celda4.fila, celda4.columna, celda4.codigo_organismo)
            celda_agregada.color = color_doctor
            lista_celda_pintadas_actualizadas.insertar(celda_agregada)

            while celdita != None:
                pintar4 = False
                #print(celdita.color)
                if celdita.color != color_doctor:
                    #print('Entro a celdita')
                    f = f 
                    c = c - 1 
                    celda_agregada = Celda(celdita.fila, celdita.columna, celdita.codigo_organismo)
                    celda_agregada.color = color_doctor
                    lista_celda_pintadas_actualizadas.insertar(celda_agregada)
                    celdita = buscar_celda(f, c - 1)

                elif celdita.color == color_doctor:
                    pintar4 = True
                    #print(celdita.color, 'Eliffffffffffffffffffffffffffffffffffffff')
                    for c in lista_celda_pintadas_actualizadas.recorrer():
                        lista_general.insertar(c)
                    break
    #print('Pintaaaaarrrrrrr', pintar)
    #if pintar == True:
    for x in lista_celdas_pintadas.recorrer():
        x2 = buscar_celda_general(x.fila, x.columna)
        if x2 == None and pintar4 == False and x.fila == fila_doctor and x.columna == columna_doctor:
            continue
        elif x2 == None:  
            lista_general.insertar(x)

    lista_celdas_pintadas = lista_general
        
    celda5 = buscar_celda(fila_doctor,columna_doctor+1)
    lista_general = Lista_simple()
    nueva = Lista_simple()
    lista_celdas_pintadas_actualizadas = nueva

    pintar5 = False

    if celda5 != None:
        if celda5.color != color_doctor:
            f = fila_doctor 
            c = columna_doctor  + 1
            celdita = buscar_celda(f , c + 1)
            celda_agregada = Celda(celda5.fila, celda5.columna, celda5.codigo_organismo)
            celda_agregada.color = color_doctor
            lista_celda_pintadas_actualizadas.insertar(celda_agregada)

            while celdita != None:
                pintar5 = False
                #print(celdita.color)
                if celdita.color != color_doctor:
                    #print('Entro a celdita')
                    f = f 
                    c = c + 1 
                    celda_agregada = Celda(celdita.fila, celdita.columna, celdita.codigo_organismo)
                    celda_agregada.color = color_doctor
                    lista_celda_pintadas_actualizadas.insertar(celda_agregada)
                    celdita = buscar_celda(f, c + 1)

                elif celdita.color == color_doctor:
                    pintar5 = True
                    #print(celdita.color, 'Eliffffffffffffffffffffffffffffffffffffff')
                    for c in lista_celda_pintadas_actualizadas.recorrer():
                        lista_general.insertar(c)
                    break
    #print('Pintaaaaarrrrrrr', pintar)
    #if pintar == True:
    for x in lista_celdas_pintadas.recorrer():
        x2 = buscar_celda_general(x.fila, x.columna)
        if x2 == None and pintar5 == False and x.fila == fila_doctor and x.columna == columna_doctor:
           continue
        elif x2 == None:  
            lista_general.insertar(x)

    lista_celdas_pintadas = lista_general

    celda6 = buscar_celda(fila_doctor+1,columna_doctor-1)
    lista_general = Lista_simple()
    nueva = Lista_simple()
    lista_celdas_pintadas_actualizadas = nueva

    pintar6 = False

    if celda6 != None:
        if celda6.color != color_doctor:
            f = fila_doctor + 1
            c = columna_doctor - 1
            celdita = buscar_celda(f + 1, c - 1)
            celda_agregada = Celda(celda6.fila, celda6.columna, celda6.codigo_organismo)
            celda_agregada.color = color_doctor
            lista_celda_pintadas_actualizadas.insertar(celda_agregada)

            while celdita != None:
                pintar6 = False
                #print(celdita.color)
                if celdita.color != color_doctor:
                    #print('Entro a celdita')
                    f = f + 1
                    c = c  - 1
                    celda_agregada = Celda(celdita.fila, celdita.columna, celdita.codigo_organismo)
                    celda_agregada.color = color_doctor
                    lista_celda_pintadas_actualizadas.insertar(celda_agregada)
                    celdita = buscar_celda(f + 1, c - 1)

                elif celdita.color == color_doctor:
                    pintar6 = True
                    #print(celdita.color, 'Eliffffffffffffffffffffffffffffffffffffff')
                    for c in lista_celda_pintadas_actualizadas.recorrer():
                        lista_general.insertar(c)
                    break
    #print('Pintaaaaarrrrrrr', pintar)
    #if pintar == True:
    for x in lista_celdas_pintadas.recorrer():
        x2 = buscar_celda_general(x.fila, x.columna)
        if x2 == None and pintar6 == False and x.fila == fila_doctor and x.columna == columna_doctor:
            continue
        elif x2 == None:  
            lista_general.insertar(x)

    lista_celdas_pintadas = lista_general

    celda7 = buscar_celda(fila_doctor+1,columna_doctor)
    lista_general = Lista_simple()
    nueva = Lista_simple()
    lista_celdas_pintadas_actualizadas = nueva

    pintar7 = False

    if celda7 != None:
        if celda7.color != color_doctor:
            f = fila_doctor + 1
            c = columna_doctor 
            celdita = buscar_celda(f + 1, c)
            celda_agregada = Celda(celda7.fila, celda7.columna, celda7.codigo_organismo)
            celda_agregada.color = color_doctor
            lista_celda_pintadas_actualizadas.insertar(celda_agregada)

            while celdita != None:
                pintar7 = False
                #print(celdita.color)
                if celdita.color != color_doctor:
                    #print('Entro a celdita')
                    f = f + 1
                    c = c  
                    celda_agregada = Celda(celdita.fila, celdita.columna, celdita.codigo_organismo)
                    celda_agregada.color = color_doctor
                    lista_celda_pintadas_actualizadas.insertar(celda_agregada)
                    celdita = buscar_celda(f + 1, c)

                elif celdita.color == color_doctor:
                    pintar7 = True
                    #print(celdita.color, 'Eliffffffffffffffffffffffffffffffffffffff')
                    for c in lista_celda_pintadas_actualizadas.recorrer():
                        lista_general.insertar(c)
                    break
    #print('Pintaaaaarrrrrrr', pintar)
    #if pintar == True:
    for x in lista_celdas_pintadas.recorrer():
        x2 = buscar_celda_general(x.fila, x.columna)
        if x2 == None and pintar7 == False and x.fila == fila_doctor and x.columna == columna_doctor:
            continue
        elif x2 == None:  
            lista_general.insertar(x)

    lista_celdas_pintadas = lista_general

    celda8 = buscar_celda(fila_doctor+1,columna_doctor+1)
    lista_general = Lista_simple()
    nueva = Lista_simple()
    lista_celdas_pintadas_actualizadas = nueva

    pintar8 = False

    if celda8 != None:
        if celda8.color != color_doctor:
            f = fila_doctor + 1
            c = columna_doctor + 1
            celdita = buscar_celda(f + 1, c + 1)
            celda_agregada = Celda(celda8.fila, celda8.columna, celda8.codigo_organismo)
            celda_agregada.color = color_doctor
            lista_celda_pintadas_actualizadas.insertar(celda_agregada)

            while celdita != None:
                pintar8 = False
                #print(celdita.color)
                if celdita.color != color_doctor:
                    #print('Entro a celdita')
                    f = f + 1
                    c = c  + 1
                    celda_agregada = Celda(celdita.fila, celdita.columna, celdita.codigo_organismo)
                    celda_agregada.color = color_doctor
                    lista_celda_pintadas_actualizadas.insertar(celda_agregada)
                    celdita = buscar_celda(f + 1, c + 1)

                elif celdita.color == color_doctor:
                    pintar8 = True
                    #print(celdita.color, 'Eliffffffffffffffffffffffffffffffffffffff')
                    for c in lista_celda_pintadas_actualizadas.recorrer():
                        lista_general.insertar(c)
                    break
    #print('Pintaaaaarrrrrrr', pintar)
    for x in lista_celdas_pintadas.recorrer():
        x2 = buscar_celda_general(x.fila, x.columna)
        if x2 == None and pintar8 == False and x.fila == fila_doctor and x.columna == columna_doctor:
            continue
        elif x2 == None:  
            lista_general.insertar(x)
        
    lista_celdas_pintadas = lista_general

    pintar_tablero()

def pintar_tablero_actualizado():
    with open('grafica.dot', 'w') as archivo:
            archivo.write('\ndigraph G {a0 [shape=record label=<<TABLE border="3" cellspacing="3" cellpadding="20">')
            for muestra in lista_muestras.recorrer():
                filas = muestra.filas
                columnas = muestra.columnas
                for x in range(int(filas)):
                    archivo.write('\n<TR>')
                    for y in range(int(columnas)):
                        celda_pintada = False
                        for celda in lista_general.recorrer():
                            if int(celda.fila) == x and int(celda.columna) == y:
                                archivo.write('\n<TD bgcolor="{}"> </TD>'.format(celda.color))
                                celda_pintada = True
                                break
                            else:
                                celda_pintada = False
                        if not celda_pintada:
                            archivo.write('\n<TD> </TD>')
                    archivo.write('\n</TR>')
                break
            archivo.write('\n</TABLE>>];}')
            archivo.close()
            os.system('dot.exe -Tpng grafica.dot -o grafica.png')
            os.startfile('grafica.png')


def buscar_celda(fila, columna):
    for celda in lista_celdas_pintadas.recorrer():
        if int(celda.fila) == fila and int(celda.columna) == columna:
            return celda
    return None


def buscar_celda_general(fila, columna):
    for celda in lista_general.recorrer():
        if int(celda.fila) == fila and int(celda.columna) == columna:
            return celda
    return None

def crear_xml():
    global lista_organismos
    global lista_muestras
    global lista_celdas_pintadas


    raiz = ET.Element('datosMarte')
    listaOrganismos = ET.SubElement(raiz,'listaOrganismos')
    for o in lista_organismos.recorrer():
         organismo = ET.SubElement(listaOrganismos, 'organismo')
         codigo = ET.SubElement(organismo, 'codigo')
         codigo.text = o.codigo
         nombre = ET.SubElement(organismo, 'nombre')
         nombre.text = o.nombre
    
    listaMuestras = ET.SubElement(raiz, 'listaMuestras')
    for m in lista_muestras.recorrer():
        muestra = ET.SubElement(listaMuestras, 'muestra')
        codigo = ET.SubElement(muestra, 'codigo')
        codigo.text = m.codigo
        descripcion = ET.SubElement(muestra, 'descripcion')
        descripcion.text = m.descripcion
        filas = ET.SubElement(muestra, 'filas')
        filas.text = m.filas
        columnas = ET.SubElement(muestra, 'columnas')
        columnas.text = m.columnas
        listadoCeldasVivas = ET.SubElement(muestra, 'listadoCeldasVivas')
        for c in lista_celdas_pintadas.recorrer():
            if c.color == m.color:
                celdaViva = ET.SubElement(listadoCeldasVivas, 'celdaViva')
                fila = ET.SubElement(celdaViva, 'fila')
                fila.text = c.fila
                columna = ET.SubElement(celdaViva, 'columna')
                columna.text = c.columna
                codigoOrganismo = ET.SubElement(celdaViva, 'codigoOrganismo')
                codigoOrganismo.text = c.codigo_organismo
    
    data = ET.tostring(raiz)
    archivo = open('xmlSalida.xml', 'wb')
    archivo.write(data)

def menu_principal():
    print('╔═══════════════Menu Principal═══════════════╗')
    print('║    1. Ingrese el tamaño del tablero        ║')
    print('║    2. Cargar el archivo xml                ║')
    print('║    3. Realizar experimento                 ║')
    print('║    4. Actualizar tablero                   ║')
    print('║    5. Generar XML-Salida                   ║')
    print('║    6. Salir                                ║')
    print('╚════════════════════════════════════════════╝')

app()






