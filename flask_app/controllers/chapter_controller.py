from flask_app import app
from flask_app.models.chapter_model import Chapter
from flask_app.models.anime_model import Anime
from flask import render_template, redirect, request, session, flash

@app.route('/show_add_chapter')
def add_chapter():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('chapter.html')

# @app.route('/add_chapter/<int:id>', methods=['POST'])
# def add_chapter(id):
#     if 'user_id' not in session:
#         return redirect('/logout')
#     if not Chapter.validate_chapter(request.form):
#         return redirect('/chapter')
#     data={
#         "chapter_title": request.form['chapter_title'],
#         "story": request.form['story'],
#         "anime_id": id,
#     }
#     chapter = Chapter.save(data)
#     return redirect("/welcome")
