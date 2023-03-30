#!/usr/bin/env python
# coding: utf-8

# In[1]:

# importing libraries
from transformers import AutoModelForSequenceClassification, AutoTokenizer, BertTokenizer, BertForSequenceClassification
import pandas as pd
import numpy as np
from transformers import EarlyStoppingCallback
from transformers import TrainingArguments, Trainer
import torch
from flask import Flask, session, render_template, request, redirect
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from flask import Flask, url_for, flash, jsonify
from firebase_admin import firestore
import pyrebase
from datetime import timedelta
from flask import session, app
import time

import os
import urllib.request
import datetime
import logging


# access database
databaseURL = 'https://read-me-a-story3-default-rtdb.firebaseio.com/'

cred_object = credentials.Certificate("./config/firebase.json")
default_app = firebase_admin.initialize_app(cred_object, {
    'databaseURL': databaseURL,
})

#  How to run flask program reference: https://flask.palletsprojects.com/en/2.2.x/quickstart/#:~:text=To%20run%20the%20application%2C%20use,with%20the%20%2D%2Dapp%20option.&text=As%20a%20shortcut%2C%20if%20the,Line%20Interface%20for%20more%20details
app = Flask(__name__)

# accessing books collection
db = firestore.client()
todo_ref = db.collection(u'books')

# for admin authentication
config = {
    'apiKey': "AIzaSyA9f97gGu55wjvB7Nsr75VJHFm71w1b7p0",
    'authDomain': "authenticatepy1.firebaseapp.com",
    'projectId': "authenticatepy1",
    'storageBucket': "authenticatepy1.appspot.com",
    'messagingSenderId': "70785395579",
    'appId': "1:70785395579:web:2ced190f1e121376b0ebde",
    'measurementId': "G-RS703MBCMF",
    'databaseURL': ''
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app.secret_key = 'secret'


class Dataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels=None):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx])
                for key, val in self.encodings.items()}
        if self.labels:
            item["labels"] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.encodings["input_ids"])


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            return redirect(url_for('options'))

        except:
            flash('Email or Password is incorrect', 'category8')
    return render_template('home.html')


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

# log out


@app.route('/logout')
def logout():
    return redirect('/')

# Home page


@app.route('/options')
def options():
    todo_id = request.args.get('id')
    if todo_id:
        todo = todo_ref.document(todo_id).get(field_paths={'moral'})
        return jsonify(todo.to_dict()), 200
    else:
        docs = todo_ref.stream()
        countP = 0
        countB = 0
        countH = 0
        countF = 0
        countR = 0
        for doc in docs:
            moral = u'{}'.format(doc.to_dict()['moral'])
            if moral == "Patience":
                value = countP + 1
                countP = value

            if moral == "Brave":
                value = countB + 1
                countB = value

            if moral == "Honesty":
                value = countH + 1
                countH = value

            if moral == "Friendship":
                value = countF + 1
                countF = value

            if moral == "Respect":
                value = countR + 1
                countR = value
    total = countP+countB+countF+countH+countR

    #  To display the total number of stories
    m1 = "The total is: {}".format(total)
    m1 = f"The total is: {total} "
    m1 = "The total is %d " % (total)
    m1 = "The Total Number Of Stories: " + str(total)

    #  To display the number of stories in each moral in home page
    #  How to use flash in flask reference : https://flask.palletsprojects.com/en/2.2.x/patterns/flashing/
    flash(m1, 'category1')
    flash(countR, 'category2')
    flash(countF, 'category3')
    flash(countH, 'category4')
    flash(countP, 'category5')
    flash(countB, 'category6')

    return render_template('options.html')

# Edit


@app.route('/Edit', methods=["GET", "POST"])
def edit():

    todo_id = request.args.get('id')
    if todo_id:
        todo = todo_ref.document(todo_id).get(field_paths={'title'})
        return jsonify(todo.to_dict()), 200
    else:

        docs = todo_ref.stream()
        for doc in docs:
            title = u'{}'.format(doc.to_dict()['title'])
            flash(title, 'category9')

    return render_template('edit.html')

    # edit-form


@app.route('/editform', methods=["GET", "POST"])
def editform():
    return render_template('edit-form.html')


@app.route("/forward/", methods=['POST'])
def move_forward():
    # Moving forward code
    # forward_message = "Moving Forward..."
    # return render_template('index.html', forward_message=forward_message)
    title2 = request.form['delete']
    docs = db.collection(u'books').where("title", "==", title2).get()
    for doc in docs:
        key = doc.id
        db.collection(u'books').document(key).delete()
    flash('book has been removed successfully', 'category3')
    return render_template('delete.html')


# Add new story

@app.route('/Add', methods=["GET", "POST"])
def hello():
    return render_template('classifier.html')

# Save data in database after adding new story


@app.route('/Save_data', methods=['GET', 'POST'])
def save_Data():
    print(request.form)

    curr_time = str(time.time_ns())

    dict1 = {}
    dict1['titleSmall'] = request.form.get("titleSmall")
    dict1['title'] = request.form.get("title")
    dict1['content'] = request.form.get("content")
    dict1['picture'] = request.form.get("picture")
    dict1['moral'] = request.form.get("moral")
    dict1['createdOn'] = firestore.SERVER_TIMESTAMP

    db.collection(u'books').document(curr_time).set(dict1)
    return "save successfully"

