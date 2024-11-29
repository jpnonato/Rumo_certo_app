from flask import jsonify
from bson import ObjectId
from pymongo import MongoClient

from .services import default_content_data, get_items_data, verify_request_data, verify_update_sent_data_request, update_time_data, get_data_by_id, verify_user_email, clean_deleted_data_inside_other_collectios, update_data_inside_other_collectios
from .model import Activity, Beneficiary, Volunteer, Admin


STR_CONNECTION = 'mongodb+srv://rumo-certo-133787:CM3gc8S1mN0wJ9MJ@rumo-certo-teste.5xwz3.mongodb.net/?retryWrites=true&w=majority&appName=rumo-certo-teste'
client = MongoClient(STR_CONNECTION)

db = client['RumoCerto']
db_collections = db.list_collection_names()
app_collections = ['Admins', 'Voluntarios', 'Atividades', 'Beneficiados', 'Conteudo']

if db_collections != app_collections:
    for collection_name in app_collections:
        if collection_name not in db_collections:
            db.create_collection(collection_name)
            if collection_name  == 'Conteudo':
                db[collection_name].insert_one(default_content_data)

admin_collection = db.get_collection('Admins')
activity_collection = db.get_collection('Atividades')
volunteer_collection = db.get_collection('Voluntarios')
page_content_collection = db.get_collection('Conteudo')
beneficiary_collection = db.get_collection('Beneficiados')

collections = {
    'admins': admin_collection,
    'activities': activity_collection,
    'volunteers': volunteer_collection,
    'page_content': page_content_collection, 
    'beneficiaries': beneficiary_collection
}

available_content_data_keys = default_content_data.keys()

DEFAULT_ADMIN_MAIL= 'admin_default@mail.com.br'
DEFAULT_ADMIN_PASSWORD= '0123'

if DEFAULT_ADMIN_MAIL and DEFAULT_ADMIN_PASSWORD:
    default_admin = {
        'nome': 'default_admin',
        'email': DEFAULT_ADMIN_MAIL , 
        'senha': DEFAULT_ADMIN_PASSWORD
        
    }
    admin = admin_collection.find_one({'email': DEFAULT_ADMIN_MAIL})
    if not admin:
        admin_collection.insert_one(default_admin)


def signin_user(data):
    email = data.get('email')
    password = data.get('senha')

    if not email or not password:
        return 'Necessário enviar email e senha do usuário!', 404
    
    for collection in [admin_collection, volunteer_collection]:

        user = collection.find_one({'email': email})

        if not user:
            continue
        
        if user.get('senha') == password:
            user_level = 1

            if collection.name == 'Voluntarios':
                user_level += 1

            elif collection.name == 'Admins':
                user_level += 2

            user_info = {
                'user_level': str(user_level),
                'name': user.get('name')
            }

            return user_info, 200
        
        else:
            return 'Senha incorreta', 400 

    return 'Usuário não registrado!', 400


##Activity
def insert_new_activity(data):

    is_wrong_data = Activity.verify_new_activity_data(data)  
    if is_wrong_data: 
        return is_wrong_data, 400

    volunteers_data = data.get('voluntario')
    for volunteer_name in volunteers_data:
        is_registered_volunteer = volunteer_collection.find_one({'nome': volunteer_name})
        if not is_registered_volunteer:
            return "Voluntário não registrado!", 400
        
    activities_data = activity_collection.find({})
    is_inexistent_data = Activity.verify_if_exist_Activity_data(data.get('nome'), activities_data)
    
    if is_inexistent_data: 
        return is_inexistent_data, 400  

    new_activity = Activity(**data).__dict__
    activity_collection.insert_one(new_activity)

    return 'Nova Atividade registrada com sucesso!', 201


def get_available_activities():

    activity_list = get_items_data(activity_collection.find({}))
    return jsonify(activity_list), 200


def  get_available_activity(data):

    wrong_request_data = verify_request_data(data, activity_collection)
    if wrong_request_data:
        return wrong_request_data, 400
    
    activity_profile = get_data_by_id(data.get('id'), activity_collection)
    return jsonify(activity_profile), 200


