import traceback
from urllib import response
from flask_restful import Resource, reqparse
from models.usuario_model import UsuarioModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from blacklist import BLACKLIST

class Usuarios(Resource):
  @jwt_required()
  def get(self):
    usuatios = [usuario.json() for usuario in UsuarioModel.query.all()]
    return {'usuatios': usuatios}

class Usuario(Resource):
  argumentos = reqparse.RequestParser()
  argumentos.add_argument('nome')
  argumentos.add_argument('email', type=str, required=True, help="The field 'email' cannot be left empty")
  
  @jwt_required()
  def get(self, id):
    usuario = UsuarioModel.find_usuario_id(id)
    if usuario is not None:
      return {'usuario': usuario.json()}
    
    return {'message': 'Usuario not found'}, 404
  
  @jwt_required()
  def put(self, id):
    usuario = UsuarioModel.find_usuario_id(id)
    if usuario is None:
      return {'message': 'Usuario not found'}, 404
    
    dados = Usuario.argumentos.parse_args()
    usuario.update_usuario(**dados)
    
    try:
      usuario.save_usuario()
    except:
      return {'message': 'An internal error ocurred trying to update usuario'}, 500

    return {'usuario': usuario.json()}, 200
  
  @jwt_required()
  def delete(self, id):
    usuario = UsuarioModel.find_usuario_id(id)
    if usuario is None:
      return {'message': 'Usuario not found'}, 404
    
    try:
      usuario.deleted_usuario()
    except:
      return {'message': 'An internal error ocurred trying to delete usuario'}, 500
    
    return {'message': 'successfully deleted usuario'}, 200

class NovoUsuario(Resource):
  argumentos = reqparse.RequestParser()
  argumentos.add_argument('nome')
  argumentos.add_argument('email', type=str, required=True, help="The field 'email' cannot be left empty")
  argumentos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left empty")
  argumentos.add_argument('ativado', type=bool)

  def post(self):
    dados = NovoUsuario.argumentos.parse_args()
    if UsuarioModel.find_usuario_email(dados['email']):
      return {'message': f"Usuario email {dados['email']} already exists"}, 400

    usuario= UsuarioModel(**dados)
    usuario.ativado = False

    try:
      usuario.save_usuario()
      response = usuario.enviar_email_confirmacao()
      print(response.status_code)
      print(response.body)
      print(response.headers)
    except:
      usuario.deleted_usuario()
      traceback.print_exc()
      return {'message': 'An internal error ocurred trying to save usuario'}, 500

    return {'message': 'successfully created new usuario'}, 201

class LoginUsuario(Resource):
  argumentos = reqparse.RequestParser()
  argumentos.add_argument('email', type=str, required=True, help="The field 'email' cannot be left empty")
  argumentos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left empty")

  @classmethod
  def post(cls):
    dados = LoginUsuario.argumentos.parse_args()
    usuario = UsuarioModel.find_usuario_email(dados['email'])
    if usuario and usuario.senha == dados['senha']:
      if usuario.ativado:
        return {'access_token': create_access_token(identity=usuario.id)}, 200

      return {'message': 'User not confirmed'}, 400

    
    return {'message': 'The email or password is incorrect'}, 401

class LogoutUsuario(Resource):
  
  @jwt_required()
  def post(self):
    jwt_id = get_jwt()['jti']
    BLACKLIST.add(jwt_id)
    return {'message': 'Logged out successfully'}, 200

class ConfirmarUsuario(Resource):

  @classmethod
  def post(cls, id):
    usuario = UsuarioModel.find_usuario_id(id)
    if usuario is None:
      return {'message': 'Usuario not found'}, 404
    
    usuario.ativado = True
    usuario.save_usuario()

    return {'message': 'User confirmed successfuly'}, 200