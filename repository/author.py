from app import app, db
from db import Author
from .base import BaseRepository

class AuthorRepository(BaseRepository):

    @staticmethod
    def create(entityName, entityPseudonym):
        entity = Author(name=entityName, pseudonym=entityPseudonym)
        return BaseRepository.create(entity)
        
    
    @staticmethod
    def read(id):
        return db.session.query(Author).get(id)
    
    @staticmethod
    def read_all():
        return db.session.query(Author).all()
    
    @staticmethod
    def update(id, entityName, entityPseudonym):
        entity = AuthorRepository.read(id)
        entity.name = entityName
        entity.pseudonym = entityPseudonym
        return BaseRepository.update(entity)

    @staticmethod
    def delete(id):
        entity = AuthorRepository.read(id)
        BaseRepository.delete(entity)