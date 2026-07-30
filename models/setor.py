# Importa a função responsável por realizar a conexão com o banco de dados.
from database import conectar

# Importa a biblioteca time para utilizar pausas no sistema.
import time


# ---------------------------------------------------------------------------
# CLASSE SETOR (Entidade / Modelo)
# ---------------------------------------------------------------------------

class Setor:
    """Representa um setor, com seus dados básicos."""

    def __init__(self, id_setor=None, nome_setor=None, descricao_setor=None):
        self.id_setor = id_setor
        self.nome_setor = nome_setor
        self.descricao_setor = descricao_setor

    def __str__(self):
        return f"ID: {self.id_setor} | Nome: {self.nome_setor} | Descrição: {self.descricao_setor}"


# ---------------------------------------------------------------------------
# CLASSE SETOR DAO (Acesso a dados / Regras de negócio com o banco)
# ---------------------------------------------------------------------------

class SetorDAO:
    """Responsável por toda a comunicação com o banco de dados para a entidade Setor."""

    # -----------------------------------------------------------------
    # LISTAR SETORES
    # -----------------------------------------------------------------
    def listar(self):
        """Lista todos os setores cadastrados. Retorna uma lista de objetos Setor."""

        conexao = None
        cursor = None

        try:
            # Abre conexão com o banco.
            conexao = conectar()
            cursor = conexao.cursor()

            # Consulta SQL para listar todos os setores.
            sql = """
            SELECT
                id_setor,
                nome_setor,
                descricao_setor
            FROM Setores
            ORDER BY nome_setor ASC;
            """

            cursor.execute(sql)

            dados = cursor.fetchall()

            # Converte cada linha do banco em um objeto Setor.
            setores = [Setor(id_setor, nome, descricao) for id_setor, nome, descricao in dados]

            return setores

        except Exception as erro:
            print("Erro ao listar setores:", erro)
            return []

        finally:
            # Fecha cursor e conexão.
            if cursor:
                cursor.close()

            if conexao:
                conexao.close()

    # -----------------------------------------------------------------
    # CADASTRAR SETOR
    # -----------------------------------------------------------------
    def criar(self, setor: Setor):
        """Cria um novo setor a partir de um objeto Setor."""

        conexao = None
        cursor = None

        try:
            # Abre conexão com o banco.
            conexao = conectar()
            cursor = conexao.cursor()

            # Insere um novo setor.
            sql = """
            INSERT INTO Setores
                (nome_setor, descricao_setor)
            VALUES (%s, %s);
            """

            cursor.execute(sql, (setor.nome_setor, setor.descricao_setor))

            # Salva as alterações.
            conexao.commit()

            print("Setor cadastrado com sucesso!")

        except Exception as erro:
            # Cancela alterações caso ocorra erro.
            if conexao:
                conexao.rollback()

            print("Erro ao criar setor:", erro)

        finally:
            # Fecha cursor e conexão.
            if cursor:
                cursor.close()

            if conexao:
                conexao.close()

    # -----------------------------------------------------------------
    # ATUALIZAR SETOR
    # -----------------------------------------------------------------
    def atualizar(self, setor: Setor):
        """Atualiza os dados de um setor a partir de um objeto Setor."""

        conexao = None
        cursor = None

        try:
            # Abre conexão com o banco.
            conexao = conectar()
            cursor = conexao.cursor()

            # Atualiza nome e descrição do setor.
            sql = """
            UPDATE Setores
            SET
                nome_setor = %s,
                descricao_setor = %s
            WHERE id_setor = %s;
            """

            cursor.execute(sql, (setor.nome_setor, setor.descricao_setor, setor.id_setor))

            # Salva as alterações.
            conexao.commit()

            # Verifica se o setor existe.
            if cursor.rowcount > 0:
                print("Setor atualizado com sucesso!")
            else:
                print("Setor não encontrado.")

        except Exception as erro:
            # Cancela alterações caso ocorra erro.
            if conexao:
                conexao.rollback()

            print("Erro ao atualizar setor:", erro)

        finally:
            # Fecha cursor e conexão.
            if cursor:
                cursor.close()

            if conexao:
                conexao.close()

    # -----------------------------------------------------------------
    # DELETAR SETOR
    # -----------------------------------------------------------------
    def deletar(self, id_setor):
        """Remove um setor do banco de dados a partir do id."""

        conexao = None
        cursor = None

        try:
            # Abre conexão com o banco.
            conexao = conectar()
            cursor = conexao.cursor()

            # Exclui o setor informado.
            sql = "DELETE FROM Setores WHERE id_setor = %s;"

            cursor.execute(sql, (id_setor,))

            # Salva as alterações.
            conexao.commit()

            # Verifica se o setor foi encontrado.
            if cursor.rowcount > 0:
                print("Setor excluído com sucesso!")
            else:
                print("Setor não encontrado.")

        except Exception as erro:
            # Cancela alterações caso ocorra erro.
            if conexao:
                conexao.rollback()

            print("Erro ao deletar setor (verifique se ainda há máquinas vinculadas a ele):", erro)

        finally:
            # Fecha cursor e conexão.
            if cursor:
                cursor.close()

            if conexao:
                conexao.close()


