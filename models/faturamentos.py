from sql_alchemy import banco


class FaturamentoModel(banco.Model):
    __tablename__ = 'faturamentos'

    faturamento_id = banco.Column(banco.Integer, primary_key=True)
    venda_id = banco.Column(banco.Integer, banco.ForeignKey('vendas.venda_id'))
    dia = banco.Column(banco.Integer)
    mes = banco.Column(banco.Integer)
    ano = banco.Column(banco.Integer)
    vendas = banco.relationship("VendaModel")

    def __init__(self, faturamento_id, venda_id, dia, mes, ano):
        self.faturamento_id = faturamento_id
        self.venda_id = venda_id
        self.dia = dia
        self.mes = mes
        self.ano = ano

    def json(self):
        return {
            'faturamento_id': self.faturamento_id,
            'dia': self.dia,
            'mes': self.mes,
            'ano': self.ano,
            'vendas': [venda.json() for venda in self.vendas]
        }

    @classmethod
    def find_faturamento(cls, faturamento_id):
        faturamento = cls.query.filter_by(faturamento_id=faturamento_id).first()
        if faturamento:
            return faturamento
        return None

    def save_faturamento(self):
        banco.session.add(self)
        banco.session.commit()

    def update_faturamento(self, venda_id, dia, mes, ano):
        self.venda_id = venda_id
        self.dia = dia
        self.mes = mes
        self.ano = ano

    def delete_faturamento(self):
        banco.session.delete(self)
        banco.session.commit()
