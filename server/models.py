from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)
    signups = db.relationship('Signup', backref='activities_backref', lazy=True)

    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
    
    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)

    signups = db.relationship('Signup', backref='campers_backref', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age
        }
    
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Camper must have a name.')
        
        return name
    
    @validates('age')
    def validate_age(self, key, age):
        if age in range(8, 19):
            return age
        else:
            raise ValueError('Age must be between 8 and 18 years old.')
    
    
    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'


class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))

    camper = db.relationship('Camper', backref='signups_backref', lazy=True)
    activity = db.relationship('Activity', backref='signups_backref', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'camper_id': self.camper_id,
            'activity_id': self.activity_id
        }
    
    @validates
    def validate_time(self, key, time):
        if time in range(0, 23):
            return time
        else:
            raise ValueError()
            
    def __repr__(self):
        return f'<Signup {self.id}>'


# add any models you may need.
