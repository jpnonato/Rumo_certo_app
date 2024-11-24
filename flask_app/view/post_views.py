from flask import request
from app.controller import signin_user
from app.controller.activity_controller import insert_new_activity

from app.controller.beneficiaries_controller import insert_new_beneficiary
from app.controller.Admins_controller import insert_new_admin
from app.controller.volunteers_controller import insert_new_volunteer
from app.controller.donations_controller import insert_new_donation


def post_routes(app):

    @app.post('/login')
    def check_user_credentials_to_signin():
        data = request.get_json()
        return signin_user(data)
    
    @app.post('/admin')
    def register_admin():
        data = request.get_json()
        return insert_new_admin(data)
    
    @app.post('/volunteer')
    def register_volunteer():
        data = request.get_json()
        return insert_new_volunteer(data)
    
    @app.post('/activity')
    def register_new_activity():
        data = request.get_json()
        return insert_new_activity(data)
    
    @app.post('/donation')
    def register_new_donation():
        data = request.get_json()
        return insert_new_donation(data)

    @app.post('/beneficiary')
    def register_new_beneficiary():
        data = request.get_json()
        return insert_new_beneficiary(data)
