from flask import Flask, render_template, url_for, request, redirect
import csv
from twilio.rest import Client

app = Flask(__name__)

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
    account_sid = 'Account sid here'
    auth_token = 'Auth token here'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
             from_='from number here',
             body="Name: " + data["name"] + " Email: " + data["email"] + " - " + data["message"],
             to='to number here'
             )
    print(message.sid)
