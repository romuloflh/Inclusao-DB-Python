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

#codigo
alunos = []

def add_aluno():
    print("\nADICIONAR ALUNO")

    nome = input("Digite o nome do aluno: ").strip()

    while True:
        try:
            idade = int(input("Digite a idade do aluno: "))

            if idade > 2:
                break
            else:
                print("A idade deve ser maior que dois.")

        except ValueError:
            print("Digite uma idade válida.")

    while True:
        try:
            nota = float(input("Digite a nota do aluno (0 a 10): "))

            if 0 <= nota <= 10:
                break
            else:
                print("A nota deve estar entre 0 e 10.")

        except ValueError:
            print("Digite uma nota válida.")

    aluno = {
        "nome": nome,
        "idade": idade,
        "nota": nota
    }
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
        (nome_busca, )
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

    for aluno in alunos:
        if aluno["nome"].lower() == nome_remover.lower():
            alunos.remove(aluno)
            print("Aluno removido com sucesso.")
            return

    print("Aluno não encontrado.")

def media_geral():
    print("\nMÉDIA GERAL")

    if len(alunos) == 0:
        print("Não há alunos cadastrados para calcular a média.")
        return

    soma = 0

    for aluno in alunos:
        soma += aluno["nota"]

    media = soma / len(alunos)

    print(f"A média geral das notas é: {media:.2f}")


# Programa principal
while True:
    print("\n")
    print("SISTEMA DE ALUNOS")
    print("\n")
    print("1 = Adicionar aluno")
    print("2 = Listar todos os alunos")
    print("3 = Buscar aluno pelo nome")
    print("4 = Remover aluno")
    print("5 = Mostrar média geral das notas")
    print("6 = Sair")
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
        print("Programa será encerrado.")
        break

    else:
        print("Opção inválida. Escolha uma das opções de 1 a 6.")

cursor.close()
conexao.close()