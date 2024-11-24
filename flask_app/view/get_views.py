from flask import request
from app.controller.page_content_controller import get_available_page_content
from app.controller.activity_controller import get_available_activities, get_available_activity
from app.controller.Admins_controller import get_available_admins, get_avaliable_admin
from app.controller.donations_controller import get_available_donation, get_available_donations
from app.controller.beneficiaries_controller import get_available_beneficiaries, get_available_beneficiary
from app.controller.volunteers_controller import get_available_volunteers, get_available_volunteer

def get_routes(app):
    
    @app.get('/activities')
    def get_activities():
        return get_available_activities()

    @app.get('/activity')
    def get_activity():
        data = request.get_json()
        return get_available_activity(data)
    
    @app.get('/admin')
    def get_admin():
         data = request.get_json()
         return get_avaliable_admin(data)
    
    @app.get('/admins')
    def get_admins():
        return get_available_admins()

    @app.get('/donation')
    def get_donation():
        data = request.get_json()
        return get_available_donation(data)
    
    @app.get('/donations')
    def get_donations():
        return get_available_donations()

    @app.get('/beneficiaries')
    def get_beneficiaries():
        return get_available_beneficiaries()

    @app.get('/beneficiary')
    def get_beneficiary():
        data = request.get_json()
        return get_available_beneficiary(data)
    
    @app.get('/volunteers')
    def get_volunteers():
        return get_available_volunteers()
    
    @app.get('/volunteer')
    def get_volunteer():
        data = request.get_json()
        return get_available_volunteer(data)
    
    @app.get('/page_content')
    def get_page_content():
        return get_available_page_content()