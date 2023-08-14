from flask import redirect, request
from flask_app import app
from flask_app.models import like

@app.route('/like/<int:show_id>/<int:user_id>')
def add_like(show_id, user_id): 
    like.Like.save_like(show_id, user_id)
    return redirect('/shows')

@app.route('/unlike/<int:show_id>/<int:user_id>')
def unlike(show_id, user_id): 
    like.Like.del_like(show_id, user_id)
    return redirect('/shows')