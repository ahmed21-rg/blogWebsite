from PIL import Image
from forms import RegisterationForm, loginform,UpdateAccountForm,PostForm
import secrets, os
from datetime import datetime
from flask import Flask
from flask import render_template, url_for, flash, redirect,request,abort
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
      page=request.args.get('page', 1, type=int)
      posts= Post.query.paginate(page=page,per_page=5)
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

def save_picture(form_picture):
      random_hex = secrets.token_hex(8)
      _, f_ext = os.path.split(form_picture.filename)
      picture_fn = random_hex + f_ext
      picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
      output_size = (125,125)
      i = Image.open(form_picture)
      i.thumbnail(output_size)
      i.save(picture_path)
      return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
      form = UpdateAccountForm()
      if form.validate_on_submit():
            if form.picture.data:
                  picture_file = save_picture(form.picture.data)
                  current_user.image_file = picture_file
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
@app.route("/post/new",methods=['GET', 'POST'])
@login_required
def new_post():
      form = PostForm()
      if form.validate_on_submit():
            post = Post(title=form.title.data, content=form.content.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('your post has been created successfully', 'success')
            return redirect(url_for('home'))
      return render_template('create_post.html', title="New Post",form=form, legend='New Post')

@app.route("/post/<int:post_id>")        # opens the post and post id 
def post(post_id):
      post = Post.query.get_or_404(post_id)           #checks if the post exist or not
      return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
      
      post = Post.query.get_or_404(post_id)
      if post.author != current_user:
            abort(403)
      
      form = PostForm()
      if form.validate_on_submit():
            post.title = form.title.data  
            post.content = form.content.data
            db.session.commit()
            flash('Post update sucessfully', 'success')
            return redirect(url_for('post', post_id=post.id))
      elif request.method == 'GET':
            form.title.data = post.title
            form.content.data = post.content
      return render_template("create_post.html", title='Update Post', form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
      post = Post.query.get_or_404(post_id)
      if post.author != current_user:
            abort(403)
      db.session.delete(post)
      db.session.commit()
      flash('Your post has been deleted', 'success')
      return redirect(url_for('home'))

if __name__ == "__main__":

    app.run(debug=True)                                      