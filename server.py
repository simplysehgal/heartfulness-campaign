from flask import Flask, request, send_from_directory
import pandas as pd
import os

app = Flask(__name__)

# Path to the CSV file
csv_file_path = 'submissions.csv'

@app.route('/submit', methods=['POST'])
def submit_form():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone = request.form['phone']
    amount = request.form['amount']
    recurring = request.form['recurring']

    # Save data to CSV
    data = {
        'first_name': [first_name],
        'last_name': [last_name],
        'email': [email],
        'phone': [phone],
        'amount': [amount],
        'recurring': [recurring]
    }
    df = pd.DataFrame(data)

    if os.path.exists(csv_file_path):
        df.to_csv(csv_file_path, mode='a', header=False, index=False)
    else:
        df.to_csv(csv_file_path, mode='w', header=True, index=False)

    return 'Form submitted successfully!'

@app.route('/redirect.html')
def serve_redirect():
    return send_from_directory(os.getcwd(), 'redirect.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
