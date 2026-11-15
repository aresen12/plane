import json

from flask import Flask, request, render_template, redirect
from forms.login_form import LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.user import User
from forms.register_form import RegisterForm
from data.paste import Paste
from data.plane import Plane
import sqlite3

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
hash_password = '7cb8fa366d774761d198d3dc6244740c'
port = 8080
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    rs = db_sess.get(User, user_id)
    db_sess.close()
    return rs

    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/check", methods=["POST"])
def check():
    db_sess = db_session.create_session()
    mess = db_sess.query(Paste).filter(Paste.id == request.form["id_mess"]).first()
    if mess.check_password(request.form["password"]):
        db_sess.close()
        return render_template("watching.html", message=mess, href=f"/{mess.id}")
    db_sess.close()
    return render_template("check.html", message=mess, errors=["Bad password"])
    
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            db_sess.close()
            return redirect("/")
        db_sess.close()
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)   
    
    
@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            db_sess.close()
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)
    
    
@app.route("/profile")
def profile():
    if current_user.is_authenticated:

        return render_template("profile.html", title='профиль')
    return redirect("/")
     
     
@app.route("/main", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "GET":
        return render_template("main.html", title='главная')
    else:
        db_sess = db_session.create_session()
        new_paste = Paste()
        new_paste.message = request.form["about"]
        db_sess.add(new_paste)
        if current_user.is_authenticated:
            new_paste.name_sender = current_user.name
            new_paste.id_sender = current_user.id
            db_sess.commit()
        else:
            new_paste.name_sender = "Анонимный пользователь"
        db_sess.commit()
        id_m = new_paste.id
        db_sess.close()
        return redirect(f"/{id_m}")


@app.route('/create', methods=['GET', 'POST'])
def create_event():
    return render_template("create.html")


@app.route('/new_plane', methods=['POST'])
def new_plane():
    data = request.get_json()
    db_sess = db_session.create_session()
    new_paste = Plane()
    new_paste.data = json.dumps(data["rows"])
    new_paste.title = data["title"]
    db_sess.add(new_paste)
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        new_paste.name_sender = current_user.name
        new_paste.id_sender = current_user.id
        db_sess.commit()
    else:
        new_paste.name_sender = "Анонимный пользователь"
    db_sess.commit()
    id_p = new_paste.id
    db_sess.close()
    return redirect(f"/plane/{id_p}")


@app.route('/my/<mode>', methods=['GET', 'POST'])
def my_param(mode):
    db_sess = db_session.create_session()
    res = []
    if current_user.is_authenticated:
        if mode == "plans":
            res = db_sess.query(Plane).filter(Plane.id_sender == current_user.id).all()
        else:
            res = db_sess.query(Paste).filter(Paste.id_sender == current_user.id).all()
    db_sess.close()
    return render_template("my.html", res=res, mode=mode)


@app.route("/<int:id_mess>")
def watching(id_mess):
    db_sess = db_session.create_session()
    mess = db_sess.query(Paste).filter(Paste.id == id_mess).first()
    db_sess.close()
    if mess is None:
        return redirect("/")
    if mess.secret:
        return render_template("check.html", message=mess)
    return render_template("watching.html", message=mess, href=f"/{id_mess}")


@app.route("/plane/<int:id_mess>")
def watching_plane(id_mess):
    db_sess = db_session.create_session()
    mess = db_sess.query(Plane).filter(Plane.id == id_mess).first()
    if mess is None:
        return redirect("/")
    mess.data = json.loads(mess.data)
    print(mess.data)
    db_sess.close()
    return render_template("plane.html", plane=mess, href=f"/{id_mess}")

    
if __name__ == "__main__":
    db_session.global_init('db/master_paste.db')
    app.run(host="0.0.0.0", debug=True, port=port)
