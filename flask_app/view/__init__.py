from .post_views import post_routes
from .get_views import get_routes 
from .patch_views import patch_routes
from .delete_views import delete_routes

def init_app(app):
    post_routes(app)
    get_routes(app)
    patch_routes(app)
    delete_routes(app)