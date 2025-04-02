import os
import psycopg2
import pandas as pd


DB_NAME = "life"
DB_USER = "jov"
DB_PASSWORD = "1000"  
DB_HOST = "localhost"
DB_PORT = "5432"


DIR_CSV = r"C:\Users\jovmd\Documents\Projetos\Python\TESTES-DE-NIVELAMENTO\Questao3\arquivos csv\2anos"


try:
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    cursor = conn.cursor()
    print("Conexão com o banco de dados bem-sucedida!")
except Exception as e:
    print("Erro ao conectar ao banco de dados:", e)
    exit()


for file in os.listdir(DIR_CSV):
    if file.endswith(".csv"):
        file_path = os.path.join(DIR_CSV, file)
        print(f"Processando o arquivo {file_path}...")

        try:
            
            df = pd.read_csv(file_path, delimiter=";", encoding="latin1", on_bad_lines="skip")

            
            df.columns = ["data", "reg_ans", "cd_conta_contabil", "descricao", "vl_saldo_inicial", "vl_saldo_final"]

          
            df["descricao"] = df["descricao"].astype(str).str.encode("ascii", "ignore").str.decode("utf-8")

            
            df["vl_saldo_inicial"] = df["vl_saldo_inicial"].astype(str).str.replace(",", ".", regex=True)
            df["vl_saldo_final"] = df["vl_saldo_final"].astype(str).str.replace(",", ".", regex=True)

            
            temp_file = file_path + ".utf8"
            df.to_csv(temp_file, sep=";", index=False, encoding="utf-8")

            
            with open(temp_file, "r", encoding="utf-8") as f:
                cursor.copy_expert(
                    "COPY despesas (data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final) FROM STDIN WITH CSV HEADER DELIMITER ';'",
                    f,
                )
            conn.commit()

            os.remove(temp_file)
            print(f"Arquivo {file} importado com sucesso!")

        except Exception as e:
            print(f"Erro ao processar {file}: {e}")


cursor.close()
conn.close()
print("Importação concluída!")
