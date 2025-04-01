import random
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

charadas = [
    {'id': 1, 'charada':'O que tem boca, mas não fala?','resposta':'O fogão'},
    {'id': 2, 'charada':'Um homem soltou dois peidos em sequência. Qual é o nome do filme?','resposta':'gás parzinho'},
    {'id': 3, 'charada':'O que só trabalha se lhe batem na cabeça?','resposta':' o prego'},
    {'id': 4, 'charada':'O que é, o que é? Quando se tira o R, fica leve como uma pena.','resposta':'a perna'},
    {'id': 5, 'charada':'Qual é a Lua que nunca esta com fome?','resposta':' a lua cheia'},
    {'id': 6, 'charada':'O que o aluno fala para a professora e gosta de receber dos pais?','resposta':'presente'},
    {'id': 7, 'charada':'Qual é o céu que não tem estrelas?','resposta':' o céu da boca'},
    {'id': 9, 'charada':'O que te pertence, mas as outras pessoas utilizam mais do que você','resposta':' o nome'},
    {'id': 10, 'charada':'O que é, o que é? Quando dizemos o seu nome, ele deixa de existir.','resposta':' o silêncio.'},
]

@app.route('/')
def index():
    return '"CHARADAS MUITO ENGRAÇADAS GOOGLE BUSCAR"'

@app.route('/charadas', methods=['GET'])
def lista():
    return jsonify(random.choice(charadas))

@app.route('/charadas/id/<int:id>', methods=['GET'])
def charada(id):
    for charada in charadas:
        if charada['id'] == id:
            return jsonify(charada), 200
    else:
        return jsonify({'mensagem':'O que é o que é? você tentou achar mas não achou!'})
    
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)