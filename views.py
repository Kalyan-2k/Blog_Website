from flask import Blueprint,render_template,request,flash,redirect,url_for,session
from models import Post,User,Comment,Like
from datetime import datetime
import codecs


views =Blueprint("views",__name__)


@views.route("/")
@views.route("/root")
def root():
    return render_template("base.html")

@views.route("/home")
def home():
    try:
        user=User.objects(username=session["username"]).first()
                #print(type(posts))  # o/p :<class 'mongoengine.queryset.queryset.QuerySet'>
        
        user_data=dict()
        post_data=list()
        for post in Post.objects().as_pymongo().order_by("-date_created"):
            post_data.append(post)

        user_data['id']=user.id
        user_data["username"]=user.username
        user_data["email"]=user.email
        user_data["date"]=user.date_created
        return render_template("home.html",user=user_data,posts=post_data)
    except Exception as e:
        print(e)
        flash('Cannot enter this page without proper login credentials','error')
        return redirect(url_for('views.root'))
    
    

@views.route("/create-post",methods=['GET','POST'])
def create_post():
    
    if request.method=="POST":
        title=request.form.get("title")
        text = request.form.get("text")
        tags = request.form.get("tags")
        tags=tags.split(" ")
        tags=[x.lower() for x in tags]
        print(tags)
        post=Post(title=title,text=text, author=session["username"],tags=tags)
        post.save()
        if not text:
            flash('Post cannot be empty',category='error')
        else:
            flash('post created !!!',category='success')
    return render_template("create_post.html",user=session["username"])


@views.route("/delete-post/<id>")
def delete_post(id):
    
    post=Post.objects(id=id).as_pymongo()
    if not post:
        flash("Post doesn't exists",category='error')
    elif session["username"] != post[0]['author']:
        flash("You do not have permission to delete this post.",category='error')
    else:
        post.delete()
        flash('post deleted successfully !!!',category='success')

    return redirect(url_for('views.home'))



@views.route("/profile")
# @login_required
def profile():  # user profile page
    try:
        user=User.objects(username=session["username"]).first()
        user_data=dict()
        user_data["id"]=str(user.id)
        user_data["username"]=user.username
        user_data["email"]=user.email
        user_data["date"]=user.date_created
        
        if not user:
            flash('No User exists with that name',category='error')
            return redirect(url_for('views.home'))
        
        post_data=list()
        
        for post in Post.objects().as_pymongo().order_by("-date_created"):
            if post['author'] == session["username"]:
                post_data.append(post)
        try:
            base64_image=codecs.encode(user.profile_img.read(),'base64')            # encding the byte like object to base64 byte object
            image = base64_image.decode('utf-8')                                    # decoding the base64 byte object using utf-8 series to base64 string 
            return render_template("profile.html",user=user_data,posts=post_data,image=image)
        
        except Exception as e:
            print("cannot display image" ,e)
        
        return render_template("profile.html",user=user_data,posts=post_data)
    except Exception as e:
        flash('Cannot enter this page without proper login credentials','error')
        return redirect(url_for('views.root'))


@views.route("/create-comment/<post_id>",methods=["POST"])
def create_comment(post_id):

    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.',category='error')
    else:
        post=Post.objects(id=post_id).get()
        comment=Comment(author=session["username"],content=text,date_created=datetime.now())
        post.comments.append(comment)
        post.save()
        return redirect(url_for('views.home'))


@views.route("/delete-comment/<post_id>/<comment_content>")
def delete_comment(post_id,comment_content):

    post=Post.objects(id=post_id).get()

    for comment in post.comments:
        
        if comment.content == comment_content:
            post.comments.remove(comment)
            post.save()
            flash('Comment deleted successfully !!!','success')
            break

    return redirect(url_for('views.home'))


@views.route("/profile-pic",methods=["POST"])
def profile_pic():

    if "profile_pic" in request.files:

        profile_pic=request.files['profile_pic']
        user=User.objects(username=session["username"]).first()
        user.profile_img.replace(profile_pic,filename=profile_pic.filename, content_type = profile_pic.content_type)  
        user.save()
    else:
        flash("please select a photo to upload","error")    
    return redirect(url_for('views.profile'))


@views.route("/like-post/<post_id>",methods=["GET"])
def like(post_id):
    
    post = Post.objects(id=post_id).get()
    like=""
    
    for doc in post.likes:
        if doc.author == session["username"]:
            like=doc
            break
    
    if not post:
        flash("Post does not exist..",category="error")
    elif like:
        post.likes.remove(like)
        post.save()
    else:
        like=Like(author=session["username"])
        post.likes.append(like)
        post.save()

    return redirect(url_for("views.home"))


@views.route("/profile/<username>",methods=["GET"])
def user_page(username):
    
    user=User.objects(username=username).first()
    user_data=dict()
    user_data["id"]=str(user.id)
    user_data["username"]=user.username
    user_data["email"]=user.email
    user_data["date"]=user.date_created
    
    if not user:
        flash('No User exists with that name',category='error')
        return redirect(url_for('views.home'))
    
    post_data=list()
    
    for post in Post.objects().as_pymongo().order_by("-date_created"):
        if post['author'] ==user_data["username"]:
            post_data.append(post)
    
    try:
        base64_image=codecs.encode(user.profile_img.read(),'base64')                    # encding the byte like object to base64 byte object
        image = base64_image.decode('utf-8')                                            # decoding the base64 byte object using utf-8 series to base64 string 
        return render_template("profile.html",user=user_data,posts=post_data,image=image)
    
    except Exception as e:
        print("cannot display image" ,e)
    
    return render_template("profile.html",user=user_data,posts=post_data)


@views.route("/search",methods=['POST'])
def search():
    if request.method=='POST':
        
        tags=request.form.get("search")
        tags=tags.lower()
        print(tags)
        if tags is None:
            flash('No tags were mentioned in search box','error')
        
        elif Post.objects(tags=tags).count() == 0:
            flash('No Posts with such tags exist','error')

        else:
            post_data=[]
            user_data=dict()
            try:
                user=User.objects(username=session["username"]).first()
                user_data['id']=user.id
                user_data["username"]=user.username
                user_data["email"]=user.email
                user_data["date"]=user.date_created
                for post in Post.objects(tags=tags).as_pymongo():
                    post_data.append(post)
                return render_template("posts.html",user=user_data,posts=post_data)
            except Exception as e:
                print("cannot load the page ",e)
        return redirect(url_for('views.home'))

