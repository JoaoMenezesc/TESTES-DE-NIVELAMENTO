from flask import Flask, request, jsonify
import pandas as pd
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  
csv_path = r"C:\Users\jovmd\Documents\Projetos\Python\TESTES-DE-NIVELAMENTO\Questao3\arquivos csv\Operadoras\relatorio.csv"

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"Arquivo CSV não encontrado: {csv_path}")

try:
    df = pd.read_csv(csv_path, delimiter=";", encoding="utf-8", dtype=str)
    df.columns = df.columns.str.strip()  
except Exception as e:
    raise RuntimeError(f"Erro ao carregar CSV: {e}")


def search(query):
    query = query.lower()
    mask = df.apply(lambda row: row.astype(str).str.contains(query, case=False, na=False).any(), axis=1)
    results = df[mask].to_dict(orient="records")
    print("Resultados encontrados:", results) 
    return results

def clean_data(results):
    """ Substitui NaN por string vazia e converte objetos para string """
    return [{k: ("" if pd.isna(v) else str(v)) for k, v in row.items()} for row in results]

@app.route("/api/search", methods=["GET"])
def search_api():
    query = request.args.get("query", "").strip()
    limit = request.args.get("limit", default=20, type=int)

    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    results = search(query)[:limit]  
    results = clean_data(results)  

    return jsonify(results), 200



if __name__ == "__main__":
    app.run(debug=True)
