def normalize_path_params(cidade=None,
    estrela_min=0, estrela_max=5, diaria_min=0,
    diaria_max=100000, limit=10, offset=0):
    default_params = {
        'estrela_min': estrela_min,
        'estrela_max': estrela_max,
        'diaria_min': diaria_min,
        'diaria_max': diaria_max,
    }

    if cidade:
      default_params['cidade'] = cidade

    default_params['limit'] = limit
    default_params['offset'] = offset

    return default_params

def consulta_sem_cidade():
   return '''SELECT * FROM hoteis
      WHERE (estrelas >= ? and estrelas <= ?)
      and (valor_diaria >= ? and valor_diaria <= ?)
      LIMIT ? OFFSET ?'''

def consulta_com_cidade():
   return '''SELECT * FROM hoteis
      WHERE (estrelas >= ? and estrelas <= ?)
      and (valor_diaria >= ? and valor_diaria <= ?)
      and cidade = ? LIMIT ? OFFSET ?'''