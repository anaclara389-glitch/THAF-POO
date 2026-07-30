# Importa a função responsável por conectar ao banco de dados.
from database import conectar

# Importa a classe datetime para manipulação de datas e horários.
from datetime import datetime


# ---------------------------------------------------------------------------
# CLASSE ORDEM DE SERVIÇO (Entidade / Modelo)
# ---------------------------------------------------------------------------

class OrdemServico:
    """Representa uma Ordem de Serviço (OS), com seus dados básicos."""

    def __init__(self, id_os=None, tag_equipamento=None, descricao_falha=None,
                 data_abertura=None, hh_inicio=None, hh_fim=None,
                 status_os=None, id_usuario=None):
        self.id_os = id_os
        self.tag_equipamento = tag_equipamento
        self.descricao_falha = descricao_falha
        self.data_abertura = data_abertura
        self.hh_inicio = hh_inicio
        self.hh_fim = hh_fim
        self.status_os = status_os
        self.id_usuario = id_usuario

    def __str__(self):
        return (f"OS: {self.id_os} | Equipamento: {self.tag_equipamento} | "
                f"Falha: {self.descricao_falha} | Abertura: {self.data_abertura} | "
                f"Início: {self.hh_inicio} | Fim: {self.hh_fim} | "
                f"Status: {self.status_os} | Usuário: {self.id_usuario}")


# ---------------------------------------------------------------------------
# CLASSE ORDEM DE SERVIÇO DAO (Acesso a dados / Regras de negócio com o banco)
# ---------------------------------------------------------------------------

