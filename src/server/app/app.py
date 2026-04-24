from flask import Flask, url_for, render_template, redirect
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from forms import *
from data import *
from data import db_session
from api import user_api
from secrets import token_urlsafe

host = '127.0.0.1'
secret_key = token_urlsafe(32)
port = 8080
app = Flask(__name__)
login_manager = LoginManager()


@app.route('/')
def main():
    return render_template('main.html', title='FaceSpace', categories=['friend', 'buisness'])


@app.route('/categories/<category>')
def categories(category):
    return render_template('main.html', title='FaceSpace', categories=['friend', 'buisness'],
                           selected_category=category)


@app.route('/profile')
def profile():
    if not current_user:
        return redirect('/login')
    else:
        return render_template('profile.html', title='Profile', profile={'name': 'username', 'nickname': 'User',
                                                                         'about': 'There some info about user...'})


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register Form',
                                   form=form,
                                   message="The passwords don't match!")
        session = db_session.create_session()
        if not form.name.data.replace('_', '').isalnum():
            return render_template('register.html', title='Register From',
                                   form=form,
                                   message="The name should contain Latin letters in any case, numbers and the _ symbol")
        elif session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register From',
                                   form=form,
                                   message="This login already exists!")
        user = User(
            name=form.name.data,
            nickname=form.nickname.data,
            email=form.email.data,
            birth_date=form.birth_date.data,
            gender=form.gender.data,
            about=form.about.data,
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/')
    return render_template('register.html', title='Register Form', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Invalid login or password",
                               form=form)
    return render_template('login.html', title='Log in', form=form)


def init():
    app.config['SECRET_KEY'] = secret_key
    login_manager.init_app(app)
    db_session.global_init('database/global_data.db')
    app.register_blueprint(user_api.blueprint)


def run():
    app.run(host, port, debug=True)


if __name__ == '__main__':
    init()
    run()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")
