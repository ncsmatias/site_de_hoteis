from resources import hotel
from sql_alchemy import db

class SiteModel(db.Model):
  __table_args__ = {'extend_existing': True}
  __tablename__ = 'sites'

  id = db.Column(db.Integer, primary_key=True)
  url = db.Column(db.String)
  nome = db.Column(db.String)
  hoteis = db.relationship('HotelModel')

  def __init__(self, url, nome):
    self.url = url
    self.nome = nome
  
  def json(self):
    return {
      'id': self.id,
      'url': self.url,
      'hoteis': [hotel.json() for hotel in self.hoteis] # type: ignore
    }
  
  @classmethod
  def find_site(cls, nome):
    site = cls.query.filter_by(nome=nome).first()
    if site:
      return site
    return None
  
  @classmethod
  def find_id(cls, id):
    site = cls.query.filter_by(id=id).first()
    if site:
      return site
    return None
  
  def save_site(self):
    db.session.add(self)
    db.session.commit()
  
  def update_site(self, url, nome):
    self.url = url
    self.nome = nome

  def delete_site(self):
    [hotel.deleted() for hotel in self.hoteis] # type: ignore

    db.session.delete(self)
    db.session.commit()
    