class OrdemServicoDAO:
    """Responsável por toda a comunicação com o banco de dados para a entidade OrdemServico."""

    # -----------------------------------------------------------------
    # LISTAR ORDENS DE SERVIÇO
    # -----------------------------------------------------------------
    def listar(self):
        """Lista todas as Ordens de Serviço cadastradas. Retorna uma lista de objetos OrdemServico."""

        conexao = None
        cursor = None

        try:
            # Abre conexão com o banco.
            conexao = conectar()
            cursor = conexao.cursor()

            # Consulta SQL que retorna todas as Ordens de Serviço.
            sql = """
            SELECT
                os.id_os,
                os.tag_equipamento,
                os.descricao_falha,
                os.data_abertura,
                os.hh_inicio,
                os.hh_fim,
                os.status_os,
                os.id_usuario
            FROM Ordens_Servico AS os
            """

            # Executa a consulta.
            cursor.execute(sql)

            # Armazena todos os registros retornados.
            dados = cursor.fetchall()

            # Converte cada linha do banco em um objeto OrdemServico.
            ordens = [
                OrdemServico(id_os, tag_equipamento, descricao_falha, data_abertura,
                             hh_inicio, hh_fim, status_os, id_usuario)
                for id_os, tag_equipamento, descricao_falha, data_abertura,
                    hh_inicio, hh_fim, status_os, id_usuario in dados
            ]

            return ordens

        except Exception as erro:
            print("Erro ao listar ordens de serviço:", erro)
            return []

        finally:
            # Fecha cursor e conexão.
            if cursor:
                cursor.close()

            if conexao:
                conexao.close()

    # -----------------------------------------------------------------
    # CRIAR ORDEM DE SERVIÇO
    # -----------------------------------------------------------------
    def criar(self, os_: OrdemServico):
        """Cria uma nova Ordem de Serviço a partir de um objeto OrdemServico."""

        conexao = None
        cursor = None

        try:
            # Abre conexão com o banco.
            conexao = conectar()
            cursor = conexao.cursor()

            # Insere uma nova Ordem de Serviço.
            # O status será "Aberto" por padrão.
            # O horário de término permanecerá nulo até o encerramento.
            sql = """
            INSERT INTO Ordens_Servico
                (id_os,
                 tag_equipamento,
                 descricao_falha,
                 data_abertura,
                 hh_inicio,
                 id_usuario)
            VALUES (%s, %s, %s, %s, %s, %s)
            """

            valores = (
                os_.id_os,
                os_.tag_equipamento,
                os_.descricao_falha,
                os_.data_abertura,
                os_.hh_inicio,
                os_.id_usuario
            )

            cursor.execute(sql, valores)

            # Salva as alterações.
            conexao.commit()

            print(f"OS {os_.id_os} criada com sucesso!")

        except Exception as erro:
            # Cancela alterações caso ocorra erro.
            if conexao:
                conexao.rollback()

            print(
                "Erro ao criar OS (verifique se o ID já existe ou se equipamento/usuário são válidos):",
                erro
            )

        finally:
            # Fecha cursor e conexão.
            if cursor:
                cursor.close()

            if conexao:
                conexao.close()

    # -----------------------------------------------------------------
    # ATUALIZAR STATUS DA OS
    # -----------------------------------------------------------------
    def atualizar_status(self, id_os, status_os):
        """Atualiza o status de uma Ordem de Serviço."""

        conexao = None
        cursor = None

        try:
            # Abre conexão com o banco.
            conexao = conectar()
            cursor = conexao.cursor()

            # Atualiza apenas o status da Ordem de Serviço.
            sql = """
            UPDATE Ordens_Servico
            SET status_os = %s
            WHERE id_os = %s
            """

            cursor.execute(sql, (status_os, id_os))

            # Salva as alterações.
            conexao.commit()

            # Verifica se a OS existe.
            if cursor.rowcount > 0:
                print(f"Status da OS {id_os} atualizado para '{status_os}'!")
            else:
                print("OS não encontrada.")

        except Exception as erro:
            # Cancela alterações caso ocorra erro.
            if conexao:
                conexao.rollback()

            print(
                "Erro ao atualizar status (verifique se o valor é válido para o ENUM):",
                erro
            )

        finally:
            # Fecha cursor e conexão.
            if cursor:
                cursor.close()

            if conexao:
                conexao.close()

    # -----------------------------------------------------------------
    # ENCERRAR OS
    # -----------------------------------------------------------------
    def encerrar(self, id_os, hh_fim):
        """Encerra uma Ordem de Serviço, atualizando o horário final e o status para Concluído."""

        conexao = None
        cursor = None

        try:
            # Abre conexão com o banco.
            conexao = conectar()
            cursor = conexao.cursor()

            sql = """
            UPDATE Ordens_Servico
            SET
                hh_fim = %s,
                status_os = 'Concluído'
            WHERE id_os = %s
            """

            cursor.execute(sql, (hh_fim, id_os))

            # Salva as alterações.
            conexao.commit()

            # Verifica se a OS foi encontrada.
            if cursor.rowcount > 0:
                print(f"OS {id_os} encerrada com sucesso!")
            else:
                print("OS não encontrada.")

        except Exception as erro:
            # Desfaz alterações caso ocorra erro.
            if conexao:
                conexao.rollback()

            print(
                "Erro ao encerrar OS (verifique se o horário de término é posterior ao de início):",
                erro
            )

        finally:
            # Fecha cursor e conexão.
            if cursor:
                cursor.close()

            if conexao:
                conexao.close()

    # -----------------------------------------------------------------
    # DELETAR OS
    # -----------------------------------------------------------------
    def deletar(self, id_os):
        """Remove uma Ordem de Serviço do banco de dados."""

        conexao = None
        cursor = None

        try:
            # Abre conexão com o banco.
            conexao = conectar()
            cursor = conexao.cursor()

            # Exclui a Ordem de Serviço.
            # Os registros relacionados serão apagados automaticamente
            # devido ao ON DELETE CASCADE.
            sql = "DELETE FROM Ordens_Servico WHERE id_os = %s"

            cursor.execute(sql, (id_os,))

            # Salva as alterações.
            conexao.commit()

            # Verifica se a OS foi removida.
            if cursor.rowcount > 0:
                print(f"OS {id_os} deletada com sucesso!")
            else:
                print("OS não encontrada.")

        except Exception as erro:
            # Cancela alterações caso ocorra erro.
            if conexao:
                conexao.rollback()

            print("Erro ao deletar OS:", erro)

        finally:
            # Fecha cursor e conexão.
            if cursor:
                cursor.close()

            if conexao:
                conexao.close()


# ---------------------------------------------------------------------------
# CLASSE FERRAMENTA DA OS DAO
# ---------------------------------------------------------------------------

