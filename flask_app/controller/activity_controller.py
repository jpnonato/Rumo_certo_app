from flask import jsonify
from bson import ObjectId
from app.model import Activity
from app.controller import collections
from app.services import get_items_data, verify_request_data, verify_update_sent_data_request, update_time_data, get_data_by_id


activity_collection = collections.get("activities") 
volunteer_collection = collections.get("volunteers")
beneficiary_collection = collections.get('beneficiaries') 

def insert_new_activity(data):

    is_wrong_data = Activity.verify_new_activity_data(data)  
    if is_wrong_data: 
        return is_wrong_data, 400

    is_registered_volunteer = volunteer_collection.find_one({'nome': data.get('voluntario')})
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



