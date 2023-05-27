# funcion de contenido del menu
# se plantea el uso de un menu de consola inicial


def menu_entrada():
    print('=============================')
    print('Menu de entrada de selección de tipos de carga')
    print('=============================')
    print()
    print('1->Carga tipo terraplen')
    print('2->Carga tipo rectangular')
    print('Otro valor->Salir del programa')
    print('=============================')

    
    tipo_calculos=int(input('Tipo de dato->'))
    if tipo_calculos==1:
        return 1 # seleccion de terraplen
    elif tipo_calculos==2:
        return 2 # selección de carga rectangular
    else:
        return 0 # no se hacen cálculos

    