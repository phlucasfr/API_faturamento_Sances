from sql_alchemy import banco


class ProdutoModel(banco.Model):
    __tablename__ = 'produtos'

    # aqui vai os campos e tipos de dados na tabela SQL.
    produto_id = banco.Column(banco.Integer, primary_key=True)
    pessoa_id = banco.Column(banco.Integer, banco.ForeignKey('pessoas.pessoa_id'))
    descricao = banco.Column(banco.String(80))
    tipo = banco.Column(banco.String(80))
    valor = banco.Column(banco.Float)
    vendas = banco.relationship('VendaModel')  # lista de objetos faturamentos

    # Valores que devem ser enviados no request
    def __init__(self, produto_id, pessoa_id, descricao, tipo, valor):
        self.produto_id = produto_id
        self.pessoa_id = pessoa_id
        self.descricao = descricao
        self.tipo = tipo
        self.valor = valor

    # Valores que devem retornar no Json
    def json(self):
        return {
            'produto_id': self.produto_id,
            'pessoa_id': self.pessoa_id,
            'descricao': self.descricao,
            'tipo': self.tipo,
            'valor': self.valor,
            'vendas': [venda.json() for venda in self.vendas]
        }

    # Metodo de busca por Id
    @classmethod
    def find_produto(cls, produto_id):
        produto = cls.query.filter_by(produto_id=produto_id).first()
        if produto:
            return produto
        return None

    # Metodo para salvar o produto
    def save_produto(self):
        banco.session.add(self)
        banco.session.commit()

    #   Metodo que selecionas os valores a serem atualizados em um PUT
    def update_produto(self, descricao, tipo, valor):
        self.descricao = descricao
        self.tipo = tipo
        self.valor = valor

    # Metodo para deletar o faturamento
    def delete_produto(self):
        banco.session.delete(self)
        banco.session.commit()
