# Importa a função responsável por conectar ao banco de dados
from database import conectar

# Importa a biblioteca time para utilizar pausas no sistema
import time


# ---------------------------------------------------------------------------
# Classe utilitária - entrada e validação de dados do usuário
# ---------------------------------------------------------------------------
class Utilidades:
    """Reúne métodos estáticos de leitura e validação de entrada do usuário."""

    @staticmethod
    def ler_inteiro(mensagem):
        """Garante que o usuário digite apenas números inteiros."""
        while True:
            valor = input(mensagem)
            try:
                return int(valor)
            except ValueError:
                print("Digite apenas números.")

    @staticmethod
    def ler_inteiro_opcional(mensagem):
        """Permite informar um número inteiro ou deixar o campo em branco (retorna None)."""
        while True:
            valor = input(mensagem)

            if valor.strip() == "":
                return None

            try:
                return int(valor)
            except ValueError:
                print("Digite apenas números ou deixe em branco.")

    @staticmethod
    def ler_texto_opcional(mensagem):
        """Permite informar um texto ou deixar o campo vazio (retorna None)."""
        valor = input(mensagem).strip()
        return valor if valor else None

    @staticmethod
    def ler_opcao_valida(mensagem, opcoes_validas):
        """Verifica se a opção digitada pertence às opções permitidas."""
        while True:
            valor = input(mensagem)

            if valor.lower() in opcoes_validas:
                return valor

            print("Opção inválida!")


