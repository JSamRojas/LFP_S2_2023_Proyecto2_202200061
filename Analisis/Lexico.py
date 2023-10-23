from Analisis.Tokens import Token
from Analisis.Errores import Error

Reservadas = ["Claves", "Registros"]
Funciones_Reservadas = ["imprimir", "imprimirln", "conteo", "promedio", "contarsi", "sumar", "max", "min", "exportarReporte"]

class Analizar():
    
    def __init__(self, Archivo):
        
        self.Archivo = Archivo
        self.fila = 1
        self.columna = 1
        self.Lista_Tokens = []
        self.ErroresLexicos = []
    
    def ObtenerTokens(self):
        
        fila = self.fila
        columna = self.columna
        Lista_Tokens = self.Lista_Tokens
        Archivo = self.Archivo
        apuntador = 0
        
        while Archivo:
            
            char = Archivo[apuntador]
            apuntador += 1
            codigo = ord(char)
            
            if (codigo >= 65 and codigo <= 90) or (codigo >= 97 and codigo <= 122):
                
                copia = Archivo
                lex, Archivo, palabra = self.palabra_clave(Archivo)
                
                if lex and Archivo and palabra:
                    
                    arma_lex = Token(palabra, lex, fila, columna)
                    columna += len(lex)
                    Lista_Tokens.append(arma_lex)
                    apuntador = 0
                
                else:
                    
                    arma_err = Error(lex, "lexico", fila, columna)
                    self.ErroresLexicos.append(arma_err)
                    Archivo = copia[len(lex):]
                    apuntador = 0
                    columna += len(lex)
            
            elif codigo == 61:
                
                arma_lex = Token("SignIgual", char, fila, columna)
                columna += 1
                Lista_Tokens.append(arma_lex)
                Archivo = Archivo[1:]
                apuntador = 0
            
            elif codigo == 91 or codigo == 93:
                
                tipo = ""
                
                if codigo == 91:
                    
                    tipo = "CorcheteAbre"
                
                else:
                    
                    tipo = "CorcheteCierre"
                
                arma_lex = Token(tipo, char, fila, columna)
                Lista_Tokens.append(arma_lex)
                columna += 1
                Archivo = Archivo[1:]
                apuntador = 0
            
            elif codigo == 34:
                
                lexema, Archivo = self.Encont_palabra(Archivo[apuntador:])
                
                if lexema and Archivo:
                    
                    arma_lex = Token("String", lexema, fila, columna)
                    columna += len(lexema)
                    columna += len(lexema) + 1
                    Lista_Tokens.append(arma_lex)
                    apuntador = 0
            
            elif codigo == 44:
                
                arma_lex = Token("Coma", char, fila, columna)
                columna += 1
                Lista_Tokens.append(arma_lex)
                Archivo = Archivo[1:]
                apuntador = 0
            
            elif codigo == 39:
                
                self.fila = fila
                self.columna = columna
                self.Lista_Tokens = Lista_Tokens
                Archivo = self.Encont_Coment_Multi(Archivo)
                columna = self.columna
                fila = self.fila
                
            elif char.isdigit() or codigo in (45,43):
                
                self.fila = fila
                self.columna = columna
                self.Lista_Tokens = Lista_Tokens
                Archivo = self.Encont_Number(Archivo)
                apuntador = 0
                columna = self.columna
            
            elif codigo == 35:
                
                lexema, Archivo = self.Encont_Coment_Simpl(Archivo[apuntador:])
                
                if lexema and Archivo:
                    
                    columna += 1
                    columna += len(lexema)
                    apuntador = 0
            
            elif codigo in (123, 125):
                
                Tipo = ""
                
                if codigo == 123:
                    
                    Tipo = "LlaveAbre"
                
                else:
                    
                    Tipo = "LlaveCierra"
                
                arma_lex = Token(Tipo, char, fila, columna)
                Lista_Tokens.append(arma_lex)
                columna += 1
                Archivo = Archivo[1:]
                apuntador = 0
            
            elif codigo in (40, 41):
                
                Tipo = ""
                
                if codigo == 40:
                    
                    Tipo = "ParentAbre"
                
                if codigo == 41:
                    
                    Tipo = "ParentCierra"

                arma_lex = Token(Tipo, char, fila, columna)
                Lista_Tokens.append(arma_lex)
                columna += 1
                Archivo = Archivo[1:]
                apuntador = 0
            
            elif codigo == 59:
                
                arma_lex = Token("PuntoyComa", char, fila, columna)
                Lista_Tokens.append(arma_lex)
                columna += 1
                Archivo = Archivo[1:]
                apuntador = 0
            
            elif codigo == 10:
                
                Archivo = Archivo[1:]
                apuntador = 0
                fila += 1
                columna = 1
            
            elif codigo == 32:
                
                Archivo = Archivo[1:]
                apuntador = 0
                columna += 1
            
            else:
                
                arma_err = Error(char, "Lexico", fila, columna)
                self.ErroresLexicos.append(arma_err)
                Archivo = Archivo[1:]
                apuntador = 0
                columna += 1
        
        for token in self.Lista_Tokens:
            
            print("Nombre: " + token.nombre + " Token: " + str(token.lexema))
        
        for error in self.ErroresLexicos:
            
            print("Lexema: " + str(error.lexema) + " fila: " + str(error.fila) + " columna: " + str(error.columna))
                              
    def palabra_clave(self, Archivo):
        
        lexema = ''
        
        for char in Archivo:
            
            codigo = ord(char)
            
            if not ((codigo >= 65 and codigo <= 90) or (codigo >= 97 and codigo <= 122)):
                
                for reservada in Reservadas:
                    
                    if lexema == reservada:
                        
                        return lexema, Archivo[len(lexema):], reservada
        
                for funcion in Funciones_Reservadas:
                    
                    if lexema == funcion:
                        
                        return lexema, Archivo[len(lexema):], funcion

                return lexema, None, None
            
            else:
                
                lexema += char
    
    def Encont_palabra(self, Archivo):
        
        lexema = ''
        clave = ''
        
        for char in Archivo:
            
            codigo = ord(char)
            clave += char
            
            if codigo == 34:
                
                return lexema, Archivo[len(clave):]
            
            else:
                
                lexema += char
        
        return None, None
    
    def Encont_Coment_Multi(self, Archivo):
        
        lexema = ''
        estado = 0
        
        for char in Archivo:
            
            codigo = ord(char)
            
            if estado == 0:
                
                if codigo == 39:
                    
                    lexema += char
                    estado = 7
                    self.columna += 1
            
            elif estado == 7:
                
                if codigo == 39:
                    
                    lexema += char
                    estado = 9
                    self.columna += 1
                
                else:
                    
                    arma_err = Error(lexema, "Lexico", self.fila, self.columna)
                    self.ErroresLexicos.append(arma_err)
                    return Archivo[len(lexema):]
            
            elif estado == 9:
                
                if codigo == 39:
                    
                    lexema += char
                    estado = 11
                    self.columna = 1
                
                else:
                    
                    arma_err = Error(lexema, "Lexico", self.fila, self.columna)
                    self.ErroresLexicos.append(arma_err)
                    return Archivo[len(lexema):]
            
            elif estado == 11:
                
                if not codigo == 39:
                    
                    if codigo == 10:
                        
                        self.fila += 1
                        self.columna = 1
                    
                    else:
                        
                        self.columna += 1
                    
                    lexema += char
                    estado = 11
                
                else:
                    
                    self.columna += 1
                    lexema += char
                    estado = 12
            
            elif estado == 12:
                
                if codigo == 39:
                    
                    lexema += char
                    estado = 13
                    self.columna += 1
                
                else:
                    
                    arma_err = Error(lexema, "Lexico", self.fila, self.columna)
                    self.ErroresLexicos.append(arma_err)
                    return Archivo [len(lexema):]
            
            elif estado == 13:
                
                if codigo == 39:
                    
                    lexema += char
                    self.columna += 1
                    return Archivo[len(lexema):]
                
                else:
                    
                    arma_err = Error(lexema, "Lexico", self.fila, self.columna)
                    self.ErroresLexicos.append(arma_err)
                    return Archivo [len(lexema):]
    
    def Encont_Number(self, Archivo):
        
        lexema = ''
        estado = 0
        
        for char in Archivo:
            
            codigo = ord(char)
            
            if estado == 0:
                
                if codigo in (43,45):
                    
                    lexema += char
                    estado = 3
                
                elif char.isdigit():
                    
                    lexema += char
                    estado = 4
                    
            elif estado == 3:
                
                if char.isdigit():
                    
                    lexema += char
                    estado = 4
                
                else:
                    
                    self.columna += len(lexema)
                    arma_err = Error(lexema, "Lexico", self.fila, self.columna)
                    self.ErroresLexicos.append(arma_err)
                    
                    return Archivo[len(lexema):]
            
            elif estado == 4:
                
                if char.isdigit():
                    
                    lexema += char
                
                elif codigo == 46:
                    
                    lexema += char
                    estado = 8
                
                else:
                    
                    self.columna += len(lexema)
                    self.Lista_Tokens.append(Token("INT", int(lexema), self.fila, self.columna))
                    
                    return Archivo[len(lexema):]
            
            elif estado == 8:
                
                if char.isdigit():
                    
                    lexema += char
                    estado = 10
                
                else:
                    
                    self.columna += len(lexema)
                    arma_err = Error(lexema, "Lexico", self.fila, self.columna)
                    self.ErroresLexicos.append(arma_err)
                    
                    return Archivo[len(lexema):]
            
            elif estado == 10:
                
                if char.isdigit():
                    
                    lexema += char
                
                else:
                    
                    self.columna += len(lexema)
                    self.Lista_Tokens.append(Token("Float", float(lexema), self.fila, self.columna))
                    
                    return Archivo[len(lexema):]
    
    def Encont_Coment_Simpl(self, Archivo):
        
        lexema = ''
        
        for char in Archivo:
            
            codigo = ord(char)
            
            if codigo == 10:
                
                return lexema, Archivo[len(lexema):]
            
            else:
                
                lexema += char
        
        return None, None
                  