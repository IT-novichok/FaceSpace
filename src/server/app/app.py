from flask import Flask, render_template, redirect, make_response, jsonify, request
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from forms import *
from api import user_api
from secrets import token_urlsafe
from data import db, User, Advertisement
from src.server.app.data import Category
from src.server.app.forms.find_form import FindForm

host = '127.0.0.1'
secret_key = token_urlsafe(32)
port = 8080
app = Flask(__name__)
login_manager = LoginManager()


@app.route('/')
def main():
    return render_template('main.html', title='FaceSpace',
                           categories=[category.name for category in db.session.query(Category).all()],
                           advertisments=db.session.query(Advertisement).all())


@app.route('/categories/<category>')
def categories(category):
    return render_template('main.html', title=category.capitalize(),
                           categories=[category.name for category in db.session.query(Category).all()],
                           selected_category=category, advertisments=[])


@app.route('/profile')
def profile():
    if not current_user.is_authenticated:
        return redirect('/login')
    else:
        return render_template('profile.html', title='Profile', profile=current_user.get_profile())


@app.route('/users/<string:name>')
def user(name: str):
    user = db.session.query(User).filter(User.name == name).one_or_none()
    if not user:
        return make_response(jsonify({'message': 'Not found'}), 404)
    elif user == current_user:
        return redirect('/profile')
    else:
        return render_template('profile.html', title='Profile', profile=user.get_profile())


@app.route('/find', methods=['GET', 'POST'])
def find():
    if not current_user.is_authenticated:
        return redirect('/login')
    form = FindForm([category.name for category in db.session.query(Category).all()])
    if form.validate_on_submit():
        advertisement = Advertisement()
        advertisement.publisher = current_user.id
        advertisement.content = form.content.data
        advertisement.category = form.category.data
        advertisement.tags = form.tags.data
        return redirect('/')
    return render_template('find.html', title='Find', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register Form',
                                   form=form,
                                   message="The passwords don't match!")
        if not form.name.data.replace('_', '').isalnum():
            return render_template('register.html', title='Register From',
                                   form=form,
                                   message="The name should contain Latin letters in any case, numbers and the _ symbol")
        elif db.session.query(User).filter(User.email == form.email.data).first():
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
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    return render_template('register.html', title='Register Form', form=form)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Invalid login or password",
                               form=form)
    return render_template('login.html', title='Log in', form=form)


@app.errorhandler(404)
def not_found(error):
    print('Error')
    return render_template('error.html', message='Not found', status_code=404), 404


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def init():
    app.config['SECRET_KEY'] = secret_key
    login_manager.init_app(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../data/db/global_data.db"
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.register_blueprint(user_api.blueprint)


def run():
    app.run(host, port, debug=True)


if __name__ == '__main__':
    init()
    run()
