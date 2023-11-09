from flask import Blueprint, Response, g, request
from app.route_guard import auth_required, special_auth_required

from app.search.model import *
from app.search.schema import *
from app.user.model import User
from helpers.langchain import do_search
from helpers.sms import send_sms

bp = Blueprint('search', __name__)

@bp.post('/search')
@special_auth_required()
def create_search():
    shortcode = request.form.get("to")
    question = request.form.get('text')
    history = Search.get_latest_by_user_id(g.user.id)
    answer = do_search(question, g.user.language, history)
    send_sms([g.user.phone], answer, sender=shortcode)
    return Response(status=200)

@bp.post('/sms')
# @auth_required()
def initiate_search():
    location = request.json.get("location")
    shortcode = request.json.get("shortcode")
    message = request.json.get('message')
    users = User.get_by_location(location)
    send_sms([user.phone for user in users], message, sender=shortcode)
    return {'message': 'Message sent successfully!'}, 200

@bp.get('/search/<int:id>')
@auth_required()
def get_search(id):
    search = Search.get_by_id(id)
    if search is None:
        return {'message': 'Search not found'}, 404
    return SearchSchema().dump(search), 200

@bp.patch('/search/<int:id>')
@auth_required()
def update_search(id):
    search = Search.get_by_id(id)
    if search is None:
        return {'message': 'Search not found'}, 404
    search.update()
    return SearchSchema().dump(search), 200

@bp.delete('/search/<int:id>')
@auth_required()
def delete_search(id):
    search = Search.get_by_id(id)
    if search is None:
        return {'message': 'Search not found'}, 404
    search.delete()
    return {'message': 'Search deleted successfully'}, 200

@bp.get('/searchs')
@auth_required()
def get_searchs():
    searchs = Search.get_all()
    return SearchSchema(many=True).dump(searchs), 200