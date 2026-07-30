class Maquina:

    TIPOS_MANUTENCAO_VALIDOS = ('Preventiva', 'Corretiva', 'Preditiva')
    STATUS_OPERACIONAL_VALIDOS = ('Operando', 'Parado', 'Em Manutenção')

    def __init__(self, tag_equipamento, modelo_maquina, numero_serie, localizacao_maquina,
                 tipo_manutencao_padrao, setor, status_operacional='Operando', ultima_manutencao=None):
        self.__tag_equipamento = tag_equipamento
        self.__modelo_maquina = modelo_maquina
        self.numero_serie = numero_serie
        self.localizacao_maquina = localizacao_maquina
        self.tipo_manutencao_padrao = tipo_manutencao_padrao
        self.__setor = setor
        self.status_operacional = status_operacional
        self.__ultima_manutencao = ultima_manutencao

    def apresentar(self):
        print("===== Dados da Máquina =====")
        print(f"TAG: {self.__tag_equipamento}")
        print(f"Modelo: {self.__modelo_maquina.nome_modelo if self.__modelo_maquina else 'Não informado'}")
        print(f"Número de série: {self.__numero_serie}")
        print(f"Localização: {self.__localizacao_maquina}")
        print(f"Tipo de manutenção padrão: {self.__tipo_manutencao_padrao}")
        print(f"Status operacional: {self.__status_operacional}")
        print(f"Última manutenção: {self.__ultima_manutencao or 'Sem registro'}")
        print(f"Setor: {self.__setor.nome_setor if self.__setor else 'Não informado'}")

    # getters
    @property
    def tag_equipamento(self):
        return self.__tag_equipamento

    @property
    def modelo_maquina(self):
        return self.__modelo_maquina

    @property
    def numero_serie(self):
        return self.__numero_serie

    @property
    def localizacao_maquina(self):
        return self.__localizacao_maquina

    @property
    def tipo_manutencao_padrao(self):
        return self.__tipo_manutencao_padrao

    @property
    def status_operacional(self):
        return self.__status_operacional

    @property
    def ultima_manutencao(self):
        return self.__ultima_manutencao

    @property
    def setor(self):
        return self.__setor

    # setters
    @modelo_maquina.setter
    def modelo_maquina(self, valor):
        self.__modelo_maquina = valor

    @numero_serie.setter
    def numero_serie(self, valor):
        if not valor or valor.strip() == "":
            raise ValueError("O número de série não pode estar vazio.")
        self.__numero_serie = valor

    @localizacao_maquina.setter
    def localizacao_maquina(self, valor):
        if not valor or valor.strip() == "":
            raise ValueError("A localização não pode estar vazia.")
        self.__localizacao_maquina = valor

    @tipo_manutencao_padrao.setter
    def tipo_manutencao_padrao(self, valor):
        if valor not in self.TIPOS_MANUTENCAO_VALIDOS:
            raise ValueError(f"Tipo de manutenção '{valor}' inválido. Valores aceitos: {self.TIPOS_MANUTENCAO_VALIDOS}")
        self.__tipo_manutencao_padrao = valor

    @status_operacional.setter
    def status_operacional(self, valor):
        if valor not in self.STATUS_OPERACIONAL_VALIDOS:
            raise ValueError(f"Status operacional '{valor}' inválido. Valores aceitos: {self.STATUS_OPERACIONAL_VALIDOS}")
        self.__status_operacional = valor

    @setor.setter
    def setor(self, novo_setor):
        self.__setor = novo_setor

    # comportamentos - RN-006
    def iniciar_manutencao(self, data_manutencao):
        self.status_operacional = 'Em Manutenção'
        self.__ultima_manutencao = data_manutencao

    def finalizar_manutencao(self, data_manutencao=None):
        self.status_operacional = 'Operando'
        if data_manutencao:
            self.__ultima_manutencao = data_manutencao

    def parar(self):
        self.status_operacional = 'Parado'