def update_activity(data: dict):
    wrong_data_request = verify_request_data(data, activity_collection, 'PATCH')
    if wrong_data_request: 
        return wrong_data_request, 400

    Activity_id = data.get('id')
    available_activity_keys = ['nome', 'horario', 'voluntarios', 'beneficiados', 'vagas',  'imagem', 'texto', 'id']

    wrong_properties = verify_update_sent_data_request(data, available_activity_keys)
    if wrong_properties:
        return wrong_properties, 400

    if data.get('voluntario'):
        volunteers_data = data.get('voluntario')
        volunteer_list = []

        for new_volunteer_name in volunteers_data:
            if not volunteer_collection.find_one({'nome': new_volunteer_name.title()}):
                return "Não existe voluntário registrado com este nome!", 409

            volunteer_list.append(new_volunteer_name.title())

        data.update({'voluntarios': volunteer_list})    


    beneficiary_list = []
    if data.get('beneficiado'):

        beneficiaries_data = [name for name in data.get('beneficiado') if name]
        if len(beneficiaries_data) > 0:

            for new_beneficiary_name in beneficiaries_data:
                if not beneficiary_collection.find_one({'nome': new_beneficiary_name.title()}):
                    return "Beneficiado inexistente!", 400

                beneficiary_list.append(new_beneficiary_name.title())
                    
        data.update({'beneficiados': beneficiary_list})

    if data.get('vagas'):
        if data.get('vagas').isnumeric():

            new_vacancy = int(data.get('vagas')) 
            if new_vacancy == 0:
                return "Numero de vagas informado deve ser maior que zero!", 400
            
            beneficiaries_number = len(beneficiary_list)
            new_number_of_vacancy = new_vacancy - beneficiaries_number

            if new_number_of_vacancy < 0:
                return "Limite de vagas foi ultrapassado!", 400

        else:
            data.update({'vagas': 'ilimitadas'})
    
    handle_keys = ['id']
    update_data = {key: data[key] for key in data.keys() if key not in handle_keys}
    
    if update_data:
        update_data['ultima_atualizacao'] = update_time_data()
        new_values = {"$set": update_data}
        activity_collection.update_one({'_id': ObjectId(Activity_id )}, new_values)
    
    return "Atividade atualizada!", 200


def delete_activity(data):

    wrong_data_request = verify_request_data(data, activity_collection, 'DELETE')
    if wrong_data_request: 
        return wrong_data_request, 400
    
    activity_id = data.get('id')
    activity_collection.delete_one({"_id": ObjectId(activity_id) })

    return 'Atividade deletada com sucesso!', 200


##Admin
def insert_new_admin(data: dict):

    is_wrong_data = Admin.verify_new_admin_data(data)

    if is_wrong_data: 
        return is_wrong_data, 400

    is_same_email = verify_user_email(data["email"], admin_collection.find({}))

    if is_same_email: 
        return is_same_email, 409

    new_Admin = Admin(**data)
    admin_collection.insert_one(new_Admin.__dict__)

    return 'Novo Administrador registrado com sucesso!', 201


def get_avaliable_admin(data):
  
    wrong_request_data = verify_request_data(data, admin_collection)
    if wrong_request_data:
        return wrong_request_data, 400

    admin_profile = get_data_by_id(data.get('id'), admin_collection)

    return jsonify(admin_profile), 200


def get_available_admins():
    
    admin_profiles = get_items_data(admin_collection.find({}))

    return jsonify(admin_profiles), 200


