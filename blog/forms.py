from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, SearchField
from wtforms.validators import Length, EqualTo, Email, DataRequired

class RegisterForm(FlaskForm):
    username = StringField(label="Username : ", validators=[Length(min=1, max=30), DataRequired()])
    fullname = StringField(label="Full Name : ", validators=[Length(min=1, max=30), DataRequired()])
    email = StringField(label="Email Address : ", validators=[Email(), DataRequired()])
    password1 = PasswordField(label="Password : ", validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label="Confirm Password : ", validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label="Submit")

class userupdateForm(FlaskForm):
    username = StringField(label="Username : ", validators=[Length(min=1, max=30), DataRequired()])
    fullname = StringField(label="Full Name : ", validators=[Length(min=1, max=30), DataRequired()])
    email = StringField(label="Email Address : ", validators=[Email(), DataRequired()])
    Profile_picture = FileField(label="Upload Profile Picture :", validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField(label="Submit")

class LoginForm(FlaskForm):
    username = StringField(label="Username : ", validators=[DataRequired()])
    password = PasswordField(label="Password : ", validators=[DataRequired()])
    submit = SubmitField(label="Submit")

class postForm(FlaskForm):
    post_title = StringField(label="Post Title : ", validators=[DataRequired()])
    post_text = StringField(label="Start a post : ", validators=[DataRequired()])
    post_picture = FileField(label="Upload Picture :", validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField(label="Submit")

class searchForm(FlaskForm):
    search = SearchField(label="Search an account : ", validators=[DataRequired()])
    submit = SubmitField(label="Search")