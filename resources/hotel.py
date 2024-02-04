from flask_restful import Resource, reqparse
from models.hotel_model import HotelModel
from flask_jwt_extended import jwt_required
import sqlite3
from models.site_model import SiteModel

from resources.filtros import consulta_com_cidade, consulta_sem_cidade, normalize_path_params

path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str, location='args')
path_params.add_argument('estrela_min', type=float, location='args')
path_params.add_argument('estrela_max', type=float, location='args')
path_params.add_argument('diaria_min', type=float, location='args')
path_params.add_argument('diaria_max', type=float, location='args')
path_params.add_argument('limit', type=int, location='args')
path_params.add_argument('offset', type=int, location='args')

class Hoteis(Resource):
  def get(self):
    connection = sqlite3.connect('instance/hoteis.db')
    
    cursor = connection.cursor()
    dados = path_params.parse_args()
    print('AQUI')
    
    params = {key: dados[key] for key in dados if dados[key] is not None}
    params = normalize_path_params(**params)
    
    print(params)
    if not params.get('cidade'):
      consulta = consulta_sem_cidade()
      tupla = tuple([params[key] for key in params])
      resultado = cursor.execute(consulta, tupla)
    else:
      consulta = consulta_com_cidade()
      tupla = tuple([params[key] for key in params])
      resultado = cursor.execute(consulta, tupla)
    
    hoteis = []
    for linha in resultado.fetchall():
      hoteis.append({
			'id': linha[0],
			'nome': linha[1],
			'estrelas': linha[2],
			'valor_diaria': linha[3],
			'cidade': linha[4]
		},)
    return {'hoteis': hoteis}

class Hotel(Resource):
  argumentos = reqparse.RequestParser()
  argumentos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left empty")
  argumentos.add_argument('estrelas')
  argumentos.add_argument('valor_diaria')
  argumentos.add_argument('cidade', type=str, required=True, help="The field 'cidade' cannot be left empty")
  argumentos.add_argument('site_id', type=int, required=True, help="The field 'site_id' cannot be left empty")
  
  def get(self, id):
    hotel = HotelModel.find_hotel(id)
    if hotel is not None:
      return {'hotel': hotel.json()}
    
    return {'message': 'Hotel not found'}, 404
  
  @jwt_required()
  def post(self, id):
    if HotelModel.find_hotel(id):
      return {'message': f'Hotel id {id} already exists'}, 400
    
    dados = Hotel.argumentos.parse_args()

    if SiteModel.find_id(dados['site_id']) is None:
       return {'message': f'Site id {id} not exists'}, 400 

    novo_hotel = HotelModel(id, **dados)

    try:
      novo_hotel.save_hotel()
    except:
      return {'message': 'An internal error ocurred trying to save hotel'}, 500

    return {'message': 'successfully created new hotel'}, 201
  
  @jwt_required()
  def put(self, id):
    hotel = HotelModel.find_hotel(id)
    if hotel is None:
      return {'message': 'Hotel not found'}, 404
    
    dados = Hotel.argumentos.parse_args()
    hotel.update_hotel(**dados)
    
    try:
      hotel.save_hotel()
    except:
      return {'message': 'An internal error ocurred trying to update hotel'}, 500

    return {'hotel': hotel.json()}, 200
  
  @jwt_required()
  def delete(self, id):
    hotel = HotelModel.find_hotel(id)
    if hotel is None:
      return {'message': 'Hotel not found'}, 404
    
    try:
      hotel.deleted()
    except:
      return {'message': 'An internal error ocurred trying to delete hotel'}, 500
    
    return {'message': 'successfully deleted hotel'}, 200


