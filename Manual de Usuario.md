# Lenguajes Formales y de Programacion
## Proyecto No.1
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

Una vez iniciada la aplicacion, lo primero que encontraremos sera esta ventana, en donde podemos visualizar 3 botones y un listado de opciones, los primeros tres botones estan relacionados al analizador directamente, mientras que el el listado de opciones y el boton de color rosado, nos sirven para todo lo relacionado con los reportes de errores, de tokens y tambien para generar el arbol de derivacion. Cada uno de los botones morados, realizan sus funciones una vez sean oprimidos, pero el listado de opciones (es donde podemos ver la opcion de **Reporte de Tokens**) funciona con el boton rosado de al lado, una vez seleccionado que queremos realizar, deberemos oprimir el boton rosado y seguido de esto, la opcion elegida se empezara a ejecutar.

![Manual Técnico](https://i.ibb.co/ypf76ZH/Menu-de-inicio.png)

### Listado de opciones
Dentro de las opciones encontramos las siguientes:
* Reporte de Tokens: esta opcion solamente funcionara despues de haber realizado el analisis del archivo, si intenta seleccionar esta opcion antes del analisis, entonces le mostrara un mensaje de error. Si ya realizo el analisis, entonces generara un archivo .html con todos los tokens encontrados, indicando el tipo de token, fila y columna.

* Reporte de Errores: si seleccionamos esta opcion, al igual que con la anterior, si el archivo no ha sido analizado, entonces mostrara un mensaje de error. Esta opcion nos generara un archivo con extension .html donde se enlistaran en una tabla todos los errores lexicos y sintacticos, colocando el error encontrado, el tipo de error, con su fila y columna.

* Arbol de derivacion: Esta opcion tambien mostrara un mensaje de error si se intenta usar antes de analizar el archivo. Generara en un archivo .html el arbol de derivacion resultante de el analisis del archivo.

![Manual Técnico](https://i.ibb.co/XzmLsCM/Opciones-Combobox.png)

### Opcion de Abrir

La opcion de **Abrir** la utilizaremos para cargar el archivo con extension .bizdata que procederemos a analizar. Al momento de utilizar el boton, nos depliegara una ventana con el explorador de archivos, si el archivo seleccionado no es uno con esa extension, entonces mostrara un mensaje de error y al igual, si no seleccionamos ningun archivo, entonces nos mostrara un error donde nos indicara que no hemos seleccionado nada. Una vez seleccionado el archivo, entonces se nos despliegara en el area de texto que se encuentra del lado izquierdo.

![Manual Técnico](https://i.ibb.co/zJBHD1n/Opcion-de-Abrir.png)

### Opcion de Analizar

La opcion de **Analizar** iniciara el proceso de analisis del archivo .bizdata cargado, cabe resaltar que si no se ha cargado ningun archivo al area de texto de la izquierda, entonces al usar el boton, nos mostrara un mensaje de error. Una vez cargado el archivo y que lo podamos visualizar en el lado izquierdo, el programa nos mostrara un mensaje indicando que el archivo fue analizado correctamente y nos mostrara en el lado derecho las instrucciones que traia el archivo, pero ya ejecutadas.

![Manual Técnico](https://i.ibb.co/GH1BRd4/Opcion-de-Analizar.png)

---

