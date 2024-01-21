from main import app
from application.sec import datastore
from application.models import db,Role
from flask_security.utils import hash_password
from werkzeug.security import generate_password_hash,check_password_hash
with app.app_context():
    db.create_all()
    datastore.find_or_create_role(name='admin',description='User is an admin')
    datastore.find_or_create_role(name='creator',description='Creator is a creator')
    datastore.find_or_create_role(name='user',description='Uusser is an user')
#! The above lines create roles in the roles table
    db.session.commit()
    if not datastore.find_user(username='admin'):
        datastore.create_user(username='admin',password='admin',roles=['admin'])
    if not datastore.find_user(username='creator1'):
        datastore.create_user(username='creator1',password='manager1',roles=['creator'],active=True)
    if not datastore.find_user(username='user1'):
        datastore.create_user(username='user1',password='user',roles=['user'])
    db.session.commit()
#! The above lines create users in the user table
