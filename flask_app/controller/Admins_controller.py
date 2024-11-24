from bson import ObjectId
from flask import jsonify
from app.model import Admin
from app.controller import admin_collection
from app.services import get_data_by_id, get_items_data, update_time_data, verify_request_data, verify_update_sent_data_request, verify_user_email


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
