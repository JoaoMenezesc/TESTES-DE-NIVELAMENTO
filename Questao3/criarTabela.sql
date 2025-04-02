CREATE TABLE IF NOT EXISTS despesas (
    id SERIAL PRIMARY KEY,
    data DATE,
    reg_ans VARCHAR(50),
    cd_conta_contabil VARCHAR(50),
    descricao VARCHAR(255),
    vl_saldo_inicial DECIMAL(15, 2),
    vl_saldo_final DECIMAL(15, 2)
);

CREATE TABLE IF NOT EXISTS operadoras (
    id SERIAL PRIMARY KEY,
    registro_ans VARCHAR(50) NOT NULL,
    cnpj VARCHAR(18) NOT NULL,
    razao_social VARCHAR(255),
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    logradouro VARCHAR(255),
    numero VARCHAR(50),
    complemento VARCHAR(255),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    uf VARCHAR(2),
    cep VARCHAR(10),
    ddd VARCHAR(3),
    telefone VARCHAR(15),
    fax VARCHAR(15),
    endereco_eletronico VARCHAR(255),
    representante VARCHAR(255),
    cargo_representante VARCHAR(100),
    regiao_comercializacao VARCHAR(100),
    data_registro_ans DATE
);
