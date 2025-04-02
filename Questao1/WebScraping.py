import requests
from bs4 import BeautifulSoup
import os
import zipfile

def baixar_e_compactar_pdfs(url, download_dir="downloads", zip_filename="anexos.zip"):
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    def download_pdf(pdf_url, filename):
        response = requests.get(pdf_url)
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Download concluído: {filename}")

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    pdf_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if 'pdf' in href:
            if 'Anexo I' in link.text or 'Anexo II' in link.text:
                pdf_url = href if href.startswith('http') else "https://www.gov.br" + href
                pdf_links.append(pdf_url)

    if len(pdf_links) < 2:
        print("Não foram encontrados dois anexos PDF.")
        return

    pdf_files = []
    for i, pdf_link in enumerate(pdf_links[:2]):  
        filename = os.path.join(download_dir, f"anexo_{i+1}.pdf")
        download_pdf(pdf_link, filename)
        pdf_files.append(filename)

    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in pdf_files:
            zipf.write(file, os.path.basename(file))

    print(f"Arquivos compactados: {zip_filename}")

url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

baixar_e_compactar_pdfs(url)
