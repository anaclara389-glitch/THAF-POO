# Importa a função responsável por realizar a conexão com o banco de dados.
from database import conectar


# ---------------------------------------------------------------------------
# CLASSE PEÇA (Entidade / Modelo)
# ---------------------------------------------------------------------------

class Peca:
    """Representa uma peça do almoxarifado, com seus dados básicos."""

    def __init__(self, id_peca=None, nome_peca=None, quantidade_estoque=None,
                 unidade_medida=None, custo_unitario=None):
        self.id_peca = id_peca
        self.nome_peca = nome_peca
        self.quantidade_estoque = quantidade_estoque
        self.unidade_medida = unidade_medida
        self.custo_unitario = custo_unitario

    def __str__(self):
        return (f"ID: {self.id_peca} | Nome: {self.nome_peca} | "
                f"Estoque: {self.quantidade_estoque} {self.unidade_medida} | "
                f"Custo Unitário: {self.custo_unitario}")


# ---------------------------------------------------------------------------
# CLASSE PEÇA DAO (Acesso a dados / Regras de negócio com o banco)
# ---------------------------------------------------------------------------

class PecaDAO:
    """Responsável por toda a comunicação com o banco de dados para a entidade Peca."""

    # -----------------------------------------------------------------
    # LISTAR PEÇAS
    # -----------------------------------------------------------------
    def listar(self):
        """Lista todas as peças cadastradas no almoxarifado. Retorna uma lista de objetos Peca."""

        conexao = None
        cursor = None

        try:
            # Abre conexão com o banco.
            conexao = conectar()
            cursor = conexao.cursor()

            # Consulta SQL para listar todas as peças.
            sql = """
            SELECT
                p.id_peca,
                p.nome_peca,
                p.quantidade_estoque,
                p.unidade_medida,
                p.custo_unitario
            FROM Almoxarifado_Pecas AS p
            """

            cursor.execute(sql)

            # Armazena os registros encontrados.
            dados = cursor.fetchall()

            # Converte cada linha do banco em um objeto Peca.
            pecas = [
                Peca(id_peca, nome_peca, quantidade_estoque, unidade_medida, custo_unitario)
                for id_peca, nome_peca, quantidade_estoque, unidade_medida, custo_unitario in dados
            ]

            return pecas

        except Exception as erro:
            print("Erro ao listar peças:", erro)
            return []

        finally:
            # Fecha cursor e conexão.
            if cursor:
                cursor.close()

            if conexao:
                conexao.close()

    # -----------------------------------------------------------------
    # CADASTRAR PEÇA
    # -----------------------------------------------------------------
    def cadastrar(self, peca: Peca):
        """Cadastra uma nova peça no banco de dados a partir de um objeto Peca."""

        conexao = None
        cursor = None

        try:
            # Abre conexão com o banco.
            conexao = conectar()
            cursor = conexao.cursor()

            # Insere uma nova peça.
            # O campo id_peca é AUTO_INCREMENT e não precisa ser informado.
            sql = """
            INSERT INTO Almoxarifado_Pecas
                (nome_peca, quantidade_estoque, unidade_medida, custo_unitario)
            VALUES (%s, %s, %s, %s)
            """

            valores = (
                peca.nome_peca,
                peca.quantidade_estoque,
                peca.unidade_medida,
                peca.custo_unitario
            )

            cursor.execute(sql, valores)

            # Salva as alterações.
            conexao.commit()

            print(f"Peça '{peca.nome_peca}' cadastrada com sucesso! (ID gerado: {cursor.lastrowid})")

        except Exception as erro:
            # Cancela alterações caso ocorra erro.
            if conexao:
                conexao.rollback()

            print("Erro ao cadastrar peça (verifique nome duplicado ou valores negativos):", erro)

        finally:
            # Fecha cursor e conexão.
            if cursor:
                cursor.close()

            if conexao:
                conexao.close()

    # -----------------------------------------------------------------
    # ATUALIZAR QUANTIDADE EM ESTOQUE
    # -----------------------------------------------------------------
    def atualizar_quantidade(self, id_peca, quantidade_estoque):
        """Atualiza a quantidade disponível de uma peça."""

        conexao = None
        cursor = None

        try:
            # Abre conexão com o banco.
            conexao = conectar()
            cursor = conexao.cursor()

            # Atualiza a quantidade em estoque.
            sql = """
            UPDATE Almoxarifado_Pecas
            SET quantidade_estoque = %s
            WHERE id_peca = %s
            """

            valores = (
                quantidade_estoque,
                id_peca
            )

            cursor.execute(sql, valores)

            # Salva as alterações.
            conexao.commit()

            # Verifica se a peça existe.
            if cursor.rowcount > 0:
                print(f"Quantidade da peça {id_peca} atualizada com sucesso!")
            else:
                print("Peça não encontrada.")

        except Exception as erro:
            # Cancela alterações caso ocorra erro.
            if conexao:
                conexao.rollback()

            print("Erro ao atualizar quantidade (verifique se o valor não é negativo):", erro)

        finally:
            # Fecha cursor e conexão.
            if cursor:
                cursor.close()

            if conexao:
                conexao.close()

    # -----------------------------------------------------------------
    # DELETAR PEÇA
    # -----------------------------------------------------------------
    def deletar(self, id_peca):
        """Remove uma peça do banco de dados a partir do id."""

        conexao = None
        cursor = None

        try:
            # Abre conexão com o banco.
            conexao = conectar()
            cursor = conexao.cursor()

            # Exclui a peça pelo ID.
            sql = "DELETE FROM Almoxarifado_Pecas WHERE id_peca = %s"

            cursor.execute(sql, (id_peca,))

            # Salva as alterações.
            conexao.commit()

            # Verifica se a peça foi encontrada.
            if cursor.rowcount > 0:
                print(f"Peça {id_peca} deletada com sucesso!")
            else:
                print("Peça não encontrada.")

        except Exception as erro:
            # Cancela alterações caso ocorra erro.
            if conexao:
                conexao.rollback()

            print("Erro ao deletar peça:", erro)

        finally:
            # Fecha cursor e conexão.
            if cursor:
                cursor.close()

            if conexao:
                conexao.close()


# ---------------------------------------------------------------------------
# CLASSE MENU PEÇA (Interface com o usuário)
# ---------------------------------------------------------------------------

class MenuPeca:
    """Responsável por exibir o menu e interagir com o usuário."""

    def __init__(self):
        # Cada menu possui seu próprio DAO para acessar o banco.
        self.dao = PecaDAO()

    # Lê apenas números inteiros.
    def ler_inteiro(self, mensagem):
        while True:
            valor = input(mensagem)
            try:
                return int(valor)
            except ValueError:
                print("Digite apenas números.")

    # Lê apenas números decimais.
    def ler_float(self, mensagem):
        while True:
            valor = input(mensagem)
            try:
                return float(valor)
            except ValueError:
                print("Digite apenas números (use ponto para decimais).")

    def exibir_lista(self):
        print("\n--- Lista de Peças ---")

        pecas = self.dao.listar()

        if not pecas:
            print("Nenhuma peça cadastrada.")
        else:
            for peca in pecas:
                print(peca)

    def exibir_cadastrar(self):
        print("\n--- Criar Peça ---")

        nome_peca = input("Nome da Peça: ")

        quantidade_estoque = self.ler_inteiro("Quantidade em Estoque: ")

        unidade_medida = input(
            "Unidade de Medida (padrão: Unidade): "
        ) or "Unidade"

        custo_unitario = self.ler_float("Custo Unitário: ")

        nova_peca = Peca(
            nome_peca=nome_peca,
            quantidade_estoque=quantidade_estoque,
            unidade_medida=unidade_medida,
            custo_unitario=custo_unitario
        )

        self.dao.cadastrar(nova_peca)

    def exibir_atualizar_quantidade(self):
        print("\n--- Atualizar Quantidade em Estoque ---")

        id_peca = self.ler_inteiro(
            "Digite o ID da peça que deseja atualizar: "
        )

        quantidade_estoque = self.ler_inteiro(
            "Nova Quantidade em Estoque: "
        )

        self.dao.atualizar_quantidade(id_peca, quantidade_estoque)

    def exibir_deletar(self):
        print("\n--- Deletar Peça ---")

        id_peca = self.ler_inteiro(
            "Digite o ID da peça que deseja deletar: "
        )

        self.dao.deletar(id_peca)

    # Menu principal responsável pelas operações de peças.
    def opcao_desejada_peca(self):

        while True:

            # Exibe o menu.
            print("\n------ Menu Peças ------")
            print("1 - Listar peças")
            print("2 - Criar peça")
            print("3 - Atualizar quantidade em estoque")
            print("4 - Deletar peça")
            print("0 - Sair")

            opcao_peca = self.ler_inteiro("Coloque qual opção deseja: ")

            # Lista todas as peças.
            if opcao_peca == 1:
                self.exibir_lista()

            # Cadastra uma nova peça.
            elif opcao_peca == 2:
                self.exibir_cadastrar()

            # Atualiza a quantidade em estoque.
            elif opcao_peca == 3:
                self.exibir_atualizar_quantidade()

            # Remove uma peça.
            elif opcao_peca == 4:
                self.exibir_deletar()

            # Sai do menu.
            elif opcao_peca == 0:
                print("Voltando...")
                break

            # Caso o usuário digite uma opção inválida.
            else:
                print("Opção inválida!")


# ---------------------------------------------------------------------------
# PONTO DE ENTRADA (exemplo de uso)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    menu = MenuPeca()
    menu.opcao_desejada_peca()
