from flask_restful import Resource, reqparse
from models.faturamentos import FaturamentoModel
from resources.filtros import normalize_path_params, consulta_com_vendas, consulta_sem_vendas
import mysql.connector

path_params = reqparse.RequestParser()
path_params.add_argument('venda_id', type=int)
path_params.add_argument('dia_min', type=int)
path_params.add_argument('dia_max', type=int)
path_params.add_argument('mes_min', type=int)
path_params.add_argument('mes_max', type=int)
path_params.add_argument('ano_min', type=int)
path_params.add_argument('ano_max', type=int)


class Faturamentos(Resource):
    def get(self):
        connection = mysql.connector.connect(user='dados da conexão')
        cursor = connection.cursor()

        dados = path_params.parse_args()
        dados_validos = {chave: dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)

        if not parametros.get('venda_id'):
            tupla = tuple([parametros[chave] for chave in parametros])
            cursor.execute(consulta_sem_vendas, tupla)
            resultado = cursor.fetchall()
        else:
            tupla = tuple([parametros[chave] for chave in parametros])
            cursor.execute(consulta_com_vendas, tupla)
            resultado = cursor.fetchall()

        faturamentos = []
        if resultado:
            for linha in resultado:
                faturamentos.append({
                    'faturamento_id': linha[0],
                    'venda_id': linha[1],
                    'dia': linha[2],
                    'mes': linha[3],
                    'ano': linha[4]
                })

        return {'faturamentos': faturamentos}  # SELECT * FROM hoteis


class Faturamento(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('venda_id')
    atributos.add_argument('dia')
    atributos.add_argument('mes')
    atributos.add_argument('ano')

    def get(self, faturamento_id):
        faturamento = FaturamentoModel.find_faturamento(faturamento_id)
        if faturamento:
            return faturamento.json()
        return {'message': 'Faturamento not found.'}, 404

    def post(self, faturamento_id):
        if FaturamentoModel.find_faturamento(faturamento_id):
            return {"message": "Faturamento '{}' already exists.".format(self)}, 400  # Bad Request

        dados = Faturamento.atributos.parse_args()
        faturamento = FaturamentoModel(faturamento_id, **dados)

        try:
            faturamento.save_faturamento()
        except:
            return {"message": "An error ocurred trying to create faturamento."}, 500  # Internal Server Error
        return faturamento.json(), 201

    def put(self, faturamento_id):
        dados = Faturamento.atributos.parse_args()
        faturamento_encontrada = FaturamentoModel.find_faturamento(faturamento_id)
        if faturamento_encontrada:
            faturamento_encontrada.update_faturamento(**dados)
            faturamento_encontrada.save_faturamento()
            return faturamento_encontrada.json(), 201
        faturamento = FaturamentoModel(faturamento_id, **dados)
        try:
            faturamento.save_faturamento()
        except:
            return {'message': 'An internal erro ocurred tryng to save faturamento'}, 500  # internal server error
        return faturamento.json(), 201  # created

    def delete(self, faturamento_id):
        faturamento = FaturamentoModel.find_faturamento(faturamento_id)
        if faturamento:
            try:
                faturamento.delete_faturamento()
            except:
                return {'message': 'An internal erro ocurred tryng to delete faturamento'}, 500  # internal server error
            return {'message': 'Faturamento deleted.'}
        return {'message': 'Faturamento not found.'}, 404
