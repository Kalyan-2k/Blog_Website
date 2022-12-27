from mongoengine import Document,EmbeddedDocument
from mongoengine import DateTimeField, StringField, IntField,ImageField,ReferenceField,ListField,EmbeddedDocumentField,FileField
from datetime import datetime

class User(Document):   # User class is nothing but User Collection
    email = StringField(max_length=150,unique=True)
    username=StringField(max_length=150,unique=True)
    password =  StringField(max_length=150)
    date_created = DateTimeField(default=datetime.now())
    profile_img=FileField()
    meta ={"allow_inheritance":True}

class Comment(EmbeddedDocument):
    author=StringField(nullable=False)
    content=StringField()
    date_created = DateTimeField(default=datetime.now())

class Like(EmbeddedDocument):
    author=StringField(nullable=False)
    date_created = DateTimeField(default=datetime.now())

class Post(Document):
    title=StringField(nullable=False)
    text=StringField(nullable=False)
    date_created = DateTimeField(default=datetime.now())
    author=ReferenceField(User,reverse_delete_rule = 2) 
    # here 2 means "Cascade" which means to delete all posts associated with a user if the user object is deleted
    tags=ListField(StringField())
    comments=ListField(EmbeddedDocumentField(Comment))
    likes=ListField(EmbeddedDocumentField(Like))

    meta={ 'allow_inheritance' : True}



