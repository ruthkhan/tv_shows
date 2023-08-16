from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models import show, user, like

# Render template views
@app.route('/shows/new') # page to request new show
def new(): 
    this_user = user.User.get_user(session['user_id'])
    return render_template("new.html", this_user=this_user)

@app.route('/shows/edit/<int:id>') # page to update show details
def edit_show(id): 
    this_show = show.Show.get_one(id)
    this_user = user.User.get_user(session['user_id'])
    return render_template("edit.html", this_show=this_show, this_user=this_user)

@app.route('/shows/<int:id>') # detailed show page
def view_ride(id): 
    this_show = show.Show.get_one(id)
    this_show.release_date = this_show.release_date.strftime("%B %d %Y")
    this_user = user.User.get_user(session['user_id'])
    like_count = like.Like.count_likes(this_show.likes)
    return render_template("details.html", this_show=this_show, this_user=this_user, like_count=like_count)

#Routes from shows page (shows.html)
@app.route('/delete/<int:id>')
def del_show(id): 
    show.Show.delete(id)
    return redirect('/shows')

#Routes from new show page (new.html)
@app.route('/add', methods=["POST"])
def add_ride(): 
    #validate entries 
    is_valid = show.Show.validate_show(request.form)
    if not is_valid: 
        return redirect('/shows/new')
    else: 
        new_show = show.Show.save_show(request.form)
        return redirect('/shows')

#Routes from edit show page (edit.html)
@app.route('/edit_show', methods=["POST"])
def edit(): 
    #validate entries 
    is_valid = show.Show.validate_show(request.form)
    id = request.form['id']
    if not is_valid: 
        return redirect(f'/shows/edit/{id}')
    else: 
        show.Show.update_show(request.form)
        return redirect('/shows')