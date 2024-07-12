from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)

logged_in = False
driver = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global logged_in
    if request.method == 'POST':
        if 'login' in request.form:
            global driver
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            driver.get('https://web.whatsapp.com/')
            logged_in = True
            return jsonify({'success': True})
        elif 'send_message' in request.form and logged_in:
            group_names = request.form.get('group_names').split(',')
            message = request.form.get('message')
            send_whatsapp_message(group_names, message)
            return jsonify({'success': True, 'message': 'Messages sent successfully!'})
    return render_template('index.html', logged_in=logged_in)

def send_whatsapp_message(group_names, message):
    for group in group_names:
        search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.clear()
        search_box.send_keys(group)
        search_box.send_keys(Keys.ENTER)
        time.sleep(2)
        message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        message_box.send_keys(message)
        message_box.send_keys(Keys.ENTER)
        time.sleep(2)

if __name__ == '__main__':
    app.run(debug=True)
