import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        """
        Inicializa o gerenciador do banco de dados e garante que a tabela `alunos` existe.
        :param db_name: Nome do arquivo do banco de dados.
        """
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.connect()
        self.create_table()

    def connect(self):
        """Estabelece a conexão com o banco de dados."""
        try:
            self.connection = sqlite3.connect(self.db_name, check_same_thread=False)
            self.cursor = self.connection.cursor()
            print(f"Conexão com o banco de dados '{self.db_name}' foi estabelecida.")
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def create_table(self):
        """Cria a tabela `alunos` caso ela não exista."""
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            placa_veiculo TEXT,
            permissao INTEGER NOT NULL DEFAULT 0 
        )
        ''' # 0 = False, 1 = True
        try:
            self.cursor.execute(create_table_sql)
            self.connection.commit()
            print("Tabela 'alunos' criada ou já existente.")
        except sqlite3.Error as e:
            print(f"Erro ao criar tabela: {e}")

    def get_register(self, plate):
        """Consulta um registro pelo número da placa."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            aluno = cursor.execute('SELECT * FROM alunos WHERE placa_veiculo = ?', (plate,)).fetchone()
        return aluno

    def close(self):
        """Fecha a conexão com o banco de dados."""
        if self.connection:
            self.connection.close()
            print("Conexão com o banco de dados foi encerrada.")

# Exemplo de uso
if __name__ == "__main__":
    db = DatabaseManager("meu_banco.db")
    db.close()
