from database import conectar
from datetime import datetime
import time

# ==============================================================================
# VALIDAÇÃO DAS ENTRADAS DO USUÁRIO NO TERMINAL
# ==============================================================================

class LeitorEntrada:
    """Classe com métodos auxiliares para validar as entradas do terminal."""

    @staticmethod
    def ler_inteiro(mensagem):
        """Pede um número inteiro ao usuário e repete até receber um valor válido."""
        while True:
            valor = input(mensagem)
            try:
                return int(valor)
            except ValueError:
                print("Digite apenas números.")
    
    @staticmethod
    def ler_opcao_valida(mensagem, opcoes_validas):
        """Pede um texto ao usuário e garante que ele esteja na lista de opções permitidas."""
        while True:
            valor = input(mensagem)
            if valor.lower() in opcoes_validas:
                return valor
            print("Opção inválida!")


# ==============================================================================
# GARANTE QUE AS REGRAS DE NEGÓCIO E VALIDAÇÕES SEJAM RESPEITADAS
# ==============================================================================

class Usuario:
    """Representa a entidade Usuário e suas regras de validação."""

    # Listas de valores permitidos para os campos restritos
    CARGOS_VALIDOS = [
        'administrador', 'sistema', 'tecnico', 'entregador',
        'ceo', 'diretor', 'gerente', 'coordenador', 'supervisor'
    ]
    STATUS_VALIDOS = ['ativo', 'inativo']
    NIVEIS_VALIDOS = ['junior', 'pleno', 'senior', 'master']
    DISPONIBILIDADES_VALIDAS = ['disponível', 'em campo', 'ferias', 'afastado']

    def __init__(self, nome_usuario, email_usuario, senha, cargo_usuario,
                 status_usuario, nivel_experiencia, disponibilidade_tecnico,
                 telefone_usuario, data_nasc_usuario, id_setor,
                 data_cadastro=None, id_usuario=None):

        self.id_usuario = id_usuario
        self.nome_usuario = nome_usuario
        self.email_usuario = email_usuario
        self.senha = senha
        
        # As atribuições acionam automaticamente os validadores
        self.cargo_usuario = cargo_usuario
        self.status_usuario = status_usuario
        self.nivel_experiencia = nivel_experiencia
        self.disponibilidade_tecnico = disponibilidade_tecnico
        
        self.telefone_usuario = telefone_usuario
        self.data_nasc_usuario = data_nasc_usuario
        self.id_setor = id_setor
        
        # Define a data atual caso não seja informada
        self.data_cadastro = data_cadastro or datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Validação do Cargo
    @property
    def cargo_usuario(self):
        return self._cargo_usuario

    @cargo_usuario.setter
    def cargo_usuario(self, valor):
        if valor.lower() not in self.CARGOS_VALIDOS:
            raise ValueError(f"Cargo inválido: {valor}")
        self._cargo_usuario = valor.lower()

    # Validação do Status
    @property
    def status_usuario(self):
        return self._status_usuario

    @status_usuario.setter
    def status_usuario(self, valor):
        if valor.lower() not in self.STATUS_VALIDOS:
            raise ValueError(f"Status inválido: {valor}")
        self._status_usuario = valor.lower()

    # Validação do Nível de Experiência
    @property
    def nivel_experiencia(self):
        return self._nivel_experiencia

    @nivel_experiencia.setter
    def nivel_experiencia(self, valor):
        if valor.lower() not in self.NIVEIS_VALIDOS:
            raise ValueError(f"Nível de experiência inválido: {valor}")
        self._nivel_experiencia = valor.lower()

    # Validação da Disponibilidade
    @property
    def disponibilidade_tecnico(self):
        return self._disponibilidade_tecnico

    @disponibilidade_tecnico.setter
    def disponibilidade_tecnico(self, valor):
        if valor.lower() not in self.DISPONIBILIDADES_VALIDAS:
            raise ValueError(f"Disponibilidade inválida: {valor}")
        self._disponibilidade_tecnico = valor.lower()

    def __repr__(self):
        """Representação detalhada do objeto para depuração."""
        return (f"Usuario(id={self.id_usuario}, nome={self.nome_usuario!r}, "
                f"cargo={self.cargo_usuario!r}, status={self.status_usuario!r})")

    def __str__(self):
        """Texto amigável exibido ao converter o objeto para string."""
        return (f"[{self.id_usuario}] {self.nome_usuario} - {self.cargo_usuario} "
                f"({self.status_usuario})")


# ==============================================================================
# PONTE DE COMUNICAÇÃO ENTRE O CÓDIGO EM PYTHON E O BANCO DE DADOS
# ==============================================================================

class UsuarioRepository:
    """Gerencia todas as operações de banco de dados (CRUD) da tabela Usuarios."""

    def listar(self):
        """Retorna todos os usuários cadastrados no banco."""
        conexao = None
        cursor = None
        try:
            conexao = conectar()
            cursor = conexao.cursor()

            sql = """
            SELECT
                id_usuario, nome_usuario, email_usuario, cargo_usuario,
                status_usuario, nivel_experiencia, disponibilidade_tecnico,
                telefone_usuario, data_nasc_usuario,
                id_setor, data_cadastro
            FROM Usuarios
            """

            cursor.execute(sql)
            dados = cursor.fetchall()

            if not dados:
                print("Nenhum usuário cadastrado.")
                return []

            return dados

        except Exception as erro:
            print("Erro ao listar usuários:", erro)
            return []

        finally:
            # Garante o fechamento do cursor e da conexão
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()

    def criar(self, usuario: Usuario):
        """Insere um novo registro de usuário no banco de dados."""
        conexao = None
        cursor = None

        try:
            conexao = conectar()
            cursor = conexao.cursor()

            sql = """
            INSERT INTO Usuarios
                (nome_usuario, email_usuario, senha, cargo_usuario,
                status_usuario, nivel_experiencia,
                disponibilidade_tecnico, telefone_usuario,
                data_nasc_usuario, id_setor, data_cadastro)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            valores = (
                usuario.nome_usuario,
                usuario.email_usuario,
                usuario.senha,
                usuario.cargo_usuario,
                usuario.status_usuario,
                usuario.nivel_experiencia,
                usuario.disponibilidade_tecnico,
                usuario.telefone_usuario,
                usuario.data_nasc_usuario,
                usuario.id_setor,
                usuario.data_cadastro
            )

            cursor.execute(sql, valores)
            conexao.commit()

            # Atribui o ID gerado pelo banco ao objeto
            usuario.id_usuario = cursor.lastrowid
            print("Usuário cadastrado com sucesso!")
            return usuario

        except Exception as erro:
            if conexao:
                conexao.rollback() # Desfaz alterações em caso de erro
            print("Erro ao criar usuário (verifique se o e-mail ou telefone já estão cadastrados):", erro)
            return None

        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()

    def atualizar(self, id_usuario, cargo_usuario, telefone_usuario, id_setor):
        """Atualiza apenas cargo, telefone e setor de um usuário pelo ID."""
        conexao = None
        cursor = None

        try:
            conexao = conectar()
            cursor = conexao.cursor()

            sql = """
            UPDATE Usuarios
            SET cargo_usuario = %s,
                telefone_usuario = %s,
                id_setor = %s
            WHERE id_usuario = %s
            """

            valores = (cargo_usuario, telefone_usuario, id_setor, id_usuario)

            cursor.execute(sql, valores)
            conexao.commit()

            # Verifica se algum registro foi alterado
            if cursor.rowcount > 0:
                print("Usuário atualizado com sucesso!")
                return True

            print("Usuário não encontrado.")
            return False

        except Exception as erro:
            if conexao:
                conexao.rollback()
            print("Erro ao atualizar usuário.", erro)
            return False

        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()

    def excluir(self, id_usuario):
        """Remove um usuário do banco pelo seu ID."""
        conexao = None
        cursor = None

        try:
            conexao = conectar()
            cursor = conexao.cursor()

            sql = "DELETE FROM Usuarios WHERE id_usuario = %s"
            cursor.execute(sql, (id_usuario,))
            conexao.commit()

            if cursor.rowcount > 0:
                print("Usuário deletado com sucesso!")
                return True

            print("Usuário não encontrado.")
            return False

        except Exception as erro:
            if conexao:
                conexao.rollback()
            print("Erro ao deletar usuário:", erro)
            return False

        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()


# ==============================================================================
# CAMADA DE APRESENTAÇÃO (MENU INTERATIVO)
# ==============================================================================

class MenuUsuario:
    """Interface via terminal para interagir com o sistema de usuários."""

    def __init__(self):
        self.repositorio = UsuarioRepository()

    def exibir(self):
        """Exibe o menu principal em loop contínuo."""
        while True:
            print("\n------ Menu Usuário ------")
            print("1 - Listar usuários")
            print("2 - Criar usuário")
            print("3 - Atualizar usuário")
            print("4 - Deletar usuário")
            print("0 - Sair")

            opcao = LeitorEntrada.ler_inteiro("Coloque qual opção deseja: ")

            if opcao == 1:
                self._listar()
            elif opcao == 2:
                self._criar()
            elif opcao == 3:
                self._atualizar()
            elif opcao == 4:
                self._excluir()
            elif opcao == 0:
                print("Voltando...")
                break
            else:
                print("Opção inválida!")

    def _listar(self):
        """Fluxo de listagem dos usuários."""
        print("\n--- Lista de Usuários ---")
        for usuario in self.repositorio.listar():
            print(usuario)
        time.sleep(2)

    def _criar(self):
        """Fluxo de coleta de dados e criação de novo usuário."""
        print("\n--- Criar Usuário ---")

        nome = input("Nome: ")
        email = input("Email: ")
        senha = input("Senha: ")

        cargo = LeitorEntrada.ler_opcao_valida(
            "Cargo (Administrador, Sistema, Tecnico, Entregador, CEO, Diretor, Gerente, Coordenador, Supervisor): ",
            Usuario.CARGOS_VALIDOS
        )
        status = LeitorEntrada.ler_opcao_valida(
            "Status (Ativo, Inativo): ",
            Usuario.STATUS_VALIDOS
        )
        nivel_experiencia = LeitorEntrada.ler_opcao_valida(
            "Nivel de experiencia (Junior, Pleno, Senior, Master): ",
            Usuario.NIVEIS_VALIDOS
        )
        disponibilidade_tecnico = LeitorEntrada.ler_opcao_valida(
            "Disponibilidade (Disponível, Em Campo, Ferias, Afastado): ",
            Usuario.DISPONIBILIDADES_VALIDAS
        )

        telefone = input("Telefone: ")
        data_nasc = input("Data de Nascimento (AAAA-MM-DD): ")
        id_setor = LeitorEntrada.ler_inteiro("ID do Setor: ")

        # Tenta instanciar o objeto e salvar no repositório
        try:
            usuario = Usuario(
                nome_usuario=nome,
                email_usuario=email,
                senha=senha,
                cargo_usuario=cargo,
                status_usuario=status,
                nivel_experiencia=nivel_experiencia,
                disponibilidade_tecnico=disponibilidade_tecnico,
                telefone_usuario=telefone,
                data_nasc_usuario=data_nasc,
                id_setor=id_setor
            )
            self.repositorio.criar(usuario)
        except ValueError as erro:
            print("Erro de validação:", erro)

    def _atualizar(self):
        """Fluxo para atualização de dados do usuário."""
        print("\n--- Atualizar Usuário ---")

        id_u = LeitorEntrada.ler_inteiro("Digite o ID do usuário que deseja atualizar: ")

        cargo = LeitorEntrada.ler_opcao_valida(
            "Novo Cargo (Administrador, Sistema, Tecnico, Entregador, CEO, Diretor, Gerente, Coordenador, Supervisor): ",
            Usuario.CARGOS_VALIDOS
        )
        telefone = input("Novo Telefone: ")
        id_setor = LeitorEntrada.ler_inteiro("Novo ID do Setor: ")

        self.repositorio.atualizar(id_u, cargo, telefone, id_setor)

    def _excluir(self):
        """Fluxo de remoção de usuário."""
        print("\n--- Deletar Usuário ---")
        id_u = LeitorEntrada.ler_inteiro("Digite o ID do usuário que deseja deletar: ")
        self.repositorio.excluir(id_u)


def opcao_desejada_usuario():
    """Função de entrada que inicializa o menu."""
    MenuUsuario().exibir()

#Execução principal do script
if __name__ == "__main__":
    opcao_desejada_usuario()