from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models import user, show

#Template Views
@app.route('/') # login page
def index(): 
    return render_template("index.html")

@app.route('/shows') # dashboard view
def rides(): 
    this_user = user.User.get_user(session['user_id'])
    all_shows = show.Show.get_all()
    return render_template("shows.html", this_user=this_user, all_shows=all_shows)

#Header Methods
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

#Login Page Methods (index.html)
@app.route('/register', methods=["POST"])
def register(): 
    is_valid = user.User.valid_reg(request.form)
    if not is_valid: 
        return redirect('/')
    else: 
        session['user_id'] = user.User.save_user(request.form)
        return redirect ('/shows')
    
@app.route('/login', methods=["POST"])
def login(): 
    is_valid = user.User.valid_login(request.form)
    if not is_valid: 
        return redirect('/')
    else: 
        session['user_id'] = user.User.get_userid(request.form)
        return redirect ('/shows')