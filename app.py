import random  # Importa o módulo random para gerar números aleatórios
from flask import Flask, jsonify, request  # Importa as classes Flask, jsonify e request do módulo flask
from flask_cors import CORS  # Importa o módulo CORS para lidar com requisições de origens diferentes
import firebase_admin  # Importa o módulo firebase_admin para interagir com o Firebase
from firebase_admin import credentials, firestore  # Importa as classes credentials e firestore do módulo firebase_admin
import os
from dotenv import load_dotenv
import json

app = Flask(__name__)  # Cria uma instância do Flask
CORS(app)  # Habilita o CORS para a aplicação Flask

FBKEY = json.loads(os.getenv('CONFIG_FIREBASE'))

cred = credentials.Certificate('FBKEY')  # Carrega as credenciais do Firebase a partir de um arquivo JSON
firebase_admin.initialize_app(cred)  # Inicializa o aplicativo Firebase
db = firestore.client()  # Cria um cliente do Firestore para interagir com o banco de dados

@app.route('/', methods=['GET'])  # Define a rota raiz da API e o método HTTP GET
def index():
    return '"CHARADAS MUITO ENGRAÇADAS GOOGLE BUSCAR"'  # Retorna uma mensagem simples

@app.route('/charadas', methods=['GET'])  # Define a rota /charadas e o método HTTP GET
def charada_aleatória():
    charadas = []  # Inicializa uma lista vazia para armazenar as charadas
    lista = db.collection('charadas').stream()  # Busca todas as charadas no Firestore

    for item in lista:  # Itera sobre os documentos retornados pelo Firestore
        charadas.append(item.to_dict())  # Converte cada documento em um dicionário e adiciona à lista

    if charadas:  # Verifica se a lista de charadas não está vazia
        return jsonify(random.choice(charadas)), 200  # Seleciona uma charada aleatória e a retorna em formato JSON
    else:  # Caso a lista de charadas esteja vazia
        return jsonify({'mensagem': 'o que é o que é? você tentou procurar e não achou!'}), 404  # Retorna uma mensagem de erro e o código de status 404

@app.route('/charadas/<id>', methods=['GET'])  # Define a rota /charadas/<id> e o método HTTP GET
def busca(id):
    doc_ref = db.collection('charadas').document(id)  # Busca o documento da charada com o ID especificado no Firestore
    doc = doc_ref.get().to_dict()  # Obtém o documento e o converte em um dicionário

    if doc:  # Verifica se o documento foi encontrado
        return jsonify(doc)  # Retorna a charada em formato JSON
    else:  # Caso o documento não tenha sido encontrado
        return jsonify({'mensagem': 'o que é o que é? você tentou procurar e não achou!'})  # Retorna uma mensagem de erro

@app.route('/charadas', methods=['POST'])  # Define a rota /charadas e o método HTTP POST
def adicionar_charada():
    dados = request.json  # Obtém os dados da charada do corpo da requisição (JSON)

    if "pergunta" not in dados or "resposta" not in dados:  # Verifica se os campos "pergunta" e "resposta" estão presentes
        return jsonify({'mensagem': 'Erro. Campos pergunta e resposta são obrigatórios'}), 404  # Retorna uma mensagem de erro e o código de status 404

    contador_ref = db.collection('controle_id').document('contador')  # Busca o documento do contador de IDs no Firestore
    contador_doc = contador_ref.get().to_dict()  # Obtém o documento e o converte em um dicionário
    ultimo_id = contador_doc.get('id')  # Obtém o último ID usado
    novo_id = int(ultimo_id) + 1  # Gera um novo ID

    contador_ref.update({'id': novo_id})  # Atualiza o contador de IDs no Firestore

    db.collection('charadas').document(str(novo_id)).set({  # Adiciona a nova charada ao Firestore
        "id": novo_id,
        "pergunta": dados['pergunta'],
        "resposta": dados['resposta']
    })

    return jsonify({'mensagem': 'Charada cadastrada com sucesso!'}), 201  # Retorna uma mensagem de sucesso e o código de status 201

@app.route('/charadas/<id>', methods=['PUT'])  # Define a rota /charadas/<id> e o método HTTP PUT
def alterar_charada(id):
    dados = request.json  # Obtém os dados atualizados da charada do corpo da requisição (JSON)

    if "pergunta" not in dados or "resposta" not in dados:  # Verifica se os campos "pergunta" e "resposta" estão presentes
        return jsonify({'mensagem': 'Erro. Campos pergunta e resposta são obrigatórios'}), 404  # Retorna uma mensagem de erro e o código de status 404

    doc_ref = db.collection('charadas').document(id)  # Busca o documento da charada com o ID especificado no Firestore
    doc = doc_ref.get()  # Obtém o documento

    if doc.exists:  # Verifica se o documento existe
        doc_ref.update({  # Atualiza a charada no Firestore
            "pergunta": dados['pergunta'],
            "resposta": dados['resposta']
        })
        return jsonify({'mensagem': 'Charada atualizada com sucesso!'}), 201  # Retorna uma mensagem de sucesso e o código de status 201
    else:  # Caso o documento não exista
        return jsonify({'mensagem': 'Erro! - Charada não encontrada'}), 404  # Retorna uma mensagem de erro e o código de status 404

@app.route('/charadas/<id>', methods=['DELETE'])  # Define a rota /charadas/<id> e o método HTTP DELETE
def excluir_charada(id):
    doc_ref = db.collection('charadas').document(id)  # Busca o documento da charada com o ID especificado no Firestore
    doc = doc_ref.get()  # Obtém o documento

    if not doc.exists:  # Verifica se o documento não existe
        return jsonify({'mensagem': 'Erro, charada não encontrada!'})  # Retorna uma mensagem de erro

    doc_ref.delete()  # Exclui a charada do Firestore
    return jsonify({'mensagem': 'Charada excluída com sucesso!'})  # Retorna uma mensagem de sucesso

if __name__ == '__main__':
    app.run(debug=True)  # Inicia o aplicativo Flask em modo de depuração