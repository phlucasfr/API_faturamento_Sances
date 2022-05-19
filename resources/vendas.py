from flask_restful import Resource, reqparse
from models.vendas import VendaModel

# Adiciona os argumentos que podem ser recebidos
path_params = reqparse.RequestParser()
path_params.add_argument('produto_id', type=int)


class Vendas(Resource):
    # Metodo para consultas gerais de vendas
    def get(self):
        return {'vendas': [venda.json() for venda in VendaModel.query.all()]}


class Venda(Resource):
    # Adiciona argumentos que podem ser recebidos
    atributos = reqparse.RequestParser()
    atributos.add_argument('produto_id', type=int, required=True, help="The field 'produto_id' cannot be left blank.")

    # Metodo para consulta por Id, GET
    def get(self, venda_id):
        venda = VendaModel.find_by_id(venda_id)
        if venda:
            return venda.json()
        return {'message': 'Venda not found.'}, 404
    
    # Metodo para cadastrar as vendas, POST
    def post(self, venda_id):
        if VendaModel.find_by_id(venda_id):
            return {"message": "Venda '{}' already exists.".format(self)}, 400  # Bad Request

        dados = Venda.atributos.parse_args()
        venda = VendaModel(venda_id, **dados)

        try:
            venda.save_venda()
        except:
            return {"message": "An error ocurred trying to create venda."}, 500  # Internal Server Error
        return venda.json(), 201

    # Metodo para alterar a venda, PUT obs: só funcionara se definirem no Model.
    def put(self, venda_id):
        dados = Venda.atributos.parse_args()
        venda_encontrada = VendaModel.find_by_id(venda_id)
        if venda_encontrada:
            venda_encontrada.update_venda(**dados)
            venda_encontrada.save_venda()
            return venda_encontrada.json(), 201
        venda = VendaModel(venda_id, **dados)
        try:
            venda.save_venda()
        except:
            return {'message': 'An internal erro ocurred tryng to save venda'}, 500  # internal server error
        return venda.json(), 201  # created

    # Metodo para deletar a venda, DELETE
    def delete(self, venda_id):
        venda = VendaModel.find_by_id(venda_id)
        if venda:
            try:
                venda.delete_venda()
            except:
                return {'message': 'An internal erro ocurred tryng to delete venda'}, 500  # internal server error
            return {'message': 'venda deleted.'}
        return {'message': 'venda not found.'}, 404
