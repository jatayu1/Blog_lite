from blog import db, login_manager
from blog import bcrypt
from flask_login import UserMixin
import datetime
from sqlalchemy import DateTime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

followers = db.Table( "follower",
    db.Column('follower_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer(), db.ForeignKey('user.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    fullname = db.Column(db.String(length=30), nullable=False)
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    email = db.Column(db.String(length=50), nullable=False)
    profilePicture = db.Column(db.String(length=50), nullable=True, default='default-profile-pic.jpg')
    password_hash = db.Column(db.String(length=60), nullable=False)
    posts_created = db.relationship('Post', backref='author')
    followed = db.relationship('User', 
                               secondary=followers, 
                               primaryjoin=(followers.c.follower_id == id), 
                               secondaryjoin=(followers.c.followed_id == id), 
                               backref=db.backref('followers', lazy='dynamic'), 
                               lazy='dynamic')

    def follow(self, users):
        if not self.is_following(users):
            self.followed.append(users)
            return self

    def unfollow(self, users):
        if self.is_following(users):
            self.followed.remove(users)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0
        
    def PostCount(self):
        return len(list(self.posts_created))

    def followedPosts(self):
        return Post.query.join(followers, (followers.c.followed_id == Post.created_by)).filter(followers.c.follower_id == self.id).order_by(Post.post_timestamp.desc())

    def myPosts(self):
        return Post.query.join(User, (self.id == Post.created_by)).order_by(Post.post_timestamp.desc())

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, normal_password):
        self.password_hash = bcrypt.generate_password_hash(normal_password).decode('utf-8')

    def passwordCheck(self, givenPassword):
        return bcrypt.check_password_hash(self.password_hash, givenPassword)

class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    created_by = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    post_title = db.Column(db.String(), nullable=False)
    post_text = db.Column(db.String(), nullable=False)
    post_timestamp = db.Column(DateTime, default=datetime.datetime.utcnow)
    posts_media = db.relationship('Media', backref='post')
    

class Media(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'), nullable=False)
    photo = db.Column(db.String(), unique=True, nullable=False)