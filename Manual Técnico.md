# Lenguajes Formales y de Programacion
## Proyecto No.2
### Segundo Semestre
```js
Universidad San Carlos de Guatemala
Programador: Jonatan Samuel Rojas Maeda
Carne: 202200061
Correo: jonas23450947@gmail.com
```
---
## Objetivos
* Objetivos Generales
    *Que el estudiante cree una herramienta la cual sea capaz de reconocer un lenguaje, dado por medio de un analizador léxico y sintactico el cual cumple con las reglas establecidas, manejando la lectura y escritura de archivos para el manejo de la información. A través de un entorno gráfico.

* Objetivos Especificos
    *Que el estudiante implemente una solución de software implementando los conceptos vistos en clase y laboratorio.
    *Que el estudiante implemente un analizador sintáctico utilizando los conceptos de gramáticas independientes de contexto y árboles de derivación.
    *Introducir al estudiante a la ejecución de instrucciones en un lenguaje de programación.
---
## Descripción del Proyecto

### Librerias Utilizadas
* from tkinter import Text
* from tkinter import ttk
* from tkinter import Tk, messagebox, filedialog
* import tkinter as tk
* from fileinput import filename
* from tkinter.filedialog import askopenfilename
* import os

### Menú Principal

Para la ventana principal, se hizo uso de la libreria de **Tkinter**, la cual ofrece una amplia cantidad de objetos visuales que son muy interactivos con el usuario, como los botones, las listas de opciones (Combobox) y tambien las etiquetas o labels. Para empezar siempre se declara una ventana o Frame principal que sera el que se utilizara para colocar cada uno de nuestros objetos, una vez declarada nuestra ventana principal, se utilizo las herramientas proporcionadas por Tkinter para generar cada uno de los elementos que conforman la interfaz grafica.

