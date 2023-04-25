from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_app.models.anime_model import Anime
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashbard():
    return render_template('dashboard.html', animes = Anime.get_all_animes())

@app.route('/show_register')
def show_register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.register_is_valid(request.form):
        return redirect('/show_register')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id

    return redirect('/show_login')

@app.route('/show_login')
def show_login():
    return render_template('login.html')

@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email","login")
        return redirect('/show_login')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/show_login')
    session['user_id'] = user.id
    return redirect('/welcome')

@app.route('/welcome')
def welcome():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template('welcome.html', user=User.get_by_id(data),animes=Anime.get_anime_by_user(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


