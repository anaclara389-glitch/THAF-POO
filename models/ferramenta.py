class Ferramenta:

    STATUS_VALIDOS = ('Disponível', 'Solicitada', 'Em Uso', 'Manutenção/Calibração', 'Extraviada')

    def __init__(self, id_ferramenta, nome_ferramenta, status_ferramenta='Disponível'):
        self.__id_ferramenta = id_ferramenta
        self.nome_ferramenta = nome_ferramenta
        self.status_ferramenta = status_ferramenta

    def apresentar(self):
        print("===== Dados da Ferramenta =====")
        print(f"Id da ferramenta: {self.__id_ferramenta}")
        print(f"Nome: {self.__nome_ferramenta}")
        print(f"Status: {self.__status_ferramenta}")

    # getters
    @property
    def id_ferramenta(self):
        return self.__id_ferramenta

    @property
    def nome_ferramenta(self):
        return self.__nome_ferramenta

    @property
    def status_ferramenta(self):
        return self.__status_ferramenta

    # setters
    @nome_ferramenta.setter
    def nome_ferramenta(self, valor):
        if not valor or valor.strip() == "":
            raise ValueError("O nome da ferramenta não pode estar vazio.")
        self.__nome_ferramenta = valor

    @status_ferramenta.setter
    def status_ferramenta(self, valor):
        if valor not in self.STATUS_VALIDOS:
            raise ValueError(f"Status '{valor}' inválido. Valores aceitos: {self.STATUS_VALIDOS}")
        self.__status_ferramenta = valor

    # comportamentos - RN-011 e RN-012
    def solicitar(self):
        if self.__status_ferramenta != 'Disponível':
            raise ValueError(f"Ferramenta '{self.__nome_ferramenta}' não está disponível para solicitação.")
        self.status_ferramenta = 'Solicitada'

    def retirar(self):
        self.status_ferramenta = 'Em Uso'

    def devolver(self, avariada=False):
        self.status_ferramenta = 'Manutenção/Calibração' if avariada else 'Disponível'

    def marcar_extraviada(self):
        self.status_ferramenta = 'Extraviada'