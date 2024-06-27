from flask import Flask, request, render_template, send_from_directory
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

# Path to the CSV file
csv_file_path = 'submissions.csv'

@app.route('/')
def form():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone = request.form['phone']
    amount = request.form['amount']
    recurring = request.form['recurring']

    # Capture data
    print('Captured Data:', { 'first_name': first_name, 'last_name': last_name, 'email': email, 'phone': phone })

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

    # Call function to fill the external form
    fill_clunky_form(request.form)

    return 'Form submitted successfully!'

def fill_clunky_form(data):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver_path = "./chromedriver"  # Ensure chromedriver is in the project directory
    driver = webdriver.Chrome(executable_path=driver_path, options=options)

    driver.get("https://donations.heartfulness.org/general-donations-to-heartfulness-institute-usa-recurring/")
    
    # Click the "Donate Now" button
    donate_now_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="site-inner"]/section/div/div[2]/div[3]/div/div[1]/div/div/div/button'))
    )
    donate_now_button.click()

    # Fill out the form fields
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'billing_first_name'))).send_keys(data['first_name'])
    driver.find_element(By.NAME, 'billing_last_name').send_keys(data['last_name'])
    driver.find_element(By.NAME, 'billing_email').send_keys(data['email'])
    driver.find_element(By.NAME, 'billing_phone').send_keys(data['phone'])
    driver.find_element(By.NAME, 'donation_amount').send_keys(data['amount'])
    # If needed, fill out more fields as required by the form

    # Submit the form
    driver.find_element(By.XPATH, '//button[contains(text(),"Submit")]').click()
    driver.quit()

@app.route('/redirect.html')
def serve_redirect():
    return send_from_directory(os.getcwd(), 'redirect.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
