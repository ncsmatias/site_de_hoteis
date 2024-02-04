from flask_restful import Resource, reqparse
from models.site_model import SiteModel

class Sites(Resource):
  def get(self):
    return {'sites': [site.json() for site in SiteModel.query.all()]}

class Site(Resource):
  argumentos = reqparse.RequestParser()
  argumentos.add_argument('url', type=str, required=True, help="The field 'url' cannot be left empty")
  argumentos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left empty")

  def get(self, nome):
    site = SiteModel.find_site(nome)
    if site:
      return site.json()
    return {'message': 'Site not foud'}, 404

  def put(self, nome):
    site = SiteModel.find_site(nome)
    if site is None:
      return {'message': 'Site not foud'}, 404

    dados = Site.argumentos.parse_args()
    site.update_site(**dados)

    try:
      site.save_site()
    except:
      return {'message': 'An internal error ocurred trying to update site'}, 500

    return {'hotel': site.json()}, 200
    
  def delete(self, nome):
    site = SiteModel.find_site(nome)
    
    if site is None:
      return {'message': 'Site not found'}, 404
    
    try:
      site.delete_site()
    except:
      return {'message': 'An internal error ocurred trying to delete site'}, 500 
    
    return {'message': 'successfully deleted site'}, 200

class NovoSite(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('url', type=str, required=True, help="The field 'url' cannot be left empty")
    argumentos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left empty")

    def post(self):
      dados = NovoSite.argumentos.parse_args()
      site = SiteModel.find_site(dados['nome'])
      if site:
        return {'message': f'The site {dados["nome"]} already exists'}, 400
      
      site_model = SiteModel(**dados)
      try:
        site_model.save_site()
      except:
        return {'message': 'An internal error ocurred trying to save site'}, 500
      
      return {'message': 'successfully created new hotel'}, 201