from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_restful import Api, Resource
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()


class Apartment(db.Model, SerializerMixin):
    __tablename__ = 'apartments'

    serialize_rules = ('-lease.apartment',)

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)

    lease = db.relationship('Lease', back_populates='apartment')


class Tenant(db.Model, SerializerMixin):
    __tablename__ = 'tenants'

    serialize_rules = ('-lease.tenant',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)

    @validates('age')
    def validate_age(self, key, age):
        if age < 18:
            raise ValueError('Must be 18 or older.')
        return age

    lease = db.relationship('Lease', back_populates='tenant')


class Lease(db.Model, SerializerMixin):
    __tablename__ = 'leases'

    serialize_rules = ('-tenant.lease', '-apartment.lease',)

    id = db.Column(db.Integer, primary_key=True)
    rent = db.Column(db.Integer)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'))
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments.id'))

    apartment = db.relationship('Apartment', back_populates='lease')
    tenant = db.relationship('Tenant', back_populates='lease')
