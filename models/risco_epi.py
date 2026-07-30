class RiscoEpi:
    """
    Representa a tabela Matriz_Riscos_EPI.
    RN-013: mapeamento de riscos (NR-01) e EPIs obrigatórios para cada atividade.
    """

    def __init__(self, id_risco, risco_nr01, epis_obrigatorios):
        self.__id_risco = id_risco
        self.risco_nr01 = risco_nr01
        self.epis_obrigatorios = epis_obrigatorios

    def apresentar(self):
        print("===== Dados do Risco (NR-01) =====")
        print(f"Id do risco: {self.__id_risco}")
        print(f"Risco: {self.__risco_nr01}")
        print(f"EPIs obrigatórios: {self.__epis_obrigatorios}")

    # getters
    @property
    def id_risco(self):
        return self.__id_risco

    @property
    def risco_nr01(self):
        return self.__risco_nr01

    @property
    def epis_obrigatorios(self):
        return self.__epis_obrigatorios

    # setters
    @risco_nr01.setter
    def risco_nr01(self, valor):
        if not valor or valor.strip() == "":
            raise ValueError("A descrição do risco não pode estar vazia.")
        self.__risco_nr01 = valor

    @epis_obrigatorios.setter
    def epis_obrigatorios(self, valor):
        if not valor or valor.strip() == "":
            raise ValueError("É obrigatório informar ao menos um EPI.")
        self.__epis_obrigatorios = valor