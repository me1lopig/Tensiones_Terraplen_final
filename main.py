# Nombre del TFG
# Nombre alumno
# EPS de Belmez
#
#
#
#
# calculo de las tensiones y asientos en terraplenes para uso academico
# Bibliografía
    # Shearing Stress and Surface Deflections due to Trapezoidal Loads D.L.Holl 
    # Poulos, H. G. and Davis, E. H. (1974). Elastic Solutions for Soil and Rock Mechanics, 1st Edition, New York, John Wiley & Sons, Inc
# mallas muy densas hacen el cálculo lento 
# recordar que Python es interpretado pero en cambio es multiplatafoma



# llamada a las librerias
import numpy as np # librería para cálculos matematicos

# llamada a librerias definidas
import funcionesCalculo as ft # libreria de funciones auxiliares y de cálculo


# importacion de datos del terreno del archivo datos_terreno.xlsx
espesor,cotas,az,nivel_freatico,pe_seco,pe_saturado,E,poisson,cohesion,fi,cc,e0,tipo_datos,tipo_calculo=ft.datos_terreno()


# importación de los datos del terraplen y del mallado obtenido de la excel datos_terraplen.xlsx
a,b,h,q,ax,incrx,incrz=ft.datos_terraplen()


# creación del directorio de trabajo para guardar resultados
directorio=ft.crea_directorio()


# definicion e iniciación de las matrices y vectores para albergar los cálculos
#xcoord=np.arange(ax,b+incrx,incrx)
xcoord=np.arange(-(ax+b),ax+b+incrx,incrx) # cubre los dos bordes del terraplén
#zcoord=np.arange(0.0001,az+incrz,incrz)
zcoord=np.arange(incrz,az+incrz,incrz)
tension_z=np.zeros((zcoord.size,xcoord.size)) # incremento de tensión en z de la carga del terraplen
tension_x=np.zeros((zcoord.size,xcoord.size)) # incrememnto de tensión en x de la carga del terraple
tension_xz=np.zeros((zcoord.size,xcoord.size)) # incremento de tension xz de la carga del terraple
tension_z_terreno=np.zeros((zcoord.size,xcoord.size)) # tension total inicial del terreno
tension_z_efectiva=np.zeros((zcoord.size,xcoord.size)) # tension efectiva inicial del terreno
#resistencia_corte=np.zeros((zcoord.size,xcoord.size)) # resistencia al corte del terreno
asientos_z=np.zeros((1,xcoord.size))


# datos de arranque del cálculo los asientos del terreno
asiento=[]
asiento_parcial=0
xarray=0


# realización de los cálculos de tensiones y asientos bajo la carga del terraplén
for x in xcoord:
    zarray=0
    for z in zcoord:
        # incrementos de tensiones provocados por la carga del terraplén
        tensionz,tensionx,tensionxz=ft.tension_terraplen(a,b,q,x+b,z) # incrementos de tensiones prodeucidas por el terraplen

        # tensiones naturales del terreno verticales
        tension_z_0=ft.presion_total(cotas,nivel_freatico,pe_saturado,pe_seco,z) # tensión total
        tension_z_ef=tension_z_0-ft.n_freatico(nivel_freatico,z)*9.81 # tensión efectiva

        # cálculo de los valores de resistencia al corte del terreno en efectivas
        resistencia_cor=ft.resistencia_MC(cotas,tension_z_ef,cohesion,fi,z)
        
        # construcción de las matrices de datos
        tension_z[zarray,xarray]=tensionz # tensiones normales en z
        tension_x[zarray,xarray]=tensionx # tensiones normales en x
        tension_xz[zarray,xarray]=tensionxz # tensiones cortantes en xz
        tension_z_terreno[zarray,xarray]=tension_z_0 # tension total del terreno en z
        tension_z_efectiva[zarray,xarray]=tension_z_ef # tension efectiva del terreno en z
        #resistencia_corte[zarray,xarray]=resistencia_cor # resistencia al corte del terreno

        zarray+=1
         
        # aqui se calculará la parte de los asientos
        # según los tipos de cálculos que se van a realizar

        # cálculo de asientos en funcion de la indicación en datos_terreno.xlsx 
        # en lo que respecta al tipo de cálculo 
        # E, e cálculo de tipo elástico
        # C,c cálculo de tipo consolidación primaria para el caso de OCR=1
        # los otros casos de consolidación no se contemplan en este Trabajo
        
        tipoCalculo=tipo_calculo[ft.parametro_terreno(cotas,z)]

        if (tipoCalculo in ['e','E']):
            asiento_parcial+=ft.asiento_elastico(cotas,z,incrz,E,poisson,tensionx,tensionz)
        
        if (tipoCalculo in ['c','C']):
            asiento_parcial+=ft.asiento_consolidacion(incrz,cc,e0,tension_z_ef,tensionz,cotas,x,z)

        
        # asiento elástico
        #asiento_parcial+=ft.asiento_elastico(cotas,z,incrz,E,poisson,tensionx,tensionz)

        # asiento por consolidación
        #asiento_parcial_consolidacion+=ft.asiento_consolidacion(incrz,cc,e0,tension_z_ef,tensionz,cotas,x,z)

    asiento.append(asiento_parcial)
    xarray+=1
    asiento_parcial=0 # se reinicia el asiento a cero para el siguiente cálculo


# exportacion a una hoja excel de los cálculos realizados tensiones y asientos
ft.guardar_xlsx_tensiones (xcoord,zcoord,tension_z,directorio,'Cal_Tension_z')
ft.guardar_xlsx_tensiones(xcoord,zcoord,tension_x,directorio,'Cal_Tension_x')
ft.guardar_xlsx_tensiones(xcoord,zcoord,tension_xz,directorio,'Cal_Tension_xz')
ft.guardar_xlsx_tensiones(xcoord,zcoord,tension_z_terreno,directorio,'Cal_Tension_Total_z')
ft.guardar_xlsx_tensiones(xcoord,zcoord,tension_z_efectiva,directorio,'Cal_Tension_Efectiva_z')
#ft.guardar_xlsx_tensiones(xcoord,zcoord,resistencia_corte,directorio,'Cal_Resistencia_corte')
ft.guardar_xlsx_asientos(xcoord,asiento,directorio,'Cal_Asientos')


#graficado de los valores de las tensiones
tipo_Grafica=['isolinea','continua']
for tG in tipo_Grafica:
    ft.graficos_tensiones(xcoord,zcoord,tension_z,directorio,'Tension z',tG,a,b,h)
    ft.graficos_tensiones(xcoord,zcoord,tension_x,directorio,'Tension x',tG,a,b,h)
    ft.graficos_tensiones(xcoord,zcoord,tension_xz,directorio,'Tensión xz',tG,a,b,h)
    ft.graficos_tensiones(xcoord,zcoord,tension_z_terreno,directorio,'Tension Total_z',tG,a,b,h)
    ft.graficos_tensiones(xcoord,zcoord,tension_z_efectiva,directorio,'Tension Efectiva_z',tG,a,b,h)
    #ft.graficos_tensiones(xcoord,zcoord,resistencia_corte,directorio,'Cal_Resistencia_corte',tG,a,b,h)


# graficado de las tensiones naturales del terreno
#ft.ploteado_tensiones_normales(cotas,nivel_freatico,pe_saturado,pe_seco,directorio,"Tensiones normales")

# graficado de cálculo de asientos
ft.grafico_asientos(xcoord,asiento,directorio,'asientos')

# emisión del informe de resultados
ft.guardar_docx_datos(a,b,h,q,ax,incrx,az,incrz,directorio,tipo_datos)
