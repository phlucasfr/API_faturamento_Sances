from sql_alchemy import banco


class VendaModel(banco.Model):
    __tablename__ = 'vendas'

    venda_id = banco.Column(banco.Integer, primary_key=True)
    produto_id = banco.Column(banco.Integer, banco.ForeignKey('produtos.produto_id'))
    faturamentos = banco.relationship('FaturamentoModel')  # lista de objetos faturamentos

    def __init__(self, venda_id, produto_id):
        self.venda_id = venda_id
        self.produto_id = produto_id

    def json(self):
        return {
            'venda_id': self.venda_id,
            'produto_id': self.produto_id,
            'faturamentos': [faturamento.json() for faturamento in self.faturamentos]
        }

    @classmethod
    def find_by_id(cls, venda_id):
        venda = cls.query.filter_by(venda_id=venda_id).first()
        if venda:
            return venda
        return None

    def save_venda(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_venda(self):
        # deletando todos os produtos associados a venda
        [produto.delete_produto() for produto in self.produtos]
        # deletando venda
        banco.session.delete(self)
        banco.session.commit()
