class Nodo:
    def __init__(self, data):
        self.data = data
        self.prox = None

    def __repr__(self) -> str:
        return f'{self.data} -> {self.prox}'


class Lista_Enc:
    def __init__(self):  # Inicia a lista vazia
        self.begin = None
        self.size = 0
    def insert(self, value, pos):
        ''' Método para inserir um elemento na lista, recebe como parametro o valor e a posição na lista que quer ser inserida'''
        self.new_data = Nodo(value)
        if pos > 0 and pos <= self.size + 1:

            if pos == 1:  # Insere na primeira posição

                if self.begin == None:
                    self.begin = self.new_data

                else:
                    self.new_data.prox = self.begin
                    self.begin = self.new_data

            else:  # Insere no meio e no final
                self.ptAux = self.begin
                self.index = 1
                while self.index < pos:

                    if self.index == pos - 1 and self.ptAux.prox != None:  # Inserir no meio
                        self.new_data.prox = self.ptAux.prox
                        self.ptAux.prox = self.new_data

                    elif self.index == pos - 1 and self.ptAux.prox == None:  # Inserir no final
                        self.ptAux.prox = self.new_data

                    else:
                        self.ptAux = self.ptAux.prox
                    self.index += 1
            self.size += 1
            return True
        else:
            return False

    def remove(self, pos):
        self.ptAux1 = self.begin
        self.ptAux2 = None
        self.index = 1

        if pos >= 1 and pos <= self.size:
            while self.index <= pos:
                if pos == 1:
                    self.begin = self.ptAux1.prox

                elif self.index == pos:
                    self.ptAux2.prox = self.ptAux1.prox

                else:
                    self.ptAux2 = self.ptAux1
                    self.ptAux1 = self.ptAux1.prox

                self.index += 1
            self.size -= 1
            return True
        else:
            return False

    def find_position(self, pos):
        self.ptAux = self.begin
        self.index = 1
        if pos >= 1 and pos <= self.size:
            while self.index <= pos:
                if self.index == pos:
                    return self.ptAux.data
                else:
                    self.ptAux = self.ptAux.prox
                    self.index += 1
        else:
            return None

    def find_value(self, value):
        ptAux = self.begin
        index = 1
        while ptAux:
            if ptAux.data == value:

                return index
            else:
                index += 1
                ptAux = ptAux.prox
        return False
