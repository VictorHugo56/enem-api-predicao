# app/app.py

import flask
import pandas as pd
import joblib
import os

# --- Carregamento do Modelo e Colunas ---

# Construir o caminho para a pasta 'models' a partir da localização de app.py
# __file__ é o caminho para o arquivo atual (app.py)
# os.path.dirname() pega o diretório desse arquivo
# os.path.join('..', 'models') sobe um nível e entra em 'models'
model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'modelo_enem_lgbm.joblib')
col_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'model_columns.joblib')

# Carregar o modelo e as colunas do modelo
try:
    model = joblib.load(model_path)
    model_columns = joblib.load(col_path)
    print("Modelo e colunas carregados com sucesso.")
except Exception as e:
    print(f"Erro ao carregar o modelo ou colunas: {e}")
    model = None
    model_columns = None

# --- Inicialização da Aplicação Flask ---
app = flask.Flask(__name__)

# --- Definição dos Endpoints da API ---

# Endpoint principal para a predição
@app.route('/predict', methods=['POST'])
def predict():
    # Garantir que o modelo foi carregado corretamente
    if model is None or model_columns is None:
        return flask.jsonify({'error': 'Modelo não está carregado, verifique os logs do servidor.'}), 500

    try:
        # Obter os dados JSON da requisição
        json_data = flask.request.get_json()
        
        # Converter os dados JSON para um DataFrame do Pandas
        input_df = pd.DataFrame(json_data)

        # Pré-processamento: One-Hot Encoding e alinhamento de colunas
        # 1. Aplicar o One-Hot Encoding nos dados de entrada
        input_encoded = pd.get_dummies(input_df)
        
        # 2. Reindexar o DataFrame de entrada para garantir que ele tenha exatamente as mesmas
        #    colunas que o modelo espera, preenchendo colunas faltantes com 0.
        #    Isso é CRUCIAL para evitar erros.
        input_final = input_encoded.reindex(columns=model_columns, fill_value=0)

        # Realizar a predição
        prediction = model.predict(input_final)

        # Formatar a resposta
        response = {
            'prediction': {
                'nota_matematica_estimada': prediction[0]
            }
        }
        
        return flask.jsonify(response)

    except Exception as e:
        # Retornar uma mensagem de erro se algo der errado
        return flask.jsonify({'error': str(e)}), 400


# Endpoint raiz para verificar se a API está online
@app.route('/', methods=['GET'])
def index():
    return "<h1>API do Modelo ENEM está online. Use o endpoint /predict para fazer previsões.</h1>"


# --- Execução da Aplicação ---
if __name__ == '__main__':
    # ATENÇÃO: Uma etapa extra é necessária aqui!
    # Precisamos salvar as colunas do modelo.
    # Volte ao notebook 03 e execute:
    #
    # import joblib
    # import os
    # model_columns = X.columns
    # caminho_colunas = os.path.join('..', 'models', 'model_columns.joblib')
    # joblib.dump(model_columns, caminho_colunas)
    # print("Colunas do modelo salvas!")
    #
    # Após salvar, você pode rodar a API.
    app.run(debug=True, host='0.0.0.0')
