class Error():
    
    def __init__(self, lexema, tipoError, fila, columna):
        
        self.lexema = lexema
        self.tipoError = tipoError
        self.fila = fila
        self.columna = columna
    
    def __str__(self):
        
        return "Lexema: " + self.lexema + ", tipo: " + self.tipoError + ", fila: " + self.fila + ", columna: " + self.columna
        