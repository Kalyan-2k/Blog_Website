from flask import Flask
from flask_login import LoginManager
from mongoengine import connect
from flask import session

""" 
SQLAlchemy is a library that facilitates the communication between Python programs and databases.
Most of the times, this library is used as an Object Relational Mapper (ORM)
tool that translates Python classes to tables on relational databases 
and automatically converts function calls to SQL statements.

"""

DB_NAME="Blog_DB"  #database name

def create_app():
    app=Flask(__name__)
    app.secret_key="sessionkey"     # for sessions
    app.config['SECRET_KEY'] ="BLOGWebsite"   # for wtf forms
    try:
        db=connect(DB_NAME,host="mongodb://localhost:27017")    #  initializing the MongoDB with the flask application(app).
    except ConnectionError as e:
        print("Error while connecting to the Database : "+e)
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views,url_prefix="/") 
    app.register_blueprint(auth,url_prefix="/")


    # from .models import User  
    
    # login_manager=LoginManager()
    # login_manager.login_view ="auth.login"
    # login_manager.init_app(app) # initializing LoginManager with the application

    # @login_manager.user_loader     # this is a decorator
    # def load_user(id):      # this function helps LoginMangaer to find the User Model
    #     return User.objects(id=ObjectId(id))
    
    return app

