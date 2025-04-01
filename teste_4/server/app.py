from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os
from fuzzywuzzy import fuzz

# Configuração de diretórios
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))

app = Flask(__name__)
CORS(app)

# Configurar Flask para JSON
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = 'application/json'

# Carregar o arquivo CSV
csv_path = os.path.join(ROOT_DIR, 'teste_3', 'downloads', 'cleaned_Relatorio_cadop.csv')
df = pd.read_csv(csv_path, sep=';', encoding='utf-8')

# Colunas padrão para pesquisa
search_columns = [
    'Razao_Social',
    'Nome_Fantasia',
    # 'Registro_ANS',
    # 'CNPJ',
    # 'Cidade',
    # 'UF'
]

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/api/search_settings', methods=['GET'])
def get_search_settings():
    return jsonify({
        "columns": list(df.columns),
        "selected_columns": search_columns
    })

@app.route('/api/search_settings', methods=['POST'])
def update_search_settings():
    global search_columns
    data = request.get_json()
    if not data or 'selected_columns' not in data:
        return jsonify({"error": "No columns selected"}), 400
    
    # Validate that all selected columns exist in the dataframe
    valid_columns = [col for col in data['selected_columns'] if col in df.columns]
    if not valid_columns:
        return jsonify({"error": "No valid columns selected"}), 400
    
    search_columns = valid_columns
    return jsonify({"message": "Search settings updated successfully"})

@app.route('/api/operadoras', methods=['GET'])
def get_all_operadoras():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    operadoras = df.iloc[start_idx:end_idx].to_dict('records')
    total = len(df)
    
    return jsonify({
        "data": operadoras,
        "total": total,
        "page": page,
        "per_page": per_page
    })

@app.route('/api/operadoras/<registro_ans>', methods=['GET'])
def get_operadora(registro_ans):
    operadora = df[df['Registro_ANS'] == registro_ans].to_dict('records')
    if not operadora:
        return jsonify({"error": "Operadora not found"}), 404
    return jsonify(operadora[0])

@app.route('/api/search', methods=['GET'])
def search_operadoras():
    query = request.args.get('q', '')
    if not query:
        return jsonify({
            "data": [],
            "total": 0,
            "query": "",
            "columns_searched": search_columns
        }), 200, {'Content-Type': 'application/json'}
    
    # print(f"Pesquisando por: {query}")
    # print(f"Usando colunas: {search_columns}")
    
    # Criar uma cópia do dataframe para pesquisa
    search_df = df.copy()
    
    # Converter colunas selecionadas para string para pesquisa
    for col in search_columns:
        search_df[col] = search_df[col].astype(str)
    
    # Calcular pontuações de similaridade para cada linha
    def calculate_similarity(row):
        max_score = 0
        for col in search_columns:
            score = fuzz.partial_ratio(query.lower(), row[col].lower())
            max_score = max(max_score, score)
        return max_score
    
    # Adicionar pontuações de similaridade
    search_df['similarity'] = search_df.apply(calculate_similarity, axis=1)
    
    # Filtrar e ordenar por similaridade
    results = search_df[search_df['similarity'] > 60].sort_values('similarity', ascending=False)
    
    # Remover a coluna de similaridade e tratar valores NaN
    results = results.drop('similarity', axis=1)
    
    # Substituir valores NaN por None (null em JSON)
    results = results.where(results.notna(), None)
    
    # Converter para registros e garantir serialização JSON
    results_list = results.to_dict('records')
    
    # Limpeza adicional para garantir serialização JSON
    for record in results_list:
        for key, value in record.items():
            if pd.isna(value) or value == 'nan':
                record[key] = None
    
    response_data = {
        "data": results_list,
        "total": len(results_list),
        "query": query,
        "columns_searched": search_columns
    }
    
    # print(f"Encontrados {len(results_list)} resultados")
    # if results_list:
    #     print(f"Primeiro resultado: {results_list[0]}")
    
    return jsonify(response_data), 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    app.run(debug=True, port=5000) 