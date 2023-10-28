from tkinter import Text
from tkinter import ttk
from tkinter import Tk, messagebox, filedialog
import tkinter as tk
from fileinput import filename
from tkinter.filedialog import askopenfilename
from Analisis.Lexico import Analizar
from Analisis.sintactico import Sintactico

ebg = '#BD0665'
fg = '#FFFFFF'
global TxtArchivo
global TxtArchivoAnalizado
global nombre_archivo
global linea
global Abrio
global ventana
global opciones
nombre_archivo = ""
Abrio = False
ventana = tk.Tk()
global TokensCopia
TokensCopia = []
global ErroresLex
ErroresLex = []
global ErroresSin
ErroresSin = []

def Vista():
    global TxtArchivo
    global TxtArchivoAnalizar
    global ventana
    global opciones
    
    ventana.title("Analizador lexico y Sintactico")
    ventana.geometry("1200x700")
    
    label = tk.Label(ventana,bg = "#0C6D5C")
    label.place(x=0, y=0, width = 1200, height = 50)
    
    style = ttk.Style()
    style.theme_use('alt') 
    
    ventana.option_add('*TCombobox*Listbox*Background', ebg)
    ventana.option_add('*TCombobox*Listbox*Foreground', fg)
    ventana.option_add('*TCombobox*Listbox*selectBackground', fg)
    ventana.option_add('*TCombobox*Listbox*selectForeground', ebg)
    
    style.map('TCombobox', fieldbackground=[('readonly', ebg)])
    style.map('TCombobox', selectbackground=[('readonly', ebg)])
    style.map('TCombobox', selectforeground=[('readonly', fg)])
    style.map('TCombobox', background=[('readonly', ebg)])
    style.map('TCombobox', foreground=[('readonly', fg)]) 
    
    opciones = ttk.Combobox(state = "readonly", values = ["Reporte de Tokens", "Reporte de Errores", "Arbol de derivacion"])
    opciones.place(x = 900, y = 10, width = 130, height = 30)
    opciones.current(0)
    
    BtnSelec = tk.Button(ventana, text = "Seleccionar", bg = "#BD0665", fg = "white", command = Seleccionar_OPC)
    BtnSelec.place(x = 1060, y = 10, width = 100, height = 30)
    
    BtnAnalizar = tk.Button(ventana, text = "Analizar", bg = "#B70DEE", fg = "white", command = Analizar_DOC)
    BtnAnalizar.place(x = 770, y = 10, width = 100, height = 30)
    
    BtnAbrir = tk.Button(ventana, text = "Abrir", bg = "#B70DEE", fg = "white", command = Abrir_DOC)
    BtnAbrir.place(x = 640, y = 10, width = 100, height = 30)
    
    TxtArchivo = Text(ventana)
    TxtArchivo.config(font = ("Consolas", 10), padx = 10, pady = 10)
    TxtArchivo.place(x = 50, y = 100, width = 500, height = 550)
    
    TxtArchivoAnalizar = Text(ventana)
    TxtArchivoAnalizar.config(font = ("Consolas", 10), padx = 10, pady = 10, state = "disabled")
    TxtArchivoAnalizar.place(x = 650, y = 100, width = 450, height = 550)
    
    ventana.mainloop()

def Abrir_DOC():
    
    global linea
    global nombre_archivo
    global TxtArchivo
    global Abrio
    global ventana
    global TxtArchivoAnalizar
    
    linea = ""
            
    Tk().withdraw()
    try:
                
        filename = askopenfilename(title="Seleccione el archivo", filetypes=[('Archivos BIZDATA', f'*.bizdata')])
        partido = filename.split("/")
        nombre_archivo = partido.pop()
                
        with open(filename, encoding='utf-8') as infile:
                linea = infile.read()
                        
    except:
                
        messagebox.showerror(message = "No selecciono ningun archivo", title = "Error")
        return
    
    TxtArchivo.delete(1.0, tk.END)
    TxtArchivo.insert(1.0,linea)
    TxtArchivoAnalizar.delete(1.0, tk.END)
    Abrio = True

