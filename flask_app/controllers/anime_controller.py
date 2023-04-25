from flask_app import app
from werkzeug.utils import secure_filename
from flask import render_template, redirect, request, session, flash
from flask_app.models.anime_model import Anime
from flask_app.models.chapter_model import Chapter
import os
ALLOWED_EXTENSIONS = {'png','jpg','jpeg'}
UPLOAD_FOLDER = os.path.join(app.root_path,'static','images','uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/show_create_anime')
def show_create_anime():
    return render_template("create_anime.html")

def allowed_file(filename):
    return'.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/create_anime', methods=['POST'])
def create_anime():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Anime.validate_anime(request.form):
        return redirect('/show_create_anime')
    file = request.files['cover']
    if file.filename == '':
        flash('No image selected for cover', 'anime')
        return redirect('/show_create_anime')
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    data ={
        "title": request.form['title'],
        "description": request.form['description'],
        "cover": filename,
        "user_id": session['user_id']
        
    }
    anime = Anime.save(data)
    return redirect('/welcome')

@app.route('/update_anime/<int:id>', methods=['POST'])
def update_anime(id):
    if not Anime.validate_anime(request.form):
        return redirect(f'/view_anime/{id}')
    file = request.files['cover']
    if file.filename == '':
        flash('No image selected for cover', 'anime')
        return redirect(f'/view_anime/{id}')
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    data ={
        "id": id,
        "title": request.form['title'],
        "description": request.form['description'],
        "cover": filename,
        "user_id": session['user_id']
        
    }
    anime = Anime.update_anime(data)
    return redirect('/welcome')

@app.route('/view_anime/<int:id>')
def view_anime(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        "id":id
    }
    return render_template("view_anime.html", anime=Anime.get_anime_by_id(data))

@app.route('/read_anime/<int:id>')
def read_anime(id):
    data={
        "id":id
    }
    return render_template("read_anime.html", anime=Anime.get_anime_by_id(data))

@app.route('/delete/<int:id>')
def delete(id):
    Anime.delete(id)
    return redirect('/welcome')