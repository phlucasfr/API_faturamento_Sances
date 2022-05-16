from flask_restful import Resource, reqparse
from models.produtos import ProdutoModel

path_params = reqparse.RequestParser()
path_params.add_argument('pessoa_id', type=int)
path_params.add_argument('descricao', type=str)
path_params.add_argument('tipo', type=str)
path_params.add_argument('valor', type=int)


class Produtos(Resource):
    def get(self):
        return {'produtos': [produto.json() for produto in ProdutoModel.query.all()]}


class Produto(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('pessoa_id', type=str,)
    atributos.add_argument('descricao', type=str, required=True, help="The field 'descricao' cannot be left blank.")
    atributos.add_argument('tipo')
    atributos.add_argument('valor')

    def get(self, produto_id):
        produto = ProdutoModel.find_produto(produto_id)
        if produto:
            return produto.json()
        return {'message': 'Produto not found.'}, 404

    def post(self, produto_id):
        if ProdutoModel.find_produto(produto_id):
            return {"message": "Nome '{}' already exists.".format(self)}, 400  # Bad Request

        dados = Produto.atributos.parse_args()
        produto = ProdutoModel(produto_id, **dados)

        try:
            produto.save_produto()
        except:
            return {"message": "An error ocurred trying to create produto."}, 500  # Internal Server Error
        return produto.json(), 201

    def put(self, produto_id):
        dados = Produto.atributos.parse_args()
        produto_encontrada = ProdutoModel.find_produto(produto_id)
        if produto_encontrada:
            produto_encontrada.update_produto(**dados)
            produto_encontrada.save_produto()
            return produto_encontrada.json(), 201
        produto = ProdutoModel(produto_id, **dados)
        try:
            produto.save_produto()
        except:
            return {'message': 'An internal erro ocurred tryng to save produto'}, 500  # internal server error
        return produto.json(), 201  # created

    def delete(self, produto_id):
        produto = ProdutoModel.find_produto(produto_id)
        if produto:
            try:
                produto.delete_produto()
            except:
                return {'message': 'An internal erro ocurred tryng to delete produto'}, 500  # internal server error
            return {'message': 'Produto deleted.'}
        return {'message': 'Produto not found.'}, 404
