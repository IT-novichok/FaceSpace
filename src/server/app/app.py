from flask import Flask, render_template, redirect, abort, jsonify, request
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from .forms import *
from .api import user_api
from secrets import token_urlsafe
from .data import db, User, Advertisement, Category
from .services import user_service, advertisement_service, category_service
from .errors import DataFormatError

host = '127.0.0.1'
secret_key = token_urlsafe(32)
port = 8080
app = Flask(__name__)
login_manager = LoginManager()


@app.route('/')
def main():
    advertisements = advertisement_service.get_all_advertisements()
    categories = category_service.get_all_categories()
    return render_template('main.html', title='FaceSpace', advertisements=advertisements, categories=categories)


@app.route('/categories/<name>')
def categories(name: str):
    selected_category = category_service.get_category_by_name(name)
    advertisements = selected_category.advertisements
    categories = category_service.get_all_categories()
    return render_template('main.html', title=selected_category.name.capitalize(),
                           categories=categories,
                           selected_category=selected_category, advertisements=advertisements)


@app.route('/profile')
def profile():
    if not current_user.is_authenticated:
        return redirect('/login')
    else:
        return render_template('profile.html', title='Profile', user=current_user)


@app.route('/users/<name>')
def user(name: str):
    user = user_service.get_user_by_name(name)
    if not user:
        return abort(404)
    elif current_user.is_authenticated:
        if user.id == current_user.id:
            return redirect('/profile')
    else:
        return render_template('profile.html', title=f"{user.name}'s profile", user=user)


@app.route('/find', methods=['GET', 'POST'])
def find():
    if not current_user.is_authenticated:
        return redirect('/login')
    categories = list(map(lambda x: x.name.capitalize(), category_service.get_all_categories()))
    form = AdvertisementForm(categories)
    if form.validate_on_submit():
        data = {
            'publisher_id': current_user.id,
            'cover': form.cover_data.data,
            'title': form.title.data,
            'content': form.content.data,
            'category_id': category_service.get_category_by_name(form.category.data.lower()).id,
        }
        try:
            advertisement_service.create_advertisement(data)
        except DataFormatError as e:
            return render_template('find.html', title='Find', form=form, message=str(e))
        return redirect('/')
    return render_template('find.html', title='Find', form=form)


@app.route('/advertisements/<int:id>/edit', methods=['GET', 'POST'])
def advertisement_edit(id):
    advertisement = advertisement_service.get_advertisement(id)
    if not advertisement:
        return abort(404)
    elif current_user.id != advertisement.publisher_id:
        return abort(403)
    else:
        form = AdvertisementForm(list(map(lambda x: x.name, category_service.get_all_categories())), 'Save changes')
        form.cover_data.data = advertisement.cover,
        form.title.data = advertisement.title
        form.content.data = advertisement.content
        form.category.data = advertisement.category.name
        if form.validate_on_submit():
            data = {
                'publisher_id': current_user.id,
                'cover': form.cover_data.data[0],
                'title': form.title.data,
                'content': form.content.data,
                'category_id': category_service.get_category_by_name(form.category.data.lower()).id,
            }
            try:
                advertisement_service.update_advertisement(id, data)
            except DataFormatError as e:
                return render_template('advertisement_edit.html', title='Edit advertisement', form=form, message=str(e))
            return redirect(f'/advertisements/{id}')
        return render_template('advertisement_edit.html', title='Edit advertisement', form=form)


@app.route('/advertisements/<int:id>')
def advertisements(id: int):
    advertisement = advertisement_service.get_advertisement(id)
    if not advertisement:
        return abort(404)
    else:
        return render_template('advertisement.html', title=advertisement.title, advertisement=advertisement, similar=[])


@app.route('/advertisements/<int:id>/delete')
@login_required
def delete_advertisement(id: int):
    advertisement = advertisement_service.get_advertisement(id)
    if not advertisement:
        return abort(404)
    elif current_user.id != advertisement.publisher_id:
        return abort(403)
    else:
        advertisement_service.delete_advertisement(id)
        return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="The passwords don't match!")
        data = {
            'name': form.name.data,
            'nickname': form.nickname.data,
            'email': form.email.data,
            'birth_date': form.birth_date.data,
            'gender': form.gender.data,
            'password': form.password.data,
        }
        try:
            user_service.create_user(data)
            login_user(user)
        except DataFormatError as e:
            return render_template('register.html', title='Registration', form=form,
                                   message=str(e))
        return redirect('/')
    return render_template('register.html', title='Register Form', form=form)


@login_manager.user_loader
def load_user(id: int):
    return user_service.get_user(id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = user_service.get_user_by_email(form.email.data)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Invalid login or password",
                               form=form)
    return render_template('login.html', title='Log in', form=form)


@app.errorhandler(404)
def not_found(error):
    print(error)
    return render_template('error.html', message='Not found', status_code=404), 404


@app.errorhandler(403)
def forbidden(error):
    return render_template('error.html', message='Forbidden', status_code=403), 403


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
