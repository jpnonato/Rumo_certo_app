from flask import request

from .controller import delete_activity, delete_beneficiary, delete_volunteer, delete_admin


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
