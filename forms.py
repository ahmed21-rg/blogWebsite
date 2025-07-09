from wtforms import StringField,validators,EmailField,PasswordField,SubmitField,BooleanField
from wtforms.validators import Email,DataRequired,length,EqualTo,ValidationError
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm
from models import Users  

from flask_login import LoginManager

class RegisterationForm(FlaskForm):
    username = StringField(
        'username', validators=[DataRequired(),length(min=2, max=14)]
        )
    
    Email = StringField(
        'Email', validators=[DataRequired(),Email()]
    )
    password = PasswordField('password',
            validators=[DataRequired()])


    confirm_password = PasswordField(
        'confirm_password', validators=[DataRequired(), EqualTo('password', message= 'password must match')]
    )
    submit = SubmitField('Sign up')
    
    remember = BooleanField('Rembember Me?')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Name is alredy taken please try a different one!')

    def validate_Email(self, email):
        user = Users.query.filter_by(Email=Email.data).first()
        if user:
            raise ValidationError('Email is alredy taken please try a different one!')

class loginform(FlaskForm):
    Email = StringField(
        'Email', validators=[DataRequired(), Email()])


    password = PasswordField(
        'password', validators=[DataRequired()])

    remember = BooleanField('Rembember Me?')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField(
        'username', validators=[DataRequired(),length(min=2, max=14)]
        )
    
    Email = StringField(
        'Email', validators=[DataRequired(),Email()]
    )
    picture = FileField('update your profile picture', FileAllowed(['jpg', 'png']))
    submit = SubmitField('update')
    

    def validate_username(self, username):
        if username != current_user.username:
            user = Users.query.filter_by(username=username).first()
            if user:
                raise ValidationError('Name is alredy taken please try a different one!')

    def validate_Email(self, email):
        if Email != current_user:
            user = Users.query.filter_by(Email=Email).first()
            if user:
                raise ValidationError('Email is alredy taken please try a different one!')
