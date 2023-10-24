from Analisis.Errores import Error
from Analisis.Tokens import Token

class Sintactico():
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.listaClaves = []
        self.listaRegistros = []
        self.errores_Sintacticos = []

        tokenNuevo = Token('EOF', 'EOF', 0, 0)
        self.tokens.append(tokenNuevo)

    def Analisis_Sintactico(self):

        self.inicio()

    def inicio(self):

        self.claves()
        self.registros()
        self.funciones()
        print(self.listaClaves)
        print(self.listaRegistros)

    # <Claves> ::= Claves igual Corchete_A String <otra_Clave> Corchete_C
    def claves(self):

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

                            self.agregar_Error(self.tokens[0])
                            self.recuperarDos("Registros", "Palabra_Clave")

                    else:

                        self.agregar_Error(self.tokens[0])
                        self.recuperar("CorcheteCierre")

                else:

                    self.agregar_Error(self.tokens[0])
                    self.recuperar("CorcheteCierre")

            else:

                self.agregar_Error(self.tokens[0])
                self.recuperar("CorcheteCierre")

        else:

            self.agregar_Error(self.tokens[0])
            self.recuperar("CorcheteCierre")

    def agregar_Error(self, token):

        lexema = token.lexema
        fila = token.fila
        columna = token.columna
        error = Error(lexema,"Sintactico" , fila, columna)
        self.errores_Sintacticos.append(error)

    def otraClave(self):

        if self.tokens[0].nombre == "Coma":

            self.tokens.pop(0)

            if self.tokens[0].nombre == "String":

                clave = self.tokens.pop(0)
                self.listaClaves.append(clave.lexema)
                self.otraClave()

            else:

                self.agregar_Error(self.tokens[0])
                self.recuperarDos("CorcheteCierre", "Registros")

    # <Registros> ::= Registros igual Corchete_A <Registro> <otro_Registro> Corchete_C
    def registros(self):

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

                        self.agregar_Error(self.tokens[0])
                        self.recuperar("Palabra_Clave")

                else:

                    self.agregar_Error(self.tokens[0])
                    self.recuperarDos("CorcheteCierre", "Palabra_Clave")

            else:

                self.agregar_Error(self.tokens[0])
                self.recuperarDos("CorcheteCierre", "Palabra_Clave")

        else:

            self.agregar_Error(self.tokens[0])
            self.recuperarDos("Registros", "Palabra_Clave")

    #<Registro> ::= LLave_A <Valor> <otro_Valor> Llave_C
    def registro(self):

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

                    self.agregar_Error(self.tokens[0])
                    self.recuperarDos("CorcheteCierre", "Palabra_Clave")

        else:

            self.agregar_Error(self.tokens[0])
            self.recuperar("Palabra_Clave")

    # <Valor> ::= String
    #             | int
    #             | float
    def valor(self):

        if self.tokens[0].nombre in ("String", "INT", "Float"):

            campo = self.tokens.pop(0)
            return campo

        else:

            self.agregar_Error(self.tokens[0])
            self.recuperar("Palabra_Clave")

    # <otro_Valor> ::= coma <Valor> <otro_Valor>
    def otroValor(self, registro):

        if self.tokens[0].nombre == "Coma":

            self.tokens.pop(0)
            res = self.valor()

            if res is not None:

                registro.append(res.lexema)
                self.otroValor(registro)

    # <otro_Registro> ::= <Registro><otro_Registro>
    #                         | ε
    def otroRegistro(self):

        if self.tokens[0].nombre == "LlaveAbre":

            self.registro()
            self.otroRegistro()

    #<Funciones> ::= <Funcion> <otra_Funcion>
    def funciones(self):
        self.funcion()
        self.otraFuncion()

    # <funcion> ::= word_key Parentesis_A <Parametros> Parentesis_C Punto_coma

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
                        self.agregar_Error(self.tokens[0])
                        self.recuperar("Palabra_Clave")
                else:
                    self.agregar_Error(self.tokens[0])
                    self.recuperar("Palabra_Clave")
            else:
                self.agregar_Error(self.tokens[0])
                self.recuperar("Palabra_Clave")
        else:
            self.agregar_Error(self.tokens[0])
            self.recuperar("Palabra_Clave")

        # <parametros> ::= <valor> <otroParametro>
        #               | ε

    def parametros(self):
        parametros = []
        if self.tokens[0].nombre != 'ParentCierre':
            valor = self.valor()
            if valor is not None:
                parametros = [valor]
                self.otroParametro(parametros)
        return parametros

        # <otroParametro> ::= coma <Valor> <otro_Parametro>
        #                  | ε

    def otroParametro(self, parametros):
        if self.tokens[0].nombre == 'Coma':
            self.tokens.pop(0)
            valor = self.valor()
            if valor is not None:
                parametros.append(valor)
                self.otroParametro(parametros)

        # <otraFuncion> ::= <funcion> <otraFuncion>
        #                | ε

    def otraFuncion(self):
        if self.tokens[0].nombre != 'EOF':
            self.funcion()
            self.otraFuncion()
        else:
            print("Analisis terminado")

        # Operación de funciones

    def operarFuncion(self, tipo, parametros):
        if len(self.errores_Sintacticos) != 0:
            return
        if tipo.lexema == 'imprimir':
            if len(parametros) == 1:
                print(parametros[0].lexema)
            else:
                print("error: demasiados parámetros en función imprimir")

        elif tipo.lexema == 'conteo':
            if len(parametros) == 0:
                print(len(self.listaRegistros))
            else:
                print("error: demasiados parámetros en función conteo")

        elif tipo.lexema == 'promedio':
            if len(parametros) == 1:
                if parametros[0].nombre == 'String':
                    self.promedio(parametros[0].lexema)
                else:
                    print("error: se esperaba una cadena como parámetro en función promedio")
            else:
                print("error: demasiados parámetros en función promedio")

        # Producción <promedio> -> tk_promedio <CadenaFin>

    def promedio(self, campo):
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
                    suma += len(registro[posicion])
                else:
                    suma += registro[posicion]
            if len(self.listaRegistros) > 0:
                promedio = suma / len(self.listaRegistros)
            print(promedio)

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
