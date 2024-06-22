from flask import Flask, request, redirect, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Flask server is running!'

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
        f'/redirect.html?billing_full_name={name}&billing_email={email}&billing_phone={phone}'
        f'&donation_amount={amount}&recurring_donation={recurring}'
    )
    return redirect(redirect_url)

@app.route('/redirect.html')
def serve_redirect():
    return send_from_directory(os.getcwd(), 'redirect.html')

if __name__ == '__main__':
    app.run(debug=True)

