from sql_alchemy import banco


class PessoaModel(banco.Model):
    __tablename__ = 'pessoas'

    pessoa_id = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.String(80))
    cidade = banco.Column(banco.String(80))
    produtos = banco.relationship('ProdutoModel')  # lista de objetos faturamentos


    def __init__(self, pessoa_id,  nome, cidade):
        self.pessoa_id = pessoa_id
        self.nome = nome
        self.cidade = cidade

    def json(self):
        return {
            'pessoa_id': self.pessoa_id,
            'nome': self.nome,
            'cidade': self.cidade,
            'produtos': [produto.json() for produto in self.produtos]
        }

    @classmethod
    def find_pessoa(cls, pessoa_id):
        pessoa = cls.query.filter_by(pessoa_id=pessoa_id).first()
        if pessoa:
            return pessoa
        return None

    def save_pessoa(self):
        banco.session.add(self)
        banco.session.commit()

    def update_pessoa(self, nome, cidade):
        self.nome = nome
        self.cidade = cidade

    def delete_pessoa(self):
        banco.session.delete(self)
        banco.session.commit()
