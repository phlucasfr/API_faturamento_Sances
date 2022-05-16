from flask_restful import Resource, reqparse
from models.produtos import DespesaModel

path_params = reqparse.RequestParser()
path_params.add_argument('tipo', type=str)
path_params.add_argument('valor', type=int)

class Despesas(Resource):
    def get(self):
        return {'despesas': [despesa.json() for despesa in DespesaModel.query.all()]}

class Despesa(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('tipo', type=str, required=True, help="The field 'tipo' cannot be left blank.")
    atributos.add_argument('valor')

    def get(self, despesa_id):
        despesa = DespesaModel.find_despesa(despesa_id)
        if despesa:
            return despesa.json()
        return {'message': 'Receita not found.'}, 404


    def post(self, despesa_id):
        if DespesaModel.find_despesa(despesa_id):
            return {"message": "Tipo '{}' already exists.".format(self)}, 400 #Bad Request

        dados = Despesa.atributos.parse_args()
        despesa = DespesaModel(despesa_id, **dados)

        try:
            despesa.save_despesa()
        except:
            return {"message": "An error ocurred trying to create receita."}, 500 #Internal Server Error
        return despesa.json(), 201

    def put(self, despesa_id):
        dados = Despesa.atributos.parse_args()
        despesa_encontrada = DespesaModel.find_despesa(despesa_id)
        if despesa_encontrada:
            despesa_encontrada.update_despesa(**dados)
            despesa_encontrada.save_despesa()
            return despesa_encontrada.json(), 201
        despesa = DespesaModel(despesa_id, **dados)
        try:
            despesa.save_despesa()
        except:
            return {'message': 'An internal erro ocurred tryng to save despesa'}, 500  # internal server error
        return despesa.json(), 201 #created

    def delete(self, despesa_id):
        despesa = DespesaModel.find_despesa(despesa_id)
        if despesa:
            try:
                despesa.delete_despesa()
            except:
                return {'message': 'An internal erro ocurred tryng to delete despesa'}, 500  # internal server error
            return {'message': 'Despesa deleted.'}
        return {'message': 'Despesa not found.'}, 404