class OSFerramentaDAO:
    """Responsável pelo vínculo entre Ordens de Serviço e ferramentas."""

    def adicionar(self, id_os, id_ferramenta):
        """Vincula uma ferramenta a uma Ordem de Serviço."""

        conexao = None
        cursor = None

        try:
            # Abre conexão com o banco.
            conexao = conectar()
            cursor = conexao.cursor()

            # Insere o vínculo entre a OS e a ferramenta.
            sql = """
            INSERT INTO OS_Ferramentas (id_os, id_ferramenta)
            VALUES (%s, %s)
            """

            cursor.execute(sql, (id_os, id_ferramenta))

            # Salva as alterações.
            conexao.commit()

            print(f"Ferramenta {id_ferramenta} vinculada à OS {id_os}!")

        except Exception as erro:
            # Cancela alterações caso ocorra erro.
            if conexao:
                conexao.rollback()

            print(
                "Erro ao vincular ferramenta (verifique se a OS e a ferramenta existem):",
                erro
            )

        finally:
            # Fecha cursor e conexão.
            if cursor:
                cursor.close()

            if conexao:
                conexao.close()

    def listar(self, id_os):
        """Lista todas as ferramentas vinculadas a uma Ordem de Serviço."""

        conexao = None
        cursor = None

        try:
            # Abre conexão com o banco.
            conexao = conectar()
            cursor = conexao.cursor()

            sql = """
            SELECT
                id_os_ferramenta,
                id_os,
                id_ferramenta
            FROM OS_Ferramentas
            WHERE id_os = %s
            """

            cursor.execute(sql, (id_os,))

            dados = cursor.fetchall()

            # Verifica se existem ferramentas cadastradas para essa OS.
            if not dados:
                print("Nenhuma ferramenta vinculada a essa OS.")
                return []

            # Exibe todas as ferramentas encontradas.
            for item in dados:
                print(item)

            return dados

        except Exception as erro:
            print("Erro ao listar ferramentas da OS:", erro)
            return []

        finally:
            # Fecha cursor e conexão.
            if cursor:
                cursor.close()

            if conexao:
                conexao.close()


# ---------------------------------------------------------------------------
# CLASSE MATERIAL (PEÇA) DA OS DAO
# ---------------------------------------------------------------------------

class OSMaterialDAO:
    """Responsável pelo vínculo entre Ordens de Serviço e materiais (peças)."""

    def adicionar(self, id_os, id_peca, quantidade_utilizada):
        """Vincula uma peça/material a uma Ordem de Serviço."""

        conexao = None
        cursor = None

        try:
            # Abre conexão com o banco.
            conexao = conectar()
            cursor = conexao.cursor()

            # Insere o vínculo entre a OS e a peça utilizada.
            sql = """
            INSERT INTO OS_Materiais
                (id_os, id_peca, quantidade_utilizada)
            VALUES (%s, %s, %s)
            """

            cursor.execute(sql, (id_os, id_peca, quantidade_utilizada))

            # Salva as alterações.
            conexao.commit()

            print(f"Material (peça {id_peca}) vinculado à OS {id_os}!")

        except Exception as erro:
            # Cancela alterações caso ocorra erro.
            if conexao:
                conexao.rollback()

            print("Erro ao vincular material (verifique se OS/peça existem e se a quantidade é maior que 0):", erro)

        finally:
            # Fecha cursor e conexão.
            if cursor:
                cursor.close()

            if conexao:
                conexao.close()

    def listar(self, id_os):
        """Lista todos os materiais vinculados a uma Ordem de Serviço."""

        conexao = None
        cursor = None

        try:
            # Abre conexão com o banco.
            conexao = conectar()
            cursor = conexao.cursor()

            sql = """
            SELECT
                id_os_material,
                id_os,
                id_peca,
                quantidade_utilizada
            FROM OS_Materiais
            WHERE id_os = %s
            """

            cursor.execute(sql, (id_os,))

            dados = cursor.fetchall()

            # Verifica se existem materiais vinculados.
            if not dados:
                print("Nenhum material vinculado a essa OS.")
                return []

            # Exibe os materiais encontrados.
            for item in dados:
                print(item)

            return dados

        except Exception as erro:
            print("Erro ao listar materiais da OS:", erro)
            return []

        finally:
            # Fecha cursor e conexão.
            if cursor:
                cursor.close()

            if conexao:
                conexao.close()


# ---------------------------------------------------------------------------
# CLASSE RISCO / EPI DA OS DAO
# ---------------------------------------------------------------------------

