from flask import Flask
from application.models import db, User,Role
from application.config import DevelopmentConfig
from flask_security.core import Security
from application.sec import datastore
def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app=app)
    app.security = Security(app,datastore=datastore) # type: ignore
    with app.app_context():
        import application.views
        db.create_all()




    return app
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)