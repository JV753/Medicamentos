# Projeto JV753

## Descrição do projeto
Este projeto foi desenvolvido para gerenciar e consultar informações sobre medicamentos de forma prática e automatizada. A ideia principal é organizar os dados em um arquivo CSV e utilizar uma aplicação em Python para realizar leitura, processamento e apresentação das informações.

O sistema permite que o usuário trabalhe com uma base de dados de medicamentos, visualize dados importantes e aplique regras de negócio para facilitar a operação de controle e consulta.

## Função dos arquivos

### main.py
O arquivo `main.py` é o ponto de entrada da aplicação. Ele é responsável por:
- carregar os dados do arquivo `medicamentos.csv`;
- processar as informações em memória;
- aplicar filtros, buscas ou validações necessárias;
- exibir os resultados ao usuário no console ou em interface gráfica, conforme a lógica implementada;
- centralizar a execução do programa.

Em outras palavras, `main.py` é o arquivo principal que controla o fluxo da aplicação.

### medicamentos.csv
O arquivo `medicamentos.csv` armazena a base de dados do projeto em formato tabular. Ele contém registros sobre medicamentos, como:
- nome;
- princípio ativo;
- categoria;
- quantidade;
- validade ou outra informação relevante;
- demais campos necessários para consulta e controle.

Esse arquivo funciona como fonte de dados da aplicação, sendo lido pelo `main.py` para que a lógica do sistema possa operar sobre as informações.

## Funcionalidades principais
O projeto pode incluir as seguintes funcionalidades, dependendo da implementação aplicada:
- cadastro de medicamentos;
- leitura de dados a partir de arquivo CSV;
- busca por nome ou princípio ativo;
- listagem de produtos cadastrados;
- organização e filtragem dos dados;
- validação de informações antes de processar os registros;
- apresentação dos resultados de forma clara e organizada.

## Como executar
1. Verifique se o Python está instalado no sistema.
2. Abra o terminal na pasta do projeto.
3. Execute o arquivo principal:

```bash
python main.py
```

Se houver dependências extras, instale-as antes com:

```bash
pip install -r requirements.txt
```

Caso o projeto não tenha arquivo `requirements.txt`, basta verificar se são necessárias bibliotecas como `pandas` ou módulos da biblioteca padrão do Python.

## Requisitos técnicos aplicados
Os requisitos técnicos aplicados neste projeto incluem:
- Python 3.x como linguagem principal;
- manipulação de arquivos CSV para armazenamento de dados;
- leitura e processamento de dados em memória;
- uso de estruturas de dados como listas, dicionários e DataFrame (quando necessário);
- organização da lógica em um ponto único de execução (`main.py`);
- aplicação de boas práticas de programação, como leitura clara do código, modularização e manutenção simples.

### Onde foi aplicado cada requisito
- Python 3.x: utilizado na criação da lógica do programa e execução da aplicação em `main.py`.
- CSV: utilizado no arquivo `medicamentos.csv` como sistema de persistência dos dados.
- Leitura e processamento de dados: aplicado na carga das informações do CSV para a aplicação.
- Estruturas de dados: usadas para organizar os medicamentos e facilitar a busca e a listagem.
- Modularização: a aplicação é centralizada em `main.py`, tornando a manutenção mais simples.

## Conclusão
O projeto combina um arquivo de dados em CSV com uma aplicação em Python para criar um sistema simples, funcional e fácil de manter. A relação entre `main.py` e `medicamentos.csv` é fundamental: o primeiro executa a lógica, e o segundo fornece as informações necessárias para o funcionamento do programa.