from app import app, db

class BaseRepository:

    @staticmethod
    def create(entity):
        db.session.add(entity)
        db.session.commit()
        return entity.id
    
    @staticmethod
    def read(id):
        return
    
    @staticmethod
    def read_all():
        return
    
    @staticmethod
    def update(entity):
        db.session.add(entity)
        db.session.commit()
        return entity.id

    @staticmethod
    def delete(entity):
        db.session.delete(entity)
        db.session.commit()