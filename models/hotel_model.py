from sql_alchemy import db

class HotelModel(db.Model):
  __table_args__ = {'extend_existing': True}
  __tablename__ = 'hoteis'
  
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String)
  estrelas = db.Column(db.Float(precision=1))
  valor_diaria = db.Column(db.Float(precision=2))
  cidade = db.Column(db.String)
  site_id = db.Column(db.Integer, db.ForeignKey('sites.id'))

  def __init__(self, id, nome, estrelas, valor_diaria, cidade, site_id):
    self.id = id
    self.nome = nome
    self.estrelas = estrelas
    self.valor_diaria = valor_diaria
    self.cidade = cidade
    self.site_id = site_id
  
  def json(self):
    return {
      'id': self.id,
      'nome': self.nome,
      'estrelas': self.estrelas,
      'valor_diaria': self.valor_diaria,
      'cidade': self.cidade,
      'site_id': self.site_id
    }
  
  @classmethod
  def find_hotel(cls, id):
    # SELECT * FROM hoteis WHERE id = id LIMIT 1
    hotel = cls.query.filter_by(id=id).first()
    if hotel:
      return hotel
    
    return None
  
  def save_hotel(self):
    db.session.add(self)
    db.session.commit()
  
  def update_hotel(self, nome, estrelas, valor_diaria, cidade):
    self.nome = nome
    self.estrelas = estrelas
    self.valor_diaria = valor_diaria
    self.cidade = cidade
  
  def deleted(self):
    db.session.delete(self)
    db.session.commit()