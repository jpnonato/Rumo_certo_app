from flask import request

from .controller import update_activity, update_volunteer, update_admin, update_beneficiary, update_page_content


def patch_routes(app):
    
    @app.patch('/activity')
    def patch_activity():
        data = request.get_json()
        return update_activity(data)
    
    @app.patch('/volunteer')
    def patch_volunteer():
        data=request.get_json()
        return update_volunteer(data)
    
    @app.patch('/admin')
    def update_admin_route():
        data = request.get_json()
        return update_admin(data)

    @app.patch('/beneficiary')
    def patch_beneficiary():
        data = request.get_json()
        return update_beneficiary(data)
    
    @app.patch('/page_content')
    def patch_page_content():
        data = request.get_json()
        return update_page_content(data)