![Manual Técnico](https://i.ibb.co/7YCkZWH/Codigo-Menu-Principal.png)

### Listado de Opciones

Para que el listado de opciones funcione, utilizamos un boton el cual cada vez que se presione, ejecutara la funcion seleccionada dentro del combobox, entonces de esta forma evitamos complicaciones a la hora de realizar la funcion seleccionada por el usuario. Para saber cual fue la opcion seleccionada, se utilizo un metodo que trae el combobox llamado **.get()** el cual nos regresa el valor de la opcion seleccionada, entonces dentro de la funcion **Seleccionar_OPC()** solamente comparamos cada una de las opciones para saber cual fue la que selecciono y dependiendo de eso, entonces el programa ejecutara la parte del codigo correspondiente.

![Manual Técnico](https://i.ibb.co/JyXN5FD/Codigo-Combobox.png)

### Tokens

Dentro de la clase **Token()**, es donde armaremos cada uno de los tokens que encontremos, ya que cuenta con 4 atributos, que son el nombre del lexema que encontro, el lexema en si, la fila y la columna en donde se encuentra dicho lexema. Entonces al momento de almacenarlos en la lista, se manda a llamar a una instancia de esta clase, donde se guardan todos los parametros y luego esa instancia, es almacenada en la lista junto con todos los demas lexemas que se vayan encontrando en el documento.

![Manual Técnico](https://i.ibb.co/kqSRBSF/Clase-Tokens.png)

### Errores

la clase **Error()** es la clase que se utilizo para armar todos los errores de tipo lexico que se fueran encontrando, cada vez que se encontraba un error, se llamaba a una instancia de esta clase para luego formar el error con la estructura que lleva, la cual es, primero el lexema no identificado, el tipo de error, que en este caso seria lexico, y la fila y columna donde se encontro a dicho lexema. Una vez creado el error, era ingresado a la lista de errores junto con los demas.

![Manual Técnico](https://i.ibb.co/W3v8ysP/Clase-Errores.png)

### Analizador Lexico

En la clase **Analizar()** es donde encontraremos todos los metodos y variables que usaremos para llevar a cabo el analisis lexico. En esta ocasion, se hizo uso del codigo ascii para determinar el tipo de caracter que encontrabamos, entonces si se encontraba una letra por su codigo ascii, se mandaba a llamar a su respectiva funcion, donde se encontraba el lexema o si el codigo ascii coincidia con el de un numero, entonces se llamaba a la respectiva funcion donde se encontraba si el numero era un entero o un decimal y asi con todos los caracteres que reconocia el lenguaje. Si encontraba un caracter que no coincidiera con ninguno de los que reconocia el lenguaje, entonces se entendia que se trataba de un error y se llamaba a la clase para formar el error. Una vez armado un lexema, este se guardaba en la lista, la cual luego de terminar con todo el documento, era enviada al analizador sintactico para operar las funciones.

![Manual Técnico](https://i.ibb.co/tD2JVY9/Clase-Analizador-Lexico.png)

### Analizador Sintactico

Dentro de la clase **Sintactico()** tenemos 3 funciones principales, las cuales son:

* **claves()**: esta funcion esta encargada de obtener todas las claves del inventario, por lo que realizara un pop() a la lista de tokens y revisara uno por uno para ver que cumpla con la estructura que debe llevar el archivo, una vez termine con la primera clave, entonces pasara a llamar a otra funcion que se encargara de obtener todas las demas claves. Si encuentra un lexema que no debe ir ahi o si falta alguno, entonces parara el flujo y creara el error, indicando si el lexema no pertenece a ese lugar o si hace falta alguno. Al encontrar un error, el programa se saltara hasta la siguiente palabra clave o, en su defecto, hasta el siguiente corchete de cierre.

![Manual Técnico](https://i.ibb.co/1ZsPY5N/Clase-Analizador-Sintactico.png)

* **registros()**: como lo indica su nombre, se encargara de obtener todos los registros que vienen en el documento. Al igual que con la anterior funcion, realizara un pop() a la lista de tokens y revisara que todos esten en orden y que no falte ninguno, si alguno faltara o si hubiera uno de mas, entonces procedera a generar el error indicando que fue lo que paso y al mismo tiempo no guardara ningun otro registro.

![Manual Técnico](https://i.ibb.co/ysBcmnR/funcion-registros.png)

* **funciones()**: En el caso de las funciones, el programa realizara lo mismo, hara un pop a la lista de tokens y confirmara si lo primero que encuentra es una palabra clave, entonces si eso es verdad, confirma que la estructura de la funcion este correcta, si no encuentra la palabra clave o si en la estructura hay algo que no se encuentra o esta de mas, entonces el programa generara el respectivo error y lo agregara a la lista de errores. Una vez compruebe que la estructura es la correcta, entonces esta es enviada a otra funcion donde sera operada, comprobando si se trata de un imprimir, imprimirln, suma, promedio, conteo, etc.

![Manual Técnico](https://i.ibb.co/dpGx186/funcion-funciones.png)

### Gramatica Independiente del contexto

Para realizar el Analizador Sintactico, se utilizo una gramatica libre de contexto o independiente del contexto, la cual fue la siguiente:

![Manual Técnico](https://i.ibb.co/Yhw7ddZ/Gramatica.png)

### Reporte de Tokens

Dentro de una de las funcionalidades que tiene el usuario, es poder generar un reporte de tokens, donde le mostrara listado, en formato html, una tabla con todos los tokens analizados y encontrados durante la ejecucion del analizador lexico. Para realizar la tabla, solamente abrimos un archivo nuevo y lo guardamos con extension html y luego procedemos a recorrer la lista de tokens que obtuvimos del analizador, para luego crear cada una de las filas de la tabla, con el nombre, el lexema, la fila y la columna de dicho token.

![Manual Técnico](https://i.ibb.co/Ht3Gf2r/reporte-de-tokens.png)

### Reporte de Errores

Dentro de una de las funcionalidades que tiene el usuario, es poder generar un reporte de Errores, donde le mostrara listado, en formato html, una tabla con todos los errores econtrados durante la ejecucion de los analizadores, por lo que le mostrara todos los errores lexicos y sintacticos. Para realizar la tabla, solamente abrimos un archivo nuevo y lo guardamos con extension html y luego procedemos a recorrer la lista de errores lexicos primero, donde iremos añadiendo cada error uno por uno, colocando el tipo de error, el lexema del error y la fila y columna del mismo; de la misma forma para la lista de errores sintacticos que obtenemos.

![Manual Técnico](https://i.ibb.co/L0TrvGs/reporte-de-errores.png)

---