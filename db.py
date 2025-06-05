from app import db, app, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin

class Author(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    pseudonym = db.Column(db.String(255), nullable=False)
    books = db.relationship('Book', backref='author', cascade='all, delete-orphan')

    def __repr__(self):
        return  "<{}, {}>".format(id, self.pseudonym)
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

book_genre = db.Table('book_genre',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id', ondelete="CASCADE")),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id', ondelete="CASCADE"))
)

class Book(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    pages = db.Column(db.Integer(), nullable=False)
    year = db.Column(db.Integer(), nullable=False)
    genres = db.relationship('Genre', secondary=book_genre, backref='books')
    author_id = db.Column(db.Integer(), db.ForeignKey('author.id'))

    def __repr__(self):
        return  "<{}, {}, {}>".format(id, self.title, self.year)
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Genre(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return  "<{}, {}>".format(id, self.name)
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)


    def __repr__(self):
        return  "<{}, {}>".format(id, self.username)
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)

def init_db():
    with app.app_context():
        db.create_all()