class OSRiscoDAO:
    """Responsável pelo vínculo entre Ordens de Serviço e riscos (EPI)."""

    def adicionar(self, id_os, id_risco):
        """Vincula um risco (EPI) a uma Ordem de Serviço."""

        conexao = None
        cursor = None

        try:
            # Abre conexão com o banco.
            conexao = conectar()
            cursor = conexao.cursor()

            sql = """
            INSERT INTO OS_Seguranca (id_os, id_risco)
            VALUES (%s, %s)
            """

            cursor.execute(sql, (id_os, id_risco))

            # Salva as alterações.
            conexao.commit()

            print(f"Risco {id_risco} vinculado à OS {id_os}!")

        except Exception as erro:
            # Cancela alterações caso ocorra erro.
            if conexao:
                conexao.rollback()

            print("Erro ao vincular risco (verifique se a OS e o risco existem):", erro)

        finally:
            # Fecha cursor e conexão.
            if cursor:
                cursor.close()

            if conexao:
                conexao.close()

    def listar(self, id_os):
        """Lista todos os riscos vinculados a uma Ordem de Serviço."""

        conexao = None
        cursor = None

        try:
            # Abre conexão com o banco.
            conexao = conectar()
            cursor = conexao.cursor()

            sql = """
            SELECT
                id_os_seguranca,
                id_os,
                id_risco
            FROM OS_Seguranca
            WHERE id_os = %s
            """

            cursor.execute(sql, (id_os,))

            dados = cursor.fetchall()

            # Verifica se existem riscos cadastrados.
            if not dados:
                print("Nenhum risco vinculado a essa OS.")
                return []

            # Exibe todos os riscos encontrados.
            for item in dados:
                print(item)

            return dados

        except Exception as erro:
            print("Erro ao listar riscos da OS:", erro)
            return []

        finally:
            # Fecha cursor e conexão.
            if cursor:
                cursor.close()

            if conexao:
                conexao.close()


# ---------------------------------------------------------------------------
# CLASSE MENU MANUTENÇÃO (Interface com o usuário)
# ---------------------------------------------------------------------------

class MenuManutencao:
    """Responsável por exibir o menu principal de Ordens de Serviço e interagir com o usuário."""

    # Lista de status válidos.
    OPCOES_STATUS = ['Aberto', 'Em andamento', 'Concluído']

    def __init__(self):
        # Cada menu possui seu próprio DAO para acessar o banco.
        self.dao = OrdemServicoDAO()
        # Menu de relacionamentos (ferramentas/materiais/riscos).
        self.menu_relacionamentos = MenuOSRelacionamentos()

    # Função que garante que o usuário digite apenas números inteiros.
    def ler_inteiro(self, mensagem):
        while True:
            valor = input(mensagem)
            try:
                return int(valor)
            except ValueError:
                print("Digite apenas números.")

    # Função que valida se a opção digitada pertence à lista de opções permitidas.
    def ler_opcao_valida(self, mensagem, opcoes_validas):
        while True:
            valor = input(mensagem)
            if valor.lower() in [o.lower() for o in opcoes_validas]:
                return valor
            print("Opção inválida!")

    def exibir_lista(self):
        print("\n--- Lista de Ordens de Serviço ---")

        ordens = self.dao.listar()

        if not ordens:
            print("Nenhuma ordem de serviço cadastrada.")
        else:
            for os_ in ordens:
                print(os_)

    def exibir_criar(self):
        print("\n--- Criar Ordem de Serviço ---")

        id_os = self.ler_inteiro("ID da OS: ")
        tag_equipamento = input("TAG do Equipamento: ")
        descricao_falha = input("Descrição da Falha: ")
        data_abertura = input("Data de Abertura (AAAA-MM-DD): ")
        hh_inicio = input("Horário de Início (HH:MM:SS): ")

        id_usuario_input = input(
            "ID do Usuário responsável (deixe em branco se não houver): "
        )
        id_usuario = int(id_usuario_input) if id_usuario_input.strip() else None

        nova_os = OrdemServico(
            id_os=id_os,
            tag_equipamento=tag_equipamento,
            descricao_falha=descricao_falha,
            data_abertura=data_abertura,
            hh_inicio=hh_inicio,
            id_usuario=id_usuario
        )

        self.dao.criar(nova_os)

    def exibir_atualizar_status(self):
        print("\n--- Atualizar Status da OS ---")

        id_os = self.ler_inteiro("ID da OS: ")
        status_os = self.ler_opcao_valida(
            f"Novo Status {self.OPCOES_STATUS}: ",
            self.OPCOES_STATUS
        )

        self.dao.atualizar_status(id_os, status_os)

    def exibir_encerrar(self):
        print("\n--- Encerrar OS ---")

        id_os = self.ler_inteiro("ID da OS: ")
        hh_fim = input("Horário de Término (HH:MM:SS): ")

        self.dao.encerrar(id_os, hh_fim)

    def exibir_deletar(self):
        print("\n--- Deletar OS ---")

        id_os = self.ler_inteiro("ID da OS que deseja deletar: ")

        self.dao.deletar(id_os)

    # Menu principal das Ordens de Serviço.
    def opcao_desejada_manutencao(self):

        while True:

            # Exibe o menu principal.
            print("\n------ Menu Manutenção (OS) ------")
            print("1 - Listar ordens de serviço")
            print("2 - Criar ordem de serviço")
            print("3 - Atualizar status da OS")
            print("4 - Encerrar OS")
            print("5 - Deletar OS")
            print("6 - Gerenciar ferramentas/materiais/riscos da OS")
            print("0 - Sair")

            opcao = self.ler_inteiro("Coloque qual opção deseja: ")

            # Lista todas as Ordens de Serviço.
            if opcao == 1:
                self.exibir_lista()

            # Cria uma nova Ordem de Serviço.
            elif opcao == 2:
                self.exibir_criar()

            # Atualiza o status da Ordem de Serviço.
            elif opcao == 3:
                self.exibir_atualizar_status()

            # Encerra uma Ordem de Serviço.
            elif opcao == 4:
                self.exibir_encerrar()

            # Remove uma Ordem de Serviço.
            elif opcao == 5:
                self.exibir_deletar()

            # Abre o menu de relacionamentos.
            elif opcao == 6:
                self.menu_relacionamentos.opcao_desejada_os_relacionamentos()

            # Sai do menu.
            elif opcao == 0:
                print("Voltando...")
                break

            else:
                print("Opção inválida!")


