from Analisis.Errores import Error
from Analisis.Tokens import Token

global lex_a_imprimir
lex_a_imprimir = ""
global err_Principal
err_Principal = False

class Sintactico():
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.listaClaves = []
        self.listaRegistros = []
        self.errores_Sintacticos = []
        self.listaProducciones = []

        tokenNuevo = Token('EOF', 'EOF', 0, 0)
        self.tokens.append(tokenNuevo)

    def Analisis_Sintactico(self):

        self.inicio()

    def inicio(self):
        global err_Principal
        err_Principal = False
        self.claves()
        self.registros()
        self.funciones()
        print(self.listaClaves)
        print(self.listaRegistros)

    def claves(self):
        global err_Principal
        if self.tokens[0].nombre == "Claves":

            self.tokens.pop(0)

            if self.tokens[0].nombre == "SignIgual":

                self.tokens.pop(0)

                if self.tokens[0].nombre == "CorcheteAbre":

                    self.tokens.pop(0)

                    if self.tokens[0].nombre == "String":

                        clave = self.tokens.pop(0)
                        self.listaClaves.append(clave.lexema)
                        self.otraClave()

                        if self.tokens[0].nombre == "CorcheteCierre":

                            self.tokens.pop(0)

                        else:
                            err_Principal = True
                            self.agregar_Error(self.tokens[0], "Falta el campo")
                            self.recuperarDos("Registros", "Palabra_Clave")

                    else:
                        err_Principal = True
                        self.agregar_Error(self.tokens[0], "Falta el Corchete de Cierre")
                        self.recuperar("CorcheteCierre")

                else:
                    err_Principal = True
                    self.agregar_Error(self.tokens[0], "Falta el Corchete de Apertura")
                    self.recuperar("CorcheteCierre")

            else:
                err_Principal = True
                self.agregar_Error(self.tokens[0], "Falta Signo Igual")
                self.recuperar("CorcheteCierre")

        else:
            err_Principal = True
            self.agregar_Error(self.tokens[0], "Falta Palabra Clave")
            self.recuperar("CorcheteCierre")

    def agregar_Error(self, token, descripcion):

        lexema = token.lexema
        fila = token.fila
        columna = token.columna
        error = Error(lexema, descripcion, fila, columna)
        self.errores_Sintacticos.append(error)

    def otraClave(self):
        global err_Principal
        if self.tokens[0].nombre == "Coma":

            self.tokens.pop(0)

            if self.tokens[0].nombre == "String":

                clave = self.tokens.pop(0)
                self.listaClaves.append(clave.lexema)
                self.otraClave()

            else:
                err_Principal = True
                self.agregar_Error(self.tokens[0], "Falta el campo")
                self.recuperarDos("CorcheteCierre", "Registros")
        
    def registros(self):
        global err_Principal
        if self.tokens[0].nombre == "Registros":

            self.tokens.pop(0)

            if self.tokens[0].nombre == "SignIgual":

                self.tokens.pop(0)

                if self.tokens[0].nombre == "CorcheteAbre":

                    self.tokens.pop(0)
                    self.registro()
                    self.otroRegistro()

                    if self.tokens[0].nombre == "CorcheteCierre":

                        self.tokens.pop(0)

                    else:
                        err_Principal = True
                        self.agregar_Error(self.tokens[0], "Sintactico")
                        self.recuperar("Palabra_Clave")

                else:
                    err_Principal = True
                    self.agregar_Error(self.tokens[0], "Falta el Corchete de Apertura")
                    self.recuperarDos("CorcheteCierre", "Palabra_Clave")

            else:
                err_Principal = True
                self.agregar_Error(self.tokens[0], "Falta el Signo Igual")
                self.recuperarDos("CorcheteCierre", "Palabra_Clave")

        else:
            err_Principal = True
            self.agregar_Error(self.tokens[0], "Falta Palabra Clave")
            self.recuperarDos("Registros", "Palabra_Clave")

    def registro(self):
        global err_Principal
        if self.tokens[0].nombre == "LlaveAbre":

            self.tokens.pop(0)
            res = self.valor()

            if res is not None:

                registro = []
                registro.append(res.lexema)
                self.otroValor(registro)

                if self.tokens[0].nombre == "LlaveCierre":

                    self.tokens.pop(0)
                    self.listaRegistros.append(registro)

                else:
                    err_Principal = True
                    self.agregar_Error(self.tokens[0], "Falta la llave de Cierre")
                    self.recuperarDos("CorcheteCierre", "Palabra_Clave")

        else:

            self.agregar_Error(self.tokens[0], "Falta la llave de Apertura")
            self.recuperar("Palabra_Clave")

    def valor(self):

        if self.tokens[0].nombre in ("String", "INT", "Float"):

            campo = self.tokens.pop(0)
            return campo

        else:

            self.agregar_Error(self.tokens[0], "Campo Invalido")
            self.recuperar("Palabra_Clave")

    def otroValor(self, registro):

        if self.tokens[0].nombre == "Coma":

            self.tokens.pop(0)
            res = self.valor()

            if res is not None:

                registro.append(res.lexema)
                self.otroValor(registro)

    def otroRegistro(self):

        if self.tokens[0].nombre == "LlaveAbre":

            self.registro()
            self.otroRegistro()

    def funciones(self):
        self.funcion()
        self.otraFuncion()

    def funcion(self):
        if self.tokens[0].nombre == 'Palabra_Clave':
            tipo = self.tokens.pop(0)
            if self.tokens[0].nombre == 'ParentAbre':
                self.tokens.pop(0)
                parametros = self.parametros()
                if self.tokens[0].nombre == 'ParentCierre':
                    self.tokens.pop(0)
                    if self.tokens[0].nombre == 'PuntoyComa':
                        self.tokens.pop(0)
                        self.operarFuncion(tipo, parametros)
                    else:
                        self.agregar_Error(self.tokens[0], "Falta el punto y Coma")
                        self.recuperar("Palabra_Clave")
                else:
                    self.agregar_Error(self.tokens[0], "Falta el parentesis de Cierre")
                    self.recuperar("Palabra_Clave")
            else:
                self.agregar_Error(self.tokens[0], "Falta el parentesis de Apertura")
                self.recuperar("Palabra_Clave")
        else:
            self.agregar_Error(self.tokens[0], "Falta el nombre de la Funcion")
            self.recuperar("Palabra_Clave")

    def parametros(self):
        parametros = []
        if self.tokens[0].nombre != 'ParentCierre':
            valor = self.valor()
            if valor is not None:
                parametros = [valor]
                self.otroParametro(parametros)
        return parametros

    def otroParametro(self, parametros):
        if self.tokens[0].nombre == 'Coma':
            self.tokens.pop(0)
            valor = self.valor()
            if valor is not None:
                parametros.append(valor)
                self.otroParametro(parametros)

    def otraFuncion(self):
        global lex_a_imprimir
        if self.tokens[0].nombre != 'EOF':
            self.funcion()
            self.otraFuncion()
        else:
            if not lex_a_imprimir == "":
                print(lex_a_imprimir)
                self.listaProducciones.append(lex_a_imprimir)
          #  print("Analisis terminado")

    def operarFuncion(self, tipo, parametros):
        global lex_a_imprimir
        if tipo.lexema == 'imprimir':
            if len(parametros) == 1:
                if lex_a_imprimir == "":
                    lex_a_imprimir += parametros[0].lexema
                else:
                    lex_a_imprimir += " "
                    lex_a_imprimir += parametros[0].lexema
            else:
                self.agregar_Error(parametros[0], "Cantidad de campos invalida para la Funcion imprimir")
                
        elif tipo.lexema == 'imprimirln':
            if len(parametros) == 1:
                print(parametros[0].lexema)
                self.listaProducciones.append(parametros[0].lexema)
            else:
                self.agregar_Error(parametros[0], "Cantidad de campos invalida para la Funcion imprimirln")
        if err_Principal == True:
            return

        elif tipo.lexema == 'conteo':
            if len(parametros) == 0:
                print(len(self.listaRegistros))
                self.listaProducciones.append(str(len(self.listaRegistros)))
            else:
                self.agregar_Error(parametros[0], "Cantidad de campos invalida para la Funcion conteo")

        elif tipo.lexema == 'promedio':
            if len(parametros) == 1:
                if parametros[0].nombre == 'String':
                    self.promedio(parametros[0].lexema, parametros[0])
                else:
                    self.agregar_Error(parametros[0], "Campo invalido para la funcion promedio")
            else:
                self.agregar_Error(parametros[0], "Cantidad de campos invalida para la Funcion promedio")
        
        elif tipo.lexema == 'contarsi':
            if len(parametros) == 2:
                if parametros[0].nombre == 'String':
                    self.contarsi(parametros[0].lexema, parametros[1].lexema, parametros)
            else: 
                if len(parametros) > 2:
                   # print("error: parametro invalido")
                    self.agregar_Error(parametros[0], "Muchos parametros para la funcion contarsi")
                elif len(parametros) < 2:
                 #   print("error: pocos parametros para la funcion")
                    self.agregar_Error(parametros[0], "Faltan parametros para la funcion contarsi")
        
        elif tipo.lexema == 'datos':
            if len(parametros) > 0:
              #  print("error: esta funcion no debe tener parametros")
                self.agregar_Error(parametros[0], "Cantidad de campos invalida para la Funcion datos")
            else:
                self.datos()
                
        elif tipo.lexema == 'sumar':
            if len(parametros) == 1:
                if parametros[0].nombre == 'String':
                    self.sumar(parametros[0].lexema, parametros[0])
                else:
                  #  print("error: parametro invalido")
                    self.agregar_Error(parametros[0], "Campo invalido para la funcion sumar")
            else:
               # print("error: Muchos parametros")
                self.agregar_Error(parametros[0], "Cantidad de campos invalida para la Funcion sumar")
        
        elif tipo.lexema == 'min':
            if len(parametros) == 1:
                if parametros[0].nombre == 'String':
                    self.min(parametros[0].lexema, parametros[0])
                else:
                  #  print("error: parametro invalido")
                    self.agregar_Error(parametros[0], "Campo invalido para la funcion min")
            else:
              #  print("error: parametro invalido")
                self.agregar_Error(parametros[0], "Cantidad de campos invalida para la Funcion min")
        
        elif tipo.lexema == 'max':
            if len(parametros) == 1:
                if parametros[0].nombre == 'String':
                    self.max(parametros[0].lexema, parametros[0])
                else:
                   # print("error: parametro invalido")
                    self.agregar_Error(parametros[0], "Campo invalido para la funcion max")
            else:
               # print("error: parametro invalido")
                self.agregar_Error(parametros[0], "Cantidad de campos invalida para la Funcion max")
        
        elif tipo.lexema == 'exportarReporte':
            if len(parametros) == 1:
                if parametros[0].nombre == 'String':
                    self.exportarReporte(parametros[0].lexema)
                else:
                   # print("error: parametro invalido")
                    self.agregar_Error(parametros[0], "Campo invalido para la funcion exportarReporte")
            else:
              # print("error: parametro invalido")
                self.agregar_Error(parametros[0], "Cantidad de campos invalida para la Funcion exportarReporte")
                     
    def promedio(self, campo, parametro):
        encontrado = False
        posicion = -1
        for c in self.listaClaves:
            posicion += 1
            if c == campo:
                encontrado = True
                break
        if encontrado:
            suma = 0
            promedio = 0
            for registro in self.listaRegistros:
                if isinstance(registro[posicion], str):
                   # print("error: parametro invalido")
                    self.agregar_Error(parametro, "Campo invalido para la funcion promedio")
                    return
                else:
                    suma += registro[posicion]
            if len(self.listaRegistros) > 0:
                promedio = suma / len(self.listaRegistros)
            print(promedio)
            self.listaProducciones.append(str(promedio))
    
    def contarsi(self, campo1, campo2, parametro):
        encontrado = False
        posicion = -1
        for c in self.listaClaves:
            posicion += 1
            if c == campo1:
                encontrado = True
                break
        if encontrado:
            contador = 0
            if isinstance(campo2, int):  
                for registro in self.listaRegistros:
                    if isinstance(registro[posicion], str):
                       # print("Error: parametro invalido")
                        self.agregar_Error(parametro[1], "Campo invalido para la funcion contarsi")
                    else:
                        ListaNumeros = registro[posicion]
                        ListaNumeros = str(ListaNumeros)
                        ListaNumeros = list(ListaNumeros)
                        for numero in ListaNumeros:
                            if numero == str(campo2):
                                contador += 1 
                print(contador)
                self.listaProducciones.append(str(contador))   
            else:
               # print("Error: parametro invalido")
                self.agregar_Error(parametro[1], "Campo invalido para la funcion contarsi")
        
    def datos(self):
        claves = ""
        registros = ""
        for clave in self.listaClaves:
            claves += clave + "\t\t"
    
        claves = ">>> " + claves
        print(claves)
        self.listaProducciones.append(claves)
        
        for registro in self.listaRegistros:
            registros = ""
            for dato in registro:
                registros += str(dato) + "\t\t"
            registros = ">>> " + registros    
            print(registros)
            self.listaProducciones.append(registros)
            
    def sumar(self, campo, parametro):
        encontrado = False
        posicion = -1
        for c in self.listaClaves:
            posicion += 1
            if c == campo:
                encontrado = True
                break
        if encontrado:
            suma = 0
            for registro in self.listaRegistros:
                if isinstance(registro[posicion], str):
                   # print("error: parametro invalido")
                    self.agregar_Error(parametro, "Campo invalido para la funcion sumar")
                    return
                else:
                    suma += registro[posicion]
            print(suma)
            self.listaProducciones.append(str(suma))
    
    def min(self, campo, parametro):
        encontrado = False
        posicion = -1
        for c in self.listaClaves:
            posicion += 1
            if c == campo:
                encontrado = True
                break
        if encontrado:
                Listavalores = []
                minimo = 0
                for registro in self.listaRegistros:
                    if isinstance(registro[posicion], str):
                       # print("error: parametro invalido")
                        self.agregar_Error(parametro, "Campo invalido para la funcion min")
                        return
                    else:
                        Listavalores.append(registro[posicion])
                minimo = min(Listavalores)
                print(minimo)
                self.listaProducciones.append(str(minimo))
    
    def max(self, campo, parametro):
        encontrado = False
        posicion = -1
        for c in self.listaClaves:
            posicion += 1
            if c == campo:
                encontrado = True
                break
        if encontrado:
                Listavalores = []
                maximo = 0
                for registro in self.listaRegistros:
                    if isinstance(registro[posicion], str):
                        #print("error: parametro invalido")
                        self.agregar_Error(parametro, "Campo invalido para la funcion max")
                        return
                    else:
                        Listavalores.append(registro[posicion])
                maximo = max(Listavalores)
                print(maximo)
                self.listaProducciones.append(str(maximo))
    
    def exportarReporte(self, campo):
        
        with open(campo + ".html", "w") as archivo_html:
            
            archivo_html.write("<html>\n")
            archivo_html.write(f"<head><title>{campo}</title></head>\n")
            archivo_html.write("<body>\n")
            archivo_html.write(f"<h1>{campo}</h1>\n")
            archivo_html.write("<table border='1'>\n")
            archivo_html.write("<tr>")
            
            for clave in self.listaClaves:
                archivo_html.write(f"<th>{clave}</th>")   
                
            archivo_html.write("</tr>\n")
            
            for registro in self.listaRegistros:
                archivo_html.write("<tr>")
                for dato in registro:
                    archivo_html.write(f"<td>{dato}</td>")
                archivo_html.write("</tr>\n")
        
            archivo_html.write("</table>\n")
            archivo_html.write("</body>\n")
            archivo_html.write("</html>\n")
               
    def recuperar(self, nombreToken):
        while self.tokens[0].nombre != 'EOF':
            if self.tokens[0].nombre == nombreToken:
                if not self.tokens[0].nombre in ("Registro", "Claves", "Palabra_Clave"):
                    self.tokens.pop(0)
                break
            else:
                self.tokens.pop(0)

    def recuperarDos(self, nombreToken1, nombreToken2):
        while self.tokens[0].nombre != 'EOF':
            if self.tokens[0].nombre in (nombreToken1, nombreToken2):
                if not self.tokens[0].nombre in ("Registro", "Claves", "Palabra_Clave"):
                    self.tokens.pop(0)
                break
            else:
                self.tokens.pop(0)
