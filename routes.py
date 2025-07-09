from forms import RegisterationForm, loginform,UpdateAccountForm  
from datetime import datetime
from flask import Flask
from flask import render_template, url_for, flash, redirect,request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,login_manager,login_user,current_user,logout_user,login_required
from flask_login import UserMixin #user authentication method
from models import db, Users, Post


print("initilazing Flask app")

app = Flask(__name__)

app.config ['SECRET_KEY'] = 'iwefuewyrewur878787458hyr84jrh48t'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:ahmed1a@127.0.0.1:3306/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db
db.init_app(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
      return Users.query.get(int(user_id))          #returns the user for that id


@app.route("/")

@app.route("/home")
def home():
      posts= [
            {
            'author' : 'mohsin nazir',
            'date_posted' : '19-04-2024',
            'title' : 'blog post 1',
            'content' : 'blog post'
      },
      {
            'author' : 'mohsin nazir',
            'date_posted' : '19-04-2024',
            'title' : 'blog post 1',
            'content' : 'blog post'
      }
      ]
      return render_template('home.html', posts=posts)

@app.route('/about')
def about():
      return render_template('about.html', title='about')

@app.route('/register', methods=['GET', 'POST'])
def register():
      if current_user.is_authenticated:
            return redirect(url_for('home'))
      form = RegisterationForm()
      if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = Users(username=form.username.data,Email=form.Email.data, password=hashed_password)

            db.session.add(user)     #this saves data in db  
            db.session.commit()

            print('form submitted successfully')
            flash(f'account created succesfully! you can now login', 'success')
            return redirect(url_for('login'))
      else:
            print('Form validation failed')
            print('Errors :', form.errors)
      return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
      if current_user.is_authenticated:
            return redirect(url_for('home'))
      form = loginform()

      if form.validate_on_submit():
            user = Users.query.filter_by(Email=form.Email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                  login_user(user, remember=form.remember.data)
                  return redirect(url_for('account'))
            else:
                  flash('login unsuccessfull. Please check Email and Password', 'danger')
      else:
            flash('login unsucessfull please login again', 'danger')
      return render_template('login.html', title=login, form=form)

@app.route('/logout')
def logout():
      logout_user()
      return redirect(url_for('home'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
      form = UpdateAccountForm()
      if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.Email = form.Email.data
            db.session.commit()
            flash('your account has been updated', 'success')
            return redirect(url_for('account'))
      elif request.method == 'GET': 
            form.username.data = current_user.username
            form.Email.data = current_user.Email
                                                                                                                                                                                         
      image_file = url_for('static', filename='profile_pics/' + (current_user.image_file or 'default.jpg'))
      return render_template('account.html', title='Account', image_file=image_file, form=form)

if __name__ == "__main__":

    app.run(debug=True)
