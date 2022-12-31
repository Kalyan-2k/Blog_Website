from flask import Blueprint,render_template,redirect,url_for,request,flash,session
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash


auth = Blueprint("auth",__name__)

@auth.route("/login",methods=["GET","POST"])
def login():

    if request.method=="POST":
        em=request.form.get("email")
        pwd=request.form.get("pwd")

        user=User.objects(email=em).first()
        # print(user.id)   #to print object ID of the document
        # print(type(user.id)) # o/p : <class 'bson.objectid.ObjectId'>
         
        # print(session["id"])
        
        if user is not None:
            
            if check_password_hash(user.password,pwd):
                flash("Logged In !!",category= 'success')
                session["id"]=str(user.id)     # converting objectid to string to store and use in sessions
                session["username"]=user["username"]
                session["email"]=user["email"]
                session["password"]=user["password"]
                return redirect(url_for('views.home'))

            else:
                flash('Incorrect Password.',category='error')
        else:
            flash("Email Id does not exists.",category='error')
    
    return render_template("login.html")

@auth.route("/register",methods=["GET","POST"])
def register():

    if request.method=="POST":
        
        em=request.form.get("email")
        username=request.form.get("username")
        pwd=request.form.get("pwd")
        cpwd=request.form.get("cpwd")

        email_exists=User.objects(email=em).first()                 # getting the first result if the email already exists
        username_exists=User.objects(username=username).first()
        print(username_exists)
        if email_exists is not None:
            flash("Email Already exists",category="error")
        elif username_exists is not None:
            flash("Username already in use.. please choose another one..",category ="error")    
        elif pwd!=cpwd:
            flash("Password mismatch!!",category='error')
        elif len(username) < 3:
            flash("Username is too short. Username should be 3-8 characters long",category='error')
        elif len(pwd) < 8:
            flash("Password is too short. Password should be atleast 8 characters long ",category='error')
        else:
            new_user = User(email=em,username=username,password=generate_password_hash(pwd,method='sha256'))
            new_user.save()
            flash("User successfully created.",category='success')
            return redirect(url_for('views.root'))
    
    return render_template("sign-up.html")


@auth.route("/logout")
def logout():

    try:
        if session is not None:
            session.pop("id",None)
            session.pop("username",None)
            session.pop("email",None)
            session.pop("password",None)
        else:
            flash("session is empty","error")
                
    finally:
        return redirect(url_for("views.root"))
