from app import app, db
from db import Book
from .base import BaseRepository

class BookRepository(BaseRepository):

    @staticmethod
    def create(entityName, entityPage, entityYear, 
               entityGenres, entityAuthorID):
        entity = Book(name=entityName, pages=entityPage, 
                      year=entityYear, genres=entityGenres, 
                      author_id=entityAuthorID)
        return BaseRepository.create(entity)
        
    @staticmethod
    def read(id):
        return db.session.query(Book).get(id)
    
    @staticmethod
    def read_all():
        return db.session.query(Book).all()
    
    @staticmethod
    def update(id, entityName, entityPage, entityYear, 
               entityGenres, entityAuthorID):
        entity = BookRepository.read(id)
        entity.name = entityName
        entity.pages = entityPage
        entity.year = entityYear
        entity.genres = entityGenres
        entity.author_id = entityAuthorID
        return BaseRepository.update(entity)

    @staticmethod
    def delete(id):
        entity = BookRepository.read(id)
        BaseRepository.delete(entity)