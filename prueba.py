import matplotlib.pyplot as plt
import numpy as np

# Datos de ejemplo
x = np.linspace(0, 5, 50)
y = np.linspace(0, 5, 40)
X, Y = np.meshgrid(x, y)
Z = np.sin(X * 2 + Y) * 3 + np.cos(Y + 5)

# Crear el gráfico de contorno
contour = plt.contour(X, Y, Z)

# Agregar la barra de colores
colorbar = plt.colorbar(contour, cmap='viridis_r')



# Mostrar el gráfico
plt.show()
