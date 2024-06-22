from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit_form():
    data = {
        'billing_full_name': request.form['billing_full_name'],
        'billing_email': request.form['billing_email'],
        'billing_phone': request.form['billing_phone'],
        'donation_amount': request.form['donation_amount'],
        'recurring_donation': request.form['recurring_donation'],
        'billing_address_1': request.form['billing_address_1'],
        'billing_city': request.form['billing_city'],
        'billing_state': request.form['billing_state'],
        'billing_postcode': request.form['billing_postcode'],
        'billing_country': request.form['billing_country'],
    }
    fill_clunky_form(data)
    return 'Form submitted successfully!'

def fill_clunky_form(data):
    driver_path = '/Users/surajs/Downloads/chromedriver-mac-x64/chromedriver'  # Replace with your actual path
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)

    driver.get('https://donations.heartfulness.org/general-donations-to-heartfulness-institute-usa-recurring/')

    time.sleep(2)  # Allow page to load

    driver.find_element_by_name('billing_full_name').send_keys(data['billing_full_name'])
    driver.find_element_by_name('billing_email').send_keys(data['billing_email'])
    driver.find_element_by_name('billing_phone').send_keys(data['billing_phone'])
    driver.find_element_by_name('donation_amount').send_keys(data['donation_amount'])
    
    if data['recurring_donation'] != 'one-time':
        driver.find_element_by_name('recurring_donation').click()
        driver.find_element_by_name('recurring_donation').send_keys(data['recurring_donation'])
    
    driver.find_element_by_name('billing_address_1').send_keys(data['billing_address_1'])
    driver.find_element_by_name('billing_city').send_keys(data['billing_city'])
    driver.find_element_by_name('billing_state').send_keys(data['billing_state'])
    driver.find_element_by_name('billing_postcode').send_keys(data['billing_postcode'])
    driver.find_element_by_name('billing_country').send_keys(data['billing_country'])

    # Submit the form
    driver.find_element_by_name('billing_country').send_keys(Keys.RETURN)

    time.sleep(2)  # Wait for form submission
    driver.quit()

if __name__ == '__main__':
    app.run(debug=True)
