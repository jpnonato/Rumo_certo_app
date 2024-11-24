from flask import request
from app.controller.activity_controller import update_activity
from app.controller.volunteers_controller import update_volunteer
from app.controller.Admins_controller import update_admin
from app.controller.donations_controller import update_donation
from app.controller.beneficiaries_controller import update_beneficiary
from app.controller.page_content_controller import update_page_content


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

    @app.patch('/donation')
    def patch_donation():
        data = request.get_json()
        return update_donation(data)

    @app.patch('/beneficiary')
    def patch_beneficiary():
        data = request.get_json()
        return update_beneficiary(data)
    
    @app.patch('/page_content')
    def patch_page_content():
        data = request.get_json()
        return update_page_content(data)
