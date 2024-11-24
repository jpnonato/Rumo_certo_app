from flask import request

from .controller import insert_new_beneficiary, insert_new_admin, insert_new_volunteer, insert_new_activity, signin_user


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

    @app.post('/beneficiary')
    def register_new_beneficiary():
        data = request.get_json()
        return insert_new_beneficiary(data)
