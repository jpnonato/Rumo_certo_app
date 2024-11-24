from datetime import datetime

class Beneficiary():
    def __init__(self, **kwargs):
        self.nome = kwargs['nome'].title()
        self.cpf = kwargs['cpf']
        self.telefone = kwargs['telefone']
        self.endereco = kwargs['endereco']
        self.data_nascimento = kwargs['data_nascimento']
        self.data_registro = datetime.now().strftime("%d/%m/%Y - %H:%M")

    @staticmethod
    def verify_new_beneficiary_data(data: dict):
        available_keys = ['nome', 'cpf', 'telefone', 'endereco', 'data_nascimento']

        data_keys = data.keys()

        if len(data_keys) < 5:
            return f'há campos faltantes no corpo da requisição.'

        wrong_keys = [key for key in data_keys if key not in available_keys]

        if wrong_keys:
            return f'Campos incorretos inseridos na requisição: {wrong_keys}'
        
        none_values = {key for key in data if not data[key] and key not in ['data_nascimento']}

        if none_values:
            return f'Foi atribuido um valor nulo nas seguintes propriedades: {none_values}'
        
        wrong_values = none_values = {key for key in data if type(data[key]) is not str and type(data[key]) is not list and type(data[key]) is not int }

        if wrong_values:
            return f'Valores incorretos foram atribuidos as seguintes propriedades: {none_values}'
        pass


    @staticmethod
    def verify_if_exist_beneficiary_data(name, beneficiary_data):
        db_beneficiaries_list = [x.get('cpf') for x in beneficiary_data]
        
        if name in db_beneficiaries_list:
            return 'Já existe um beneficiado registrado com este CPF!'