# ---------------------------------------------------------------------------
# CLASSE MENU RELACIONAMENTOS DA OS (Interface com o usuário)
# ---------------------------------------------------------------------------

class MenuOSRelacionamentos:
    """Responsável por exibir o menu de ferramentas/materiais/riscos vinculados a uma OS."""

    def __init__(self):
        self.ferramenta_dao = OSFerramentaDAO()
        self.material_dao = OSMaterialDAO()
        self.risco_dao = OSRiscoDAO()

    def ler_inteiro(self, mensagem):
        while True:
            valor = input(mensagem)
            try:
                return int(valor)
            except ValueError:
                print("Digite apenas números.")

    # Menu responsável pelos relacionamentos da Ordem de Serviço.
    def opcao_desejada_os_relacionamentos(self):

        while True:

            # Exibe o menu de relacionamentos.
            print("\n--- Ferramentas / Materiais / Riscos da OS ---")
            print("1 - Vincular ferramenta a uma OS")
            print("2 - Listar ferramentas de uma OS")
            print("3 - Vincular material (peça) a uma OS")
            print("4 - Listar materiais de uma OS")
            print("5 - Vincular risco/EPI a uma OS")
            print("6 - Listar riscos de uma OS")
            print("0 - Voltar")

            opcao = self.ler_inteiro("Coloque qual opção deseja: ")

            # Vincula uma ferramenta.
            if opcao == 1:
                id_os = self.ler_inteiro("ID da OS: ")
                id_ferramenta = self.ler_inteiro("ID da Ferramenta: ")
                self.ferramenta_dao.adicionar(id_os, id_ferramenta)

            # Lista as ferramentas da OS.
            elif opcao == 2:
                id_os = self.ler_inteiro("ID da OS: ")
                self.ferramenta_dao.listar(id_os)

            # Vincula um material.
            elif opcao == 3:
                id_os = self.ler_inteiro("ID da OS: ")
                id_peca = self.ler_inteiro("ID da Peça: ")
                quantidade_utilizada = self.ler_inteiro("Quantidade Utilizada: ")
                self.material_dao.adicionar(id_os, id_peca, quantidade_utilizada)

            # Lista os materiais da OS.
            elif opcao == 4:
                id_os = self.ler_inteiro("ID da OS: ")
                self.material_dao.listar(id_os)

            # Vincula um risco.
            elif opcao == 5:
                id_os = self.ler_inteiro("ID da OS: ")
                id_risco = self.ler_inteiro("ID do Risco: ")
                self.risco_dao.adicionar(id_os, id_risco)

            # Lista os riscos da OS.
            elif opcao == 6:
                id_os = self.ler_inteiro("ID da OS: ")
                self.risco_dao.listar(id_os)

            # Retorna ao menu anterior.
            elif opcao == 0:
                break

            # Opção inválida.
            else:
                print("Opção inválida!")


# ---------------------------------------------------------------------------
# PONTO DE ENTRADA (exemplo de uso)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    menu = MenuManutencao()
    menu.opcao_desejada_manutencao()