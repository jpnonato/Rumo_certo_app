from flask import request

from app.controller.activity_controller import delete_activity
from app.controller.beneficiaries_controller import delete_beneficiary
from app.controller.volunteers_controller import delete_volunteer
from app.controller.Admins_controller import delete_admin
from app.controller.donations_controller import delete_donation


def delete_routes(app):
    
    @app.delete('/activity')
    def remove_activity():
        data = request.get_json()
        return delete_activity(data)
    
    @app.delete('/beneficiary')
    def remove_benefited():
        data = request.get_json()
        return delete_beneficiary(data)

    @app.delete('/volunteer')
    def remove_volunteer():
        data = request.get_json()
        return delete_volunteer(data)
    
    @app.delete('/admin')
    def delete_admin_route():
        data = request.get_json()
        return delete_admin(data)

    @app.delete('/donation')
    def remove_donation():
        data = request.get_json()
        return delete_donation(data)
