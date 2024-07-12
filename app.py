from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import threading
import time

app = Flask(__name__)

driver = None
logged_in = False

def open_whatsapp():
    global driver, logged_in
    options = Options()
    # Remove headless mode for login phase to interact with QR code
    # options.add_argument('--headless')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get('https://web.whatsapp.com/')
    while not logged_in:
        try:
            if driver.find_element(By.XPATH, '//canvas[@aria-label="Scan me!"]'):
                print("Waiting for QR code scan...")
                time.sleep(10)  # Increase wait time to allow QR code scanning
        except Exception as e:
            print(f"Error: {e}")
            continue
        logged_in = True

@app.route('/')
def index():
    return render_template('index.html', logged_in=logged_in)

@app.route('/login', methods=['POST'])
def login():
    global logged_in
    if not logged_in:
        threading.Thread(target=open_whatsapp).start()
    return jsonify({'success': True})

@app.route('/check_login', methods=['GET'])
def check_login():
    global logged_in
    return jsonify({'logged_in': logged_in})

@app.route('/send_message', methods=['POST'])
def send_message():
    group_names = request.form.get('group_names').split(',')
    message = request.form.get('message')
    try:
        send_whatsapp_message(group_names, message)
        return jsonify({'success': True, 'message': 'Messages sent successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

def send_whatsapp_message(group_names, message):
    global driver
    for group in group_names:
        try:
            search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
            search_box.clear()
            search_box.send_keys(group)
            search_box.send_keys(Keys.ENTER)
            time.sleep(2)
            message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
            message_box.send_keys(message)
            message_box.send_keys(Keys.ENTER)
            time.sleep(2)
        except Exception as e:
            print(f"Error sending message to {group}: {e}")

if __name__ == '__main__':
    app.run(debug=True)
