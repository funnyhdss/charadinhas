API de Charadas Engraçadas

Descrição

Esta e uma API simples desenvolvida com Flask que fornece charadas aleatorias ou especificas por ID.

Tecnologias Utilizadas:
Este projeto foi desenvolvido utilizando as seguintes tecnologias:
Python 3.x: Linguagem de programacao principal.
Flask: Microframework para a construcao da API.
Flask-CORS: Extensao para habilitar o CORS e permitir requisicoes de diferentes origens.
Random: Biblioteca padrao do Python utilizada para selecionar charadas aleatorias.

Para executar este projeto, voce precisa ter instalado:
Python 3.x
Flask
Flask-CORS

Estrutura do Codigo:
O codigo esta estruturado da seguinte forma:
Lista de Charadas: Um array contendo charadas e suas respectivas respostas.
Rota Principal (/): Retorna uma mensagem estatica indicando que a API esta ativa.
Rota /charadas: Retorna uma charada aleatoria escolhida pela funcao random.choice().
Rota /charadas/id/<int:id>: Busca uma charada especifica pelo ID e a retorna. Caso o ID nao seja encontrado, retorna uma mensagem de erro personalizada.
Execucao do Servidor: Configurado para rodar na porta 5000 e aceitar conexoes externas (host='0.0.0.0').

Autor:
Heitor Schutz - GitHub: funnyhdss