# ---------------------------------------------------------------------------
# Classe de modelo/repositório - CRUD de Movimentação de Ferramentas
# ---------------------------------------------------------------------------
class MovimentacaoFerramentas:
    """Encapsula todas as operações de CRUD relacionadas às movimentações de ferramentas."""

    # Status permitidos para uma movimentação.
    STATUS_VALIDOS = ['solicitado', 'em uso', 'atrasado', 'devolvido']
    STATUS_PADRAO = 'Solicitado'

    def listar(self):
        """Lista todas as movimentações cadastradas."""
        conexao = None
        cursor = None

        try:
            conexao = conectar()
            cursor = conexao.cursor()

            sql = """
            SELECT
                id_movimentacao,
                id_os_ferramenta,
                id_os,
                id_usuario_solicitante,
                id_usuario_entregador,
                data_retirada,
                data_devolucao_prevista,
                data_devolucao_real,
                status_movimentacao,
                observacoes
            FROM Movimentacao_Ferramentas
            """

            cursor.execute(sql)
            dados = cursor.fetchall()

            if not dados:
                print("Nenhuma movimentação cadastrada.")
                return

            for movimentacao in dados:
                print(movimentacao)

        except Exception as erro:
            print("Erro ao listar movimentações:", erro)

        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()

    def cadastrar(self, id_os_ferramenta, id_os, id_usuario_solicitante,
                  id_usuario_entregador, data_retirada, data_devolucao_prevista,
                  observacoes, status_movimentacao=STATUS_PADRAO):
        """Cadastra uma nova movimentação de ferramenta."""
        conexao = None
        cursor = None

        try:
            conexao = conectar()
            cursor = conexao.cursor()

            sql = """
            INSERT INTO Movimentacao_Ferramentas
                (id_os_ferramenta, id_os, id_usuario_solicitante,
                id_usuario_entregador, data_retirada,
                data_devolucao_prevista, status_movimentacao, observacoes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            valores = (
                id_os_ferramenta,
                id_os,
                id_usuario_solicitante,
                id_usuario_entregador,
                data_retirada,
                data_devolucao_prevista,
                status_movimentacao,
                observacoes
            )

            cursor.execute(sql, valores)
            conexao.commit()

            print("Movimentação cadastrada com sucesso!")

        except Exception as erro:
            if conexao:
                conexao.rollback()
            print("Erro ao cadastrar movimentação (verifique se os IDs informados existem):", erro)

        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()

    def atualizar_status(self, id_movimentacao, status_movimentacao):
        """Atualiza o status de uma movimentação."""
        conexao = None
        cursor = None

        try:
            conexao = conectar()
            cursor = conexao.cursor()

            sql = """
            UPDATE Movimentacao_Ferramentas
            SET status_movimentacao = %s
            WHERE id_movimentacao = %s
            """

            valores = (status_movimentacao, id_movimentacao)
            cursor.execute(sql, valores)
            conexao.commit()

            if cursor.rowcount > 0:
                print(f"Status da movimentação {id_movimentacao} atualizado com sucesso!")
            else:
                print("Movimentação não encontrada.")

        except Exception as erro:
            if conexao:
                conexao.rollback()
            print("Erro ao atualizar status da movimentação:", erro)

        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()

    def registrar_devolucao(self, id_movimentacao, data_devolucao_real):
        """Registra a devolução de uma ferramenta."""
        conexao = None
        cursor = None

        try:
            conexao = conectar()
            cursor = conexao.cursor()

            sql = """
            UPDATE Movimentacao_Ferramentas
            SET
                data_devolucao_real = %s,
                status_movimentacao = 'Devolvido'
            WHERE id_movimentacao = %s
            """

            valores = (data_devolucao_real, id_movimentacao)
            cursor.execute(sql, valores)
            conexao.commit()

            if cursor.rowcount > 0:
                print(f"Devolução da movimentação {id_movimentacao} registrada com sucesso!")
            else:
                print("Movimentação não encontrada.")

        except Exception as erro:
            if conexao:
                conexao.rollback()
            print("Erro ao registrar devolução:", erro)

        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()

    def deletar(self, id_movimentacao):
        """Remove uma movimentação cadastrada."""
        conexao = None
        cursor = None

        try:
            conexao = conectar()
            cursor = conexao.cursor()

            sql = "DELETE FROM Movimentacao_Ferramentas WHERE id_movimentacao = %s"
            cursor.execute(sql, (id_movimentacao,))
            conexao.commit()

            if cursor.rowcount > 0:
                print(f"Movimentação {id_movimentacao} deletada com sucesso!")
            else:
                print("Movimentação não encontrada.")

        except Exception as erro:
            if conexao:
                conexao.rollback()
            print("Erro ao deletar movimentação:", erro)

        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()


# ---------------------------------------------------------------------------
# Classe de interface - Menu de Movimentação de Ferramentas
# ---------------------------------------------------------------------------
class MenuMovimentacao:
    """Camada de interação com o usuário (menu no terminal) para as movimentações."""

    def __init__(self):
        self.movimentacao = MovimentacaoFerramentas()

    def exibir(self):
        """Mantém o menu em execução até que o usuário escolha sair."""
        while True:
            print("\n------ Menu Movimentação de Ferramentas ------")
            print("1 - Listar movimentações")
            print("2 - Cadastrar movimentação")
            print("3 - Atualizar status da movimentação")
            print("4 - Registrar devolução")
            print("5 - Deletar movimentação")
            print("0 - Sair")

            opcao = Utilidades.ler_inteiro("Coloque qual opção deseja: ")

            if opcao == 1:
                self._listar()
            elif opcao == 2:
                self._cadastrar()
            elif opcao == 3:
                self._atualizar_status()
            elif opcao == 4:
                self._registrar_devolucao()
            elif opcao == 5:
                self._deletar()
            elif opcao == 0:
                print("Voltando...")
                break
            else:
                print("Opção inválida!")

    def _listar(self):
        print("\n--- Lista de Movimentações ---")
        self.movimentacao.listar()
        time.sleep(2)

    def _cadastrar(self):
        print("\n--- Cadastrar Movimentação ---")

        id_os_ferramenta = Utilidades.ler_inteiro("ID da ferramenta na OS (id_os_ferramenta): ")
        id_os = Utilidades.ler_inteiro("ID da Ordem de Serviço: ")
        id_usuario_solicitante = Utilidades.ler_inteiro("ID do usuário solicitante: ")

        id_usuario_entregador = Utilidades.ler_inteiro_opcional(
            "ID do usuário entregador (deixe em branco se ainda não definido): "
        )

        data_retirada = Utilidades.ler_texto_opcional(
            "Data de retirada AAAA-MM-DD HH:MM:SS (deixe em branco se ainda não retirou): "
        )

        data_devolucao_prevista = input(
            "Data de devolução prevista (AAAA-MM-DD HH:MM:SS): "
        )

        observacoes = Utilidades.ler_texto_opcional("Observações (opcional): ")

        self.movimentacao.cadastrar(
            id_os_ferramenta,
            id_os,
            id_usuario_solicitante,
            id_usuario_entregador,
            data_retirada,
            data_devolucao_prevista,
            observacoes
        )

    def _atualizar_status(self):
        print("\n--- Atualizar Status da Movimentação ---")

        id_m = Utilidades.ler_inteiro("Digite o ID da movimentação que deseja atualizar: ")

        status = Utilidades.ler_opcao_valida(
            "Novo status (Solicitado, Em Uso, Atrasado, Devolvido): ",
            MovimentacaoFerramentas.STATUS_VALIDOS
        )

        self.movimentacao.atualizar_status(id_m, status)

    def _registrar_devolucao(self):
        print("\n--- Registrar Devolução ---")

        id_m = Utilidades.ler_inteiro("Digite o ID da movimentação a ser devolvida: ")

        data_devolucao_real = input(
            "Data de devolução real (AAAA-MM-DD HH:MM:SS): "
        )

        self.movimentacao.registrar_devolucao(id_m, data_devolucao_real)

    def _deletar(self):
        print("\n--- Deletar Movimentação ---")

        id_m = Utilidades.ler_inteiro("Digite o ID da movimentação que deseja deletar: ")

        self.movimentacao.deletar(id_m)


# ---------------------------------------------------------------------------
# Função de conveniência para manter compatibilidade com o código antigo
# ---------------------------------------------------------------------------
def opcao_desejada_movimentacao():
    """Ponto de entrada equivalente à função original — abre o menu de movimentações."""
    MenuMovimentacao().exibir()


if __name__ == "__main__":
    opcao_desejada_movimentacao()