from flask import Flask, renderTemplate, request, jsonify
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

driver = None

@app.route('/')
def index():
    return renderTemplate('index.html')

@app.route('/login', methods=['POST'])
def login():
    global driver
    driver = webdriver.Chrome()
    driver.get("https://web.whatsapp.com/")
    return jsonify(status='waiting')

@app.route('/check_login', methods=['POST'])
def check_login():
    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "canvas[aria-label='Scan me!']")))
        return jsonify(status='waiting')
    except Exception:
        return jsonify(status='logged_in')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    group_names = data['groups']
    message = data['message']

    for name in group_names:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/button'))
        )
        search_box.click()
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div[1]/p'))
        )
        search_input.send_keys(name + Keys.ENTER)
        time.sleep(2)
        message_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'))
        )
        message_box.send_keys(message)
        send_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span'))
        )
        send_button.click()
        time.sleep(3)
    
    return jsonify(status='success')

if __name__ == '__main__':
    app.run(debug=True)