# ---------------------------------------------------------------------------
# CLASSE MENU SETOR (Interface com o usuário)
# ---------------------------------------------------------------------------

class MenuSetor:
    """Responsável por exibir o menu e interagir com o usuário."""

    def __init__(self):
        # Cada menu possui seu próprio DAO para acessar o banco.
        self.dao = SetorDAO()

    # Garante que o usuário digite apenas números inteiros.
    def ler_inteiro(self, mensagem):
        while True:
            valor = input(mensagem)
            try:
                return int(valor)
            except ValueError:
                print("Digite apenas números.")

    def exibir_lista(self):
        print("\n--- Lista de Setores ---")

        setores = self.dao.listar()

        if not setores:
            print("Nenhum setor cadastrado.")
        else:
            for setor in setores:
                print(setor)

        time.sleep(2)

    def exibir_criar(self):
        print("\n--- Criar Setor ---")

        nome = input("Nome do setor: ")
        descricao = input("Descrição do setor: ")

        novo_setor = Setor(nome_setor=nome, descricao_setor=descricao)

        self.dao.criar(novo_setor)

    def exibir_atualizar(self):
        print("\n--- Atualizar Setor ---")

        id_setor = self.ler_inteiro("ID do setor: ")
        nome = input("Novo nome: ")
        descricao = input("Nova descrição: ")

        setor_atualizado = Setor(id_setor=id_setor, nome_setor=nome, descricao_setor=descricao)

        self.dao.atualizar(setor_atualizado)

    def exibir_deletar(self):
        print("\n--- Deletar Setor ---")

        id_setor = self.ler_inteiro("ID do setor: ")

        self.dao.deletar(id_setor)

    # Menu principal responsável pelas operações dos setores.
    def opcao_desejada_setor(self):

        while True:

            # Exibe o menu de opções.
            print("\n------Menu Setor------")
            print("1 - Listar setor")
            print("2 - Criar setor")
            print("3 - Atualizar setor")
            print("4 - Deletar setor")
            print("0 - Sair")

            opcao_setor = self.ler_inteiro("Coloque qual opção deseja: ")

            # Lista todos os setores.
            if opcao_setor == 1:
                self.exibir_lista()

            # Cadastra um novo setor.
            elif opcao_setor == 2:
                self.exibir_criar()

            # Atualiza um setor existente.
            elif opcao_setor == 3:
                self.exibir_atualizar()

            # Remove um setor.
            elif opcao_setor == 4:
                self.exibir_deletar()

            # Sai do menu.
            elif opcao_setor == 0:
                print("Voltando")
                break

            # Caso seja digitada uma opção inválida.
            else:
                print("Opção inválida!")


# ---------------------------------------------------------------------------
# PONTO DE ENTRADA (exemplo de uso)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    menu = MenuSetor()
    menu.opcao_desejada_setor()