from flask import Flask, request, redirect, url_for
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    amount = request.form['amount']
    recurring = request.form['recurring']

    # Capture data (you can save it to a database here)
    print('Captured Data:', { 'name': name, 'email': email, 'phone': phone })

    # Prepare redirect URL with pre-filled data
    redirect_url = (
        f'https://donations.heartfulness.org/general-donations-to-heartfulness-institute-usa-recurring/'
        f'?billing_full_name={name}&billing_email={email}&billing_phone={phone}&donation_amount={amount}'
        f'&recurring_donation={recurring}'
    )
    return redirect(redirect_url)

if __name__ == '__main__':
    app.run(debug=True)
