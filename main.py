import glfw
from OpenGL.GL import *
from easy_shaders import SimpleTransformShader
from basic_shapes import *
import constants as const
from drawable_logos import *
import transformations as tr
import sys

#@autor: Diego Zúñiga.

#Variables del input.
####################################################################
if len(sys.argv)==4:
    nombre = sys.argv[1]
    iniciales = sys.argv[2]
    rut = int(sys.argv[3])
else:
    nombre = "Diego"
    iniciales = "DZ"
    rut = 20973826
largo = len(nombre)
my_color = [ord(nombre[0%largo]) * ord(nombre[1%largo]) % 255 /255,
            ord(nombre[2%largo]) * ord(nombre[3%largo]) % 255 /255,
            ord(nombre[4%largo]) * ord(nombre[5%largo]) % 255 /255]
s = rut/20000000
if s<1.2:
    s=1.5
alpha = ord(iniciales[0]) * ord(iniciales[1])
x = 350*np.cos(alpha)
y = 350*np.sin(alpha)
####################################################################
#Logo y estados del logo.

#Inicialmente el gato se creó en una ventana de 900x900, por lo que, para evitar que las translaciones distorcionen la figura
#en ventanas de diferentes dimensiones, se optó por multiplicar los parámetros usando dos constantes (CX, CY) que mantienen
#las figuras en la posición original que tenían en la ventana de 900x900.
cat = [[createTriangle(90,my_color), [tr.translate(-0.15*const.CX,0.23*const.CY,0), tr.perfectRotationZ(np.pi*0.15)]], #orejas 1(2)
        [createTriangle(90,my_color), [tr.translate(0.15*const.CX,0.23*const.CY,0), tr.perfectRotationZ(-np.pi*0.15)]],
        [createElipse(230,200, my_color, 30), [tr.translate(0,0.1*const.CY,0)]],#cabeza 3(4)
        [createElipse(220,190, const.BACKGROUND, 30), [tr.translate(0,0.1*const.CY,0)]],
        [createSlice(60,my_color, np.pi*0.8, 10), [tr.perfectRotationZ(np.pi*1.1)]], #boca-nariz 5(6)
        [createSlice(60,const.BACKGROUND,np.pi*0.7, 10), [tr.translate(0,-0.01*const.CY,0), tr.perfectRotationZ(np.pi*1.15)]],
        [createRectangle(10,25,my_color), [tr.translate(0,0.015*const.CY,0)]],
        [createSlice(80,my_color, np.pi*0.5, 10), [tr.translate(0, 0.025*const.CY,0), tr.perfectRotationZ(np.pi*0.25)]],
        [createRectangle(15,7.5, my_color), [tr.translate(-0.065*const.CX,-0.02*const.CY,0), tr.perfectRotationZ(-np.pi*0.2)]],
        [createRectangle(15,7.5, my_color), [tr.translate(0.065*const.CX,-0.02*const.CY,0), tr.perfectRotationZ(np.pi*0.2)]],
        [createRectangle(4, 65,my_color), [tr.translate(-0.1*const.CX, 0.01*const.CY, 0), tr.perfectRotationZ(-np.pi*0.45)]], #bigotes 11(12)
        [createRectangle(4,65,my_color), [tr.translate(-0.1*const.CX, 0.045*const.CY, 0), tr.perfectRotationZ(np.pi*0.45)]], 
        [createRectangle(4,65,my_color), [tr.translate(0.1*const.CX, 0.01*const.CY, 0), tr.perfectRotationZ(np.pi*0.45)]],
        [createRectangle(4,65,my_color), [tr.translate(0.1*const.CX, 0.05*const.CY, 0), tr.perfectRotationZ(-np.pi*0.45)]],
        #parte del gato que va cambiando para generar diferentes "estados"
        [createElipse(45.6,56,my_color,20), [tr.translate(0.125*const.CX, 0.16*const.CY, 0), tr.perfectRotationZ(np.pi*0.1)]], #ojo derecho 15(16)
        [createElipse(45.6,48,const.BACKGROUND,20), [tr.translate(0.12*const.CX, 0.155*const.CY, 0), tr.perfectRotationZ(np.pi*0.1)]],
        [createElipse(40,48,my_color,20), [tr.translate(0.115*const.CX, 0.15*const.CY, 0), tr.perfectRotationZ(np.pi*0.1)]],
        [createSlice(27, const.BACKGROUND, np.pi*1.1, 5), [tr.translate(0.11*const.CX, 0.165*const.CY, 0), tr.perfectRotationZ(np.pi*0.1)]],
        [createElipse(45.6,56,my_color,20), [tr.translate(-0.125*const.CX, 0.16*const.CY, 0), tr.perfectRotationZ(-np.pi*0.1)]], #ojo izquierdo 19(20)
        [createElipse(45.6,48,const.BACKGROUND,20), [tr.translate(-0.12*const.CX, 0.155*const.CY, 0), tr.perfectRotationZ(-np.pi*0.1)]],
        [createElipse(40,48,my_color,20), [tr.translate(-0.115*const.CX, 0.15*const.CY, 0), tr.perfectRotationZ(-np.pi*0.1)]],
        [createSlice(27, const.BACKGROUND, np.pi*1.1, 5), [tr.translate(-0.12*const.CX, 0.165*const.CY, 0), tr.perfectRotationZ(np.pi*0.07)]]
        ]

