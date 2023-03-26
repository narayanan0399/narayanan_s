from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import csv
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="narayanans",
    password="Pythonsql",
    hostname="narayanans.mysql.pythonanywhere-services.com",
    databasename="narayanans$narayanswebsite",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class ContactInfo(db.Model):

    __tablename__ = "contactinfo"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60))
    name = db.Column(db.String(60))
    message = db.Column(db.String(8192))

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/<page_name>')
def htmlpage(page_name):
    page = page_name + '.html'
    return render_template(page)

@app.route('/submit_form', methods=['GET', 'POST'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            print(data)
            write_to_csv(data)
            send_sms(data)
            return redirect('/thankyou')
        except:
            return "did not save to database"
    else:
        return "Error sumitting form, please try again"

def write_to_csv(data):
    with open("./database.csv", mode="a", newline="") as database:
        email = data["email"]
        name = data["name"]
        message = data["message"]
        csv_writer = csv.writer(database, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, name, message])

def send_sms(data):
    proxy_client = TwilioHttpClient(proxy={'http': os.environ['http_proxy'], 'https': os.environ['https_proxy']})
    account_sid = 'account_sid'
    auth_token = 'auth_token'
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages.create(
             from_='from_number',
             body="Name: " + data["name"] + " Email: " + data["email"] + " - " + data["message"],
             to='to_number'
             )
    print(message.sid)

def write_to_db(data):
    email = data["email"]
    name = data["name"]
    message = data["message"]
    # db.session.add(email)
