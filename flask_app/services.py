from datetime import datetime
from bson import ObjectId


def verify_user_email(email, collection_data):

    user_list = [user for user in collection_data]

    for user in user_list:
        if user.get("email") == email:
            return 'Email já cadastrado!'
        

def get_items_data(data_collection):

    data_list = [data for data in data_collection]

    for index, elt in enumerate(data_list):
        data_list[index] = {key: elt[key] if key != '_id' else str(elt[key]) for key in elt}
    
    return data_list


def get_data_by_id(item_id, collection):
    
    try:
        data_id = ObjectId(item_id)
    except:
        return

    item = collection.find_one({'_id': data_id})

    if item:
        item['_id'] = item_id

        return item


def get_user_by_email(email, collection):

    user_data = collection.find_one({'email': email})
    user = {key: user_data[key] for key in user_data if key in ['_id', 'name', 'subject']}
    user.update({'_id': str(user_data['_id'])})

    return user


def verify_update_sent_data_request(data, available_keys):
        
    wrong_properties = []
    for key in data.keys():
        if key not in available_keys:
            wrong_properties.append({key: data[key]})
    
    if wrong_properties:
        return f"Propriedade(s) invalida(s): {wrong_properties}"


def verify_request_data(request_data, collection, request_type=None):
    
    data_id = request_data.get('id')
    collection_name = collection.name

    if not data_id:
        return 'Necessário enviar a propriedade "id" e seu respectivo valor no corpo da requisição'

    if not ObjectId.is_valid(data_id):
        return 'O valor da propriedade "id" enviado não é válido!'

    if len(request_data.keys()) == 1 and request_type == 'PATCH':
        return  'Necessário enviar mais um ou mais valores para a execução desta requisição'
    
    if len(request_data.keys()) > 1 and request_type == 'DELETE':
        return  'Necessário enviar somente o id para a execução desta requisição'
    
    item_data = collection.find_one({"_id": ObjectId(data_id)})
    if not item_data:
        if collection_name not in ['Doacoes', 'Atividades']:
            return 'Usuário inexistente'
        
        if collection_name == 'Doacoes':
            return "Doação não registrada"
        
        if collection_name == 'Atividades':
            return "Atividade inexistente"


def update_data_inside_other_collectios( item_name, updated_item_name, item_collection, collections):

    updated_item_collection_name = item_collection.name
    activity_collection = collections.get('activities')

    if updated_item_collection_name == 'Voluntarios':

        for activity in activity_collection.find({}):
            
            activity_id = activity.get('_id')
            activity_volunteers = activity.get('voluntarios')

            if item_name in activity_volunteers:
                filtered_volunteers = [name for name in activity_volunteers if name != item_name]
                filtered_volunteers.append(updated_item_name)

                new_values = {"$set": {'voluntarios': filtered_volunteers}}
                activity_collection.update_one({'_id' : ObjectId(activity_id)}, new_values)

    if updated_item_collection_name == 'Beneficiados':

        for activity in activity_collection.find({}):
            
            activity_id = activity.get('_id')
            activity_beneficiaries = activity.get('beneficiados')

            if item_name in activity_beneficiaries:
                filtered_beneficiaries = [name for name in activity_beneficiaries if name != item_name]
                filtered_beneficiaries.append(updated_item_name)

                new_values = {"$set": {'beneficiados': filtered_beneficiaries}}
                activity_collection.update_one({'_id' : ObjectId(activity_id)}, new_values)
        

def clean_deleted_data_inside_other_collectios(deleted_item_name, item_collection, collections):

    deleted_item_collection_name = item_collection.name
    activity_collection = collections.get('activities')

    if deleted_item_collection_name == 'Voluntarios':

        for activity in activity_collection.find({}):
            
            activity_id = activity.get('_id')
            activity_volunteers = activity.get('voluntarios')
            if deleted_item_name in activity_volunteers:
                filtered_volunteers = [name for name in activity_volunteers if name != deleted_item_name]
                new_values = {"$set": {'voluntarios': filtered_volunteers}}
                activity_collection.update_one({'_id' : ObjectId(activity_id)}, new_values)

    if deleted_item_collection_name == 'Beneficiados':

        for activity in activity_collection.find({}):
            
            activity_id = activity.get('_id')
            activity_beneficiaries = activity.get('beneficiados')

            if deleted_item_name in activity_beneficiaries:
                filtered_beneficiaries = [id for id in activity_beneficiaries if id != deleted_item_name]
                new_values = {"$set": {'beneficiados': filtered_beneficiaries}}
                activity_collection.update_one({'_id' : ObjectId(activity_id)}, new_values)


def update_time_data():

    now_datetime = datetime.now().strftime("%d/%m/%Y - %H:%M")
    return now_datetime



default_content_data = {
    "text_1": "O Projeto Rumo Certo nasceu há 16 anos para cuidar de pessoas, e assim transformar nossa comunidade. Desde então, seguimos nossa missão de impactar vidas através de cursos profissionalizantes, atividades físicas, cursos e atendimento psicológico, nutricional e jurídico.",
    "text_2": "A partir da percepção das necessidades da população de BH e grande BH, foi criado o Projeto Rumo Certo. Com um pouco mais de 3 meses de atuação, passou a ser reconhecido pela população, que enxergou, no projeto, uma oportunidade de aperfeiçoamento profissional e um acolhimento humanitário para as necessidades sociais e psicológicas. Os atendimentos de assistência jurídica, psicológica foram ampliados e foi implantada uma extensa grade de cursos profissionalizantes.",
    "text_3": "xxxxxxxxxxxxxxx",
    "doacao_estatisticas": {
        "entregas": 222, 
        "beneficiados": 0, 
        "projetos": 0, 
        "voluntários": 0
    },
    "doacao_data_info": {
        "projectName": "Projeto Rumo Certo",
        "cnpj": "10238963000181", 
        "banco": "xxxxxx", 
        "agencia": "xxx",
        "conta": "xxxxxx", 
        "chave_pix":"xxxxxx",
        "telefone": "(31) 3142-3136", 
        "email": "asbd.bh@gmail.com"
    },
    "depoimentos": [],
    "footer_texto": {
        "telefone": "(31) 3142-3136",
        "emial": "Gmail@ProjetoRumoCerto.com.br",
        "endereco": "Rua João Magela Luz, 15 - Bairro Céu Azul"
    },
    "carrossel_data_info": {
        'URL1': '/slideimage1.png', 
        'URL2': '/slideimage2.png', 
        'URL3': '/slideimage3.png'
        }
}
