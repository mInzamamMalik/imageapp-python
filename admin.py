#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
from flask import Flask, request, url_for
from firebase_admin import firestore
import pyrebase

databaseURL = 'https://read-me-a-story3-default-rtdb.firebaseio.com/'

cred_object = credentials.Certificate("./config/firebase.json")
default_app = firebase_admin.initialize_app(cred_object, {
    'databaseURL': databaseURL,
})


app = Flask(__name__)

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


# In[2]:




# In[3]:


# In[4]:
# Create torch dataset


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

# In[5]:

# def prediction(x):
#   x_test = ['']
#   tokenizer = AutoTokenizer.from_pretrained("roberta-base")
#   X_test_tokenized = tokenizer(x_test, padding=True, truncation=True, max_length=512)

#   # Create torch da

#   test_dataset = Dataset(X_test_tokenized)

#   # Load trained model
#   model_path = "./classifier_directory"
#   model = AutoModelForSequenceClassification.from_pretrained(model_path, num_labels=5)

#   # Define test trainer
#   test_trainer = Trainer(model)

#   # Make prediction
#   raw_pred, _, _ = test_trainer.predict(test_dataset)
#   tokenizer = AutoTokenizer.from_pretrained("roberta-base")


#   # Preprocess raw predictions
#   y_pred = np.argmax(raw_pred, axis=1)
#   if y_pred == 0:
#     return 'Friendship'
#   elif y_pred == 1:
#     return 'Honesty'
#   elif y_pred == 2:
#     return 'Patience'
#   elif y_pred == 3:
#     return 'Brave'
#   elif y_pred == 4:
#     return 'Respect'

# pred=prediction(['afraid,fear,courage,brave,determined '])
# print(pred)


# In[ ]:

# In[ ]:

# log in

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
            return 'Failed to login'
    return render_template('home.html')
# log out


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')


@app.route('/options')
def options():
    return render_template('options.html')

# add


@app.route('/Add', methods=["GET", "POST"])
def hello():
    return render_template('classifier.html')


@app.route('/Save_data', methods=['GET', 'POST'])
def save_Data():
    db_store = firestore.client()
    users_ref = db_store.collection(u'books')
    docs = users_ref.stream()
    checklength = []
    for doc in docs:
        checklength.append(doc)

    print(request.form)
    dict1 = {}
    dict1['titleSmall'] = request.form.get("titleSmall")
    dict1['title'] = request.form.get("title")
    dict1['content'] = request.form.get("content")
    dict1['picture'] = request.form.get("picture")
    dict1['moral'] = request.form.get("moral")  # this shows overload error

    doc_ref = db_store.collection(u'books').document(
        u''+str(len(checklength)+1))
    doc_ref.set(dict1)
    return "save sucessfully"


@app.route('/Add_pred', methods=['GET', 'POST'])
def prediction():

    print('text from front end')
    print(request.form.get('content'))
   # prediction
    tokenizer = AutoTokenizer.from_pretrained("roberta-base")
    X_test = [request.form.get('content')]
    #X_test=['honesty truth lie honest']
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


# In[ ]:
if __name__ == "__main__":
    # app.debug = True
    app.run(debug=True, port=5000)


# In[ ]:
