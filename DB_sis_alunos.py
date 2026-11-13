import psycopg2
# Conectar ao banco de dados PostgreSQL
conexao = psycopg2.connect(
host="localhost",
database="mafra",
user="postgres",
password="1234",
port="5432"
)
cursor = conexao.cursor()

# Codigo
def add_aluno():
    print("\nCADASTRAR ALUNO")

    nome = input("Digite o nome do aluno: ")
    idade = int(input("Digite a idade do aluno: "))
    nota = float(input("Digite a nota do aluno: "))

    try:
        cursor.execute(
            "INSERT INTO aluno (nome, idade, nota) VALUES (%s, %s, %s)",
            (nome, idade, nota)
        )

        conexao.commit()
        print("Aluno cadastrado com sucesso!")

    except psycopg2.Error as erro:
        conexao.rollback()
        print("Erro ao cadastrar aluno:", erro)

def listar_alunos():
    print("\nLISTA DE ALUNOS")

    cursor.execute("SELECT * FROM aluno")
    registros = cursor.fetchall()

    if not registros:
        print("Não há alunos cadastrados.")

    for aluno in registros:
        print(f"ID: {aluno[0]}")
        print(f"Nome: {aluno[1]}")
        print(f"Idade: {aluno[2]} anos")
        print(f"Nota: {aluno[3]:.1f}")

def buscar_aluno():
    print("\nBUSCAR ALUNO")

    nome_busca = input("Digite o nome do aluno: ").strip()

    cursor.execute(
        "SELECT * FROM aluno WHERE LOWER(nome) = LOWER(%s)",
        (nome_busca,)
    )

    aluno = cursor.fetchone()

    if aluno:
        print("\nAluno encontrado:")
        print(f"ID: {aluno[0]}")
        print(f"Nome: {aluno[1]}")
        print(f"Idade: {aluno[2]} anos")
        print(f"Nota: {aluno[3]:.1f}")
    else:
        print("Aluno não encontrado.")


def rem_aluno():
    print("\nREMOVER ALUNO")

    nome_remover = input("Digite o nome do aluno: ").strip()

    try:
        cursor.execute(
            "DELETE FROM aluno WHERE LOWER(nome) = LOWER(%s)",
            (nome_remover,)
        )

        conexao.commit()

        if cursor.rowcount > 0:
            print("Aluno removido com sucesso.")
        else:
            print("Aluno não encontrado.")

    except psycopg2.Error as erro:
        conexao.rollback()
        print("Erro ao remover aluno:", erro)


def media_geral():
    print("\nMÉDIA GERAL")

    cursor.execute("SELECT AVG(nota) FROM aluno")

    resultado = cursor.fetchone()

    if resultado[0] is None:
        print("Não há alunos cadastrados para calcular a média.")
    else:
        media = resultado[0]
        print(f"A média geral das notas é: {media:.2f}")

def atualizar_aluno():
    print("\nATUALIZAR ALUNO")

    try:
        id_aluno = int(input("Digite o ID do aluno que deseja atualizar: "))
    except ValueError:
        print("Digite um ID válido.")
        return

    cursor.execute(
        "SELECT * FROM alunos WHERE id = %s",
        (id_aluno,)
    )

    aluno = cursor.fetchone()

    if not aluno:
        print("Aluno não encontrado.")
        return

    print("\nDados atuais do aluno:")
    print(f"Nome: {aluno[1]}")
    print(f"Idade: {aluno[2]}")
    print(f"Nota: {aluno[3]}")

    nome = input("\nDigite o novo nome: ").strip()

    while True:
        try:
            idade = int(input("Digite a nova idade: "))

            if idade > 2:
                break
            else:
                print("A idade deve ser maior que dois.")

        except ValueError:
            print("Digite uma idade válida.")

    while True:
        try:
            nota = float(input("Digite a nova nota (0 a 10): "))

            if 0 <= nota <= 10:
                break
            else:
                print("A nota deve estar entre 0 e 10.")

        except ValueError:
            print("Digite uma nota válida.")

    try:
        cursor.execute(
            """UPDATE alunos
               SET nome = %s, idade = %s, nota = %s
               WHERE id = %s""",
            (nome, idade, nota, id_aluno)
        )

        conexao.commit()

        print("Aluno atualizado com sucesso!")

    except psycopg2.Error as erro:
        conexao.rollback()
        print("Erro ao atualizar aluno:", erro)

# Programa principal
while True:
    print("\n")
    print("SISTEMA DE ALUNOS")
    print("\n")
    print("1 - Adicionar aluno")
    print("2 - Listar todos os alunos")
    print("3 - Buscar aluno pelo nome")
    print("4 - Remover aluno")
    print("5 - Mostrar média geral das notas")
    print("6 - Atualizar dados do aluno")
    print("7 - Sair")
    print("\n")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        add_aluno()

    elif opcao == "2":
        listar_alunos()

    elif opcao == "3":
        buscar_aluno()

    elif opcao == "4":
        rem_aluno()

    elif opcao == "5":
        media_geral()

    elif opcao == "6":
        atualizar_aluno()

    elif opcao == "7":
        print("Programa será encerrado.")
        break

    else:
        print("Opção inválida. Escolha uma das opções de 1 a 7.")

cursor.close()
conexao.close()