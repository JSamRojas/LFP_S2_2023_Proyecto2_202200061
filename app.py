from tkinter import Text
from tkinter import ttk
from tkinter import Tk, messagebox, filedialog
import tkinter as tk
from fileinput import filename
from tkinter.filedialog import askopenfilename
from Analisis.Lexico import Analizar

ebg = '#BD0665'
fg = '#FFFFFF'
global TxtArchivo
global TxtArchivoAnalizado
global nombre_archivo
global linea
global Abrio
global ventana
nombre_archivo = ""
Abrio = False
ventana = tk.Tk()

def Vista():
    global TxtArchivo
    global TxtArchivoAnalizar
    global ventana
    
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
    
    BtnSelec = tk.Button(ventana, text = "Seleccionar", bg = "#BD0665", fg = "white")
    BtnSelec.place(x = 1060, y = 10, width = 100, height = 30)
    
    BtnAnalizar = tk.Button(ventana, text = "Analizar", bg = "#B70DEE", fg = "white", command = Analizar_DOC)
    BtnAnalizar.place(x = 770, y = 10, width = 100, height = 30)
    
    BtnAbrir = tk.Button(ventana, text = "Abrir", bg = "#B70DEE", fg = "white", command = Abrir_DOC)
    BtnAbrir.place(x = 640, y = 10, width = 100, height = 30)
    
    TxtArchivo = Text(ventana)
    TxtArchivo.config(font = ("Consolas", 10), padx = 10, pady = 10)
    TxtArchivo.place(x = 100, y = 100, width = 500, height = 550)
    
    TxtArchivoAnalizar = Text(ventana)
    TxtArchivoAnalizar.config(font = ("Consolas", 10), padx = 10, pady = 10, state = "disabled")
    TxtArchivoAnalizar.place(x = 750, y = 100, width = 350, height = 550)
    
    ventana.mainloop()

def Abrir_DOC():
    
    global linea
    global nombre_archivo
    global TxtArchivo
    global Abrio
    global ventana
    
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
    
    TxtArchivo.insert(1.0,linea)
    Abrio = True

def Analizar_DOC():
    
    global Abrio
    
    if Abrio == False:
        
        messagebox.showerror(message = "No ha cargado ningun archivo Bizdata", title = "Error")
    
    else:
        
        Analisis = Analizar(linea)
        Analisis.ObtenerTokens()
        
        if not len(Analisis.ErroresLexicos) == 0:
            
            messagebox.showwarning(message = "Errores detectados", title = "Warning")
        
        else:
            
            messagebox.showinfo(message = "Analisis realizado con Exito!", title = "Analizar lexico y sintactico")
        
Vista()
    