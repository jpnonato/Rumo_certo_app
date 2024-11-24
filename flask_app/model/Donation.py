
class Donation:
    def __init__(self, **kwargs):

        self.nome = kwargs['nome']
        self.beneficiados = []
        
    @staticmethod
    def verify_new_donation_data(data: dict):
        available_keys = ['nome']

        data_keys = data.keys()

        if len(data_keys) < 1:
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
        pass


    @staticmethod
    def verify_if_exist_donation_data(name, donations_data):
        db_donations_list = [x.get('nome') for x in donations_data]
        
        if name in db_donations_list:
            return 'Já existe uma doação registrada com este nome!'
