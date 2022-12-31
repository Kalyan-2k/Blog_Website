from flask import Flask
from mongoengine import connect
from flask import session
import os

DB_NAME="Blog_DB"  #database name

app=Flask(__name__)
app.secret_key="sessionkey"     # for sessions
app.config['SECRET_KEY'] ="BLOGWebsite"
try:
    #db=connect(DB_NAME,host="mongodb://localhost:27017")    #  initializing the MongoDB with the flask application(app).
    db=connect(DB_NAME,host="mongodb://mongo:lFmtFO8meezMkobPl5ES@containers-us-west-183.railway.app:6304")
except ConnectionError as e:
    print("Error while connecting to the Database : "+e)

from Routes.views import views
from Routes.auth import auth

app.register_blueprint(views,url_prefix="/") 
app.register_blueprint(auth,url_prefix="/")

if __name__=="__main__":    
    app.run(debug=True,host='0.0.0.0',port=os.getenv("PORT", default=5000))
    # app.run(host='0.0.0.0')   # experiment
