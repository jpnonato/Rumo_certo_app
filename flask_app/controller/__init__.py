import os
#import urllib.parse
from pymongo import MongoClient
from dotenv import load_dotenv

from app.services.default_content import default_content_data

load_dotenv()
# DB_USER = urllib.parse.quote_plus(os.getenv('DB_USER'))
# PASSWORD = urllib.parse.quote_plus(os.getenv('PASSWORD'))
# STR_CONNECTION = os.getenv('DB_STR_CONNECTION').format(DB_USER, PASSWORD)
STR_CONNECTION = os.getenv('DB_STR_CONNECTION')
client = MongoClient(STR_CONNECTION)

db = client['RumoCerto']
db_collections = db.list_collection_names()
app_collections = ['Admins', 'Voluntarios', 'Atividades', 'Beneficiados', 'Doacoes', 'Conteudo']

if db_collections != app_collections:
    for collection_name in app_collections:
        if collection_name not in db_collections:
            db.create_collection(collection_name)
            if collection_name  == 'Conteudo':
                db[collection_name].insert_one(default_content_data)

admin_collection = db.get_collection('Admins')
donation_collection = db.get_collection('Doacoes')
activity_collection = db.get_collection('Atividades')
volunteer_collection = db.get_collection('Voluntarios')
page_content_collection = db.get_collection('Conteudo')
beneficiary_collection = db.get_collection('Beneficiados')

collections = {
    'admins': admin_collection,
    'donations': donation_collection,
    'activities': activity_collection,
    'volunteers': volunteer_collection,
    'page_content': page_content_collection, 
    'beneficiaries': beneficiary_collection
}

DEFAULT_ADMIN_MAIL= os.getenv('DEFAULT_ADMIN_MAIL')
DEFAULT_ADMIN_PASSWORD= os.getenv('DEFAULT_ADMIN_PASSWORD')

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
