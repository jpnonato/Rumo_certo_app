
from datetime import datetime

class Activity():
    def __init__(self, **kwargs):
        self.nome = kwargs['nome'].title()
        self.dia = kwargs['dia'].title()
        self.horario = kwargs['horario']
        self.voluntarios = [kwargs['voluntario']]
        self.beneficiados = [kwargs['beneficiado']] if kwargs['beneficiado'] else []
        self.vagas = kwargs['vagas'] if kwargs['vagas'].isnumeric() else 'ilimitadas'
        self.imagem = kwargs['imagem']
        self.texto = kwargs['texto']
        self.ultima_atualizacao = datetime.now().strftime('%d/%m/%Y - %H:%M')
    

    @staticmethod
    def verify_new_activity_data(data: dict):
        available_keys = ['nome', 'horario', 'dia', 'voluntario', 'vagas', 'beneficiado', 'imagem', 'texto']

        data_keys = data.keys()

        if len(data_keys) < 8:
            return f'há campos faltantes no corpo da requisição.'

        wrong_keys = [key for key in data_keys if key not in available_keys]

        if wrong_keys:
            return f'Campos incorretos inseridos na requisição: {wrong_keys}'
        
        none_values = {key for key in data if not data[key] and key not in ['imagem', 'texto', 'beneficiado', 'dia']}

        if none_values:
            return f'Foi atribuido um valor nulo nas seguintes propriedades: {none_values}'
        
        wrong_values = {key for key in data if type(data[key]) is not str and type(data[key]) is not list and type(data[key]) is not int }

        if wrong_values:
            return f'Valores incorretos foram atribuidos as seguintes propriedades: {wrong_values}'
        pass


    @staticmethod
    def verify_if_exist_Activity_data(name, activities_data):
        db_activities_list = [x.get('nome') for x in activities_data]

        if name.title() in db_activities_list:
            return 'Já existe uma Atividade registrada com este nome!'