def update_admin(data):
    wrong_data_request = verify_request_data(data, admin_collection, 'PATCH')
    if wrong_data_request: 
        return wrong_data_request, 400
      
    admin_id = data.get('id')
    available_keys = ['id', 'nome', 'email', 'senha']

    wrong_properties = verify_update_sent_data_request(data, available_keys)
    if wrong_properties:
        return wrong_properties, 400
    
    admin = admin_collection.find_one({'_id': ObjectId(admin_id)})
    if not admin:
        return "Administrador não encontrado!", 404
    
    update_data = {key: data[key] for key in data.keys() if key in available_keys and key != 'id'}

    if update_data:
        update_data['ultima_atualizacao'] = update_time_data()
        admin_collection.update_one({'_id': ObjectId(admin_id)}, {"$set": update_data})

    return "Administrador(a) atualizado(a) com sucesso!", 200

  
def delete_admin(data):

    wrong_data_request = verify_request_data(data, admin_collection, 'DELETE')
    if wrong_data_request: 
        return wrong_data_request, 400
    
    admin_id = data.get('id')
    admin_collection.delete_one({"_id": ObjectId(admin_id) })

    return 'Administrador(a) deletado(a) com sucesso!', 200


##Benefiary
def get_available_beneficiaries():

    beneficiaries_list = get_items_data(beneficiary_collection.find({}))
    return jsonify(beneficiaries_list), 200


def  get_available_beneficiary(data):

    wrong_request_data = verify_request_data(data, beneficiary_collection)
    if wrong_request_data:
        return wrong_request_data, 400
    
    beneficiary_profile = get_data_by_id(data.get('id'), beneficiary_collection)

    return jsonify(beneficiary_profile), 200


def insert_new_beneficiary(data):

    is_wrong_data = Beneficiary.verify_new_beneficiary_data(data)  
    if is_wrong_data: 
        return is_wrong_data, 400
   
    beneficiary_data = beneficiary_collection.find({})
    is_inexistent_data = Beneficiary.verify_if_exist_beneficiary_data(data.get('cpf'), beneficiary_data)
    
    if is_inexistent_data: 
        return is_inexistent_data, 400  

    new_beneficiary = Beneficiary(**data).__dict__
    beneficiary_collection.insert_one(new_beneficiary)

    return 'Novo Beneficiário registrado com sucesso!', 201


def update_beneficiary(data):
    wrong_data_request = verify_request_data(data, beneficiary_collection, 'PATCH')
    if wrong_data_request: 
        return wrong_data_request, 400
    
    beneficiary_id = data.get('id')
    available_keys = ['nome', 'telefone', 'cpf', 'endereco', 'id', 'data_nascimento']

    wrong_properties = verify_update_sent_data_request(data, available_keys)
    if wrong_properties:
        return wrong_properties, 400

    beneficiary = beneficiary_collection.find_one({"_id": ObjectId(beneficiary_id)})

    if not beneficiary:
        return "Beneficiado não encontrado!", 404
    
    update_data = {key: data[key] for key in data.keys() if key != 'id'}

    if update_data:
        
        if update_data.get('nome'):
            new_beneficiary_name = update_data.get('nome').title()
            update_data['nome'] = new_beneficiary_name

            beneficiary_name = beneficiary.get('nome')
            update_data_inside_other_collectios(beneficiary_name, new_beneficiary_name, beneficiary_collection, collections)

        new_values = {"$set": update_data}
        beneficiary_collection.update_one({'_id': ObjectId(beneficiary_id)}, new_values)

    return "Perfil de beneficiado atualizado!", 200


def delete_beneficiary(data):

    wrong_data_request = verify_request_data(data, beneficiary_collection, 'DELETE')
    if wrong_data_request: 
        return wrong_data_request, 400
    
    beneficiary_id = data.get('id')
    beneficiary_name = get_data_by_id(data.get('id'), beneficiary_collection).get('nome')
    
    beneficiary_collection.delete_one({"_id": ObjectId(beneficiary_id) })
    clean_deleted_data_inside_other_collectios(beneficiary_name, beneficiary_collection, collections) 
    
    return 'Atividade deletada com sucesso!', 200


