#!/usr/bin/env python
# coding: utf-8

# In[1]:


import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from flask import Flask, request , url_for
from firebase_admin import firestore
import pyrebase

databaseURL ='https://read-me-a-story3-default-rtdb.firebaseio.com/'

cred_object = credentials.Certificate("./config/firebase.json")
default_app = firebase_admin.initialize_app(cred_object, {
    'databaseURL':databaseURL ,
})

from flask import Flask, session, render_template, request, redirect

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


HTML_TEXT = '''
 <html>
<body style="font-size: 22px;background:#BDD5C8 ;background-size: cover;">
        <table id="content" cellpadding="10" style="width: 990px;max-width: 990px;min-height: 570px;background: #C4C2C2;margin: 100px auto;border-radius: 20px;overflow: hidden">
<tr style="border-radius: 20px;">
	<td valign="middle" colspan="2" style="height: 70px;background: #C4C2C2">
    <form method="post" action="#">
      <h1 style="color:black; text-align:center;">Add New story</h1> <br>
            <ul style="width: auto;height: auto ;margin-left: 200px;">
            <label for='title' >Title:</label><br>
            <input type="text" name="title" id='title' style="width: 70%; padding: 12px; border: 1px solid #ccc; border-radius: 4px;"><br><hr>
            <label for='story' >Content:</label><br>
            <textarea name='content' placeholder="Enter content here ....." style="width: 510px;height: 150px;padding: 12px 20px;box-sizing: border-box;border: 2px solid #ccc;border-radius: 4px;background-color: #f8f8f8;font-size: 16px;resize: none;"></textarea><br> <hr>
            <label for="picture" >Upload story picture:</label><br>
            <input type="file" name='picture' id="picture"><br><hr>
            
       <br /><br /><br />

      <input  onClick="alert('Added successfully')" style="height:50px;width:150px; font-size: 20px;margin-left: 10%;" type="submit" value="approve" >
      <input  onClick="alert('story is cancelled')" style="height:50px;width:150px; font-size: 20px;margin-left: 15%;" type="Reset" value="cancel" >


</ul>
            </form>
	</td>
</tr>
</table>
    
    </body>
    </html>
    '''
    
# In[3]:

# import torch
# from transformers import TrainingArguments, Trainer
# from transformers import  AutoModelForSequenceClassification, AutoTokenizer ,BertTokenizer, BertForSequenceClassification
# from transformers import EarlyStoppingCallback
# import numpy as np
# import pandas as pd

# # In[4]:
# # Create torch dataset
# class Dataset(torch.utils.data.Dataset):
#     def __init__(self, encodings, labels=None):
#         self.encodings = encodings
#         self.labels = labels

#     def __getitem__(self, idx):
#         item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
#         if self.labels:
#             item["labels"] = torch.tensor(self.labels[idx])
#         return item

#     def __len__(self):
#         return len(self.encodings["input_ids"])

# In[5]:
# def prediction(self):
#   self = ['']
#   tokenizer = AutoTokenizer.from_pretrained("roberta-base")
#   X_test_tokenized = tokenizer(self, padding=True, truncation=True, max_length=512)

#   # Create torch da

#   test_dataset = Dataset(X_test_tokenized)

#   # Load trained model
#   model_path = "./classifier_directory3"
#   model = AutoModelForSequenceClassification.from_pretrained(model_path, num_labels=5)

#   # Define test trainer
#   test_trainer = Trainer(model)
 
#   # Make prediction
#   raw_pred, _, _ = test_trainer.predict(test_dataset)

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


#pred=prediction(['There was a girl called Rose who loved to sleep with her parents because she afraid to sleep alone. Her parents used to tuck her up in bed every night, but she always went to their bed in the middle of the night: “Can I sleep with you?” – she would ask.Her parent always let her sleep with them, but she was not a baby anymore, so, one day they told her:– “Rose, you are a big girl now, and you can´t sleep with us every night. Big girls have to sleep in their own beds, so we want to help you do that by singing you a song at bedtime.”Rose couldn´t wait until bedtime to hear the song. Her parents finally arrived to her room to sing their song: “Twinkle, twinkle, little star… how I wonder what you are…”Rose fell asleep, and didn´t wake up during the night.She had learnt to confront her fear and to be brave girl and  s '])
#print(pred) 
#pred=prediction(request.form.get("content"))  

# In[ ]:

# In[ ]:



@app.route('/', methods=['POST', 'GET'])
def index():
   
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email,password)
            session['user'] = email
            return redirect (url_for('options'))
        except:
            return 'Failed to login'
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')

@app.route('/options')
def options():
    return render_template('options.html')

@app.route('/Add', methods =["GET","POST"])
def hello():
    db_store = firestore.client()
    users_ref = db_store.collection(u'books')
    docs = users_ref.stream()

    checklength = []
    for doc in docs:
        checklength.append(doc)

       

    dict1 = {}
    # dict1['author'] = request.form.get("author")
    dict1['content'] = request.form.get("content")
    dict1['title'] = request.form.get("title")    
    dict1['moral'] = request.form.get("moral")

    # dict1['moral'] = prediction(request.form.get("content")) 


    doc_ref = db_store.collection(u'books').document(u''+str(len(checklength)+1))
    doc_ref.set(dict1)

    return HTML_TEXT 
    
    






# In[ ]:
#please open collab file 
if __name__ == "__main__":
    app.run()


# In[ ]:





