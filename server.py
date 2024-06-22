from flask import Flask, request, redirect, send_from_directory
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit_form():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone = request.form['phone']
    amount = request.form['amount']
    recurring = request.form['recurring']

    # Capture data (you can save it to a database here)
    print('Captured Data:', { 'first_name': first_name, 'last_name': last_name, 'email': email, 'phone': phone })

    # Pass data to fill_clunky_form
    data = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'phone': phone,
        'donation_amount': amount,
        'recurring_donation': recurring
    }
    fill_clunky_form(data)
    return 'Form submitted successfully!'

def fill_clunky_form(data):
    driver_path = '/Users/surajs/Downloads/chromedriver-mac-x64/chromedriver'  # Replace with your actual path
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    driver.get('https://donations.heartfulness.org/general-donations-to-heartfulness-institute-usa-recurring/')

    time.sleep(2)  # Allow page to load

    # Click the "Donate Now" button using JavaScript
    donate_button = driver.find_element(By.XPATH, '//*[@id="site-inner"]/section/div/div[2]/div[3]/div/div[1]/div/div/div/button')
    driver.execute_script("arguments[0].click();", donate_button)

    time.sleep(2)  # Allow page to load

    # Wait for the form fields to be present
    wait = WebDriverWait(driver, 10)
    first_name = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Name"]')))
    last_name = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Last Name"]')))
    email = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Email Id"]')))
    phone = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="1 (702) 123-4567"]')))
    donation_amount = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="0"]')))

    # Fill out the form
    first_name.send_keys(data['first_name'])
    last_name.send_keys(data['last_name'])
    email.send_keys(data['email'])
    phone.send_keys(data['phone'])
    donation_amount.send_keys(data['donation_amount'])

    # Submit the form
    driver.find_element(By.XPATH, '//button[text()="Submit"]').send_keys(Keys.RETURN)

    time.sleep(2)  # Wait for form submission
    driver.quit()

@app.route('/redirect.html')
def serve_redirect():
    return send_from_directory(os.getcwd(), 'redirect.html')

if __name__ == '__main__':
    app.run(debug=True)
