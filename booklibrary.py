from flask import Flask, render_template, request, session, redirect, url_for
from forms import SignupForm, LoginForm,AddBookForm
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BookLibrary.sqlite3'
app.secret_key = "development-key"

db = SQLAlchemy(app)

class User(db.Model):
  __tablename__ = 'users'
  uid = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  email = db.Column(db.String(120), unique=True)
  pwdhash = db.Column(db.String(54))

  def __init__(self, firstname, lastname, email, password):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.email = email.lower()
    self.set_password(password)

  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)


class Book(db.Model):
  __tablename__ = 'books'
  uid = db.Column(db.Integer, primary_key = True)
  bookname = db.Column(db.String(100))
  contributorname = db.Column(db.String(100))
  description = db.Column(db.String(100))
  setcount = db.Column(db.Integer)
  email = db.Column(db.String(120))


  def __init__(self, bookname, contributorname, description, setcount,email):
    self.bookname = bookname.upper()
    self.contributorname = contributorname.title()
    self.description = description.title()
    self.setcount = setcount
    self.email = email.lower()

class IssueBook(db.Model):
  __tablename__ = 'issuebooks'
  uid = db.Column(db.Integer, primary_key = True)
  bookname = db.Column(db.String(100))
  requestoremail = db.Column(db.String(100))
  issuedate = db.Column(db.DateTime)
  receivedate = db.Column(db.DateTime)

  def __init__(self, bookname, contributorname, description, setcount,email):
    self.bookname = bookname.upper()
    self.contributorname = contributorname.title()
    self.description = description.title()
    self.setcount = setcount
    self.email = email.lower()



@app.route("/")
def index():
  return render_template("index.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
  if 'email' in session:
    return redirect(url_for('home'))

  form = SignupForm()

  if request.method == "POST":
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()

      session['email'] = newuser.email
      return redirect(url_for('home'))

  elif request.method == "GET":
    return render_template('signup.html', form=form)

@app.route("/AddBook", methods=["GET", "POST"])
def AddBook():
  form = AddBookForm()

  if request.method == "POST":
    if form.validate() == False:
      return render_template('addbook.html', form=form)
    else:
      newbook = Book(form.book_name.data, form.contributor_name.data, form.description.data,form.setcount.data,form.email.data)
      db.session.add(newbook)
      db.session.commit()

      session['email'] = newbook.email
      return redirect(url_for('bookshome'))

  elif request.method == "GET":
    return render_template('addbook.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
  if 'email' in session:
    return redirect(url_for('home'))

  form = LoginForm()

  if request.method == "POST":
    if form.validate() == False:
      return render_template("login.html", form=form)
    else:
      email = form.email.data
      password = form.password.data

      user = User.query.filter_by(email=email).first()


      if user is not None and user.check_password(password):
        session['email'] = form.email.data
        return redirect(url_for('home'))

      else:
        return redirect(url_for('login'))

  elif request.method == 'GET':
    return render_template('login.html', form=form)

@app.route("/Adminlogin", methods=["GET", "POST"])
def Adminlogin():
  if 'email' in session:
    return redirect(url_for('adminhome'))

  form = LoginForm()

  if request.method == "POST":
    if form.validate() == False:
      return render_template("adminlogin.html", form=form)
    else:
      email = form.email.data
      password = form.password.data

      user = User.query.filter_by(email=email).first()


      if user is not  'None' and user.check_password(password):
        session['email'] = form.email.data
        return redirect(url_for('adminhome'))

      else:
        return redirect(url_for('Adminlogin'))

  elif request.method == 'GET':
    return render_template('adminlogin.html', form=form)


@app.route("/logout")
def logout():
  session.pop('email', None)
  return redirect(url_for('index'))

@app.route("/home", methods=["GET", "POST"])
def home():
  if 'email' not in session:
    return redirect(url_for('login'))

  return render_template("home.html",User=User.query.order_by('firstname'))

@app.route("/adminhome", methods=["GET", "POST"])
def adminhome():
  if 'email' not in session:
    return redirect(url_for('login'))

  return render_template("adminhome.html",User=User.query.order_by('firstname'))

@app.route("/bookshome", methods=["GET", "POST"])
def bookshome():
  if 'email' not in session:
    return redirect(url_for('login'))

  return render_template("bookshome.html",Book=Book.query.order_by('bookname'))

@app.route('/Catalog')
def Catalog():
    if 'email' not in session:
      return redirect(url_for('login'))

    return render_template('home.html',User=User.query.order_by('firstname'))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
