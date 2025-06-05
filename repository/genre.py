from app import app, db
from db import Genre
from .base import BaseRepository

class GenreRepository(BaseRepository):

    @staticmethod
    def create(entityName):
        entity = Genre(name=entityName)
        return BaseRepository.create(entity)
        
    
    @staticmethod
    def read(id):
        return db.session.query(Genre).get(id)
    
    @staticmethod
    def read_by_ids(ids):
        return Genre.query.filter(Genre.id.in_(ids)).all()
    
    @staticmethod
    def read_all():
        return db.session.query(Genre).all()
    
    @staticmethod
    def update(id, entityName):
        entity = GenreRepository.read(id)
        entity.name = entityName
        return BaseRepository.update(entity)

    @staticmethod
    def delete(id):
        entity = GenreRepository.read(id)
        BaseRepository.delete(entity)