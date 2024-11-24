from datetime import datetime

class Volunteer():
    def __init__(self, **kwargs):
        self.nome = kwargs['nome'].title()
        self.email = kwargs['email']
        self.telefone = kwargs['telefone']
        self.senha = kwargs["senha"]
        self.data_registro = datetime.now().strftime("%d/%m/%Y - %H:%M")

    @staticmethod
    def verify_new_volunteer_data(data: dict):

            available_keys = ['nome', 'email','telefone', 'senha']

            data_keys = data.keys()

            if len(data_keys) < 4:
                return f'há campos faltantes no corpo da requisição.'

            wrong_keys = [key for key in data_keys if key not in available_keys]

            if wrong_keys:
                return f'Campos incorretos inseridos na requisição: {wrong_keys}'
            
            none_values = {key for key in data if not data[key]}

            if none_values:
                return f'Foi atribuido um valor nulo nas seguintes propriedades: {none_values}'
            
            wrong_values = none_values = {key for key in data if type(data[key]) is not str and type(data[key]) is not list }

            if wrong_values:
                return f'Valores incorretos foram atribuidos as seguintes propriedades: {none_values}'