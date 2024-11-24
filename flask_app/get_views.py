from flask import request

from .controller import get_available_activities, get_available_activity, get_available_page_content, get_available_admins, get_avaliable_admin, get_available_beneficiaries, get_available_beneficiary, get_available_volunteers, get_available_volunteer


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