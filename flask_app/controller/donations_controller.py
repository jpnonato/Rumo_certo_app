from flask import jsonify
from app.controller import collections
from app.model import Donation
from bson import ObjectId
from app.services import  get_items_data, verify_request_data, verify_update_sent_data_request, update_time_data, get_data_by_id, clean_deleted_data_inside_other_collectios


donation_collection = collections.get("donations") 
beneficiary_collection = collections.get("beneficiaries") 

def get_available_donation(data):
    wrong_request_data = verify_request_data(data, donation_collection)
    if wrong_request_data:
        return wrong_request_data, 400
    
    donation_profile = get_data_by_id(data.get('id'), donation_collection)

    return jsonify(donation_profile), 200


def get_available_donations():
    donations_list = get_items_data(donation_collection.find({}))
    return jsonify(donations_list), 200

def insert_new_donation(data):
    
    is_wrong_data = Donation.verify_new_donation_data(data)  
    if is_wrong_data: 
        return is_wrong_data, 400
    
    
    donations_data = donation_collection.find({})
    is_inexistent_data = Donation.verify_if_exist_donation_data(data.get('name'), donations_data)
    
    if is_inexistent_data: 
        return is_inexistent_data, 400  

    new_donation = Donation(**data).__dict__
    donation_collection.insert_one(new_donation)

    return 'Nova doação registrada com sucesso!', 201

def delete_donation(data):

    wrong_data_request = verify_request_data(data, donation_collection)
    if wrong_data_request: 
        return wrong_data_request, 400
    
    donation_id = data.get('id')
    donation_collection.delete_one({"_id": ObjectId(donation_id) })
    clean_deleted_data_inside_other_collectios(donation_id, donation_collection, collections)

    return 'Doação deletada com sucesso!', 200

def update_donation(data): 
    wrong_data_request = verify_request_data(data, donation_collection, 'PATCH')
    if wrong_data_request: 
        return wrong_data_request, 400
    
    donation_id = data.get('id')
    available_donation_keys = ['name','beneficiary', 'id']

    wrong_properties = verify_update_sent_data_request(data, available_donation_keys)
    if wrong_properties:
        return wrong_properties, 400

    donation = donation_collection.find_one({'_id': ObjectId(donation_id)})

    if data.get('beneficiary'):
        new_beneficiary_id = data.get('beneficiary')

        if not beneficiary_collection.find_one({'_id': ObjectId(new_beneficiary_id)}):
            return "Beneficiado inexistente!", 400

        beneficiary_list = donation.get('beneficiados')
        beneficiary_list.append(new_beneficiary_id)

        new_values = {"$set": {'beneficiados': beneficiary_list}}
        donation_collection.update_one({'_id' : ObjectId(donation_id)}, new_values)

    if data.get('name'):
        new_donation_name = data.get('name')
        if donation_collection.find_one({'nome':new_donation_name}):
            return "Já existe um registro de doação com esse nome!", 400

        new_values = {"$set": {'nome':new_donation_name }}
        donation_collection.update_one({'_id' : ObjectId(donation_id)}, new_values)
   
    return "Doação atualizada!", 200