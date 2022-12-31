from flask import Flask
from mongoengine import connect
from flask import session


DB_NAME="Blog_DB"  #database name


def create_app(host=None,debug=False):
    app=Flask(__name__)
    app.secret_key="sessionkey"     # for sessions
    app.config['SECRET_KEY'] ="BLOGWebsite"
    try:
        #db=connect(DB_NAME,host="mongodb://localhost:27017")    #  initializing the MongoDB with the flask application(app).
        db=connect(DB_NAME,host="mongodb://mongo:lFmtFO8meezMkobPl5ES@containers-us-west-183.railway.app:6304")
    except ConnectionError as e:
        print("Error while connecting to the Database : "+e)
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views,url_prefix="/") 
    app.register_blueprint(auth,url_prefix="/")

    return app

