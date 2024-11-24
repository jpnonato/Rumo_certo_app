from flask import jsonify
from app.controller import collections
from app.services.default_content import default_content_data


activity_collection = collections.get("activities") 
content_collection = collections.get("page_content")
voluntary_collection = collections.get("volunteers") 
beneficiary_collection = collections.get("beneficiaries")
available_content_data_keys = default_content_data.keys()

def get_available_page_content():
    content_data = content_collection.find_one({})

    if content_data:

        data_id = content_data.get('_id')
        for key in available_content_data_keys:
            
            text = content_data.get(key)
            if not text:

               content_data.update({key: default_content_data.get(key)})
               content_collection.update_one({'_id': data_id}, {"$set": content_data}) 

    else:
        content_data = default_content_data

    content_data = {k: content_data[k] for k in available_content_data_keys if k != "_id"}

    beneficiaries_number = len(list(beneficiary_collection.find({})))
    voluntaries_number = len(list(voluntary_collection.find({})))

    # statistic_data = { 
    #     'beneficiados': beneficiaries_number,
    #     'voluntarios': voluntaries_number,
    # }
    
    content_data['doacao_estatisticas']['beneficiados'] =  beneficiaries_number
    content_data['doacao_estatisticas']['voluntarios'] =  voluntaries_number

    return jsonify(content_data), 200


def update_page_content(data):
    current_page_content = content_collection.find_one({})
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
        content_collection.update_one({'_id': content_id}, {"$set": current_page_content})

    return 'requisição processada com sucesso!', 200
