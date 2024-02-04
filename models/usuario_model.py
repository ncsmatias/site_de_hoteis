import os 
from flask import request, url_for
from sql_alchemy import db
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class UsuarioModel(db.Model):
  __table_args__ = {'extend_existing': True}
  __tablename__ = 'usuarios'
  
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String)
  email = db.Column(db.String, unique=True)
  senha = db.Column(db.String(40))
  ativado = db.Column(db.Boolean, default=False)

  def __init__(self, nome, email, senha, ativado):
    self.nome = nome
    self.email = email
    self.senha = senha
    self.ativado = ativado
  
  def enviar_email_confirmacao(self):
    link = request.url_root[:-1] +  url_for('confirmarusuario', id=self.id)

    message = Mail(from_email="ncs.matias@gmail.com", 
    to_emails= self.email,
    subject="Confirmação de criação de conta",
    plain_text_content='alguma coisa',
    html_content=f'<a href={link}>Click para confirmar</a>'
    )
  
    sg = SendGridAPIClient(os.environ.get('SEND_GRID_KEY'))
    response = sg.send(message)  
    return response
  
  def json(self):
    return {
      'id': self.id,
      'nome': self.nome,
      'email': self.email,
      'ativado': self.ativado
    }
  
  @classmethod
  def find_usuario_email(cls, email):
    usuario = cls.query.filter_by(email=email).first()
    if usuario:
      return usuario
    
    return None
  
  @classmethod
  def find_usuario_id(cls, id):
    usuario = cls.query.filter_by(id=id).first()
    if usuario:
      return usuario
    
    return None
  
  def save_usuario(self):
    db.session.add(self)
    db.session.commit()
  
  def update_usuario(self, nome, email):
    self.nome = nome
    self.email = email
  
  def deleted_usuario(self):
    db.session.delete(self)
    db.session.commit()