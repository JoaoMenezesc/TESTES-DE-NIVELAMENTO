# Passo a Passo para Execução dos Scripts SQL e Python

## 1. Criar o usuário para acesso ao banco de dados
Executar o seguinte script SQL para criar o usuário:
```sh
psql -U postgres -f criarUsuario.sql
```

## 2. Criar as tabelas do banco de dados
Executar o script SQL para criação das tabelas:
```sh
psql -U jov -d life -f criarTabela.sql
```

## 3. Importar os arquivos CSV dos últimos 2 anos
Executar o seguinte comando Python:
```sh
python importar2anos.py
```

## 4. Importar o arquivo CSV relatorio.csv
Executar o script Python para importar os operadores:
```sh
python importarOperadoras.py
```

## 5. Executar a consulta das 10 maiores despesas do último trimestre
Executar o script SQL:
```sh
psql -U jov -d life -f top10DespesasTrimestre.sql
```

## 6. Executar a consulta das 10 maiores despesas do último ano
Executar o script SQL:
```sh
psql -U jov -d life -f top10DespesasAno.sql
```

Agora o banco de dados está configurado e pronto para uso!

