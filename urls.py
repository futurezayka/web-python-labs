from app import app, db
from db import User
from flask import request, redirect, url_for, render_template
from repository import *
from form import *
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=['post', 'get'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username == 
                                             form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['get', 'post'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User()
        user.name = form.name.data
        user.username = form.username.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route("/author", methods=['get'])
def getAuthors():
    return render_template('entityTable.html', entities=AuthorRepository.read_all())

@app.route("/author/<id>", methods=['get'])
def getAuthor(id):
    entity = AuthorRepository.read(id)
    if entity is not None:
        return render_template('entity.html', entity=entity)
    return redirect(url_for('getAuthors'))

@app.route("/author/create", methods=['get', 'post'])
@login_required
def createAuthor():
    form = AuthorCreationForm()
    if form.validate_on_submit():
        name = form.name.data
        pseudonym = form.pseudonym.data
        id = AuthorRepository.create(name, pseudonym)
        return redirect(url_for('getAuthor', id=id))
    return render_template('entityCreation.html', form=form)

@app.route('/author/edit/<id>', methods=['get', 'post'])
@login_required
def editAuthor(id):
    entity = AuthorRepository.read(id)
    if entity is not None:
        form = AuthorCreationForm(obj=entity)
        if form.validate_on_submit():
            name = form.name.data
            pseudonym = form.pseudonym.data
            AuthorRepository.update(id, name, pseudonym)
            return redirect(url_for('getAuthor', id=id))
        return render_template('entityCreation.html', form=form)
    return redirect(url_for('getAuthors'))

@app.route('/author/delete/<id>', methods=['get', 'post'])
@login_required
def deleteAuthor(id):
    AuthorRepository.delete(id)
    return redirect(url_for('getAuthors'))

@app.route("/book", methods=['get'])
def getBooks():
    return render_template('entityTable.html', entities=BookRepository.read_all())

@app.route("/book/<id>", methods=['get'])
def getBook(id):
    entity = BookRepository.read(id)
    if entity is not None:
        genres = entity.genres
        return render_template('entity.html', entity=entity, genres=genres)
    return redirect(url_for('getBooks'))

@app.route("/book/create", methods=['get', 'post'])
@login_required
def createBook():
    form = BookCreationForm()
    form.author_id.choices = [(a.id, a.name) for a in AuthorRepository.read_all()]
    form.genres.choices = [(g.id, g.name) for g in GenreRepository.read_all()]
    if form.validate_on_submit():
        name = form.name.data
        page = form.page.data
        year = form.year.data
        genres = GenreRepository.read_by_ids(form.genres.data)
        author_id = form.author_id.data
        id = BookRepository.create(name, page, year, genres, author_id)
        return redirect(url_for('getBook', id=id))
    return render_template('entityCreation.html', form=form)

@app.route('/book/edit/<id>', methods=['get', 'post'])
@login_required
def editBook(id):
    entity = BookRepository.read(id)
    if entity is not None:
        form = BookCreationForm()
        form.author_id.choices = [(a.id, a.name) for a in AuthorRepository.read_all()]
        form.genres.choices = [(g.id, g.name) for g in GenreRepository.read_all()]
        form = BookCreationForm(obj=entity)
        form.genres.data = [g.id for g in entity.genres]
        if form.validate_on_submit():
            name = form.name.data
            page = form.page.data
            year = form.year.data
            genres = GenreRepository.read_by_ids(form.genres.data)
            author_id = form.author_id.data
            BookRepository.create(id, name, page, year, genres, author_id)
            return redirect(url_for('getBook', id=id))
        return render_template('entityCreation.html', form=form)
    return redirect(url_for('getBooks'))

@app.route('/book/delete/<id>', methods=['get', 'post'])
@login_required
def deleteBook(id):
    BookRepository.delete(id)
    return redirect(url_for('getBooks'))

@app.route("/genre", methods=['get'])
def getGenres():
    return render_template('entityTable.html', entities=GenreRepository.read_all())

@app.route("/genre/<id>", methods=['get'])
def getGenre(id):
    entity = GenreRepository.read(id)
    if entity is not None:
        return render_template('entity.html', entity=entity)
    return redirect(url_for('getGenres'))

@app.route("/genre/create", methods=['get', 'post'])
@login_required
def createGenre():
    form = GenreCreationForm()
    if form.validate_on_submit():
        name = form.name.data
        id = GenreRepository.create(name)
        return redirect(url_for('getGenre', id=id))
    return render_template('entityCreation.html', form=form)

@app.route('/genre/edit/<id>', methods=['get', 'post'])
@login_required
def editGenre(id):
    entity = GenreRepository.read(id)
    if entity is not None:
        form = GenreCreationForm(obj=entity)
        if form.validate_on_submit():
            name = form.name.data
            GenreRepository.update(id, name)
            return redirect(url_for('getGenre', id=id))
        return render_template('entityCreation.html', form=form)
    return redirect(url_for('getGenres'))

@app.route('/genre/delete/<id>', methods=['get', 'post'])
@login_required
def deleteGenre(id):
    GenreRepository.delete(id)
    return redirect(url_for('getGenres'))