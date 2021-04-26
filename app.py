#import libraries
import numpy as np
import pandas as pd
from flask import Flask, request, render_template
from flask_cors import CORS
import os
import flask
import urllib
import random
import tweepy

#initialize the app
app = Flask(__name__)
CORS(app)
app = flask.Flask(__name__,template_folder='templates')

@app.route('/')
def main():
    return render_template('index.html')
  
def query_gen(city):
    return "verified {} (bed OR beds OR icu OR oxygen OR ventilator OR ventilators) -'not verified -'unverified' -'needed' -'need' -'needs' -'required' -'require' -'requires' -'requirement' -'requirements -'please'".format(city)
  
def fetch_data(city):
  consumer_key = 'XbLfkF6AtwTrMuhJeaMnTUdVC'
  consumer_secret = 'dnf1cUYaVGtOEYvWbRYvixEajYnNM9T2nM232CrOInzDX1Idkn'
  access_token = '1334156476315693058-9wvgPCZ2U7nvGMpH7FkUEnT7RI69tB'
  access_token_secret = 'AVCwCajD4sl6QMUIk0HuGXfk4kNtpZLaoaut24nWdqxUN'
  bearer = 'AAAAAAAAAAAAAAAAAAAAALOTOwEAAAAABOkjYT4MbWwCvvnPw8Wo7iafbqk%3DdBz8kfy0wdzAV67CZI40srVRDQkyCmcCbquUl6d4fiE8LJkil8'
  
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)
  api = tweepy.API(auth)
  
  T = api.search(query_gen(city),
                 lang = 'en', 
                 tweet_mode='extended', 
                 count=100,
                 result_type='recent')
  txt = []
  ctr = 0
  for i in T:
      try:
          try:
              txt.append([ctr,i._json['retweeted_status']['full_text'].lower(),i.entities["media"][0]["media_url"],i.user.screen_name])
              ctr += 1
          except:
              txt.append([ctr,i._json['retweeted_status']['full_text'].lower(),None,i.user.screen_name])
              ctr += 1
      except:
          try:
              txt.append([ctr, i.full_text.lower(),i.entities["media"][0]["media_url"],i.user.screen_name])
              ctr += 1
          except:
              txt.append([ctr, i.full_text.lower(),None,i.user.screen_name])
              ctr += 1
  df = pd.DataFrame(txt, columns = ['Index','Tweet','image','username'])
  return df

  
  

#using NLP to parse the article
@app.route('/find',methods=['GET','POST'])
def find():
    city = request.get_data(as_text = True)
    data = fetch_data(city)
    return render_template('data.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)

if __name__ == "__main__":
    port = int(os.environ.get('PORT',5000))
    app.run(port = port,debug = True,use_reloader=False)
