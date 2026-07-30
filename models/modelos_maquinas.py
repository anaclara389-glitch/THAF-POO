class ModeloMaquina:

    def __init__(self, id_maquina, nome_maquina, fabricante_maquina, nome_modelo,
                 descricao_tecnica=None, potencia_especificacao=None):
        self.__id_maquina = id_maquina
        self.nome_maquina = nome_maquina
        self.fabricante_maquina = fabricante_maquina
        self.nome_modelo = nome_modelo
        self.descricao_tecnica = descricao_tecnica
        self.potencia_especificacao = potencia_especificacao

    def apresentar(self):
        print("===== Dados do Modelo de Máquina =====")
        print(f"Id do modelo: {self.__id_maquina}")
        print(f"Nome da máquina: {self.__nome_maquina}")
        print(f"Fabricante: {self.__fabricante_maquina}")
        print(f"Modelo: {self.__nome_modelo}")
        print(f"Descrição técnica: {self.__descricao_tecnica or 'Não informada'}")
        print(f"Potência: {self.__potencia_especificacao or 'Não informada'}")

    # getters
    @property
    def id_maquina(self):
        return self.__id_maquina

    @property
    def nome_maquina(self):
        return self.__nome_maquina

    @property
    def fabricante_maquina(self):
        return self.__fabricante_maquina

    @property
    def nome_modelo(self):
        return self.__nome_modelo

    @property
    def descricao_tecnica(self):
        return self.__descricao_tecnica

    @property
    def potencia_especificacao(self):
        return self.__potencia_especificacao

    # setters
    @nome_maquina.setter
    def nome_maquina(self, valor):
        if not valor or valor.strip() == "":
            raise ValueError("O nome da máquina não pode estar vazio.")
        self.__nome_maquina = valor

    @fabricante_maquina.setter
    def fabricante_maquina(self, valor):
        if not valor or valor.strip() == "":
            raise ValueError("O fabricante não pode estar vazio.")
        self.__fabricante_maquina = valor

    @nome_modelo.setter
    def nome_modelo(self, valor):
        if not valor or valor.strip() == "":
            raise ValueError("O nome do modelo não pode estar vazio.")
        self.__nome_modelo = valor

    @descricao_tecnica.setter
    def descricao_tecnica(self, valor):
        self.__descricao_tecnica = valor

    @potencia_especificacao.setter
    def potencia_especificacao(self, valor):
        self.__potencia_especificacao = valor