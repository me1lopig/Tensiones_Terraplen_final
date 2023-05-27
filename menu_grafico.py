# entrada del tipo de cálculo de forma gráfica


import tkinter as tk

class Ventana:

    def __init__(self):
        
        # características de la ventana 
        self.tipoCalculo = tk.Tk()
        self.tipoCalculo.title("Seleccionar tipo de carga")
        self.tipoCalculo.geometry("250x120")
        self.tipoCalculo.resizable(False, False)
        self.tipoCalculo.eval('tk::PlaceWindow . center')

        # contenedor de los botones de seleccion
  
        # declaración de la variable de salida de la selección
        self.tipo_calculos=tk.IntVar()

        # Crear el widget Radio para la carga tipo terraplén
        self.opcion_terraplen = tk.Radiobutton(self.tipoCalculo,text="Carga tipo terraplén",variable=self.tipo_calculos,value=1)
        self.opcion_terraplen.grid(column=0, row=0)


        # Crear el widget Radio para la carga tipo rectangular
        self.opcion_rectangular = tk.Radiobutton(self.tipoCalculo,text="Carga tipo rectangular",variable=self.tipo_calculos,value=2)
        self.opcion_rectangular.grid(column=0, row=1)


        # Crear  envío a cálculo y salir
        self.boton_calcular = tk.Button(self.tipoCalculo,text="Calcular",command=self.tipoCalculo.quit)
        self.boton_calcular.grid(column=0, row=2)
 
        # Crear  salir sin calcular
        self.boton_salir = tk.Button(self.tipoCalculo,text="Salir",
            command=self.salir)
        self.boton_salir.grid(column=0, row=3)
    
        self.tipoCalculo.mainloop()


    # funciones auxiliares
    def salir(self):
    # pone el valor de salida a 0 
    # cierra la ventana
        self.tipo_calculos.set(0)
        self.tipoCalculo.quit()




# probamos la funcion con estas lineas
#if __name__ == '__main__':
#    ventana = Ventana()
#    tipo_calculos = ventana.tipo_calculos.get()
#    print(f"Tipo de cálculos seleccionado: {tipo_calculos}")