##Page_content
def get_available_page_content():
    content_data = page_content_collection.find_one({})

    if content_data:

        data_id = content_data.get('_id')
        for key in available_content_data_keys:
            
            text = content_data.get(key)
            if not text:

               content_data.update({key: default_content_data.get(key)})
               page_content_collection.update_one({'_id': data_id}, {"$set": content_data}) 

    else:
        content_data = default_content_data

    content_data = {k: content_data[k] for k in available_content_data_keys if k != "_id"}

    beneficiaries_number = len(list(beneficiary_collection.find({})))
    voluntaries_number = len(list(volunteer_collection.find({})))
    
    content_data['doacao_estatisticas']['beneficiados'] =  beneficiaries_number
    content_data['doacao_estatisticas']['voluntarios'] =  voluntaries_number

    return jsonify(content_data), 200


def update_page_content(data):
    current_page_content = page_content_collection.find_one({})
    available_keys = [key for key in current_page_content.keys() if key != '_id']

    if not data:
        return 'Necessário enviar um ou mais parâmetros para esta requisição', 401
    
    if not data.keys():
        return 'Necessário enviar um ou mais parâmetros para esta requisição', 400
    
    updated_properties = []
    for key in data:
        if key not in available_keys:
            return f'Parâmetro {key} não é permitido', 400
        
        if current_page_content[key] != data.get(key):
            updated_properties.append(key)
            current_page_content[key] = data.get(key)
    
    if len(updated_properties) > 0:
        content_id = current_page_content.get('_id')
        page_content_collection.update_one({'_id': content_id}, {"$set": current_page_content})

    return 'requisição processada com sucesso!', 200


##Volunteer
def get_available_volunteer(data):
    wrong_request_data = verify_request_data(data, volunteer_collection)
    if wrong_request_data:
        return wrong_request_data, 400
    
    volunteer_profile = get_data_by_id(data.get('id'), volunteer_collection)

    return jsonify(volunteer_profile), 200


def get_available_volunteers():
    volunteers_list = get_items_data(volunteer_collection.find({}))
    return jsonify(volunteers_list), 200


def insert_new_volunteer(data: dict):

    is_wrong_data = Volunteer.verify_new_volunteer_data(data)

    if is_wrong_data: 
        return is_wrong_data, 400

    is_same_email = verify_user_email(data["email"], volunteer_collection.find({}))

    if is_same_email: 
        return is_same_email, 409

    new_Volunteer = Volunteer(**data)
    volunteer_collection.insert_one(new_Volunteer.__dict__)

    return 'Novo Voluntário registrado com sucesso!', 201


def update_volunteer(data: dict):

    is_wrong_data = verify_request_data(data, volunteer_collection, 'PATCH')
    if is_wrong_data:
        return is_wrong_data, 400

    volunteer_id = data.get('id')
    available_activity_keys = ['nome', 'email', 'telefone', 'senha', 'id']

    wrong_properties = verify_update_sent_data_request(data, available_activity_keys)
    if wrong_properties:
        return wrong_properties, 400
    
    volunteer = volunteer_collection.find_one({"_id": ObjectId(volunteer_id)})

    if not volunteer:
        return "Voluntário não encontrado!", 404

    update_data = {key: data[key] for key in data.keys() if key != 'id'}
   
    if update_data.get('nome'):
            new_volunteer_name = update_data.get('nome').title()
            update_data['nome'] = new_volunteer_name

            volunteer_name = volunteer.get('nome')
            update_data_inside_other_collectios(volunteer_name, new_volunteer_name, volunteer_collection, collections)

    volunteer_collection.update_one({"_id": ObjectId(volunteer_id)}, {"$set": update_data})

    return 'Voluntário atualizado com sucesso!', 200


def delete_volunteer(data):

    wrong_data_request = verify_request_data(data, volunteer_collection, 'DELETE')
    if wrong_data_request: 
        return wrong_data_request, 400
    
    volunteer_id = data.get('id')
    volunteer_name = get_data_by_id(data.get('id'), volunteer_collection).get('nome')
    volunteer_collection.delete_one({"_id": ObjectId(volunteer_id) })
    clean_deleted_data_inside_other_collectios(volunteer_name, volunteer_collection, collections)

    return 'Voluntário deletada com sucesso!', 200
