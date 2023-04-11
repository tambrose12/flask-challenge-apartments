from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Apartment, Tenant, Lease

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///apartments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Home(Resource):
    def get(self):
        response_dict = {'message': 'Hello!!!'}

        response = make_response(response_dict, 200,)

        return response


api.add_resource(Home, '/')


class Apartments(Resource):
    def get(self):
        apartments = [a.to_dict() for a in Apartment.query.all()]

        return make_response(apartments, 200)

    def post(self):
        data = request.get_json()
        new_apartment = Apartment(number=data['number'])

        db.session.add(new_apartment)
        db.session.commit()

        response_dict = new_apartment.to_dict()
        response = make_response(response_dict, 201)
        return response


api.add_resource(Apartments, '/apartments')


class ApartmentsById(Resource):
    def get(self, id):
        apartment = Apartment.query.filter_by(id=id).first().to_dict()
        response = make_response(apartment, 200,)

        return response

    def patch(self, id):
        data = request.form
        apartment = Apartment.query.filter_by(id=id).first()
        for attr in data:
            setattr(apartment, attr, data[attr])
        db.session.add(apartment)
        db.session.commit()

        response_dict = apartment.to_dict()

        response = make_response(
            response_dict,
            200
        )

        return response

    def delete(self, id):
        apartment = Apartment.query.filter_by(id=id).first()
        db.session.delete(apartment)
        db.session.commit()


api.add_resource(ApartmentsById, '/apartments/<int:id>')


class Tenants(Resource):
    def get(self):
        tenants = [t.to_dict() for t in Tenant.query.all()]
        return make_response(tenants, 200)

    def post(self):
        data = request.get_json()
        new_tenant = Tenant(name=data['name'], age=data['age'])

        db.session.add(new_tenant)
        db.session.commit()

        response_dict = new_tenant.to_dict()
        response = make_response(response_dict, 201)
        return response


api.add_resource(Tenants, '/tenants')


class TenantsById(Resource):
    def get(self, id):
        tenant = Tenant.query.filter_by(id=id).first().to_dict()

        response = make_response(tenant, 200)
        return response

    def patch(self, id):
        data = request.get_json()
        tenant = Tenant.query.filter_by(id=id).first()
        for attr in data:
            setattr(tenant, attr, data[attr])

        db.session.add(tenant)
        db.session.commit()

        response_dict = tenant.to_dict()

        response = make_response(
            response_dict,
            200
        )

        return response

    def delete(self, id):
        tenant = Tenant.query.filter_by(id=id).first()
        db.session.delete(tenant)
        db.session.commit()


api.add_resource(TenantsById, '/tenants/<int:id>')


class Leases(Resource):
    def get(self):
        leases = [l.to_dict() for l in Lease.query.all()]
        response = make_response(leases, 200)
        return response

    def post(self):
        data = request.get_json()
        new_lease = Lease(
            rent=data['rent'], tenant_id=data['tenant_id'], apartment_id=data['apartment_id'])

        db.session.add(new_lease)
        db.session.commit()

        new_lease_dict = new_lease.to_dict()

        response = make_response(new_lease_dict, 201)
        return response


api.add_resource(Leases, '/leases')


class LeasesById(Resource):
    def get(self, id):
        lease = Lease.query.filter_by(id=id).first().to_dict()
        response = make_response(lease, 200)
        return response

    def delete(self, id):
        lease = Lease.query.filter_by(id=id).first()
        db.session.delete(lease)
        db.session.commit()

        response = make_response('Lease Deleted', 201)
        return response


api.add_resource(LeasesById, '/leases/<int:id>')

if __name__ == '__main__':
    app.run(port=3000, debug=True)
