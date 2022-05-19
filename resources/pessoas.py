from flask_restful import Resource, reqparse
from models.pessoas import PessoaModel

# Adiciona os argumentos que podem ser recebidos
path_params = reqparse.RequestParser()
path_params.add_argument('nome', type=str)
path_params.add_argument('cidade', type=str)


class Pessoas(Resource):

    # Metodo para consultas gerais de pessoas
    def get(self):
        return {'pessoas': [pessoa.json() for pessoa in PessoaModel.query.all()]}


class Pessoa(Resource):
    # Adiciona argumentos que podem ser recebidos
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank.")
    atributos.add_argument('cidade', type=str)

    # Metodo para consulta por Id, GET
    def get(self, pessoa_id):
        pessoa = PessoaModel.find_pessoa(pessoa_id)
        if pessoa:
            return pessoa.json()
        return {'message': 'Pessoa not found.'}, 404
   
    # Metodo para cadastrar as pessoas, POST
    def post(self, pessoa_id):
        if PessoaModel.find_pessoa(pessoa_id):
            return {"message": "Nome '{}' already exists.".format(self)}, 400  # Bad Request

        dados = Pessoa.atributos.parse_args()
        pessoa = PessoaModel(pessoa_id, **dados)

        try:
            pessoa.save_pessoa()
        except:
            return {"message": "An error ocurred trying to create pessoa."}, 500  # Internal Server Error
        return pessoa.json(), 201
    
    # Metodo para alterar a pessoa, PUT
    def put(self, pessoa_id):
        dados = Pessoa.atributos.parse_args()
        pessoa_encontrada = PessoaModel.find_pessoa(pessoa_id)
        if pessoa_encontrada:
            pessoa_encontrada.update_pessoa(**dados)
            pessoa_encontrada.save_pessoa()
            return pessoa_encontrada.json(), 201
        pessoa = PessoaModel(pessoa_id, **dados)
        try:
            pessoa.save_pessoa()
        except:
            return {'message': 'An internal erro ocurred tryng to save pessoa'}, 500  # internal server error
        return pessoa.json(), 201  # created

    # Metodo para deletar a pessoa, DELETE
    def delete(self, pessoa_id):
        pessoa = PessoaModel.find_pessoa(pessoa_id)
        if pessoa:
            try:
                pessoa.delete_pessoa()
            except:
                return {'message': 'An internal erro ocurred tryng to delete pessoa'}, 500  # internal server error
            return {'message': 'Pessoa deleted.'}
        return {'message': 'Pessoa not found.'}, 404
