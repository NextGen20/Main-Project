from gzip import FNAME
from flask import Flask
import os.path
from flask import Flask, request, redirect, session, url_for
from flask.templating import render_template


app = Flask(__name__)
app.secret_key = 'amit'

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form.get("fname")
        last_name = request.form.get("lname")
        password = request.form.get("password")
        email = request.form.get("email")
        session['fname'] = first_name
    
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