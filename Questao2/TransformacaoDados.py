import zipfile
import os
import tabula
import pandas as pd
from datetime import datetime

def extrair_pdf_do_zip(zip_filename):
    with zipfile.ZipFile(zip_filename, 'r') as zipf:
        zip_files = zipf.namelist()
        print("Arquivos no ZIP:", zip_files)
        
        if not zip_files:
            print("Erro: Nenhum arquivo encontrado no ZIP.")
            return None
        
        pdf_filename = zip_files[0]  
        extracted_path = f"extraido_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        zipf.extract(pdf_filename, path=".")
        os.rename(pdf_filename, extracted_path)
        
        print(f"Arquivo {pdf_filename} extraído e renomeado para {extracted_path}.")
        return extracted_path

def extrair_e_transformar_pdf(pdf_path, zip_filename):
    print("Iniciando extração do PDF...")

    tables = tabula.read_pdf(pdf_path, pages="all", multiple_tables=True, lattice=True)
    if not tables:
        print("Nenhuma tabela encontrada no PDF!")
        return
    
    df = pd.concat(tables, ignore_index=True)
    
    print(df.head())

    substituicoes = {
        "OD": "Descrição Completa OD",
        "AMB": "Descrição Completa AMB"
    }

    df.replace(substituicoes, inplace=True)
    
    output_csv = f"tabela_extraida_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(output_csv, index=False)
    print(f"CSV gerado: {output_csv}")
    
    output_zip = "Teste_JoaoVictorMenezes.zip"
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        zipf.write(output_csv, os.path.basename(output_csv))
    print(f"Arquivo ZIP gerado: {output_zip}")
    
    os.remove(pdf_path)
    os.remove(output_csv)
    print("Arquivos temporários removidos.")

zip_filename = "anexos.zip"

pdf_path = extrair_pdf_do_zip(zip_filename)

if pdf_path:
    extrair_e_transformar_pdf(pdf_path, zip_filename)