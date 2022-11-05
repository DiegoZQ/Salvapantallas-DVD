import constants as const
from gpu_shape import GPUShape
from OpenGL.GL import *
import transformations as tr
from basic_shapes import *
import copy

#Crea un gpuShape a partir de un pipeline y un shape.
def createGPUShape(pipeline, shape):
    gpuShape = GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertexData, shape.indexData)

    return gpuShape

#Dibuja un gpuShape usando transformaciones y un pipeline.
def draw(pipeline, gpuShape, transformations):
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE,
        tr.matmul(transformations)
    )
    pipeline.drawCall(gpuShape)

#Logo es la clase encargada de almacenar todos los gpuShapes con sus respectivas transformaciones
#cuyo proposito consiste en servir como punto de referencia a la hora de mover la figura y aplicar
#diversas transformaciones sobre sublistas especificas de gpuShapes.
class Logo:
    #el movimiento se obtendra al dibujar a partir de la self.position de logo.
    def __init__(self, pipeline, startPosition, velocity):
        self.pipeline = pipeline #pipeline usado por el logo
        self.gpuShapes = [] #gpuShape, transformations
        self.startPosition = startPosition
        self.position = [0,0] #posicion en x,y del logo en general
        self.velocity = velocity #velocidad en x,y del logo
        self.size = [tr.scale(1,1,1), "NORMAL"]
        self.scale = 1
        self.angle = 0 #angulo incial del logo
        #los estados corresponden a matrices de gpuShapes que se van intercambio constantemente
        #cada vez que el logo "rebota" dando asi el efecto de expresiones faciales.
        self.states = []
        self.stateIndex = 0
        
    #Convierte un shape en un gpuShape con su transformaciones respectivas 
    #y lo añade a la lista de gpuShapes del logo.
    def addAndConvertShape(self, shape, transformations):
        self.gpuShapes.append([createGPUShape(self.pipeline, shape), transformations])
    
    #Convierte una matriz de shapes con sus transformaciones en gpuShapes
    #y lo añade a la lista de gpuShapes del logo.
    def addAndConvertShapes(self, shapesAndTransformations):
        for i in shapesAndTransformations:
            shape, transformation = i[0], i[1]
            self.addAndConvertShape(shape, transformation) 

    #Dibuja todos los gpuShapes contenidos en la lista con su posicion relativa al centro
    #del logo, sus transformaciones y la rotacion que deben tener dado el angulo del logo.
    def draw(self):
        for gpuShape in self.gpuShapes:
            draw(self.pipeline, gpuShape[0], 
            #aplica las transofrmaciones y luego translada a su posicion relativa c/r al logo
             [tr.translate(self.position[0], self.position[1], 0)] + [self.size[0]] +
              [tr.perfectRotationZ(self.angle)] + gpuShape[1]) #.transformation

    #Permite que el logo se mueva una posición usando su velocidad y delta de tiempo t.
    def move(self, t):
        self.position[0] += self.startPosition[0] + self.velocity[0]*t
        self.position[1] += self.startPosition[1] + self.velocity[1]*t

    #Cambia de tamaño entre "NORMAL" y "GRANDE".
    def changeSize(self):
        if (self.size[0]==tr.scale(1,1,1)).all():
            self.size[0]=tr.scale(self.scale,self.scale,self.scale)
            self.size[1]="GRANDE"
        else:
            self.size[0]=tr.scale(1,1,1)
            self.size[1]="NORMAL"

    #Intercambia las últimas gpuShapes por otras contenidas en self.state.
    def changeState(self):
        self.gpuShapes = self.gpuShapes[0:15] #base del gato
        self.addAndConvertShapes(self.states[self.stateIndex%len(self.states)])
        self.stateIndex += 1          
        
    #Aplica una transformación sobre un rango de gpuShapes contenidas en el logo.
    #Método ineficiente si se quieren aplicar varias transformaciones seguidas en un corto periodo de tiempo.
    def transform(self, transformation, range):
        for i in range:
            self.gpuShapes[i][1] = [transformation] + self.gpuShapes[i][1]

    #Aplica una transformación sobre todos las gpuShapes contenidas en el logo.
    def transform2(self, transformation):
        for i in range(len(self.gpuShapes)):
            self.gpuShapes[i][1] = [transformation] + self.gpuShapes[i][1]

    #Da el efecto de rebote, cambio de tamaño, estado y rotación cada vez que el logo toca el borde
    #de la ventana.
    def rebote(self, axis, sign):
        self.velocity[axis] = sign*abs(self.velocity[axis])
        self.changeSize()
        self.angle += np.pi/2 
        self.changeState()

    #Teletransporta el logo dentro de la ventana si este se escapa
    #viendo el eje y la dirección del teleport.
    #Por ejemplo, si el eje es 0 (x) y el signo negativo, entonces
    #lo teletransporta hacia la izquierda.
    def teleportInside(self, axis, sign):
        if (self.size[1]=="NORMAL"):
            if (axis==0):
                self.position[axis] = sign*(160/const.WIDHT - 1) 
            else:
                self.position[axis] = sign*(120/const.HEIGHT - 1)
        else:
            if (axis==0):
                self.position[axis] = sign*(120*self.scale/const.WIDHT - 1)
            else:
                self.position[axis] = sign*(160*self.scale/const.HEIGHT - 1)  
    
    #Realiza ciertas operaciones si el logo interactúa, tanto en versión normal como grande,
    #con los bordes de la ventana.
    #Este metodo en especifico, corresponde a una abstraccion de los metodos collideWithBordes
    #y fixCollide.
    def collideOperation(self, op):
        if self.size[1]=="GRANDE": #si el logo está en grande
            #choca con el borde derecho
            if self.position[0]+120*self.scale/const.WIDHT > 1.0: 
                op(0, -1)
            #choca con el borde izquierdo
            if self.position[0]-120*self.scale/const.WIDHT < -1.0: 
                op(0, 1)
            #choca con el borde superior
            if self.position[1]+160*self.scale/const.HEIGHT > 1.0:
                op(1, -1)
            #choca con el borde inferior
            if self.position[1]-160*self.scale/const.HEIGHT < -1.0:
                op(1, 1)
        elif self.size[1]=="NORMAL":
            #choca con el borde derecho
            if self.position[0]+160/const.WIDHT > 1.0 :
                op(0, -1)
            #choca con el borde izquierdo
            if self.position[0]-160/const.WIDHT < -1.0 :
                op(0, 1)
            #choca con el borde superior
            if self.position[1]+120/const.HEIGHT > 1.0 :
                op(1, -1)
            #choca con el borde inferior
            if self.position[1]-120/const.HEIGHT < -1.0 :
                op(1, 1)

    #Aplica la operación de rebote sobre el logo cada vez que colisiona con los bordes.
    def collideWithBorders(self):
        self.collideOperation(self.rebote)

    #Aplica la operación de teleportInside sobre el logo después de haber colisionado con los bordes.
    def fixCollide(self):
        self.collideOperation(self.teleportInside)
                                      
    #Limpia los gpuShapes.
    def clear(self):
        for gpuShape in self.gpuShapes:
            gpuShape[0].clear()