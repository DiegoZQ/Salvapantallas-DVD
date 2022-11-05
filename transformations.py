import numpy as np
import constants as const

#Retorna una matriz de traslacion en tx, ty, tz.
def translate(tx, ty, tz):
    return np.array([
        [1,0,0,tx],
        [0,1,0,ty],
        [0,0,1,tz],
        [0,0,0,1]], dtype = np.float32)

#Retorna una matriz de escalamiento en sx, sy, sz.
def scale(sx, sy, sz):
    return np.array([
        [sx,0,0,0],
        [0,sy,0,0],
        [0,0,sz,0],
        [0,0,0,1]], dtype = np.float32)

#Retorna una matriz de rotacion para el plano xy con un angulo theta.
def rotationZ(theta):
    sin_theta = np.sin(theta) # 1, const.CX
    cos_theta = np.cos(theta) # const.CY, const.CX

    return np.array([
        [cos_theta,-sin_theta,0,0],
        [sin_theta,cos_theta,0,0],
        [0,0,1,0],
        [0,0,0,1]], dtype = np.float32)

#Retorna una matriz de rotacion en z sobre un círculo unitario independiente de las 
#dimensiones de la ventana.
def perfectRotationZ(theta):

    return matmul([scale(1,const.RATIO, 1), rotationZ(theta), scale(1,1/const.RATIO, 1)])

#Funcion encargada de multiplicar matrices
def matmul(mats):
    out = mats[0]
    for i in range(1, len(mats)):
        out = np.matmul(out, mats[i])

    return out