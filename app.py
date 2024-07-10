# from flask import Flask, render_template, request, jsonify
# from utils import model_predict
# app = Flask(__name__)
#
#
# @app.route("/")
# def home():
#     return render_template("index.html")
#
#
# @app.route('/predict', methods=['POST'])
# def predict():
#     email = request.form.get('content')
#     prediction = model_predict(email)
#     return render_template("index.html", prediction=prediction, email=email)
#
# # Create an API endpoint
# @app.route('/api/predict', methods=['POST'])
# def predict_api():
#     data = request.get_json(force=True)  # Get data posted as a json
#     email = data['content']
#     prediction = model_predict(email)
#     return jsonify({'prediction': prediction, 'email': email})  # Return prediction
#
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8080, debug=True)

from flask import Flask, render_template, request, jsonify, redirect
from datetime import datetime
from utils import model_predict

app = Flask(__name__)

# In-memory storage for emails
emails = {}
email_id_counter = 1

@app.route("/")
def home():
    return render_template("index.html", emails=emails.values())

@app.route('/predict', methods=['POST'])
def predict():
    global email_id_counter
    email = request.form.get('content')
    prediction = model_predict(email)

    # Store email with prediction and timestamp
    email_data = {
        'id': email_id_counter,
        'content': email,
        'prediction': prediction,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    emails[email_id_counter] = email_data
    email_id_counter += 1

    return render_template("index.html", prediction=prediction, email=email, emails=emails.values())

@app.route('/delete/<int:email_id>', methods=['POST'])
def delete_email(email_id):
    if email_id in emails:
        del emails[email_id]
    return redirect('/')

@app.route('/modify/<int:email_id>', methods=['POST'])
def modify_email(email_id):
    new_content = request.form['new_content']
    if email_id in emails:
        emails[email_id]['content'] = new_content
        emails[email_id]['prediction'] = model_predict(new_content)
        emails[email_id]['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return redirect('/')

# Create an API endpoint
@app.route('/api/predict', methods=['POST'])
def predict_api():
    data = request.get_json(force=True)  # Get data posted as a json
    email = data['content']
    prediction = model_predict(email)
    return jsonify({'prediction': prediction, 'email': email})  # Return prediction

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
