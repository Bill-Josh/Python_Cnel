# Este módulo proporciona una forma portátil de utilizar la funcionalidad dependiente del sistema operativo.
import os
import re
from datetime import datetime
import json


# funcion para invocar al menu principal y mostrar las opciones de usuario
def menuprincipal():
    os.system('clear')
    print("BIENVENIDOS AL SISTEMA DE CNEL\n")
    print(" ** MENU PRINCIPAL **")
    print("\t1. Administrar Medidores")
    print("\t2. Reportes")
    print("\t3. Diccionario")
    print("\t4. Salir")


# funcion para invocar el menu de registro de medidores
def menumedidores():
    print("** ADMINISTRAR MEDIDORES **\n")
    # Se solicita al usuario ingresar los datos especificados.
    print("Ingrese los datos del medidor\n")
    # Se guardan los datos ingresados en el input 'medidor'
    medidor = input("Favor ingrese un codigo, tipo, año, propietario y cantidad de planillas, "
                    "\nseparados por un carácter especial, un guion(-). Para terminar escribir 'Salir':")
    # Ejemplo de datos correctos:
    # M101-digital-2015-rafael rivadeneira-5
    # K202-ANALGICO-2018-eduardo campos-2
    # Z335-Digital-2013-KAREN DELGADO-1
    medfinal = medidor.title()  # .title regresa las palabras con la primera letra Mayuscula y el resto Minusculas.
    placa = medfinal.split("-")[0]  # Se almacena el primer valor de la Placa a validar y elimina cualquier separador
    # determinado, en este caso "-"

    # Esto validara si el primer caracter es una letra Mayuscula y los 3 caracteres restantes son numeros.
    # ok almacenara si o no dependiendo si cumple con la validacion.
    mayusdigit = re.match(r"^[A-Z]\d{3}\Z", placa)
    if mayusdigit:
        okmayus = True
    else:
        okmayus = False
    # Esto validara que la placa tenga 4 caracteres, valida si okmayus es True, confirmando la primera validacion
    # y determine si el tercer valor en la lista es int y mayor a 2000
    if len(str(placa)) == 4 and okmayus is True and (int(medfinal.split("-")[2]) > 2000):
        # Se guardan los datos de la manera solicitada
        formatmedidor = placa + "-" + medfinal.split("-")[1] + "-" + medfinal.split("-")[2] + "-" + medfinal.split("-")[
            3].title() + "-" + medfinal.split("-")[4]
        file = open("DB/medidores.txt", "a")  # Crea un .txt llamado medidores donde guardara los datos validados
        file.write(formatmedidor + "\n")
        file.close()
        print("\nRegistro exitoso\n")
    else:
        if medfinal == "Salir":  # Se determino una variable con .title para aceptar el valor "Salir"
            # indistinto de si es mayuscula o minuscula.
            print("\nHa terminado el proceso de registro de datos\n")
        else:
            print("\nPlaca o año incorrectos, verifique que empiece con letra mayuscula y tenga 4 caracteres,"
                  "\nsiendo estos 3 ultimos enteros. Ej: X000 o que el año sea mayor a 2000\n")
    while medfinal != "Salir":
        medidor1 = input("Favor ingrese un codigo, tipo, año, propietario y cantidad de planillas, "
                         "\nseparados por un carácter especial, un guion(-). Para terminar escribir 'Salir':")
        medfinal1 = medidor1.title()
        placa1 = medfinal1.split("-")[0]

        mayusdigit = re.match(r"^[A-Z]\d{3}\Z", placa1)
        if mayusdigit:
            okmayus = True
        else:
            okmayus = False
        if len(str(placa1)) == 4 and okmayus is True and (int(medfinal1.split("-")[2]) > 2000) and (
                medfinal1 != "Salir") and (
                medfinal != "Salir"):
            formatmedidor1 = placa1 + "-" + medfinal1.split("-")[1] + "-" + medfinal1.split("-")[2] + "-" + \
                             medfinal1.split("-")[3].title() + "-" + medfinal1.split("-")[4]
            file = open("DB/medidores.txt", "a")
            file.write(formatmedidor1 + "\n")
            file.close()
            print("\nRegistro exitoso\n")
        else:
            if (medfinal1 == "Salir") | (medfinal == "Salir"):
                print("\nHa terminado el proceso de registro de datos\n")
                break  # Se cierra el ciclo
            else:
                print("\nPlaca o año incorrectos, verifique que empiece con letra mayuscula y tenga 4 caracteres,"
                      "\nsiendo estos 3 ultimos enteros. Ej: X000 o que el año sea mayor a 2000\n")


# Se invoca al menu de reportes, para mostrar los datos guardados en 'medidores.txt'
def menureportes():
    try:
        # Se abre el archivo txt
        filemedidor = open('DB/medidores.txt', 'r')
        filemedidor.readline()
        lines = len(filemedidor.readlines())
        finallines = int(lines) + 1

        print("** REPORTES **")
        print(" \nEn total existen ", finallines, " medidores y son los siguientes:\n\n")
        filedatamedidor = open("DB/medidores.txt", "r")
        now = datetime.now()  # Se crea una variable donde se guarde la fecha actual para mostrar resultado al dar print
        for line in filedatamedidor.readlines():  # Lee las lineas del archivo medidores.txt
            if len(line) > 1:
                # Muestra el dato almacenado por cada posicion de elemento en lista.
                print("Placa: " + line.split('-')[0], end=' \n')
                print("Tipo: " + line.split('-')[1], end=' \n')
                aniofinal = int(now.year) - int(line.split('-')[2])
                print("Año: {anio} [{a} Años]".format(anio=line.split('-')[2], a=aniofinal))
                print("Propietario: " + line.split('-')[3], end=' \n')
                total = int(line.split('-')[4])
                print("Planillas: {a}[Total: ${b}00]".format(a=line.split('-')[4], b=total))
                print('\n')
        filemedidor.close()
    except FileNotFoundError:  # Si no hay archivo mostrara un mensaje de error.
        print("\nNO EXISTE INFORMACION INGRESADA\n")


# Invoca al menu diccionario
# Para esto usamos la libreria Json, y crearemos un .json a partir de un .txt
# Luego se le hara print al .json , el cual imprimira los datos en el formato solicitado
def menudiccionario():
    try:
        print("** DICCIONARIO **\n")
        # El archivo que sera convertido a .Json
        filename = 'DB/medidores.txt'
        # Diccionario resultante
        dict1 = {}

        # Campos que se encuentran en el archivo .txt
        fields = ['Tipo', 'Anio', 'Planillas']

        with open(filename) as fh:
            # count variable for employee id creation Variable de numero para la creacion de Id del propietario
            l = 1

            for line in fh:
                line = line.strip()
                # Leyendo linea por linea del .txt
                description = list(line.split("-"))

                # Para imprimir que se encuentra almacenado en la lista actual llamada 'description'
                # print(description)

                # Para la creacion automatica del id de cada Propietario
                sno = "Propietario - " + description.pop(3)
                cde = "Placa - " + description.pop(0)

                # Variable para bucle
                i = 0

                # Diccionarios intermedio
                dict2 = {}

                # Diccionario interno
                dict3 = {}
                while i < len(fields):
                    # Creando un diccionario para los campos de description
                    dict3[fields[i]] = description[i]
                    i = i + 1
                # Adjunta el registro de cada Propietario al
                # Diccionario Principal
                dict2[cde] = dict3
                dict1[sno] = dict2
                l = l + 1

        # Creando el archivo Json
        out_file = open("DB/medidoresAlpha.json", "w")
        json.dump(dict1, out_file, indent=4)
        out_file.close()
        with open("DB/medidoresAlpha.json", "r") as read_file:
            # Convierte el archivo JSON file a tipo de Python para lectura
            obj = json.load(read_file)

            # Se imprime con formato solicitado el archivo JSON, dando 4 de sangria
            pretty_json = json.dumps(obj, indent=4)
            print(pretty_json)
            out_file.close()

    except IOError as e:  # En caso de que no exista el documento se mostrara este error.
        print(":: No existe documento para mostrar. Ingrese datos primero. ==>", str(e), "\n")


class Cnel:
    # Mostrar menu de CNEL
    menuprincipal()
    while True:
        # solicitar Opcion a Usuario para llamar a cada metodo segun lo indicado por input
        opcionMenu = input("Ingrese una opción: ")

        if opcionMenu == "1":
            menumedidores()

        elif opcionMenu == "2":
            menureportes()

        elif opcionMenu == "3":
            menudiccionario()

        elif opcionMenu == "4":
            print("FIN DEL PROGRAMA")  # Opcion para finalizar el programa
            break

        else:
            print("Opción invalida")
