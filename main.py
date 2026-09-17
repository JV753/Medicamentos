import ast
import csv
import os

ARQUIVO_CSV = 'medicamentos.csv'
COLUNAS_CSV = ['Nome do medicamento', 'Classe do medicamento', 'Quantidade em Estoque']


def _normalizar_item(item):
    """Valida e normaliza um item de medicamento."""
    # Garante que o dado recebido tenha a estrutura esperada: [nome, classe, quantidade].
    if not isinstance(item, (list, tuple)) or len(item) < 3:
        return None

    # Converte os campos para texto e remove espaços extras, evitando entradas vazias.
    nome = str(item[0]).strip()
    classe = str(item[1]).strip()
    quantidade = str(item[2]).strip()

    # A validação impede que campos essenciais fiquem vazios.
    if not nome or not classe or not quantidade:
        return None

    # Converte a quantidade para inteiro e rejeita valores inválidos ou negativos.
    try:
        quantidade = int(quantidade)
    except ValueError:
        return None

    if quantidade < 0:
        return None

    # Retorna a estrutura padronizada para uso em outras funções.
    return (nome, classe, quantidade)


def _importar_dados_para_csv(itens):
    """Importa apenas itens válidos e sem duplicatas para o CSV principal."""
    # Evita processamento desnecessário caso a lista esteja vazia.
    if not itens:
        return 0

    # Normaliza cada item para o formato esperado antes de importar.
    itens_validos = []
    for item in itens:
        item_normalizado = _normalizar_item(item)
        if item_normalizado:
            itens_validos.append(item_normalizado)

    # Se nenhum dado passou na validação, não há o que importar.
    if not itens_validos:
        return 0

    # Carrega o CSV atual para impedir duplicatas de nome + classe.
    if os.path.exists(ARQUIVO_CSV):
        with open(ARQUIVO_CSV, 'r', encoding='utf-8', newline='') as f:
            leitor = csv.reader(f)
            linhas = list(leitor)
    else:
        linhas = []

    # Mantém um conjunto das chaves já existentes para comparação rápida.
    ja_existentes = {
        (linha[0].strip().lower(), linha[1].strip().lower())
        for linha in linhas[1:]
        if len(linha) >= 3
    }

    # Seleciona apenas os registros que ainda não existem no arquivo.
    novos = []
    for nome, classe, quantidade in itens_validos:
        chave = (nome.lower(), classe.lower())
        if chave not in ja_existentes:
            ja_existentes.add(chave)
            novos.append((nome, classe, quantidade))

    # Se todos já existem, não registra nada.
    if not novos:
        return 0

    # Adiciona os registros novos ao fim do arquivo CSV.
    with open(ARQUIVO_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(novos)

    # Retorna a quantidade de itens realmente importados.
    return len(novos)


def _extrair_medicamentos_de_dados(dados):
    """Extrai itens válidos de listas/dicionários de dados."""
    # A função aceita apenas listas/tuplas; qualquer outro tipo é descartado.
    if not isinstance(dados, (list, tuple)):
        return []

    # Percorre a estrutura e só mantém registros válidos após a normalização.
    itens = []
    for item in dados:
        item_normalizado = _normalizar_item(item)
        if item_normalizado:
            itens.append(item_normalizado)

    return itens


def inicializar_arquivo():
    """Cria ou organiza o arquivo CSV com cabeçalho padronizado."""
    # Cria o arquivo e o cabeçalho caso ele ainda não exista.
    if not os.path.exists(ARQUIVO_CSV):
        with open(ARQUIVO_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(COLUNAS_CSV)
        return

    # Lê o CSV atual para verificar se o cabeçalho está correto.
    with open(ARQUIVO_CSV, 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        linhas = list(reader)

    # Reorganiza o arquivo caso ele exista sem a estrutura esperada, preservando os dados válidos.
    if not linhas or linhas[0] != COLUNAS_CSV:
        with open(ARQUIVO_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(COLUNAS_CSV)
            for linha in linhas[1:]:
                if len(linha) >= 3:
                    nome, classe, quantidade = linha[:3]
                    writer.writerow([nome, classe, quantidade])

def adicionar_medicamento():
    """Adiciona um novo medicamento ao cadastro"""
    # Coleta os dados do usuário e remove espaços em excesso para padronizar a entrada.
    nome = input("Nome do medicamento: ").strip()
    classe = input("Classe do medicamento: ").strip()

    # Evita cadastro com dados vazios, que não têm sentido para o sistema.
    if not nome or not classe:
        print("Nome e classe do medicamento não podem estar vazios!\n")
        return

    # Valida a quantidade em estoque antes de gravar no arquivo.
    try:
        quantidade = int(input("Quantidade em estoque: "))
        if quantidade < 0:
            print("A quantidade não pode ser negativa!\n")
            return
    except ValueError:
        print("Quantidade inválida! Digite um número inteiro.\n")
        return

    # Evita cadastrar novamente o mesmo medicamento na mesma classe.
    if os.path.exists(ARQUIVO_CSV):
        with open(ARQUIVO_CSV, 'r', encoding='utf-8', newline='') as f:
            registros = list(csv.reader(f))
        duplicado = any(
            len(linha) >= 2
            and linha[0].strip().lower() == nome.lower()
            and linha[1].strip().lower() == classe.lower()
            for linha in registros[1:]
        )
        if duplicado:
            print("Esse medicamento já está cadastrado nessa classe!\n")
            return

    # Grava a linha no CSV em formato padronizado [nome, classe, quantidade].
    with open(ARQUIVO_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([nome, classe, quantidade])

    print(f"Medicamento '{nome}' cadastrado com sucesso!\n")

def listar_medicamentos():
    """Lista todos os medicamentos cadastrados"""
    # Se o arquivo ainda não existe, a listagem deve informar que não há registros.
    if not os.path.exists(ARQUIVO_CSV):
        print("Nenhum medicamento cadastrado ainda.\n")
        return

    # Lê todas as linhas do CSV para exibir os dados cadastrados.
    with open(ARQUIVO_CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        medicamentos = list(reader)

    # O cabeçalho é a primeira linha; se apenas ele existir, não há itens para mostrar.
    if len(medicamentos) <= 1:
        print("Nenhum medicamento cadastrado ainda.\n")
        return

    # Cabeçalho visual amigável para a apresentação dos registros.
    print("\n--- MEDICAMENTOS CADASTRADOS ---")
    print(f"{'Nome':<30} {'Classe':<20} {'Quantidade':<15}")
    print("-" * 65)

    # Itera a partir da segunda linha para ignorar o cabeçalho.
    for i in range(1, len(medicamentos)):
        nome, classe, quantidade = medicamentos[i]
        print(f"{nome:<30} {classe:<20} {quantidade:<15}")
    print()

def buscar_medicamento():
    """Busca um medicamento pelo nome ou categoria"""
    # Verifica se há dados para pesquisar antes de tentar abrir o arquivo.
    if not os.path.exists(ARQUIVO_CSV):
        print("Nenhum medicamento cadastrado ainda.\n")
        return

    # Normaliza o termo para comparação sem diferenciar letras maiúsculas/minúsculas.
    termo = input("Digite o nome ou classe para buscar: ").strip().lower()

    if not termo:
        print("Termo de busca inválido.\n")
        return

    # Carrega todos os registros para verificar quais atendem ao critério.
    with open(ARQUIVO_CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        medicamentos = list(reader)

    if len(medicamentos) <= 1:
        print("Nenhum medicamento cadastrado ainda.\n")
        return

    # Busca por coincidência no nome ou na classe do medicamento.
    resultados = []
    for i in range(1, len(medicamentos)):
        nome, classe, quantidade = medicamentos[i]
        if termo in nome.lower() or termo in classe.lower():
            resultados.append((nome, classe, quantidade))

    if not resultados:
        print("Nenhum medicamento encontrado com esse termo.\n")
        return

    # Exibe os resultados em formato tabular para facilitar a leitura.
    print("\n--- RESULTADO DA BUSCA ---")
    print(f"{'Nome':<30} {'Classe':<20} {'Quantidade':<15}")
    print("-" * 65)

    for nome, classe, quantidade in resultados:
        print(f"{nome:<30} {classe:<20} {quantidade:<15}")
    print()

def buscar_medicamento_avancado(termo):
    """Busca medicamentos por termo (função com parâmetro e retorno).
    Retorna lista de tuplas (nome, classe, quantidade)."""
    # Permite reutilizar a busca em outros trechos do código, sem depender de entrada do usuário.
    if not os.path.exists(ARQUIVO_CSV):
        return []

    # Padroniza a pesquisa para comparar textos em minúsculas e ignorar espaços extras.
    termo = termo.strip().lower()
    if not termo:
        return []

    # Leitura dos registros em memória para validar nome e classe contra o termo informado.
    resultados = []
    with open(ARQUIVO_CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        medicamentos = list(reader)

    for i in range(1, len(medicamentos)):
        nome, classe, quantidade = medicamentos[i]
        if termo in nome.lower() or termo in classe.lower():
            resultados.append((nome, classe, quantidade))

    return resultados

def contar_por_categoria(categoria):
    """Conta quantos medicamentos existem em uma classe/categoria.
    Recebe a classe (string) e retorna um inteiro."""
    # Se o arquivo não existir, o número de medicamentos nessa categoria é zero.
    if not os.path.exists(ARQUIVO_CSV):
        return 0

    # Normaliza a categoria para comparar sem diferenciar maiúsculas/minúsculas.
    cat = categoria.strip().lower()
    if not cat:
        return 0

    # Faz a contagem iterando sobre todas as linhas do arquivo, exceto o cabeçalho.
    contador = 0
    with open(ARQUIVO_CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        medicamentos = list(reader)

    for i in range(1, len(medicamentos)):
        _, classe_linha, _ = medicamentos[i]
        if cat == classe_linha.strip().lower():
            contador += 1

    return contador


def remover_medicamento():
    """Remove um medicamento pelo nome."""
    nome_remover = input("Digite o nome do medicamento a remover: ").strip().lower()
    if not nome_remover:
        print("Nome inválido.\n")
        return

    if not os.path.exists(ARQUIVO_CSV):
        print("Nenhum medicamento cadastrado ainda.\n")
        return

    with open(ARQUIVO_CSV, 'r', encoding='utf-8', newline='') as f:
        linhas = list(csv.reader(f))

    removidos = 0
    novas_linhas = linhas[:1]
    for linha in linhas[1:]:
        if len(linha) >= 3 and linha[0].strip().lower() == nome_remover:
            removidos += 1
        else:
            novas_linhas.append(linha)

    if removidos:
        with open(ARQUIVO_CSV, 'w', encoding='utf-8', newline='') as f:
            csv.writer(f).writerows(novas_linhas)
        print(f"Medicamento '{nome_remover}' removido com sucesso.\n")
    else:
        print("Medicamento não encontrado.\n")


def atualizar_estoque():
    """Atualiza a quantidade em estoque de um medicamento."""
    nome = input("Digite o nome do medicamento: ").strip().lower()
    if not nome or not os.path.exists(ARQUIVO_CSV):
        print("Medicamento não encontrado.\n")
        return

    with open(ARQUIVO_CSV, 'r', encoding='utf-8', newline='') as f:
        linhas = list(csv.reader(f))

    encontrados = [linha for linha in linhas[1:]
                   if len(linha) >= 3 and linha[0].strip().lower() == nome]
    if not encontrados:
        print("Medicamento não encontrado.\n")
        return

    try:
        quantidade = int(input("Digite a nova quantidade em estoque: ").strip())
        if quantidade < 0:
            raise ValueError
    except ValueError:
        print("Quantidade inválida! Digite um número inteiro não negativo.\n")
        return

    for linha in encontrados:
        linha[2] = str(quantidade)

    with open(ARQUIVO_CSV, 'w', encoding='utf-8', newline='') as f:
        csv.writer(f).writerows(linhas)

    print("Estoque atualizado com sucesso.\n")


def menu():
    """Exibe o menu principal e repete até sair"""
    # O loop principal mantém a aplicação em execução até o usuário escolher a opção de saída.
    while True:
        print("=== SISTEMA DE CADASTRO DE MEDICAMENTOS ===")
        print("1. Adicionar medicamento")
        print("2. Listar medicamentos")
        print("3. Buscar medicamento")
        print("4. Buscar medicamento (avançado)")
        print("5. Contar por classe")
        print("6. Remover medicamento")
        print("7. Atualizar estoque")
        print("8. Sair")

        opcao = input("Escolha uma opção: ").strip()

        # Cada bloco identifica a ação escolhida e dispara a rotina correspondente.
        if opcao == '1':
            adicionar_medicamento()
        elif opcao == '2':
            listar_medicamentos()
        elif opcao == '3':
            buscar_medicamento()
        elif opcao == '4':
            termo = input("Digite o nome ou classe para busca avançada: ")
            resultados = buscar_medicamento_avancado(termo)
            if not resultados:
                print("Nenhum medicamento encontrado com esse termo.\n")
            else:
                print("\n--- RESULTADO DA BUSCA AVANÇADA ---")
                print(f"{'Nome':<30} {'Classe':<20} {'Quantidade':<15}")
                print("-" * 65)
                for nome, classe, quantidade in resultados:
                    print(f"{nome:<30} {classe:<20} {quantidade:<15}")
                print()
        elif opcao == '5':
            categoria = input("Digite a classe para contar: ").strip()
            total = contar_por_categoria(categoria)
            print(f"Total de medicamentos na classe '{categoria}': {total}\n")
        elif opcao == '6':
            remover_medicamento()
        elif opcao == '7':
            atualizar_estoque()
        elif opcao == '8':
            print("Programa encerrado.")
            break
        else:
            print("Opção inválida! Tente novamente.\n")

if __name__ == "__main__":
    # Antes de iniciar o menu, garante-se que o arquivo físico do cadastro existe em formato correto.
    inicializar_arquivo()
    menu()
