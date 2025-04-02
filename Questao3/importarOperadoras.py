import os
import psycopg2
import pandas as pd


DB_NAME = "life"
DB_USER = "jov"
DB_PASSWORD = "1000"  
DB_HOST = "localhost"
DB_PORT = "5432"

FILE_CSV = r"/home/joao/Documentos/Teste/Questao3/arquivos csv/Operadoras/relatorio.csv"


try:
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    cursor = conn.cursor()
    print("Conexão com o banco de dados bem-sucedida!")
except Exception as e:
    print("Erro ao conectar ao banco de dados:", e)
    exit()


try:
    print(f"Processando o arquivo {FILE_CSV}...")

    
    df = pd.read_csv(FILE_CSV, delimiter=";", encoding="latin1", on_bad_lines="skip")

   
    df.columns = [
        "registro_ans", "cnpj", "razao_social", "nome_fantasia", "modalidade",
        "logradouro", "numero", "complemento", "bairro", "cidade", "uf", "cep",
        "ddd", "telefone", "fax", "endereco_eletronico", "representante",
        "cargo_representante", "regiao_comercializacao", "data_registro_ans"
    ]

   
    def clean_text(text):
        if isinstance(text, str):
            return text.encode("latin1", "ignore").decode("utf-8", "ignore") 
        return text

    for col in df.columns:
        df[col] = df[col].astype(str).apply(clean_text)

    
    df["numero"] = df["numero"].astype(str).str.replace(",", ".", regex=True)
    df["cep"] = df["cep"].astype(str).str.replace(",", ".", regex=True)

    
    df["ddd"] = df["ddd"].astype(str).str.split('.').str[0]
    df["ddd"] = df["ddd"].str[:3]

    
    df["telefone"] = df["telefone"].astype(str).str.split('.').str[0]
    df["telefone"] = df["telefone"].str[:15]

    df["fax"] = df["fax"].astype(str).str.split('.').str[0]
    df["fax"] = df["fax"].str[:15]

    
    temp_file = FILE_CSV + ".utf8"
    df.to_csv(temp_file, sep=";", index=False, encoding="utf-8")

    
    with open(temp_file, "r", encoding="utf-8") as f:
        cursor.copy_expert(
            "COPY operadoras (registro_ans, cnpj, razao_social, nome_fantasia, modalidade, logradouro, numero, complemento, bairro, cidade, uf, cep, ddd, telefone, fax, endereco_eletronico, representante, cargo_representante, regiao_comercializacao, data_registro_ans) FROM STDIN WITH CSV HEADER DELIMITER ';'",
            f,
        )
    conn.commit()

    os.remove(temp_file)
    print(f"Arquivo {FILE_CSV} importado com sucesso!")

except Exception as e:
    print(f"Erro ao processar {FILE_CSV}: {e}")


cursor.close()
conn.close()
print("✅ Importação concluída!")
