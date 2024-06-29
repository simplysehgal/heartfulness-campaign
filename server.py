from flask import Flask, request, send_from_directory
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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

    fill_clunky_form(data)

    return 'Form submitted successfully!'

@app.route('/redirect.html')
def serve_redirect():
    return send_from_directory(os.getcwd(), 'redirect.html')

def fill_clunky_form(data):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get('https://donations.heartfulness.org/general-donations-to-heartfulness-institute-usa-recurring/')

    wait = WebDriverWait(driver, 10)

    donate_now_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="site-inner"]/section/div/div[2]/div[3]/div/div[1]/div/div/div/button')))
    driver.execute_script("arguments[0].click();", donate_now_button)

    billing_full_name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Name"]')))
    billing_full_name.send_keys(data['first_name'][0])

    billing_last_name = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Last Name"]')
    billing_last_name.send_keys(data['last_name'][0])

    email_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Email Id"]')
    email_input.send_keys(data['email'][0])

    phone_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="1 (702) 123-4567"]')
    phone_input.send_keys(data['phone'][0])

    amount_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="0"]')
    amount_input.send_keys(data['amount'][0])

    # Submit the form or any additional steps here

    driver.quit()

if __name__ == '__main__':
    app.run(debug=True)