#Mismas 8 últimas figuras de cat, sólo que normalizadas dentro de la hitbox.
normal = copy.deepcopy(cat[14:22])
for gpuShape in normal:
    gpuShape[1] = [tr.translate(0,-0.07*const.CY,0), tr.scale(0.7,0.53,1)] + gpuShape[1]

feliz1 = [[createTriangle(30,my_color), [tr.translate(0.07*const.CX,0,0), tr.scale(1.2,1,1)]],
          [createTriangle(30,const.BACKGROUND), [tr.translate(0.07*const.CX,-0.02*const.CY,0), tr.scale(1.2,1,1)]],
          [createTriangle(30,my_color), [tr.translate(-0.07*const.CX,0.0,0), tr.scale(1.2,1,1)]],
          [createTriangle(30,const.BACKGROUND), [tr.translate(-0.07*const.CX,-0.02*const.CY,0), tr.scale(1.2,1,1)]]
          ]

feliz2 = [[createTriangle(30,my_color), [tr.translate(0.1*const.CX,0.02*const.CY,0), tr.scale(1.2,1,1), tr.perfectRotationZ(np.pi/2)]],
          [createTriangle(30,const.BACKGROUND), [tr.translate(0.12*const.CX,0.02*const.CY,0), tr.scale(1.2,1,1), tr.perfectRotationZ(np.pi/2)]],
          [createTriangle(30,my_color), [tr.translate(-0.1*const.CX,0.02*const.CY,0), tr.scale(1.2,1,1), tr.perfectRotationZ(-np.pi/2)]],
          [createTriangle(30,const.BACKGROUND), [tr.translate(-0.12*const.CX,0.02*const.CY,0), tr.scale(1.2,1,1), tr.perfectRotationZ(-np.pi/2)]],
          [createTriangle(30,my_color), [tr.translate(0,-0.08*const.CY,0), tr.scale(1.4,0.8,1), tr.perfectRotationZ(np.pi)]],
          [createTriangle(20,const.BACKGROUND), [tr.translate(0,-0.08*const.CY,0), tr.scale(1.4,0.8,1), tr.perfectRotationZ(np.pi)]]
          ]


#Funcion prinicipal.
def main():
    
    if not glfw.init():
        glfw.set_window_should_close(window, True)
        return -1

    #Crea ventana con sus respectivas dimensiones y nombre
    window = glfw.create_window(const.WIDHT, const.HEIGHT, "Tarea 1: Muerte segura", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)
        return -1
        
    glfw.make_context_current(window)
    pipeline = SimpleTransformShader()
    glUseProgram(pipeline.shaderProgram)

    #Creación del logo con pipeline centrado en 0,0 y velocidades de X, Y normalizadas según la ventana
    logo = Logo(pipeline, [0,0], [2*x/const.WIDHT,2*y/const.HEIGHT])
    logo.addAndConvertShape(createRectangle(160,120,const.BACKGROUND), []) #se añade un hitbox
    logo.addAndConvertShapes(cat) #se carga la figura del gato
    logo.states = [feliz1, feliz2, normal] #le añade estados al gato
    logo.scale = s #lo que se escalara el logo al cambiar de tamanio
    #Se adecua la figura del gato dentro del hitbox
    logo.transform2(tr.scale(0.7,0.53,1)) 
    logo.transform2(tr.translate(0,-0.07*const.CY,0))
    #Se coloca el color del fondo "totalmente negro"
    glClearColor(0, 0, 0, 1.0)

    i = 0
    a = 0
    while not glfw.window_should_close(window):
        glfw.poll_events()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glClear(GL_COLOR_BUFFER_BIT)
        #Permite calcular la diferencia positiva delta entre 2 cuadros 
        if (i%2==0): #si i es par
            b = glfw.get_time()
            delta = b-a
        else: #si i es impar
            a = glfw.get_time()
            delta = a-b
        logo.draw() #dibuja el logo
        logo.move(delta) #mueve el logo
        #Chequea si el logo colisiona con los bordes para aplicar transformaciones
        logo.collideWithBorders()
        #Mueve la figura dentro de la ventana por si esta se llega a salir debido 
        #a las transformaciones
        logo.fixCollide()
    
        glfw.swap_buffers(window)
        i+=1
        
    logo.clear()
    glfw.terminate()

    return 0

if __name__ == "__main__":
    main()