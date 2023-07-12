from gzip import FNAME
from flask import Flask
import os.path
from flask import Flask, request, redirect, session, url_for
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)
app.secret_key = 'amit'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    
    def __str__(self):
        return f"Name:{self.first_name}, Last:{self.last_name}"

# remove all the names that signup to the website  
@app.route("/remove_all")
def remove_all():
    Profile.query.delete()
    db.session.commit()
    return 'Remove all from DB'
    # return redirect('/homepage')

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form.get("fname")
        last_name = request.form.get("lname")
        password = request.form.get("password")
        email = request.form.get("email")
        session['fname'] = first_name
        p = Profile(first_name=first_name, last_name=last_name, password=password, email=email)
        db.session.add(p)
        db.session.commit()
        # session["first_name"] = first_name
        return redirect('/homepage')
    else:
        return render_template('signup.html')
        
    
@app.route('/')
def root():
    return redirect('/signup')

@app.route("/homepage")
def homepage():
    fname = session.get('fname', '')
    return render_template('homepage.html', message=fname)

if __name__ == "__main__":
    app.run(debug=True , host="0.0.0.0", port=5000)