from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os
from flask_session import Session
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TESTING'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config["SESSION_PERMANENT"] = False

Session(app)
db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()


class Urls(db.Model):
    id_ = db.Column("id_", db.Integer, primary_key=True)
    date = db.Column("date", db.String(), nullable=False)
    long = db.Column("long", db.String(), nullable=False)
    short = db.Column("short", db.String(), nullable=False)

    def __init__(self, date, long, short):
        self.date = date
        self.long = long
        self.short = short



@app.route("/", methods=['GET', 'POST'])
def default():
    return redirect('https://ieeesiesgst.in/')


@app.route("/login/", methods=['GET', 'POST'])
def login():
    if 'logged_in' not in session:
        if request.method == 'POST':
            password = request.form.get("password")
            passw = os.environ.get('SECRET_PASS')
            if password == passw:
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                return render_template("login.html", msg=True)

        return render_template("login.html")
    else:
        return redirect(url_for('home'))



@app.route('/adminnnnnnnnn/linkerr', methods=['POST', 'GET'])
def home():
    if 'logged_in' in session:
        if request.method == "POST":
            url_received = request.form["long-url"]
            custom_short_key = request.form["custom-key"]
            small_url = Urls.query.filter_by(short=custom_short_key).first()
            birth=date.today().strftime('%d/%m/%Y')
            if small_url:
                return render_template("main.html", vars="alert alert-danger", msg="This short key is already taken")
            else:
                new_url = Urls(birth, url_received, custom_short_key)
                db.session.add(new_url)
                db.session.commit()
                return render_template("main.html", vars="alert alert-info", msg='https://links.ieeesiesgst.in/'+custom_short_key)
        else:
            return render_template('main.html')
    else:
        return redirect(url_for('login'))



@app.route('/<short_url>')
def redirection(short_url):
    long_url = Urls.query.filter_by(short=short_url).first()
    if long_url:
        return redirect(long_url.long)
    else:
        return render_template('404.html')




@app.route('/deleeeeteeeeeeeeeee/<int:id>', methods=['POST', 'GET'])
def delete(id):
    if 'logged_in' in session:
        user_to_delete = Urls.query.get_or_404(id)
        if user_to_delete:
            db.session.delete(Urls.query.filter_by(id_=id).first())
            db.session.commit()
            return redirect(url_for('all_urls'))
    else:
        return redirect(url_for('login'))




@app.route('/updaaateeeee/<int:id>', methods=['POST', 'GET'])
def update(id):
    if 'logged_in' in session:
        if request.method == "POST":
            urls = Urls.query.get_or_404(id)
            long = request.form["update-long-url"]
            short = request.form["update-custom-key"]
            birth=date.today().strftime('%d/%m/%Y')
            small_url = Urls.query.filter_by(short=short).first()
            if small_url:
                return render_template("update.html", vars="alert alert-danger", msg="This short key is already taken")
            else:
                urls.date = birth
                urls.long = long
                urls.short = short
                db.session.commit()
                return render_template("update.html", vars="alert alert-info", msg='https://links.ieeesiesgst.in/'+short)
        else:
            return render_template('update.html', urls=Urls.query.get(id))
    else:
        return redirect(url_for('login'))



@app.route('/allzzz-urlzz', methods=['POST', 'GET'])
def all_urls():
    if 'logged_in' in session:
        return render_template('links.html', vals=Urls.query.all())
    else:
        return redirect(url_for('login'))



@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")



if __name__ == '__main__':
    app.run(port=5000)
