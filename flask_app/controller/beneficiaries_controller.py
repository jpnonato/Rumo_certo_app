from flask import jsonify
from bson import ObjectId
from app.model import Beneficiary
from app.controller import collections
from app.services import get_items_data, verify_request_data, verify_update_sent_data_request, get_data_by_id, clean_deleted_data_inside_other_collectios, update_data_inside_other_collectios


beneficiary_collection = collections.get("beneficiaries") 

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

