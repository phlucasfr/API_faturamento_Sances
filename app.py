from flask import Flask, render_template
from flask_cors import CORS
from flask_restful import Api
from resources.pessoas import Pessoas, Pessoa
from resources.produtos import Produtos, Produto
from resources.vendas import Vendas, Venda
from resources.faturamentos import Faturamentos, Faturamento
from flask_jwt_extended import JWTManager
from sql_alchemy import banco

#aponta o caminho dos templates e arquivos estaticos.
app = Flask(__name__, template_folder='/home/phlucasfr/templates/', static_folder='/home/phlucasfr/templates/static/')

#configs do app
CORS(app)
banco.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'dados da conexão com o db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)

#defines as rotas
@app.route('/')
def entry():
    return render_template('index.html')

#criar o banco de dados no primeiro request recebido
@app.before_first_request
def cria_banco():
    banco.create_all()

#lista de rotas
api.add_resource(Pessoas, '/pessoas')
api.add_resource(Pessoa, '/pessoa/<int:pessoa_id>')
api.add_resource(Produtos, '/produtos')
api.add_resource(Produto, '/produto/<int:produto_id>')
api.add_resource(Vendas, '/vendas')
api.add_resource(Venda, '/venda/<int:venda_id>')
api.add_resource(Faturamentos, '/faturamentos')
api.add_resource(Faturamento, '/faturamento/<int:faturamento_id>')

