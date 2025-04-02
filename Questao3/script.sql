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

SELECT d.reg_ans, 
       d.descricao,
       SUM(COALESCE(d.vl_saldo_inicial, 0) + COALESCE(d.vl_saldo_final, 0)) AS total_despesas
FROM despesas d
WHERE (d.descricao ILIKE '%SINISTRO%' 
       OR d.descricao ILIKE '%EVENTOS%' 
       OR d.descricao ILIKE '%ASSISTÊNCIA%' 
       OR d.descricao ILIKE '%MÉDICO%' 
       OR d.descricao ILIKE '%HOSPITALAR%')
  AND d.data >= CURRENT_DATE - INTERVAL '6 months' --Não existe dados do ultimo trimestre, os arquivos são de antes, por isso usei o outro trimestre.
GROUP BY d.reg_ans, d.descricao
ORDER BY total_despesas DESC
LIMIT 10;

SELECT d.reg_ans, 
       d.descricao,
       SUM(COALESCE(d.vl_saldo_inicial, 0) + COALESCE(d.vl_saldo_final, 0)) AS total_despesas
FROM despesas d
WHERE (d.descricao ILIKE '%SINISTRO%' 
       OR d.descricao ILIKE '%EVENTOS%' 
       OR d.descricao ILIKE '%ASSISTÊNCIA%' 
       OR d.descricao ILIKE '%MÉDICO%' 
       OR d.descricao ILIKE '%HOSPITALAR%')
  AND d.data >= CURRENT_DATE - INTERVAL '1 year'
GROUP BY d.reg_ans, d.descricao
ORDER BY total_despesas DESC
LIMIT 10;
