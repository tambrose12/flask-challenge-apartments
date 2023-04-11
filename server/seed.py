from random import choice as rc, randint


from app import app
from models import db, Apartment, Tenant, Lease

if __name__ == '__main__':
    with app.app_context():
        # a1 = Apartment(number=1)
        # t1 = Tenant(name='Bob', age=25)
        # l1 = Lease(rent=2000, tenant_id=1, apartment_id=1)
        # db.session.add(a1)
        # db.session.add(t1)
        # db.session.add(l1)
        # a2 = Apartment(number=2)
        # t2 = Tenant(name='Larry', age=19)
        # l2 = Lease(rent=1500, tenant_id=2, apartment_id=2)
        # db.session.add(a2)
        # db.session.add(t2)
        # db.session.add(l2)
        # db.session.commit()

        a3 = Apartment(number=3)
        a4 = Apartment(number=4)
        a9 = Apartment(number=9)
        t9 = Tenant(name='Nick', age=30)
        l9 = Lease(rent=1700, tenant_id=5, apartment_id=5)
        apartments = [a3, a4, a9, t9, l9]
        db.session.add_all(apartments)
        db.session.commit()
