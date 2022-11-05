import numpy as np
from OpenGL.GL import *
import constants as const

#Clase encargada de almacenar la posicion de los vertices en el plano xy,
#sus respectivos colores y las aristas de los triangulos que se forman.
class Shape:
    def __init__(self, vertexData, indexData):
        self.vertexData = vertexData
        self.indexData = indexData


#Normaliza un lado (en pixeles) según las dimensiones de la ventana.
def resize(lado):

    return [lado/const.WIDHT, lado/const.HEIGHT]

#Multiplica una variable (index de 0 a 5) de todos los vértices contenidos en vertexData 
#por un valor específico(value) (versión challa de scale aplicado a arreglos 1D).
def multiplicar(vertexData, index, value):
    for i in range(index, len(vertexData), 6):
        vertexData[i] *= value

#Crea un cuadrado con lado (en pixeles) y color (rgb normalizado).
def createQuad(lado, color):
    x, y = resize(lado)
    r, g, b = color
    vertexData = np.array([
    #   posiciones        colores
        -x, -y, 0.0,  r, g, b, 
         x, -y, 0.0,  r, g, b, 
         x,  y, 0.0,  r, g, b, 
        -x,  y, 0.0,  r, g, b 
        ], dtype = np.float32)
    indexData = np.array(
        [0, 1, 2,
         2, 3, 0], dtype= np.uint32)

    return Shape(vertexData, indexData)

#Crea triángulo equilatero con lado (en pixeles) y color (rgb normalizado).
def createTriangle(lado, color):
    x,y = resize(lado)
    r, g, b = color
    vertexData = np.array([
    #   posiciones        colores
        -x, 0.0, 0.0,  r, g, b, 
         x, 0.0, 0.0,  r, g, b, 
         0.0, y*np.sin(np.pi/3)*2, 0.0,  r, g, b
        ], dtype = np.float32)
    indexData = np.array(
        [0, 1, 2], dtype= np.uint32)

    return Shape(vertexData, indexData)

#Crea un slice con un radio (en pixeles), color rg normalizado, angulo 
#y numero de puntos que tendra (para suavizar la curva).
def createSlice(radio, color, angulo, N):
    x, y = resize(radio)
    r, g, b = color
    vertexData = [
        # posición     # color
        0.0, 0.0, 0.0, r, g, b
    ]
    indexData = []
    deltaAngulo = angulo/N
    vertexData += [x, 0 , 0, r, g, b]
    for i in range(1, N+1):
        vertexData += [x*np.cos(i*deltaAngulo), y*np.sin(i*deltaAngulo), 0, r, g, b]
        indexData += [0, i, i+1]

    return Shape(vertexData, indexData)

#Crea un circulo con un radio (en pixeles), con color rgb normalizado
#y un numero especifico de puntos en la curva, todo esto haciendo uso
#de la funcion createSlice.
def createCircle(radio, color, N):

    return createSlice(radio, color, 2*np.pi, N)

#Crea un semicirculo con un radio (en pixeles), con color rgb normalizado
#y un numero especifico de puntos en la curva, todo esto haciendo uso
#de la funcion createSlice.
def createHalfCircle(radio, color, N):

    return createSlice(radio, color, np.pi, N)


#Crea un rectangulo con ladoX y ladoY (en pixeles), color rgb normalizado,
#haciendo uso de la funcion createQuad y luego modificando uno de sus lados
#con la funcion multiplicar.
def createRectangle(ladoX, ladoY, color):
    rectangle = createQuad(ladoX, color)
    multiplicar(rectangle.vertexData, 1, ladoY/ladoX)

    return rectangle

#Crea una elise con radioX y radioY (en pixeles), color rgb normalizado,
#haciendo uso de la funcion createCircle y luego modificando uno de sus lados
#con la funcion multiplicar.
def createElipse(radioX, radioY, color, N):
    elipse = createCircle(radioX, color, N) 
    multiplicar(elipse.vertexData, 1, radioY/radioX)
    
    return elipse