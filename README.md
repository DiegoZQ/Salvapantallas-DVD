# Salvapantallas DVD
La presente carpeta corresponde a la tarea 1 de Modelacion y Computacion Grafica para Ingenieros,
dentro de la cual se encuentran todos los archivos necesarios para correr lo pedido en el pdf de 
la tarea.
En el archivo basic_shapes esta la clase que crea todas las figuras utilizadas a la hora de 
ensamblar el logo principal, en transformations se encuentran las matrices de transformacion
usadas para aplicar sobre las distintas figuras, en gpu_shape estan resumidas todas las funciones
necesarias para crear gpuShapes y manipularlos en 3 simples metodos, en easy_shaders estan los
shaders necesarios para el dibujo en patalla de los gpuShapes y sus respectivas transformaciones.
Luego, pasando a los 2 archivos principales, tenemos drawable_logos, el cual se encarga de crear
figuras complejas a partir de figuras simples, conteniendo una lista de estas y realizando
las operaciones pertinentes sobre ellas para lograr lo pedido en el enunciado, ademas de poseer
funcionalidades extras, como modificar partes del logo cada vez que este choque con un borde,
simulando asi ligeras variaciones sobre el logo, el cual en este caso es un gatito y sus variaciones
corresponden a distintos estados de animo (solo contiene 3). Pasando al archivo principal, main.py
es el archivo en el cual se ejecuta y visualiza todo el apartado grafico, en el tenemos el ensamblaje del gato,
sus estados, tambien unas variables dependientes del input al ejecutar el programa, o en el caso
de no haber input, se colocan simplemente mis datos, posterior a eso, en la funcion, esta la creacion del logo 
mas todas las operaciones de asignacion sobre el para hacerlo funcionar correctamente y finalmente en el while
estan todos los metodos extraidos de la clase Logo para dibujar al gato, moverlo, y realizar las transformaciones
correspondientes segun toque algun borde.