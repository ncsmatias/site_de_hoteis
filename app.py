from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.hotel import Hoteis, Hotel
from resources.sites import NovoSite, Site, Sites
from resources.usuario import ConfirmarUsuario, Usuarios, Usuario, NovoUsuario, LoginUsuario, LogoutUsuario
from blacklist import BLACKLIST

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hoteis.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'HS256'
app.config['JWT_BLACKLIST_ENABLE'] = True

jwt = JWTManager(app)
api = Api(app)

@app.before_request
def create_database():
  db.create_all()

@jwt.token_in_blocklist_loader
def verifica_blacklist(self,token):
  return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidao(jwt_header, jwt_payload):
  return jsonify({'message': 'You have been logged out'}), 401

api.add_resource(Sites, '/sites')
api.add_resource(Site, '/site/<string:nome>')
api.add_resource(NovoSite, '/adicionar')

api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<int:id>')

api.add_resource(Usuarios, '/usuarios')
api.add_resource(Usuario, '/usuarios/<int:id>')
api.add_resource(NovoUsuario, '/cadastro')

api.add_resource(LoginUsuario, '/login')
api.add_resource(LogoutUsuario, '/logout')

api.add_resource(ConfirmarUsuario, '/confirmacao/<int:id>')

if __name__ == '__main__':
  from sql_alchemy import db
  db.init_app(app)
  app.run(debug=True)