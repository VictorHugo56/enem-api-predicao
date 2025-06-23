# test_api.py
import requests
import json

# URL do nosso endpoint local
url = 'http://127.0.0.1:5000/predict'

# Dados de um aluno de exemplo para teste.
# As chaves devem corresponder exatamente às features que usamos ANTES do One-Hot Encoding.
test_data = {
    'NU_NOTA_CN': [650.5],
    'NU_NOTA_CH': [700.1],
    'NU_NOTA_LC': [680.0],
    'NU_NOTA_REDACAO': [800.0],
    'Q001': ['E'], # Ensino Médio completo
    'Q002': ['F'], # Faculdade completa
    'Q006': ['G'], # Renda de 4 a 5 salários mínimos
    'Q022': ['C'], # Tem 2 celulares
    'Q024': ['B'], # Tem computador
    'Q025': ['B'], # Tem internet
    'TP_ESCOLA': [3],  # Privada
    'TP_LINGUA': [0]   # Inglês
}

# Enviar a requisição POST com os dados em formato JSON
try:
    response = requests.post(url, json=test_data)
    response.raise_for_status()  # Lança um erro para status ruins (4xx ou 5xx)

    # Imprimir a resposta
    print(f"Status Code: {response.status_code}")
    print("Resposta da API:")
    print(json.dumps(response.json(), indent=4))

except requests.exceptions.RequestException as e:
    print(f"Erro ao fazer a requisição: {e}")