def Analizar_DOC():
    
    global Abrio
    global TokensCopia
    global ErroresLex
    global ErroresSin
    global TxtArchivoAnalizar
    
    if Abrio == False:
        
        messagebox.showerror(message = "No ha cargado ningun archivo Bizdata", title = "Error")
    
    else:
        
        Analisis = Analizar(linea)
        Analisis.ObtenerTokens()
        TokensCopia = Analisis.Lista_Tokens[:]
        ErroresLex = Analisis.ErroresLexicos[:]
        Analisis_Sint = Sintactico(Analisis.Lista_Tokens)
        Analisis_Sint.Analisis_Sintactico()
        ErroresSin = Analisis_Sint.errores_Sintacticos[:]
        Producciones = Analisis_Sint.listaProducciones[:]
        TxtArchivoAnalizar.config(state = "normal")
        
        i = 1
        TxtArchivoAnalizar.delete(1.0, tk.END)
        while Producciones:
            
            TxtArchivoAnalizar.insert(float(i), Producciones[0] + "\n")
            Producciones.pop(0)
            i += 1
            
        if len(Analisis.ErroresLexicos) != 0 and len(ErroresSin) != 0:
            messagebox.showwarning(message = "Errores lexicos y sintacticos detectados", title = "Warning")
            messagebox.showinfo(message = "Analisis realizado con Exito!", title = "Analizar lexico y sintactico")
        elif len(Analisis.ErroresLexicos) != 0:
            messagebox.showwarning(message = "Errores lexicos detectados", title = "Warning")
            messagebox.showinfo(message = "Analisis realizado con Exito!", title = "Analizar lexico y sintactico")
        elif len(ErroresSin) != 0:
            messagebox.showwarning(message = "Errores lexicos detectados", title = "Warning")
            messagebox.showinfo(message = "Analisis realizado con Exito!", title = "Analizar lexico y sintactico")
        else:
            
            messagebox.showinfo(message = "Analisis realizado con Exito!", title = "Analizar lexico y sintactico")

def Seleccionar_OPC():
    
    global opciones
    TipoRepor = ""
    global Abrio
    
    if opciones.get() == "Reporte de Tokens":

        if Abrio == False:
            
            messagebox.showerror(message = "No ha cargado ningun archivo Bizdata", title = "Error")
        
        else:
            
            TipoRepor = "Tokens"
            Reportes(TipoRepor)
    
    elif opciones.get() == "Reporte de Errores":
        
        if Abrio == False:
            
            messagebox.showerror(message = "No ha cargado ningun archivo Bizdata", title = "Error")
        
        else:
            
            TipoRepor = "Errores"
            Reportes(TipoRepor)
            

def Reportes(Tipo):
    
    global TokensCopia
    global ErroresLex
    global ErroresSin

    if Tipo == "Tokens":
        
        with open("Reporte de Tokens.html", "w") as archivo_html:
            
            archivo_html.write("<html>\n")
            archivo_html.write("<head><title>Reporte de Tokens</title></head>\n")
            archivo_html.write("<body>\n")
            archivo_html.write("<h1>Tokens Encontrados</h1>\n")
            archivo_html.write("<table border='1'>\n")
            archivo_html.write("<tr><th>Tipo de Token</th><th>Nombre de Token</th><th>Fila</th><th>Columna</th></tr>\n")
            
            for tokens in TokensCopia:
                
                archivo_html.write("<tr>")
                archivo_html.write(f"<td>{tokens.nombre}</td>")
                archivo_html.write(f"<td>{tokens.lexema}</td>")
                archivo_html.write(f"<td>{tokens.fila}</td>")
                archivo_html.write(f"<td>{tokens.columna}</td>")
                archivo_html.write("</tr>\n")
                
            archivo_html.write("</table>\n")
            archivo_html.write("</body>\n")
            archivo_html.write("</html>\n")
                            
    elif Tipo == "Errores":
        
        with open("Errores.html", "w") as archivo_html:
            
            archivo_html.write("<html>\n")
            archivo_html.write("<head><title>Reporte de Errores</title></head>\n")
            archivo_html.write("<body>\n")
            archivo_html.write("<h1>Errores Encontrados</h1>\n")
            archivo_html.write("<table border='1'>\n")
            archivo_html.write("<tr><th>Tipo de Error</th><th>Descripcion</th><th>Fila</th><th>Columna</th></tr>\n")
            
            for errlex in ErroresLex:
                
                archivo_html.write("<tr>")
                archivo_html.write(f"<td>{errlex.tipoError}</td>")
                archivo_html.write(f"<td>{errlex.lexema}</td>")
                archivo_html.write(f"<td>{errlex.fila}</td>")
                archivo_html.write(f"<td>{errlex.columna}</td>")
                archivo_html.write("</tr>\n")
            
            for errsin in ErroresSin:
                
                archivo_html.write("<tr>")
                archivo_html.write(f"<td>{errsin.tipoError}</td>")
                archivo_html.write(f"<td>{errsin.lexema}</td>")
                archivo_html.write(f"<td>{errsin.fila}</td>")
                archivo_html.write(f"<td>{errsin.columna}</td>")
                archivo_html.write("</tr>\n")
            
            archivo_html.write("</table>\n")
            archivo_html.write("</body>\n")
            archivo_html.write("</html>\n")
        
Vista()
    