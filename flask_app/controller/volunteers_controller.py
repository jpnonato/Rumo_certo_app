from flask import jsonify
from bson import ObjectId
from app.model import Volunteer
from app.controller import volunteer_collection
from app.controller import collections
from app.services import verify_user_email, verify_request_data, verify_update_sent_data_request, clean_deleted_data_inside_other_collectios, get_data_by_id, get_items_data, update_data_inside_other_collectios


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
