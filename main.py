# calculo de las tensiones y asientos en terraplenes para uso academico
# version 02/10/2022
# Germán López Pineda
# Ingeniero de Caminos Canales y Puertos UGR
# Master en Matemática Computacional UJI
# Master en Ingeniería del Terreno UCO
# Grupo de investigación RNM 244 Ingeniería Ambiental y Geofísica Universidad de Córdoba
# Bibliografía
    # Shearing Stress and Surface Deflections due to Trapezoidal Loads D.L.Holl 
    # Poulos, H. G. and Davis, E. H. (1974). Elastic Solutions for Soil and Rock Mechanics, 1st Edition, New York, John Wiley & Sons, Inc
# mallas muy densas hacen el cálculo lento 
# recordar que Python es interpretado



# llamada a las librerias
import numpy as np # libería para cálculos matematicos

# llamada a librerias definidas
import funcionesCalculo as ft # libreria de funciones de cálculo


# importacion de datos del terreno
espesor,cotas,az,nivel_freatico,pe_seco,pe_saturado,E,poisson,cohesion,fi,cc,e0,tipo_datos=ft.datos_terreno()


# importación de los datos del terraplen y del mallado obtenido de la excel datos_terraplen.xlsx
a,b,h,q,ax,incrx,incrz=ft.datos_terraplen()


# creación del directorio de trabajo para guardar resultados
directorio=ft.crea_directorio()


# definicion e iniciación de las matrices y vectores para albergar los cálculos
#xcoord=np.arange(ax,b+incrx,incrx)
xcoord=np.arange(-(ax+b),ax+b+incrx,incrx) # cubre los dos bordes del terraplén
zcoord=np.arange(0.0001,az+incrz,incrz)
tension_z=np.zeros((zcoord.size,xcoord.size))
tension_x=np.zeros((zcoord.size,xcoord.size))
tension_xz=np.zeros((zcoord.size,xcoord.size))
tension_z_terreno=np.zeros((zcoord.size,xcoord.size))
asientos_z=np.zeros((1,xcoord.size))


# realización de los cálculos de tensiones y asientos bajo la carga del terraplén
asiento=[]
asiento_parcial=0
xarray=0
for x in xcoord:
    zarray=0
    for z in zcoord:
        tensionz,tensionx,tensionxz=ft.tension_terraplen(a,b,q,x+b,z)    
        # tensiones naturales del terreno verticales y horizontales
        #tension_z_0=ft.tension_total(z,cotas,pe_saturado,pe_seco,nivel_freatico)
        
        # construcción de las matrices de datos
        tension_z[zarray,xarray]=tensionz # tensiones normales en z
        tension_x[zarray,xarray]=tensionx # tensiones normales en x
        tension_xz[zarray,xarray]=tensionxz # tensiones cortantes en xz
        #tension_z_terreno[zarray,xarray]=tension_z_0 # tension natural del terreno en z
        zarray+=1
         
         # aqui se calculará la parte de los asientos
        asiento_parcial+=ft.asiento_elastico(cotas,z,incrz,E,poisson,tensionx,tensionz)

    asiento.append(asiento_parcial)
    xarray+=1
    asiento_parcial=0 # se reinicia el asiento a cero para el siguiente cálculo


# exportacion a una hoja excel de los cálculos realizados tensiones y asientos
ft.guardar_xlsx_tensiones (xcoord,zcoord,tension_z,directorio,'Cal_Tension_z')
ft.guardar_xlsx_tensiones(xcoord,zcoord,tension_x,directorio,'Cal_Tension_x')
ft.guardar_xlsx_tensiones(xcoord,zcoord,tension_xz,directorio,'Cal_Tension_xz')
#ft.guardar_xlsx_tensiones(xcoord,zcoord,tension_z_terreno,directorio,'Cal_Tension_Total_z')
ft.guardar_xlsx_asientos(xcoord,asiento,directorio,'Cal_Asientos')


#graficado de los valores de las tensiones
tipo_Grafica=['isolinea','continua']
for tG in tipo_Grafica:
    ft.graficos_tensiones(xcoord,zcoord,tension_z,directorio,'Tension z',tG,a,b,h)
    ft.graficos_tensiones(xcoord,zcoord,tension_x,directorio,'Tension x',tG,a,b,h)
    ft.graficos_tensiones(xcoord,zcoord,tension_xz,directorio,'Tensión xz',tG,a,b,h)
    #ft.graficos_tensiones(xcoord,zcoord,tension_z_terreno,directorio,'Tension terreno_z',tG,a,b,h)


# graficado de cálculo de asientos
ft.grafico_asientos(xcoord,asiento,directorio,'asientos')

# emisión del informe de resultados
ft.guardar_docx_datos(a,b,h,q,ax,incrx,az,incrz,directorio,tipo_datos)