# when admin disapproves story it will be saved in canceledStories collection


@app.route('/Cancel_data', methods=['GET', 'POST'])
def cancel_Data():
    print(request.form)

    curr_time = str(time.time_ns())

    dict1 = {}
    dict1['titleSmall'] = request.form.get("titleSmall")
    dict1['title'] = request.form.get("title")
    dict1['content'] = request.form.get("content")
    dict1['picture'] = request.form.get("picture")
    dict1['moral'] = request.form.get("moral")
    dict1['createdOn'] = firestore.SERVER_TIMESTAMP

    db.collection(u'canceledStories').document(curr_time).set(dict1)
    return "canceled sucessfully"


# The classifier
@app.route('/Add_pred', methods=['GET', 'POST'])
def prediction():

    os.environ["TOKENIZERS_PARALLELISM"] = "false"  # to avoide dead lock

    # Initialize logger
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler('my_log_file.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.info('text from front end')
    logger.info(request.form)
    logger.info(request.form.get('content'))

    print('text from front end')
    print(request.form)
    print(request.form.get('content'))
    # prediction
    tokenizer = AutoTokenizer.from_pretrained("roberta-base")
    X_test = [request.form.get('content')]
    # X_test=['honesty truth lie honest']
    print(X_test)
    X_test_tokenized = tokenizer(
        X_test, padding=True, truncation=True, max_length=512)
    print(X_test_tokenized)
# Create torch dataset
    test_dataset = Dataset(X_test_tokenized)

 # Load trained model
    model_path = "./classifier_directory"
    model = AutoModelForSequenceClassification.from_pretrained(
        model_path, num_labels=5)

    # Define test trainer
    test_trainer = Trainer(model)

    # Make prediction

    raw_pred, _, _ = test_trainer.predict(test_dataset)

    # Preprocess raw predictions
    y_pred = np.argmax(raw_pred, axis=1)
    pred = ''
    if y_pred == 0:
        pred = 'Friendship'
    elif y_pred == 1:
        pred = 'Honesty'
    elif y_pred == 2:
        pred = 'Patience'
    elif y_pred == 3:
        pred = 'Brave'
    elif y_pred == 4:
        pred = 'Respect'

    return pred


# @app.route('/download_model', methods=['GET'])
# def download_file():
#     url = 'https://firebasestorage.googleapis.com/v0/b/sysborg-air.appspot.com/o/model%2Fpytorch_model.bin?alt=media&token=5eaa3b0d-cc85-4abf-aff5-8a1d2799dd78'
#     # url = 'https://mgmotors.com.pk/storage/img/details_4/homepage_models-mg-zs-ev-new.jpg'
#     filename = "pytorch_model.bin"  # Fixed file name
#     folder = "classifier_directory"  # Folder to save the file

#     # Check if file with that name already exists
#     if os.path.exists(os.path.join(folder, filename)):
#         return jsonify({'error': 'File already exists'}), 400

#     # Download file from URL and save it in the specified folder with the fixed name
#     try:
#         urllib.request.urlretrieve(url, os.path.join(folder, filename))
#         return jsonify({'message': 'File downloaded successfully'}), 200
#     except Exception as e:
#         print(e)
#         return jsonify({'error': str(e)}), 500

# def auto_download_file():
#     url = 'https://firebasestorage.googleapis.com/v0/b/sysborg-air.appspot.com/o/model%2Fpytorch_model.bin?alt=media&token=5eaa3b0d-cc85-4abf-aff5-8a1d2799dd78'
#     filename = "pytorch_model.bin"  # Fixed file name
#     folder = "classifier_directory"  # Folder to save the file

#     # Check if file with that name already exists
#     if os.path.exists(os.path.join(folder, filename)):
#         print( 'error: File already exists')
#     else:
#         # Download file from URL and save it in the specified folder with the fixed name
#         try:
#             urllib.request.urlretrieve(url, os.path.join(folder, filename))
#             print( 'message: File downloaded successfully')
#         except Exception as e:
#             print(e)
#             print(str(e))

# # auto_download_file();

# @app.route('/delete_model', methods=['GET'])
# def delete_file():
#     filename = "pytorch_model.bin"  # Fixed file name
#     folder = "classifier_directory"  # Folder to save the file

#     # Check if file with that name exists
#     if not os.path.exists(os.path.join(folder, filename)):
#         return jsonify({'error': 'File not found'}), 404

#     # Delete the file
#     try:
#         os.remove(os.path.join(folder, filename))
#         return jsonify({'message': 'File deleted successfully'}), 200
#     except Exception as e:
#         print(e)
#         return jsonify({'error': str(e)}), 500

# @app.route('/check_model')
# def check_file():
#     filename = "pytorch_model.bin"  # Fixed file name
#     folder = "classifier_directory"  # Folder to save the file
#     file_path = os.path.join(folder, filename)
#     if os.path.exists(file_path):
#         try:
#             # Get the file size
#             file_size = os.path.getsize(file_path)
#             # Get the last modified date of the file
#             last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
#             return f"File name: {filename}, File size: {file_size} (file size should be: 498669549), Last modified: {last_modified}"
#         except OSError as e:
#             return str(e)
#     else:
#         return f"File {filename} does not exist"

if __name__ == '__main__':
    app.run()  # for google app engine
