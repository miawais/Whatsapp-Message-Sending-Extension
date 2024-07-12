from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

logged_in = False

@app.route('/', methods=['GET', 'POST'])
def index():
    global logged_in
    if request.method == 'POST':
        if 'login' in request.form:
            logged_in = True
            return jsonify({'success': True})
        elif 'send_message' in request.form and logged_in:
            group_names = request.form.get('group_names')
            message = request.form.get('message')
            # Add logic to send messages to the specified groups
            return jsonify({'success': True, 'message': 'Messages sent successfully!'})
    return render_template('index.html', logged_in=logged_in)

if __name__ == '__main__':
    app.run(debug=True)
